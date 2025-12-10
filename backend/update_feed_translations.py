"""
Update Community Feed Posts with translations from CSV
The original CSV contains all translations - we just need to update the DB
"""
import csv
import asyncio
import os
import ast
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'wine_pairing_db')]


def parse_content(content_str: str) -> dict:
    """Parse the content string which is a Python dict literal"""
    try:
        return ast.literal_eval(content_str)
    except (ValueError, SyntaxError) as e:
        return {}


async def update_translations(csv_path: str):
    """Update posts with translations from CSV"""
    
    print("🌍 Updating Feed Posts with Translations\n")
    print("=" * 60)
    
    updated = 0
    errors = 0
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            post_id = row['id']
            content = parse_content(row['content'])
            
            if not content:
                errors += 1
                continue
            
            # Build experience texts for each language
            location_de = content.get('location_de', content.get('location', ''))
            location_en = content.get('location_en', '')
            location_fr = content.get('location_fr', '')
            
            occasion_de = content.get('occasion_de', content.get('occasion', ''))
            occasion_en = content.get('occasion_en', '')
            occasion_fr = content.get('occasion_fr', '')
            
            description_de = content.get('description_de', content.get('description', ''))
            description_en = content.get('description_en', '')
            description_fr = content.get('description_fr', '')
            
            # Build full experience with location/occasion prefix
            def build_experience(loc, occ, desc):
                if loc and occ:
                    return f"📍 {loc} | 🎉 {occ}\n\n{desc}"
                elif loc:
                    return f"📍 {loc}\n\n{desc}"
                elif occ:
                    return f"🎉 {occ}\n\n{desc}"
                return desc
            
            experience_de = build_experience(location_de, occasion_de, description_de)
            experience_en = build_experience(location_en, occasion_en, description_en)
            experience_fr = build_experience(location_fr, occasion_fr, description_fr)
            
            # Update document
            update_data = {
                # German (primary)
                "dish": content.get('dish_de', content.get('dish', '')),
                "experience": experience_de,
                # English
                "dish_en": content.get('dish_en', ''),
                "description_en": description_en,
                "experience_en": experience_en,
                "location_en": location_en,
                "occasion_en": occasion_en,
                # French
                "dish_fr": content.get('dish_fr', ''),
                "description_fr": description_fr,
                "experience_fr": experience_fr,
                "location_fr": location_fr,
                "occasion_fr": occasion_fr,
                # Location/occasion in German for reference
                "location": location_de,
                "occasion": occasion_de,
            }
            
            result = await db.feed_posts.update_one(
                {"id": post_id},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                updated += 1
    
    print(f"✅ Updated {updated} posts with translations")
    print(f"⚠️ Errors: {errors}")
    
    # Verify
    sample = await db.feed_posts.find_one(
        {"dish_en": {"$exists": True, "$ne": ""}},
        {"_id": 0, "dish": 1, "dish_en": 1, "dish_fr": 1, "experience_en": 1}
    )
    if sample:
        print(f"\n📍 Sample:")
        print(f"   DE: {sample.get('dish', '')}")
        print(f"   EN: {sample.get('dish_en', '')}")
        print(f"   FR: {sample.get('dish_fr', '')}")
        if sample.get('experience_en'):
            print(f"   Experience EN: {sample.get('experience_en', '')[:100]}...")


async def main():
    csv_path = '/tmp/community.csv'
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return
    
    await update_translations(csv_path)
    print("\n" + "=" * 60)
    print("✅ Translation Update Complete!")


if __name__ == '__main__':
    asyncio.run(main())
