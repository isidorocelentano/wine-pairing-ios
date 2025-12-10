"""
Re-import Community Feed Posts with all translations
Clears existing posts and imports fresh with all multilingual content
"""
import csv
import asyncio
import os
import ast
import random
from pathlib import Path
from datetime import datetime, timezone, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import uuid

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'wine_pairing_db')]

# Demo Users
DEMO_USERS = [
    {"id": "claude_sommelier", "name": "Claude Sommelier"},
    {"id": "maria_veneto", "name": "Maria aus Veneto"},
    {"id": "hans_rheingau", "name": "Hans vom Rheingau"},
    {"id": "sophie_bordeaux", "name": "Sophie de Bordeaux"},
    {"id": "marco_toscana", "name": "Marco Toscana"},
    {"id": "lisa_wien", "name": "Lisa aus Wien"},
    {"id": "pierre_bourgogne", "name": "Pierre Bourgogne"},
    {"id": "anna_piemont", "name": "Anna Piemonte"},
    {"id": "thomas_mosel", "name": "Thomas Mosel"},
    {"id": "elena_rioja", "name": "Elena Rioja"},
]

COMMENT_TEMPLATES = {
    "de": ["Tolle Kombination! 🍷", "Genau mein Geschmack!", "Fantastisch!", "Der Wein ist top!", "Muss ich probieren!"],
    "en": ["Great pairing! 🍷", "Exactly my taste!", "Fantastic!", "That wine is great!", "Need to try this!"],
    "fr": ["Super combinaison! 🍷", "Exactement mon goût!", "Fantastique!", "Ce vin est top!", "À essayer!"],
}


def determine_wine_type(wine_name: str, description: str) -> str:
    context = f"{wine_name} {description}".lower()
    if any(w in context for w in ['bianco', 'blanc', 'white', 'weiss', 'weiß', 'grillo', 'chardonnay', 'riesling', 'sauvignon']):
        return 'weiss'
    if any(w in context for w in ['rosé', 'rose', 'rosato', 'rosado']):
        return 'rose'
    if any(w in context for w in ['spumante', 'champagne', 'prosecco', 'cava', 'sekt', 'schaumwein', 'brut']):
        return 'schaumwein'
    return 'rot'


def generate_random_date(days_back_max: int = 60) -> datetime:
    days_ago = random.randint(0, days_back_max)
    hours_ago = random.randint(0, 23)
    return datetime.now(timezone.utc) - timedelta(days=days_ago, hours=hours_ago)


def generate_comments(num_comments: int, post_date: datetime) -> list:
    comments = []
    for i in range(num_comments):
        commenter = random.choice(DEMO_USERS)
        comment_date = post_date + timedelta(hours=random.randint(1, 72))
        lang = random.choice(["de", "en", "fr"])
        content = random.choice(COMMENT_TEMPLATES[lang])
        
        comments.append({
            "id": str(uuid.uuid4()),
            "author_name": commenter["name"],
            "author_id": commenter["id"],
            "content": content,
            "created_at": comment_date.isoformat()
        })
    return comments


def build_experience(loc, occ, desc):
    """Build experience text with location and occasion prefix"""
    if not desc:
        return ""
    if loc and occ:
        return f"📍 {loc} | 🎉 {occ}\n\n{desc}"
    elif loc:
        return f"📍 {loc}\n\n{desc}"
    elif occ:
        return f"🎉 {occ}\n\n{desc}"
    return desc


async def reimport_community_posts(csv_path: str):
    """Clear and reimport all posts with translations"""
    
    print("🍷 Re-importing Community Feed with Translations\n")
    print("=" * 60)
    
    # Clear existing posts
    deleted = await db.feed_posts.delete_many({})
    print(f"🗑️  Cleared {deleted.deleted_count} existing posts")
    
    posts_to_insert = []
    
    # Read CSV with proper parsing
    with open(csv_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse CSV manually to handle complex content field
    lines = content.strip().split('\n')
    header = lines[0].split(',')
    
    # Find column indices
    try:
        id_idx = header.index('id')
        content_idx = header.index('content')
    except ValueError:
        print("❌ Could not find required columns")
        return
    
    current_row = ""
    rows_data = []
    
    for line in lines[1:]:
        current_row += line
        # Check if we have a complete row (content dict is closed)
        if current_row.count('{') == current_row.count('}'):
            rows_data.append(current_row)
            current_row = ""
        else:
            current_row += "\n"
    
    print(f"📊 Found {len(rows_data)} rows to process")
    
    for row_str in rows_data:
        try:
            # Extract content dict using regex
            import re
            content_match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", row_str)
            if not content_match:
                continue
            
            content_str = content_match.group()
            content = ast.literal_eval(content_str)
            
            # Extract ID (first UUID in the row)
            id_match = re.search(r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}", row_str)
            post_id = id_match.group() if id_match else str(uuid.uuid4())
            
            # Get all translations
            wine_name = content.get('wine', '')
            
            # German
            dish_de = content.get('dish_de', content.get('dish', ''))
            description_de = content.get('description_de', content.get('description', ''))
            location_de = content.get('location_de', content.get('location', ''))
            occasion_de = content.get('occasion_de', content.get('occasion', ''))
            
            # English
            dish_en = content.get('dish_en', '')
            description_en = content.get('description_en', '')
            location_en = content.get('location_en', '')
            occasion_en = content.get('occasion_en', '')
            
            # French
            dish_fr = content.get('dish_fr', '')
            description_fr = content.get('description_fr', '')
            location_fr = content.get('location_fr', '')
            occasion_fr = content.get('occasion_fr', '')
            
            if not wine_name or not dish_de:
                continue
            
            # Build experiences
            experience_de = build_experience(location_de, occasion_de, description_de)
            experience_en = build_experience(location_en, occasion_en, description_en)
            experience_fr = build_experience(location_fr, occasion_fr, description_fr)
            
            # Generate metadata
            author = random.choice(DEMO_USERS)
            wine_type = determine_wine_type(wine_name, description_de)
            post_date = generate_random_date(60)
            num_likes = random.randint(0, 25)
            num_comments = random.randint(0, 5) if random.random() < 0.4 else 0
            likes = list(set([random.choice(DEMO_USERS)["id"] for _ in range(num_likes)]))
            comments = generate_comments(num_comments, post_date)
            
            post = {
                "id": post_id,
                "author_name": author["name"],
                "author_id": author["id"],
                "wine_name": wine_name,
                "wine_type": wine_type,
                "rating": random.randint(4, 5),
                "image_base64": None,
                "likes": likes,
                "comments": comments,
                "created_at": post_date.isoformat(),
                # German (primary)
                "dish": dish_de,
                "experience": experience_de,
                "location": location_de,
                "occasion": occasion_de,
                # English
                "dish_en": dish_en,
                "experience_en": experience_en,
                "description_en": description_en,
                "location_en": location_en,
                "occasion_en": occasion_en,
                # French
                "dish_fr": dish_fr,
                "experience_fr": experience_fr,
                "description_fr": description_fr,
                "location_fr": location_fr,
                "occasion_fr": occasion_fr,
            }
            
            posts_to_insert.append(post)
            
        except Exception as e:
            print(f"  ⚠️ Error parsing row: {e}")
            continue
    
    print(f"📝 Parsed {len(posts_to_insert)} posts")
    
    if posts_to_insert:
        await db.feed_posts.insert_many(posts_to_insert)
        print(f"✅ Inserted {len(posts_to_insert)} posts")
    
    # Verify translations
    sample = await db.feed_posts.find_one(
        {"dish_en": {"$exists": True, "$ne": ""}},
        {"_id": 0, "dish": 1, "dish_en": 1, "dish_fr": 1, "experience_en": 1}
    )
    if sample:
        print(f"\n📍 Sample Translation:")
        print(f"   DE: {sample.get('dish', '')}")
        print(f"   EN: {sample.get('dish_en', '')}")
        print(f"   FR: {sample.get('dish_fr', '')}")
        if sample.get('experience_en'):
            print(f"   Exp EN: {sample.get('experience_en', '')[:80]}...")
    
    # Count posts with translations
    with_en = await db.feed_posts.count_documents({"dish_en": {"$exists": True, "$ne": ""}})
    print(f"\n📊 Posts with English translation: {with_en}/{len(posts_to_insert)}")


async def main():
    csv_path = '/tmp/community.csv'
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return
    
    await reimport_community_posts(csv_path)
    print("\n" + "=" * 60)
    print("✅ Re-import Complete!")


if __name__ == '__main__':
    asyncio.run(main())
