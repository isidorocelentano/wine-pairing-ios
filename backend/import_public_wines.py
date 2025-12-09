"""
Import wines from Excel into the public_wines collection
Handles TWO different formats in the 'Appellation / Status' field:

Format A: "Region / Appellation_or_Class / Country"
  Example: "Südtirol / Alto Adige / Italien"
  Example: "Rioja / Gran Reserva / Spanien"

Format B: "Country / Classification / Region"  
  Example: "Deutschland / Kult-Wein / Mosel"
  Example: "Österreich / Prestige-Wein / Wachau"
"""
import openpyxl
import asyncio
import os
import re
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'wine_pairing_db')]

# Define known countries (lowercase -> display name)
KNOWN_COUNTRIES = {
    'italien': 'Italien',
    'frankreich': 'Frankreich', 
    'spanien': 'Spanien',
    'deutschland': 'Deutschland',
    'österreich': 'Österreich',
    'schweiz': 'Schweiz',
    'portugal': 'Portugal',
    'usa': 'USA',
    'australien': 'Australien',
    'chile': 'Chile',
    'argentinien': 'Argentinien',
    'ungarn': 'Ungarn',
    'neuseeland': 'Neuseeland',
    'südafrika': 'Südafrika',
}

# Classification terms that are NOT geographic
CLASSIFICATION_TERMS = {
    # Quality classifications
    'cru', 'doc', 'docg', 'igt', 'vdit', 'do', 'doca',
    'reserva', 'crianza', 'gran reserva', 'grand cru', 'premier cru',
    'gran selezione', 'riserva', 'superiore',
    'premier cru supérieur', 'premier cru classé', 'deuxième cru',
    'cinquième cru', 'cru classé', 'troisième cru', 'quatrième cru',
    # Wine types (not geographic)
    'rotwein', 'weißwein', 'schaumwein', 'süßwein', 'rosado', 'rosé',
    'cava', 'champagner', 'sekt', 'prosecco',
    # Status terms
    'status', 'prestige-wein', 'kult-wein', 'ikone', 'ikonen-status', 
    'basiswein', 'zweitwein', 'super tuscan',
    # Generic
    'appellation',
}


def is_country(value: str) -> bool:
    """Check if value is a known country"""
    return value.lower().strip() in KNOWN_COUNTRIES


def is_classification(value: str) -> bool:
    """Check if value is a classification term"""
    return value.lower().strip() in CLASSIFICATION_TERMS


def parse_appellation_status(value: str) -> dict:
    """
    Parse the 'Appellation / Status' field handling both formats.
    
    Returns dict with: country, region, appellation, classification
    """
    if not value:
        return {'country': None, 'region': None, 'appellation': None, 'classification': None}
    
    parts = [p.strip() for p in value.split(' / ') if p.strip()]
    
    country = None
    region = None
    appellation = None
    classification = None
    
    if len(parts) == 3:
        first, second, third = parts
        
        # Detect format based on first and third parts
        first_is_country = is_country(first)
        third_is_country = is_country(third)
        second_is_class = is_classification(second)
        
        if first_is_country and not third_is_country:
            # Format B: Country / Classification / Region
            # Example: "Deutschland / Kult-Wein / Mosel"
            country = KNOWN_COUNTRIES.get(first.lower(), first)
            classification = second if second_is_class else None
            region = third
            appellation = third  # Use region as appellation
            
        elif third_is_country and not first_is_country:
            # Format A: Region / Appellation_or_Class / Country
            # Example: "Südtirol / Alto Adige / Italien"
            country = KNOWN_COUNTRIES.get(third.lower(), third)
            region = first
            
            if second_is_class:
                classification = second
                appellation = first  # Use region as appellation
            else:
                appellation = second  # Real appellation
                
        else:
            # Fallback: try to make sense of it
            # Check if any part is a country
            for i, part in enumerate(parts):
                if is_country(part):
                    country = KNOWN_COUNTRIES.get(part.lower(), part)
                    remaining = [p for j, p in enumerate(parts) if j != i]
                    if remaining:
                        region = remaining[0]
                        appellation = remaining[1] if len(remaining) > 1 else remaining[0]
                    break
            
            if not country:
                # No country found - use first as region
                region = first
                appellation = second if not second_is_class else first
                classification = second if second_is_class else None
                
    elif len(parts) == 2:
        first, second = parts
        
        if is_country(first):
            # "Country / Region"
            country = KNOWN_COUNTRIES.get(first.lower(), first)
            region = second
            appellation = second
        elif is_country(second):
            # "Region / Country"
            country = KNOWN_COUNTRIES.get(second.lower(), second)
            region = first
            appellation = first
        else:
            # Neither is country
            region = first
            if is_classification(second):
                classification = second
                appellation = first
            else:
                appellation = second
                
    elif len(parts) == 1:
        region = parts[0]
        appellation = parts[0]
        # Try to detect country from context
        if is_country(parts[0]):
            country = KNOWN_COUNTRIES.get(parts[0].lower(), parts[0])
            region = None
            appellation = None
    
    return {
        'country': country,
        'region': region,
        'appellation': appellation,
        'classification': classification
    }


def extract_multilingual_description(desc_text: str) -> tuple:
    """Extract German, English, and French descriptions."""
    if not desc_text:
        return ('', '', '')
    
    desc_de = desc_text
    desc_en = desc_text
    desc_fr = desc_text
    
    paren_matches = re.findall(r'\(([^)]+)\)', desc_text)
    
    if len(paren_matches) >= 2:
        desc_en = paren_matches[0]
        desc_fr = paren_matches[1]
        first_paren = desc_text.find('(')
        if first_paren > 0:
            desc_de = desc_text[:first_paren].strip()
    elif len(paren_matches) == 1:
        desc_en = paren_matches[0]
        desc_fr = paren_matches[0]
        first_paren = desc_text.find('(')
        if first_paren > 0:
            desc_de = desc_text[:first_paren].strip()
    
    return (desc_de, desc_en, desc_fr)


def determine_wine_color(wine_name: str, grape: str, region: str, classification: str) -> str:
    """Determine wine color based on various indicators"""
    context = f"{wine_name} {grape} {region} {classification or ''}".lower()
    
    white_indicators = [
        'weiss', 'weiß', 'white', 'blanc', 'bianco',
        'chardonnay', 'riesling', 'sauvignon blanc', 'pinot grigio', 'pinot gris',
        'gewürztraminer', 'moscato', 'grüner veltliner', 'albariño', 'verdejo',
        'viognier', 'chenin', 'semillon', 'trebbiano', 'vermentino', 'weißwein',
        'gruner veltliner', 'silvaner', 'müller-thurgau'
    ]
    
    rose_indicators = ['rosé', 'rose', 'rosado', 'rosato']
    sweet_indicators = ['sauternes', 'süß', 'sweet', 'tokaji', 'eiswein', 'auslese', 
                       'beerenauslese', 'trockenbeerenauslese', 'süßwein', 'dessert']
    sparkling_indicators = ['champagne', 'champagner', 'sekt', 'cava', 'prosecco', 
                           'crémant', 'spumante', 'schaumwein', 'franciacorta', 'brut']
    
    if any(ind in context for ind in sparkling_indicators):
        return 'schaumwein'
    if any(ind in context for ind in sweet_indicators):
        return 'suesswein'
    if any(ind in context for ind in rose_indicators):
        return 'rose'
    if any(ind in context for ind in white_indicators):
        return 'weiss'
    
    return 'rot'


def determine_price_category(classification: str, wine_name: str) -> str:
    """Determine price category based on classification and name"""
    context = f"{classification or ''} {wine_name}".lower()
    
    luxury_terms = ['premier cru classé', 'grand cru', 'gran selezione', 'ikone', 
                   'ikonen-status', 'kult-wein', 'pétrus', 'lafite', 'latour', 
                   'margaux', 'mouton', 'prestige-wein']
    premium_terms = ['reserva', 'gran reserva', 'barbaresco', 'barolo', 'brunello', 
                    'super tuscan', 'crianza', 'riserva', 'cru classé']
    
    if any(term in context for term in luxury_terms):
        return 'luxury'
    if any(term in context for term in premium_terms):
        return 'premium'
    
    return 'mid-range'


def extract_wines_from_excel(file_path):
    """Extract wines from Excel with semicolon-separated data."""
    wb = openpyxl.load_workbook(file_path, data_only=True)
    all_wines = []
    
    print(f"📊 Processing {len(wb.sheetnames)} sheets")
    
    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        
        header_row = sheet[1]
        header_value = header_row[0].value if header_row[0].value else ""
        
        if ';' not in str(header_value):
            print(f"\n   ⚠️ Sheet '{sheet_name}' - Not semicolon format, skipping")
            continue
            
        print(f"\n   📄 Sheet '{sheet_name}'")
        
        sheet_wines = 0
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not row or not row[0]:
                continue
            
            row_data = str(row[0]).split(';')
            
            if len(row_data) < 4:
                continue
            
            wine_name = row_data[0].strip() if len(row_data) > 0 else None
            appellation_status = row_data[1].strip() if len(row_data) > 1 else None
            classification_col = row_data[2].strip() if len(row_data) > 2 else None
            description = row_data[3].strip() if len(row_data) > 3 else None
            grape = row_data[4].strip() if len(row_data) > 4 else 'Unbekannt'
            pairing = row_data[5].strip() if len(row_data) > 5 else ''
            
            if not wine_name or not description:
                continue
            
            # Parse hierarchy
            hierarchy = parse_appellation_status(appellation_status)
            
            # Use classification from column if available
            classification = hierarchy.get('classification') or classification_col
            
            # Extract descriptions
            desc_de, desc_en, desc_fr = extract_multilingual_description(description)
            
            # Parse pairings
            pairings = [p.strip() for p in pairing.split(',') if p.strip()] if pairing else []
            
            # Extract winery
            winery = wine_name.split()[0] if wine_name else 'Unbekannt'
            
            # Determine color and price
            wine_color = determine_wine_color(wine_name, grape, hierarchy.get('region', ''), classification)
            price_category = determine_price_category(classification, wine_name)
            
            wine = {
                'id': str(uuid.uuid4()),
                'name': wine_name,
                'winery': winery,
                'country': hierarchy.get('country') or 'Unbekannt',
                'region': hierarchy.get('region') or 'Unbekannt',
                'appellation': hierarchy.get('appellation') or hierarchy.get('region') or 'Unbekannt',
                'grape_variety': grape if grape else 'Unbekannt',
                'wine_color': wine_color,
                'year': None,
                'description_de': desc_de,
                'description_en': desc_en,
                'description_fr': desc_fr,
                'tasting_notes': classification,
                'food_pairings_de': pairings,
                'food_pairings_en': pairings,
                'food_pairings_fr': pairings,
                'alcohol_content': None,
                'price_category': price_category,
                'image_url': '/placeholder-wine.png',
                'rating': None,
                'created_at': datetime.now(timezone.utc).isoformat()
            }
            
            all_wines.append(wine)
            sheet_wines += 1
        
        print(f"      → Extracted {sheet_wines} wines")
    
    print(f"\n✅ Total wines extracted: {len(all_wines)}")
    return all_wines


async def import_to_db(wines):
    """Import wines to database"""
    
    await db.public_wines.delete_many({})
    print("\n🗑️  Cleared public_wines collection")
    
    if wines:
        await db.public_wines.insert_many(wines)
        print(f"💾 Inserted {len(wines)} wines")
    
    count = await db.public_wines.count_documents({})
    print(f"✅ Final count: {count}")
    
    # Statistics
    print("\n📊 Statistics:")
    
    countries = await db.public_wines.distinct("country")
    valid_countries = sorted([c for c in countries if c != 'Unbekannt'])
    print(f"   Countries ({len(valid_countries)}): {', '.join(valid_countries)}")
    
    # Count by country
    print("\n   Wines per country:")
    for country in valid_countries[:10]:
        cnt = await db.public_wines.count_documents({"country": country})
        print(f"      {country}: {cnt}")
    
    colors = await db.public_wines.distinct("wine_color")
    print(f"\n   Wine colors: {', '.join(sorted(colors))}")
    
    # Sample hierarchy
    print("\n📍 Sample Hierarchy:")
    samples = await db.public_wines.find(
        {"country": {"$ne": "Unbekannt"}}, 
        {"_id": 0, "name": 1, "country": 1, "region": 1, "appellation": 1}
    ).limit(10).to_list(10)
    
    for s in samples:
        name = s['name'][:30] + '...' if len(s['name']) > 30 else s['name']
        print(f"   {name}: {s['country']} → {s['region']} → {s['appellation']}")


async def main():
    print("🍷 Wine Database Import - Dual Format Handler\n")
    print("=" * 60)
    
    file_path = '/app/wine_db_gross.xlsx'
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"📂 Source: {file_path}\n")
    
    wines = extract_wines_from_excel(file_path)
    
    if wines:
        await import_to_db(wines)
    else:
        print("❌ No wines extracted!")
    
    print("\n" + "=" * 60)
    print("✅ Import Complete!")


if __name__ == '__main__':
    asyncio.run(main())
