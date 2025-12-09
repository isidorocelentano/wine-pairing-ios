"""
Clean up regions and appellations hierarchy
- Move appellations from region field to appellation field
- Add proper Bordeaux region
- Fix inconsistencies
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# Bordeaux appellations that are wrongly in region field
BORDEAUX_APPELLATIONS = {
    'Margaux', 'Pauillac', 'Pessac-Léognan', 'Pomerol', 
    'Saint-Estèphe', 'Saint-Julien', 'Saint-Émilion',
    'Médoc', 'Haut-Médoc', 'Graves', 'Listrac-Médoc',
    'Moulis-en-Médoc', 'Fronsac', 'Canon-Fronsac'
}

# Region name fixes
REGION_FIXES = {
    'Champagner': 'Champagne',
    'Bourgogne': 'Burgund',
    'Alsace': 'Elsass',
}


async def clean_regions_appellations():
    """Clean up regions and appellations"""
    
    wines = await db.public_wines.find({}, {"_id": 0}).to_list(10000)
    print(f"📊 Processing {len(wines)} wines\n")
    
    updated = 0
    
    for wine in wines:
        wine_id = wine['id']
        name = wine['name']
        region = wine.get('region', '')
        appellation = wine.get('appellation', '')
        country = wine.get('country', '')
        
        changed = False
        new_region = region
        new_appellation = appellation
        
        # Fix Bordeaux appellations
        if region in BORDEAUX_APPELLATIONS:
            print(f"📍 {name}: {region} → Bordeaux (appellation: {region})")
            new_region = 'Bordeaux'
            new_appellation = region
            changed = True
        
        # Fix region names
        if region in REGION_FIXES:
            old_region = region
            new_region = REGION_FIXES[region]
            print(f"🔄 {name}: {old_region} → {new_region}")
            changed = True
        
        # Ensure appellation is not empty or same as region
        if not new_appellation or new_appellation == 'Unbekannt':
            if new_region and new_region != 'Unbekannt':
                new_appellation = new_region
                changed = True
        
        # Update if needed
        if changed:
            await db.public_wines.update_one(
                {"id": wine_id},
                {"$set": {
                    "region": new_region,
                    "appellation": new_appellation
                }}
            )
            updated += 1
    
    print(f"\n✅ Updated {updated} wines")
    
    # Show final distribution
    print("\n" + "=" * 60)
    print("REGION DISTRIBUTION")
    print("=" * 60)
    
    regions = await db.public_wines.aggregate([
        {"$match": {"country": "Frankreich"}},
        {"$group": {"_id": "$region", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]).to_list(100)
    
    print("\nFrankreich Regionen:")
    for r in regions:
        print(f"  {r['_id']}: {r['count']} wines")
    
    # Show Bordeaux appellations
    print("\n" + "=" * 60)
    print("BORDEAUX APPELLATIONS")
    print("=" * 60)
    
    bordeaux_apps = await db.public_wines.aggregate([
        {"$match": {"region": "Bordeaux"}},
        {"$group": {"_id": "$appellation", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]).to_list(100)
    
    for app in bordeaux_apps:
        print(f"  {app['_id']}: {app['count']} wines")


async def main():
    print("🍷 Cleaning Regions & Appellations")
    print("=" * 60)
    await clean_regions_appellations()
    print("\n✅ Done!")


if __name__ == '__main__':
    asyncio.run(main())
