"""
Import wines from Excel into the public_wines collection
Handles semicolon-separated data in single column (wine_db_gross.xlsx format)
Correctly parses the hierarchical structure from 'Appellation / Status' field.

Data format analysis:
- "Region / Classification or Appellation / Country"
- Examples:
  - "Südtirol / Alto Adige / Italien" → Region: Südtirol, Appellation: Alto Adige
  - "Rioja / Gran Reserva / Spanien" → Region: Rioja, Classification: Gran Reserva (NOT appellation)
  - "Bordeaux / Margaux / Frankreich" → Region: Bordeaux, Appellation: Margaux
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

# Known appellations (real geographic sub-regions)
KNOWN_APPELLATIONS = {
    # France - Bordeaux
    'margaux', 'pauillac', 'saint-estèphe', 'saint-julien', 'pomerol', 
    'saint-émilion', 'pessac-léognan', 'sauternes', 'barsac', 'graves',
    'médoc', 'haut-médoc', 'listrac', 'moulis', 'côtes de bordeaux',
    # France - Burgundy
    'gevrey-chambertin', 'chambolle-musigny', 'vosne-romanée', 'nuits-saint-georges',
    'beaune', 'pommard', 'volnay', 'meursault', 'puligny-montrachet', 'chassagne-montrachet',
    'chablis', 'côte de nuits', 'côte de beaune', 'mâconnais', 'côte chalonnaise',
    # Italy
    'alto adige', 'brunello di montalcino', 'chianti classico', 'valpolicella',
    'barolo', 'barbaresco', 'amarone', 'prosecco', 'franciacorta', 'montepulciano',
    'bolgheri', 'montalcino', 'maremma', 'langhe', 'roero', 'gavi',
    # Spain  
    'rioja alta', 'rioja alavesa', 'rioja baja', 'ribera del duero',
    'priorat', 'penedès', 'rías baixas', 'rueda', 'toro', 'navarra',
    'jerez', 'manchuela', 'jumilla', 'yecla', 'alicante',
    # Germany
    'mosel', 'rheingau', 'rheinhessen', 'pfalz', 'nahe', 'baden', 'franken',
    'württemberg', 'ahr', 'mittelrhein',
    # Portugal
    'douro', 'dão', 'alentejo', 'bairrada', 'vinho verde',
    # Other
    'napa valley', 'sonoma', 'willamette valley', 'marlborough', 'barossa valley',
    'mendoza', 'maipo valley', 'colchagua', 'casablanca valley',
}

# Classification terms that should NOT be used as appellation
CLASSIFICATION_TERMS = {
    # Quality classifications
    'cru', 'doc', 'docg', 'igt', 'vdit', 'do', 'doca',
    'reserva', 'crianza', 'gran reserva', 'grand cru', 'premier cru',
    'gran selezione', 'riserva', 'superiore',
    'premier cru supérieur', 'premier cru classé', 'deuxième cru',
    # Wine types (not geographic)
    'rotwein', 'weißwein', 'schaumwein', 'süßwein', 'rosado', 'rosé',
    'cava', 'champagner', 'sekt', 'prosecco',
    # Status terms
    'status', 'prestige-wein', 'kult-wein', 'ikone', 'ikonen-status', 
    'basiswein', 'zweitwein', 'super tuscan',
    # Generic
    'appellation',
}


def is_classification_term(value: str) -> bool:
    """Check if a value is a classification term, not a geographic appellation"""
    if not value:
        return True
    value_lower = value.lower().strip()
    return value_lower in CLASSIFICATION_TERMS


def is_known_appellation(value: str) -> bool:
    """Check if a value is a known geographic appellation"""
    if not value:
        return False
    value_lower = value.lower().strip()
    return value_lower in KNOWN_APPELLATIONS


def parse_appellation_status(value: str) -> dict:
    """
    Parse the 'Appellation / Status' field.
    Format: "Region / Classification or Appellation / Country"
    
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
    
    # Standard format: Region / Appellation_or_Class / Country
    if len(parts) == 3:
        # Last part is usually country
        if parts[2].lower() in KNOWN_COUNTRIES:
            country = KNOWN_COUNTRIES[parts[2].lower()]
        
        # First part is region
        region = parts[0]
        
        # Middle part: check if it's a classification or real appellation
        middle = parts[1]
        if is_classification_term(middle):
            classification = middle
            # For classification-only cases, use region as appellation too
            appellation = region
        else:
            # It's a real appellation
            appellation = middle
            
    elif len(parts) == 2:
        # Could be Region / Country or Region / Classification
        if parts[1].lower() in KNOWN_COUNTRIES:
            country = KNOWN_COUNTRIES[parts[1].lower()]
            region = parts[0]
            appellation = parts[0]  # Use region as appellation
        else:
            region = parts[0]
            if is_classification_term(parts[1]):
                classification = parts[1]
                appellation = region
            else:
                appellation = parts[1]
    elif len(parts) == 1:
        region = parts[0]
        appellation = parts[0]
    
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
        'viognier', 'chenin', 'semillon', 'trebbiano', 'vermentino', 'weißwein'
    ]
    
    rose_indicators = ['rosé', 'rose', 'rosado', 'rosato']
    sweet_indicators = ['sauternes', 'süß', 'sweet', 'tokaji', 'eiswein', 'auslese', 
                       'beerenauslese', 'trockenbeerenauslese', 'süßwein']
    sparkling_indicators = ['champagne', 'champagner', 'sekt', 'cava', 'prosecco', 
                           'crémant', 'spumante', 'schaumwein', 'franciacorta']
    
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
                   'ikonen-status', 'pétrus', 'lafite', 'latour', 'margaux', 'mouton']
    premium_terms = ['reserva', 'gran reserva', 'barbaresco', 'barolo', 'brunello', 
                    'super tuscan', 'crianza', 'riserva']
    
    if any(term in context for term in luxury_terms):
        return 'luxury'
    if any(term in context for term in premium_terms):
        return 'premium'
    
    return 'mid-range'


def extract_wines_from_semicolon_format(file_path):
    """Extract wines from Excel where data is semicolon-separated in single column."""
    wb = openpyxl.load_workbook(file_path, data_only=True)
    all_wines = []
    
    print(f"📊 Processing {len(wb.sheetnames)} sheets")
    
    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        
        header_row = sheet[1]
        header_value = header_row[0].value if header_row[0].value else ""
        
        if ';' in str(header_value):
            print(f"\n   📄 Sheet '{sheet_name}' - Semicolon-separated format")
            headers = [h.strip() for h in str(header_value).split(';')]
            
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
                
                # Use classification from column if not found in hierarchy
                classification = hierarchy.get('classification') or classification_col
                
                # Extract multilingual descriptions
                desc_de, desc_en, desc_fr = extract_multilingual_description(description)
                
                # Parse pairings
                pairings = [p.strip() for p in pairing.split(',') if p.strip()] if pairing else []
                
                # Extract winery
                winery = wine_name.split()[0] if wine_name else 'Unbekannt'
                
                # Determine wine color (use classification for better detection)
                wine_color = determine_wine_color(wine_name, grape, hierarchy.get('region', ''), classification)
                
                # Determine price category
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
    """Import wines to public_wines collection"""
    
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
    
    regions = await db.public_wines.distinct("region")
    valid_regions = sorted([r for r in regions if r and r != 'Unbekannt'])
    print(f"   Regions ({len(valid_regions)}): {', '.join(valid_regions[:20])}...")
    
    appellations = await db.public_wines.distinct("appellation")
    valid_apps = sorted([a for a in appellations if a and a != 'Unbekannt'])
    print(f"   Appellations ({len(valid_apps)}): {', '.join(valid_apps[:20])}...")
    
    colors = await db.public_wines.distinct("wine_color")
    print(f"   Wine colors ({len(colors)}): {', '.join(sorted(colors))}")
    
    # Sample hierarchy
    print("\n📍 Sample Hierarchy:")
    samples = await db.public_wines.find(
        {"country": {"$ne": "Unbekannt"}}, 
        {"_id": 0, "name": 1, "country": 1, "region": 1, "appellation": 1}
    ).limit(8).to_list(8)
    
    for s in samples:
        name = s['name'][:35] + '...' if len(s['name']) > 35 else s['name']
        print(f"   {name}: {s['country']} → {s['region']} → {s['appellation']}")


async def main():
    print("🍷 Wine Database Import - Correct Hierarchical Structure\n")
    print("=" * 60)
    
    file_path = '/app/wine_db_gross.xlsx'
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"📂 Source: {file_path}\n")
    
    wines = extract_wines_from_semicolon_format(file_path)
    
    if wines:
        await import_to_db(wines)
    else:
        print("❌ No wines extracted!")
    
    print("\n" + "=" * 60)
    print("✅ Import Complete!")


if __name__ == '__main__':
    asyncio.run(main())
