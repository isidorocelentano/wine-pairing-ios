"""
Import wines from Excel into the NEW public_wines collection
Clean start - no legacy issues
"""
import openpyxl
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'wine_pairing_db')]

def extract_wines_from_excel(file_path):
    """Extract all wines from Excel file"""
    wb = openpyxl.load_workbook(file_path, data_only=True)
    all_wines = []
    
    print(f"📊 Processing {len(wb.sheetnames)} sheets\n")
    
    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        
        # Get headers
        headers = [str(cell.value).strip() if cell.value else "" for cell in sheet[1]]
        if not headers or not any(headers):
            continue
        
        # Process rows
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not any(row):
                continue
            
            row_data = {}
            for idx, value in enumerate(row):
                if idx < len(headers) and value:
                    row_data[headers[idx]] = str(value).strip()
            
            if not row_data:
                continue
            
            # Extract wine info
            wine = extract_wine_info(row_data, sheet_name)
            if wine:
                all_wines.append(wine)
    
    print(f"✅ Extracted {len(all_wines)} wines\n")
    return all_wines

def extract_wine_info(row_data, sheet_name):
    """Extract wine information from row"""
    
    # Get wine name
    name = None
    for key in ['Château', 'Château / Domaine', 'Premier Cru', 'Cru', 'Wein', 'Appellation', 'MGA-Lage (Gemeinde)', 'Grand Cru (Lage)']:
        if key in row_data:
            name = row_data[key]
            break
    
    if not name:
        return None
    
    # Get description
    description_de = row_data.get('Beschreibung', row_data.get('Emotionaler Charakter', row_data.get('Stil-Beschreibung', '')))
    if not description_de:
        return None
    
    # Get other fields
    region = row_data.get('Region', row_data.get('Appellation', 'Unbekannt'))
    grape_variety = row_data.get('Rebsorten-DNA (Dominant)', row_data.get('Rebsorten-DNA', row_data.get('Dominante Rebsorten', 'Unbekannt')))
    pairings_text = row_data.get('Das perfekte Pairing', '')
    pairings_list = [p.strip() for p in pairings_text.split(',') if p.strip()] if pairings_text else []
    
    # Determine wine color
    context = (sheet_name + ' ' + name + ' ' + region).lower()
    if any(w in context for w in ['weiß', 'white', 'blanc', 'chardonnay', 'riesling', 'sauvignon']):
        wine_color = 'weiss'
    elif any(w in context for w in ['sauternes', 'süß', 'sweet']):
        wine_color = 'suesswein'
    elif any(w in context for w in ['champagner', 'champagne', 'sekt']):
        wine_color = 'schaumwein'
    elif any(w in context for w in ['rosé', 'rose', 'provence']):
        wine_color = 'rose'
    else:
        wine_color = 'rot'
    
    # Determine country
    context_country = (sheet_name + ' ' + region).lower()
    if any(w in context_country for w in ['bordeaux', 'burgund', 'rhône', 'loire', 'champagne', 'provence', 'alsace']):
        country = 'Frankreich'
    elif any(w in context_country for w in ['toskana', 'piemont', 'venetien', 'barolo', 'brunello', 'chianti']):
        country = 'Italien'
    elif any(w in context_country for w in ['deutschland', 'mosel', 'rheingau', 'pfalz']):
        country = 'Deutschland'
    elif any(w in context_country for w in ['spanien', 'rioja', 'ribera', 'priorat']):
        country = 'Spanien'
    elif any(w in context_country for w in ['portugal', 'douro', 'porto']):
        country = 'Portugal'
    elif any(w in context_country for w in ['usa', 'napa', 'california']):
        country = 'USA'
    else:
        country = 'Frankreich'
    
    # Determine price category
    sheet_lower = sheet_name.lower()
    if any(w in sheet_lower or w in name.lower() for w in ['premier cru classé', '1. gcc', 'grand cru', 'pétrus', 'lafite', 'latour', 'margaux']):
        price_category = 'luxury'
    elif any(w in sheet_lower for w in ['deuxièmes', '2.', 'troisièmes', '3.', 'barbaresco', 'barolo', 'brunello']):
        price_category = 'premium'
    elif any(w in sheet_lower for w in ['cru bourgeois', 'premier cru']):
        price_category = 'mid-range'
    else:
        price_category = 'mid-range'
    
    return {
        'id': str(uuid.uuid4()),
        'name': name,
        'winery': name,
        'country': country,
        'region': region,
        'appellation': region,
        'grape_variety': grape_variety,
        'wine_color': wine_color,
        'year': None,
        'description_de': description_de,
        'description_en': description_de,  # Fallback to DE
        'description_fr': description_de,  # Fallback to DE
        'tasting_notes': row_data.get('Stil-Beschreibung'),
        'food_pairings_de': pairings_list,
        'food_pairings_en': pairings_list,
        'food_pairings_fr': pairings_list,
        'alcohol_content': None,
        'price_category': price_category,
        'image_url': '/placeholder-wine.png',
        'rating': None,
        'created_at': datetime.now(timezone.utc).isoformat()
    }

async def import_to_db(wines):
    """Import wines to public_wines collection"""
    
    # Clear existing data
    await db.public_wines.delete_many({})
    print("🗑️  Cleared public_wines collection\n")
    
    # Insert all wines
    if wines:
        await db.public_wines.insert_many(wines)
        print(f"💾 Inserted {len(wines)} wines\n")
    
    # Verify
    count = await db.public_wines.count_documents({})
    print(f"✅ Final count in public_wines: {count}")
    
    # Show sample
    sample = await db.public_wines.find_one({}, {"_id": 0, "name": 1, "country": 1, "wine_color": 1, "description_de": 1})
    if sample:
        print(f"\n📝 Sample wine:")
        print(f"   Name: {sample['name']}")
        print(f"   Country: {sample['country']}")
        print(f"   Color: {sample['wine_color']}")
        print(f"   Has description_de: {bool(sample.get('description_de'))}")

async def main():
    print("🍷 Starting Fresh Wine Database Import\n")
    print("=" * 60)
    
    wines = extract_wines_from_excel('/app/wine_db_source.xlsx')
    
    if wines:
        await import_to_db(wines)
    else:
        print("❌ No wines extracted!")
    
    print("\n" + "=" * 60)
    print("✅ Import Complete!")

if __name__ == '__main__':
    asyncio.run(main())
