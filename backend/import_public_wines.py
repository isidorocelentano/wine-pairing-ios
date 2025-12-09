"""
Import wines from Excel into the public_wines collection
Handles semicolon-separated data in single column (wine_db_gross.xlsx format)
Correctly parses the hierarchical structure from 'Appellation / Status' field:
Format: "Region / Appellation / Country" (e.g., "Südtirol / Alto Adige / Italien")
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

# Define known countries for validation
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

# Classification terms that should NOT be used as region/appellation
CLASSIFICATION_TERMS = {
    'cru', 'doc', 'docg', 'igt', 'reserva', 'crianza', 'gran reserva', 'grand cru', 
    'premier cru', 'rotwein', 'weißwein', 'schaumwein', 'süßwein', 'status',
    'prestige-wein', 'kult-wein', 'ikone', 'ikonen-status', 'basiswein', 'zweitwein',
    'super tuscan', 'rosado', 'cava', 'gran selezione', 'vdit', 'do', 'premier cru supérieur'
}


def parse_appellation_status(value: str) -> dict:
    """
    Parse the 'Appellation / Status' field which contains hierarchical info.
    Format: "Region / Appellation or Classification / Country"
    Example: "Südtirol / Alto Adige / Italien"
    
    Returns dict with: country, region, appellation, classification
    """
    if not value:
        return {'country': None, 'region': None, 'appellation': None, 'classification': None}
    
    # Split by " / "
    parts = [p.strip() for p in value.split(' / ') if p.strip()]
    
    country = None
    region = None
    appellation = None
    classification = None
    
    # Find country first (it's usually at the end)
    remaining_parts = []
    for part in parts:
        part_lower = part.lower()
        if part_lower in KNOWN_COUNTRIES:
            country = KNOWN_COUNTRIES[part_lower]
        elif part_lower in CLASSIFICATION_TERMS:
            classification = part
        else:
            remaining_parts.append(part)
    
    # Assign remaining parts to region and appellation
    if len(remaining_parts) >= 2:
        region = remaining_parts[0]
        appellation = remaining_parts[1]
    elif len(remaining_parts) == 1:
        region = remaining_parts[0]
        appellation = remaining_parts[0]  # Use region as appellation if only one
    
    return {
        'country': country,
        'region': region,
        'appellation': appellation,
        'classification': classification
    }


def extract_multilingual_description(desc_text: str) -> tuple:
    """
    Extract German, English, and French descriptions from the combined text.
    Format: "German text. (English text.) (French text.)"
    """
    if not desc_text:
        return ('', '', '')
    
    desc_de = desc_text
    desc_en = desc_text
    desc_fr = desc_text
    
    # Look for parenthetical translations
    paren_matches = re.findall(r'\(([^)]+)\)', desc_text)
    
    if len(paren_matches) >= 2:
        # Has both EN and FR in parentheses
        desc_en = paren_matches[0]
        desc_fr = paren_matches[1]
        # German is the text before first parenthesis
        first_paren = desc_text.find('(')
        if first_paren > 0:
            desc_de = desc_text[:first_paren].strip()
    elif len(paren_matches) == 1:
        # Only one translation
        desc_en = paren_matches[0]
        desc_fr = paren_matches[0]
        first_paren = desc_text.find('(')
        if first_paren > 0:
            desc_de = desc_text[:first_paren].strip()
    
    return (desc_de, desc_en, desc_fr)


def determine_wine_color(wine_name: str, grape: str, region: str, sheet_name: str) -> str:
    """Determine wine color based on various indicators"""
    context = f"{wine_name} {grape} {region} {sheet_name}".lower()
    
    # White wine indicators
    white_indicators = [
        'weiss', 'weiß', 'white', 'blanc', 'bianco',
        'chardonnay', 'riesling', 'sauvignon blanc', 'pinot grigio', 'pinot gris',
        'gewürztraminer', 'moscato', 'grüner veltliner', 'albariño', 'verdejo',
        'viognier', 'chenin', 'semillon', 'trebbiano', 'vermentino'
    ]
    
    # Rosé indicators
    rose_indicators = ['rosé', 'rose', 'rosado', 'rosato']
    
    # Sweet wine indicators
    sweet_indicators = ['sauternes', 'süß', 'sweet', 'tokaji', 'eiswein', 'auslese', 'beerenauslese', 'trockenbeerenauslese']
    
    # Sparkling wine indicators
    sparkling_indicators = ['champagne', 'champagner', 'sekt', 'cava', 'prosecco', 'crémant', 'spumante', 'schaumwein']
    
    if any(ind in context for ind in sparkling_indicators):
        return 'schaumwein'
    if any(ind in context for ind in sweet_indicators):
        return 'suesswein'
    if any(ind in context for ind in rose_indicators):
        return 'rose'
    if any(ind in context for ind in white_indicators):
        return 'weiss'
    
    return 'rot'


def determine_price_category(classification: str, wine_name: str, sheet_name: str) -> str:
    """Determine price category based on classification and name"""
    context = f"{classification or ''} {wine_name} {sheet_name}".lower()
    
    luxury_terms = ['premier cru classé', 'grand cru', 'gran selezione', 'ikone', 'pétrus', 'lafite', 'latour', 'margaux', 'mouton']
    premium_terms = ['reserva', 'gran reserva', 'barbaresco', 'barolo', 'brunello', 'super tuscan', 'crianza']
    
    if any(term in context for term in luxury_terms):
        return 'luxury'
    if any(term in context for term in premium_terms):
        return 'premium'
    
    return 'mid-range'


def extract_wines_from_semicolon_format(file_path):
    """
    Extract wines from Excel where data is semicolon-separated in single column.
    Format: wine_name;appellation_status;classification;description;grape;pairing
    """
    wb = openpyxl.load_workbook(file_path, data_only=True)
    all_wines = []
    
    print(f"📊 Processing {len(wb.sheetnames)} sheets")
    print(f"   Sheets: {', '.join(wb.sheetnames)}\n")
    
    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        
        # Get header row to understand column structure
        header_row = sheet[1]
        header_value = header_row[0].value if header_row[0].value else ""
        
        # Check if data is semicolon-separated
        if ';' in str(header_value):
            print(f"   📄 Sheet '{sheet_name}' - Semicolon-separated format detected")
            headers = [h.strip() for h in str(header_value).split(';')]
            print(f"      Headers: {headers}")
            
            # Map headers to indices
            header_map = {h.lower(): i for i, h in enumerate(headers)}
            
            sheet_wines = 0
            for row_num, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                if not row or not row[0]:
                    continue
                
                # Parse semicolon-separated data
                row_data = str(row[0]).split(';')
                
                if len(row_data) < 4:  # Need at least name, location, classification, description
                    continue
                
                # Map to fields based on header positions
                wine_name = row_data[0].strip() if len(row_data) > 0 else None
                appellation_status = row_data[1].strip() if len(row_data) > 1 else None
                classification = row_data[2].strip() if len(row_data) > 2 else None
                description = row_data[3].strip() if len(row_data) > 3 else None
                grape = row_data[4].strip() if len(row_data) > 4 else 'Unbekannt'
                pairing = row_data[5].strip() if len(row_data) > 5 else ''
                
                if not wine_name or not description:
                    continue
                
                # Parse hierarchy from appellation_status
                hierarchy = parse_appellation_status(appellation_status)
                
                # Extract multilingual descriptions
                desc_de, desc_en, desc_fr = extract_multilingual_description(description)
                
                # Parse pairings
                pairings = [p.strip() for p in pairing.split(',') if p.strip()] if pairing else []
                
                # Extract winery from wine name (first word)
                winery = wine_name.split()[0] if wine_name else 'Unbekannt'
                
                # Determine wine color
                wine_color = determine_wine_color(wine_name, grape, hierarchy.get('region', ''), sheet_name)
                
                # Determine price category
                price_category = determine_price_category(classification, wine_name, sheet_name)
                
                # Use classification from hierarchy if separate column is just generic
                final_classification = hierarchy.get('classification') or classification
                
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
                    'tasting_notes': final_classification,
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
            
            print(f"      → Extracted {sheet_wines} wines from sheet")
        else:
            print(f"   📄 Sheet '{sheet_name}' - Standard multi-column format")
            # Handle standard format (not semicolon-separated)
            # ... (original logic for wine_db_source.xlsx)
    
    print(f"\n✅ Total wines extracted: {len(all_wines)}")
    return all_wines


async def import_to_db(wines):
    """Import wines to public_wines collection"""
    
    # Clear existing data
    await db.public_wines.delete_many({})
    print("\n🗑️  Cleared public_wines collection")
    
    # Insert all wines
    if wines:
        await db.public_wines.insert_many(wines)
        print(f"💾 Inserted {len(wines)} wines")
    
    # Verify
    count = await db.public_wines.count_documents({})
    print(f"✅ Final count in public_wines: {count}")
    
    # Show statistics
    print("\n📊 Statistics:")
    
    countries = await db.public_wines.distinct("country")
    print(f"   Countries ({len(countries)}): {', '.join(sorted([c for c in countries if c != 'Unbekannt']))}")
    
    regions = await db.public_wines.distinct("region")
    valid_regions = sorted([r for r in regions if r and r != 'Unbekannt'])
    print(f"   Regions ({len(valid_regions)}): {', '.join(valid_regions[:15])}{'...' if len(valid_regions) > 15 else ''}")
    
    colors = await db.public_wines.distinct("wine_color")
    print(f"   Wine colors ({len(colors)}): {', '.join(sorted(colors))}")
    
    # Show hierarchy samples
    print("\n📍 Sample Hierarchy (5 wines):")
    samples = await db.public_wines.find(
        {"country": {"$ne": "Unbekannt"}}, 
        {"_id": 0, "name": 1, "country": 1, "region": 1, "appellation": 1}
    ).limit(5).to_list(5)
    
    for s in samples:
        print(f"   {s['name'][:40]}: {s['country']} → {s['region']} → {s['appellation']}")


async def main():
    print("🍷 Wine Database Import - Hierarchical Structure\n")
    print("=" * 60)
    
    # Use wine_db_gross.xlsx (the main file with 1000+ wines)
    file_path = '/app/wine_db_gross.xlsx'
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"📂 Source file: {file_path}\n")
    
    wines = extract_wines_from_semicolon_format(file_path)
    
    if wines:
        await import_to_db(wines)
    else:
        print("❌ No wines extracted!")
    
    print("\n" + "=" * 60)
    print("✅ Import Complete!")


if __name__ == '__main__':
    asyncio.run(main())
