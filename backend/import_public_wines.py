"""
Import wines from Excel into the public_wines collection
Correctly parses the hierarchical structure from 'Appellation / Status' column:
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
    Parse the 'Appellation / Status' column which contains hierarchical info.
    Format varies but generally: "Region / Appellation or Classification / Country"
    
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
    
    # Try to find the pattern: German (English) (French)
    # Pattern: text before first ( is German, then (english), then (french)
    
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


def extract_wines_from_excel(file_path):
    """Extract all wines from Excel file with correct hierarchy parsing"""
    wb = openpyxl.load_workbook(file_path, data_only=True)
    all_wines = []
    
    print(f"📊 Processing {len(wb.sheetnames)} sheets")
    print(f"   Sheets: {', '.join(wb.sheetnames)}\n")
    
    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        
        # Get headers from first row
        headers = []
        for cell in sheet[1]:
            if cell.value:
                headers.append(str(cell.value).strip())
            else:
                headers.append("")
        
        if not headers or not any(headers):
            print(f"   ⚠️ Skipping sheet '{sheet_name}' - no headers")
            continue
        
        print(f"   📄 Sheet '{sheet_name}' - Headers: {headers}")
        
        # Find key column indices
        col_indices = {}
        for idx, header in enumerate(headers):
            header_lower = header.lower()
            if 'wein' in header_lower or 'kategorie' in header_lower:
                col_indices['wine_name'] = idx
            elif 'appellation' in header_lower or 'status' in header_lower:
                col_indices['appellation_status'] = idx
            elif 'klassifikation' in header_lower or 'reifung' in header_lower:
                col_indices['classification'] = idx
            elif 'beschreibung' in header_lower or 'charakter' in header_lower:
                col_indices['description'] = idx
            elif 'rebsorte' in header_lower:
                col_indices['grape'] = idx
            elif 'pairing' in header_lower:
                col_indices['pairing'] = idx
        
        sheet_wines = 0
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not any(row):
                continue
            
            # Get wine name
            wine_name = None
            if 'wine_name' in col_indices and col_indices['wine_name'] < len(row):
                wine_name = row[col_indices['wine_name']]
            
            if not wine_name:
                continue
            
            wine_name = str(wine_name).strip()
            
            # Get appellation/status (contains region/appellation/country hierarchy)
            appellation_status = None
            if 'appellation_status' in col_indices and col_indices['appellation_status'] < len(row):
                appellation_status = row[col_indices['appellation_status']]
            
            if appellation_status:
                appellation_status = str(appellation_status).strip()
            
            # Parse the hierarchy
            hierarchy = parse_appellation_status(appellation_status)
            
            # Get description
            description = None
            if 'description' in col_indices and col_indices['description'] < len(row):
                description = row[col_indices['description']]
            
            if not description:
                continue
                
            description = str(description).strip()
            desc_de, desc_en, desc_fr = extract_multilingual_description(description)
            
            # Get grape variety
            grape = 'Unbekannt'
            if 'grape' in col_indices and col_indices['grape'] < len(row):
                grape_val = row[col_indices['grape']]
                if grape_val:
                    grape = str(grape_val).strip()
            
            # Get food pairings
            pairings = []
            if 'pairing' in col_indices and col_indices['pairing'] < len(row):
                pairing_val = row[col_indices['pairing']]
                if pairing_val:
                    pairings = [p.strip() for p in str(pairing_val).split(',') if p.strip()]
            
            # Get classification from separate column if exists
            classification = hierarchy.get('classification')
            if 'classification' in col_indices and col_indices['classification'] < len(row):
                class_val = row[col_indices['classification']]
                if class_val:
                    classification = str(class_val).strip()
            
            # Extract winery from wine name (usually first word or before space)
            winery = wine_name.split()[0] if wine_name else 'Unbekannt'
            
            # Determine wine color
            wine_color = determine_wine_color(wine_name, grape, hierarchy.get('region', ''), sheet_name)
            
            # Determine price category
            price_category = determine_price_category(classification, wine_name, sheet_name)
            
            wine = {
                'id': str(uuid.uuid4()),
                'name': wine_name,
                'winery': winery,
                'country': hierarchy.get('country') or 'Unbekannt',
                'region': hierarchy.get('region') or 'Unbekannt',
                'appellation': hierarchy.get('appellation') or hierarchy.get('region') or 'Unbekannt',
                'grape_variety': grape,
                'wine_color': wine_color,
                'year': None,
                'description_de': desc_de,
                'description_en': desc_en,
                'description_fr': desc_fr,
                'tasting_notes': classification,
                'food_pairings_de': pairings,
                'food_pairings_en': pairings,  # TODO: translate in future
                'food_pairings_fr': pairings,  # TODO: translate in future
                'alcohol_content': None,
                'price_category': price_category,
                'image_url': '/placeholder-wine.png',
                'rating': None,
                'created_at': datetime.now(timezone.utc).isoformat()
            }
            
            all_wines.append(wine)
            sheet_wines += 1
        
        print(f"      → Extracted {sheet_wines} wines from sheet")
    
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
    print(f"   Countries ({len(countries)}): {', '.join(sorted(countries))}")
    
    colors = await db.public_wines.distinct("wine_color")
    print(f"   Wine colors ({len(colors)}): {', '.join(sorted(colors))}")
    
    # Show hierarchy samples
    print("\n📍 Sample Hierarchy:")
    samples = await db.public_wines.find(
        {"country": {"$ne": "Unbekannt"}}, 
        {"_id": 0, "name": 1, "country": 1, "region": 1, "appellation": 1}
    ).limit(5).to_list(5)
    
    for s in samples:
        print(f"   {s['name']}: {s['country']} → {s['region']} → {s['appellation']}")


async def main():
    print("🍷 Wine Database Import - Hierarchical Structure\n")
    print("=" * 60)
    
    # Use the correct Excel file
    file_path = '/app/wine_db_gross.xlsx'
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        # Try alternative
        file_path = '/app/wine_db_source.xlsx'
        if os.path.exists(file_path):
            print(f"   Using alternative: {file_path}")
        else:
            print("❌ No Excel file found!")
            return
    
    print(f"📂 Source file: {file_path}\n")
    
    wines = extract_wines_from_excel(file_path)
    
    if wines:
        await import_to_db(wines)
    else:
        print("❌ No wines extracted!")
    
    print("\n" + "=" * 60)
    print("✅ Import Complete!")


if __name__ == '__main__':
    asyncio.run(main())
