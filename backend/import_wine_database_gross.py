"""
Import wine database from "Weindatenbank gross 01.xlsx"
- Separate DE/EN/FR descriptions from parentheses
- Handle duplicates
- Clean data structure
"""
import openpyxl
import asyncio
import os
import re
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]


def parse_multilingual_description(text):
    """
    Parse description with format: 
    German text. (English text.) (French text.)
    Returns: (de, en, fr)
    """
    if not text:
        return '', '', ''
    
    # Extract German (everything before first parenthesis)
    german_match = re.match(r'^([^(]+?)(?:\s*\(|$)', text)
    german = german_match.group(1).strip() if german_match else text
    
    # Extract English (first parenthesis)
    english_match = re.search(r'\(([^)]+)\)', text)
    english = english_match.group(1).strip() if english_match else german
    
    # Extract French (second parenthesis)
    french_matches = re.findall(r'\(([^)]+)\)', text)
    french = french_matches[1].strip() if len(french_matches) > 1 else german
    
    return german, english, french


def extract_wines_from_excel(file_path):
    """Extract wines from the Excel file"""
    wb = openpyxl.load_workbook(file_path, data_only=True)
    sheet = wb.active
    
    wines = []
    seen_names = set()  # Track duplicates
    duplicate_count = 0
    
    print(f"📊 Processing Excel file\n")
    
    # Get headers
    headers = [cell.value for cell in sheet[1] if cell.value]
    print(f"Headers: {headers}\n")
    
    # Expected headers
    # 0: Wein / Kategorie
    # 1: Appellation / Status
    # 2: Klassifikation / Reifung
    # 3: Detaillierte Beschreibung / Emotionaler Charakter
    # 4: Dominante Rebsorten
    # 5: Das perfekte Pairing
    
    for row_num, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        if not any(row):
            continue
        
        wine_name = str(row[0]).strip() if row[0] else ''
        appellation_status = str(row[1]).strip() if row[1] else ''
        classification = str(row[2]).strip() if row[2] else ''
        description_full = str(row[3]).strip() if row[3] else ''
        grape_variety = str(row[4]).strip() if row[4] else ''
        food_pairings = str(row[5]).strip() if row[5] else ''
        
        if not wine_name or wine_name.lower() in ['wein', 'kategorie', 'none']:
            continue
        
        # Check for duplicates
        name_key = wine_name.lower()
        if name_key in seen_names:
            duplicate_count += 1
            print(f"  ⏭️  Skipping duplicate: {wine_name}")
            continue
        
        seen_names.add(name_key)
        
        # Parse multilingual description
        desc_de, desc_en, desc_fr = parse_multilingual_description(description_full)
        
        # Parse region and country from appellation
        parts = [p.strip() for p in appellation_status.split('/')]
        region = parts[0] if len(parts) > 0 else 'Unbekannt'
        appellation = parts[1] if len(parts) > 1 else region
        country = parts[-1] if len(parts) > 2 else 'Unbekannt'
        
        # Determine wine color from name and grape variety
        context = (wine_name + ' ' + grape_variety).lower()
        if any(w in context for w in ['pinot grigio', 'chardonnay', 'sauvignon blanc', 'riesling', 'grüner veltliner', 'weiss', 'white', 'blanc']):
            wine_color = 'weiss'
        elif any(w in context for w in ['rosé', 'rose']):
            wine_color = 'rose'
        elif any(w in context for w in ['champagne', 'prosecco', 'cava', 'sekt', 'crémant']):
            wine_color = 'schaumwein'
        else:
            wine_color = 'rot'
        
        # Determine price category from classification
        if any(w in classification.lower() for w in ['ikone', 'autor', 'grand cru']):
            price_category = 'luxury'
        elif any(w in classification.lower() for w in ['cru', 'reserva', 'riserva']):
            price_category = 'premium'
        else:
            price_category = 'mid-range'
        
        # Parse food pairings
        pairings_list = [p.strip() for p in food_pairings.split(',') if p.strip()]
        
        wine_entry = {
            'id': str(uuid.uuid4()),
            'name': wine_name,
            'winery': wine_name.split()[0] if ' ' in wine_name else wine_name,  # First word as winery
            'country': country,
            'region': region,
            'appellation': appellation,
            'grape_variety': grape_variety,
            'wine_color': wine_color,
            'year': None,
            'description_de': desc_de,
            'description_en': desc_en,
            'description_fr': desc_fr,
            'tasting_notes': classification,
            'food_pairings_de': pairings_list,
            'food_pairings_en': pairings_list,  # Same for now
            'food_pairings_fr': pairings_list,  # Same for now
            'alcohol_content': None,
            'price_category': price_category,
            'image_url': '/placeholder-wine.png',
            'rating': None,
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        
        wines.append(wine_entry)
    
    print(f"\n✅ Extracted {len(wines)} unique wines")
    print(f"⏭️  Skipped {duplicate_count} duplicates")
    
    return wines


async def import_to_db(wines):
    """Import wines to public_wines collection, replacing old data"""
    
    # Clear existing data
    deleted = await db.public_wines.delete_many({})
    print(f"\n🗑️  Cleared {deleted.deleted_count} existing wines\n")
    
    # Insert all wines
    if wines:
        await db.public_wines.insert_many(wines)
        print(f"💾 Inserted {len(wines)} wines\n")
    
    # Verify
    count = await db.public_wines.count_documents({})
    print(f"✅ Final count in public_wines: {count}")
    
    # Show sample
    sample = await db.public_wines.find_one({}, {"_id": 0, "name": 1, "country": 1, "description_de": 1, "description_en": 1})
    if sample:
        print(f"\n📝 Sample wine:")
        print(f"   Name: {sample['name']}")
        print(f"   Country: {sample['country']}")
        print(f"   Description DE: {sample['description_de'][:80]}...")
        print(f"   Description EN: {sample['description_en'][:80]}...")


async def main():
    print("🍷 Wine Database Import - Weindatenbank gross 01")
    print("=" * 60)
    
    # Download file
    print("\n📥 Downloading Excel file...")
    import urllib.request
    url = "https://customer-assets.emergentagent.com/job_sommbot/artifacts/j1svwmne_Weindatenbank%20gross%2001.xlsx"
    file_path = '/app/wine_db_gross.xlsx'
    urllib.request.urlretrieve(url, file_path)
    print(f"✅ Downloaded to {file_path}\n")
    
    wines = extract_wines_from_excel(file_path)
    
    if wines:
        await import_to_db(wines)
    else:
        print("❌ No wines extracted!")
    
    print("\n" + "=" * 60)
    print("✅ Import Complete!")


if __name__ == '__main__':
    asyncio.run(main())
