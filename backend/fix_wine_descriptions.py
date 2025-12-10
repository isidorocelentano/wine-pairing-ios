"""
Fix specific wine description mismatches
"""
import asyncio
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]


# Correct wine descriptions with specific country/region context
WINE_FIXES = [
    {
        "country": "Frankreich",
        "wine_name": "Pinot Noir aus Burgund",
        "descriptions": {
            "de": "Eleganter, komplexer Rotwein mit Aromen von roten Beeren, Erde und Gewürzen. Die Burgundy Pinot Noirs gehören zu den feinsten und elegantesten Rotweinen der Welt.",
            "en": "Elegant, complex red wine with aromas of red berries, earth and spices. Burgundy Pinot Noirs are among the finest and most elegant red wines in the world.",
            "fr": "Vin rouge élégant et complexe aux arômes de baies rouges, terre et épices. Les Pinot Noirs de Bourgogne sont parmi les vins rouges les plus fins et élégants du monde."
        }
    },
    {
        "country": "Schweiz",
        "wine_name": "Pinot Noir",
        "descriptions": {
            "de": "Schweizer Pinot Noir aus der Bündner Herrschaft – elegant mit feinen Fruchtaromen und alpiner Frische.",
            "en": "Swiss Pinot Noir from Graubünden Herrschaft – elegant with fine fruit aromas and alpine freshness.",
            "fr": "Pinot Noir suisse de la Seigneurie des Grisons – élégant avec de fins arômes fruités et une fraîcheur alpine."
        }
    },
    {
        "country": "Deutschland",
        "wine_name_regex": "Riesling",
        "descriptions": {
            "de": "Deutscher Riesling mit Steinobst, Zitrus und markanter Säure. Der Riesling ist Deutschlands große Rebsorte mit unverwechselbarer Mineralität.",
            "en": "German Riesling with stone fruit, citrus and pronounced acidity. Riesling is Germany's great grape variety with unmistakable minerality.",
            "fr": "Riesling allemand aux fruits à noyau, agrumes et acidité marquée. Le Riesling est le grand cépage allemand à la minéralité incomparable."
        }
    },
    {
        "country": "Frankreich",
        "region": "Elsass",
        "wine_name_regex": "Riesling",
        "descriptions": {
            "de": "Trockener Elsässer Riesling mit präziser Säure und mineralischen Noten. Der Elsass produziert kraftvolle, aromatische Rieslinge mit Eleganz.",
            "en": "Dry Alsatian Riesling with precise acidity and mineral notes. Alsace produces powerful, aromatic Rieslings with elegance.",
            "fr": "Riesling alsacien sec avec une acidité précise et des notes minérales. L'Alsace produit des Rieslings puissants et aromatiques avec élégance."
        }
    }
]


async def fix_wines():
    """Apply specific fixes to wine descriptions"""
    
    print("🔧 Fixing Wine Descriptions\n")
    print("=" * 60)
    
    fixed_count = 0
    
    for fix in WINE_FIXES:
        # Build query
        query = {}
        
        if "country" in fix:
            query["country"] = fix["country"]
        
        if "region" in fix:
            query["region"] = fix["region"]
        
        if "wine_name" in fix:
            query["wine_name"] = fix["wine_name"]
        elif "wine_name_regex" in fix:
            query["wine_name"] = {"$regex": fix["wine_name_regex"], "$options": "i"}
        
        # Apply update
        result = await db.regional_pairings.update_many(
            query,
            {
                "$set": {
                    "wine_description": fix["descriptions"]["de"],
                    "wine_description_en": fix["descriptions"]["en"],
                    "wine_description_fr": fix["descriptions"]["fr"]
                }
            }
        )
        
        if result.modified_count > 0:
            fixed_count += result.modified_count
            
            # Print what was fixed
            display_query = []
            if "country" in fix:
                display_query.append(f"Country: {fix['country']}")
            if "region" in fix:
                display_query.append(f"Region: {fix['region']}")
            if "wine_name" in fix:
                display_query.append(f"Wine: {fix['wine_name']}")
            elif "wine_name_regex" in fix:
                display_query.append(f"Wine: *{fix['wine_name_regex']}*")
            
            print(f"✓ Fixed {result.modified_count} pairing(s): {', '.join(display_query)}")
    
    print(f"\n{'='*60}")
    print(f"✅ Fixed {fixed_count} wine descriptions")
    
    # Verify the Boeuf Bourguignon fix
    print(f"\n📊 Verification:")
    boeuf = await db.regional_pairings.find_one(
        {"dish": {"$regex": "Boeuf Bourguignon"}},
        {"_id": 0, "dish": 1, "wine_name": 1, "wine_description": 1}
    )
    
    if boeuf:
        print(f"\nBoeuf Bourguignon + {boeuf['wine_name']}:")
        print(f"  DE: {boeuf['wine_description'][:70]}...")
        
        if "Schweiz" in boeuf['wine_description'] or "Graubünden" in boeuf['wine_description']:
            print(f"  ❌ Still has Swiss references!")
        else:
            print(f"  ✅ Correctly describes Burgundy Pinot Noir")


async def main():
    await fix_wines()
    print("\n" + "=" * 60)


if __name__ == '__main__':
    asyncio.run(main())
