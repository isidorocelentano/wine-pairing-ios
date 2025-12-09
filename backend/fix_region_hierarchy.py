"""
Fix region and appellation hierarchy in wine database
Create clean country -> region -> appellation mapping
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv('/app/backend/.env')

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# Mapping of regions to countries
REGION_TO_COUNTRY = {
    # Italien
    'Südtirol': 'Italien', 'Alto Adige': 'Italien', 'Toskana': 'Italien', 'Piemont': 'Italien',
    'Venetien': 'Italien', 'Apulien': 'Italien', 'Sizilien': 'Italien', 'Sardinien': 'Italien',
    'Lombardei': 'Italien', 'Friaul': 'Italien', 'Trentino': 'Italien', 'Umbrien': 'Italien',
    'Bolgheri': 'Italien', 'Barolo': 'Italien', 'Barbaresco': 'Italien', 'Chianti': 'Italien',
    'Montalcino': 'Italien', 'Montepulciano': 'Italien',
    
    # Frankreich
    'Bordeaux': 'Frankreich', 'Burgund': 'Frankreich', 'Bourgogne': 'Frankreich',
    'Champagne': 'Frankreich', 'Rhône': 'Frankreich', 'Loire': 'Frankreich',
    'Elsass': 'Frankreich', 'Alsace': 'Frankreich', 'Provence': 'Frankreich',
    'Languedoc-Roussillon': 'Frankreich', 'Côtes du Rhône': 'Frankreich',
    'Sauternes': 'Frankreich', 'Pomerol': 'Frankreich', 'Saint-Émilion': 'Frankreich',
    'Médoc': 'Frankreich', 'Margaux': 'Frankreich', 'Pauillac': 'Frankreich',
    'Saint-Estèphe': 'Frankreich', 'Saint-Julien': 'Frankreich',
    
    # Deutschland
    'Mosel': 'Deutschland', 'Rheingau': 'Deutschland', 'Rheinhessen': 'Deutschland',
    'Pfalz': 'Deutschland', 'Baden': 'Deutschland', 'Franken': 'Deutschland',
    'Württemberg': 'Deutschland', 'Nahe': 'Deutschland', 'Ahr': 'Deutschland',
    
    # Spanien
    'Rioja': 'Spanien', 'Ribera del Duero': 'Spanien', 'Priorat': 'Spanien',
    'Penedès': 'Spanien', 'Rías Baixas': 'Spanien', 'Jerez': 'Spanien',
    'Navarra': 'Spanien', 'Toro': 'Spanien', 'Rueda': 'Spanien',
    
    # Portugal
    'Douro': 'Portugal', 'Alentejo': 'Portugal', 'Dão': 'Portugal',
    'Vinho Verde': 'Portugal', 'Porto': 'Portugal',
    
    # Österreich
    'Wachau': 'Österreich', 'Kamptal': 'Österreich', 'Kremstal': 'Österreich',
    'Burgenland': 'Österreich', 'Steiermark': 'Österreich',
    
    # USA
    'Napa Valley': 'USA', 'Sonoma': 'USA', 'California': 'USA',
    'Oregon': 'USA', 'Washington': 'USA',
    
    # Australien
    'Barossa Valley': 'Australien', 'Margaret River': 'Australien',
    'Hunter Valley': 'Australien', 'Yarra Valley': 'Australien',
    
    # Neuseeland
    'Marlborough': 'Neuseeland', 'Central Otago': 'Neuseeland',
    'Hawke\'s Bay': 'Neuseeland',
    
    # Südafrika
    'Stellenbosch': 'Südafrika', 'Paarl': 'Südafrika',
    'Constantia': 'Südafrika', 'Franschhoek': 'Südafrika',
    
    # Chile
    'Maipo Valley': 'Chile', 'Colchagua Valley': 'Chile',
    'Casablanca Valley': 'Chile',
    
    # Argentinien
    'Mendoza': 'Argentinien', 'Salta': 'Argentinien',
}


async def fix_hierarchy():
    """Fix country, region, appellation hierarchy"""
    
    wines = await db.public_wines.find({}, {"_id": 0}).to_list(10000)
    print(f"📊 Processing {len(wines)} wines\n")
    
    updated = 0
    errors = 0
    
    # Track hierarchy
    hierarchy = defaultdict(lambda: defaultdict(set))
    
    for wine in wines:
        wine_id = wine['id']
        name = wine['name']
        region = wine.get('region', 'Unbekannt')
        country = wine.get('country', 'Unbekannt')
        appellation = wine.get('appellation', region)
        
        # Fix country based on region
        if region in REGION_TO_COUNTRY:
            correct_country = REGION_TO_COUNTRY[region]
            if country != correct_country:
                country = correct_country
        
        # Clean up region/appellation
        if '/' in region:
            parts = [p.strip() for p in region.split('/')]
            region = parts[0]
            if appellation == wine.get('region'):
                appellation = parts[1] if len(parts) > 1 else region
        
        # Ensure appellation is more specific than region
        if appellation == region or not appellation or appellation == 'Unbekannt':
            # Try to use more specific data
            if '/' in wine.get('appellation', ''):
                parts = wine.get('appellation').split('/')
                appellation = parts[-1].strip()
        
        # Update wine
        try:
            await db.public_wines.update_one(
                {"id": wine_id},
                {"$set": {
                    "country": country,
                    "region": region,
                    "appellation": appellation
                }}
            )
            
            # Track hierarchy
            hierarchy[country][region].add(appellation)
            updated += 1
            
        except Exception as e:
            print(f"❌ Error updating {name}: {str(e)}")
            errors += 1
    
    print(f"\n✅ Updated {updated} wines")
    print(f"❌ Errors: {errors}")
    
    # Print hierarchy
    print("\n" + "=" * 60)
    print("WINE HIERARCHY")
    print("=" * 60)
    
    for country in sorted(hierarchy.keys()):
        print(f"\n🌍 {country}")
        for region in sorted(hierarchy[country].keys()):
            print(f"  📍 {region}")
            appellations = sorted(hierarchy[country][region])
            for app in appellations[:5]:  # Show first 5
                if app != region:
                    print(f"      • {app}")
            if len(appellations) > 5:
                print(f"      ... and {len(appellations) - 5} more")


async def main():
    print("🍷 Fixing Region Hierarchy")
    print("=" * 60)
    await fix_hierarchy()
    print("\n✅ Done!")


if __name__ == '__main__':
    asyncio.run(main())
