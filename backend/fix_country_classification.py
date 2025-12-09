"""
Fix country classification - move regions from country field to proper countries
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# Mapping of incorrectly classified "countries" to their actual countries
REGION_FIX_MAP = {
    # USA Regions
    'Napa Valley': 'USA',
    'Kalifornien': 'USA',
    'California': 'USA',
    'Sonoma Coast': 'USA',
    'Santa Cruz Mountains': 'USA',
    'Oregon': 'USA',
    'Washington': 'USA',
    
    # Italien Regions
    'Toskana': 'Italien',
    'Piemont': 'Italien',
    'Südtirol': 'Italien',
    'Alto Adige': 'Italien',
    'Venetien': 'Italien',
    'Friaul': 'Italien',
    'Lombardei': 'Italien',
    
    # Österreich Regions
    'Wachau': 'Österreich',
    'Steiermark': 'Österreich',
    'Burgenland': 'Österreich',
    'Kamptal': 'Österreich',
    'Kremstal': 'Österreich',
    
    # Deutschland Regions
    'Rheinhessen': 'Deutschland',
    'Mosel': 'Deutschland',
    'Rheingau': 'Deutschland',
    'Nahe': 'Deutschland',
    'Pfalz': 'Deutschland',
    'Baden': 'Deutschland',
    'Franken': 'Deutschland',
    
    # Portugal Regions
    'Douro': 'Portugal',
    'Alentejo': 'Portugal',
    'Dão': 'Portugal',
    
    # Spanien Regions
    'Rioja': 'Spanien',
    'Ribera del Duero': 'Spanien',
    'Priorat': 'Spanien',
    
    # Argentinien Regions
    'Mendoza': 'Argentinien',
    
    # Chile Regions
    'Aconcagua Valley': 'Chile',
    'Maipo Valley': 'Chile',
    'Colchagua Valley': 'Chile',
    'Casablanca Valley': 'Chile',
    'Puente Alto': 'Chile',
    
    # Australien Regions
    'South Australia': 'Australien',
    'Eden Valley': 'Australien',
    'Barossa Valley': 'Australien',
    'Margaret River': 'Australien',
    
    # Schweiz Regions
    'Graubünden': 'Schweiz',
    'Wallis': 'Schweiz',
    'Tessin': 'Schweiz',
}


async def fix_countries():
    """Fix country classification"""
    
    updated = 0
    
    for wrong_country, correct_country in REGION_FIX_MAP.items():
        # Find wines with wrong country
        wines = await db.public_wines.find({"country": wrong_country}, {"_id": 0, "id": 1, "name": 1, "region": 1}).to_list(1000)
        
        if not wines:
            continue
        
        print(f"\n📍 {wrong_country} → {correct_country} ({len(wines)} wines)")
        
        for wine in wines:
            # Current region might be the same as country
            current_region = wine.get('region', wrong_country)
            
            # If region is empty or same as wrong country, use wrong_country as region
            if not current_region or current_region == wrong_country:
                new_region = wrong_country
            else:
                new_region = current_region
            
            # Update wine
            await db.public_wines.update_one(
                {"id": wine['id']},
                {"$set": {
                    "country": correct_country,
                    "region": new_region
                }}
            )
            
            print(f"  ✅ {wine['name']}: {new_region}, {correct_country}")
            updated += 1
    
    print(f"\n✅ Updated {updated} wines")
    
    # Show new distribution
    print("\n" + "=" * 60)
    print("NEW COUNTRY DISTRIBUTION")
    print("=" * 60)
    
    countries = await db.public_wines.aggregate([
        {"$group": {"_id": "$country", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]).to_list(100)
    
    for country in countries:
        print(f"  {country['_id']}: {country['count']} wines")


async def main():
    print("🍷 Fixing Country Classification")
    print("=" * 60)
    await fix_countries()
    print("\n✅ Done!")


if __name__ == '__main__':
    asyncio.run(main())
