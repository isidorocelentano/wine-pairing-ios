"""
Final Import v2: Community Feed Posts with Regex extraction
Extracts multilingual content using regex patterns
"""
import asyncio
import os
import re
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
    "de": ["Tolle Kombination! 🍷", "Genau mein Geschmack!", "Fantastisch!", "Der Wein ist top!"],
    "en": ["Great pairing! 🍷", "Exactly my taste!", "Fantastic!", "That wine is great!"],
    "fr": ["Super combinaison! 🍷", "Exactement mon goût!", "Fantastique!", "Ce vin est top!"],
}


def extract_field(line: str, field_name: str) -> str:
    """Extract a field value from the CSV line using regex"""
    # Pattern for 'field': 'value' - handle escaped quotes and special chars
    pattern = rf"'{field_name}':\s*'([^']*(?:''[^']*)*)'"
    match = re.search(pattern, line)
    if match:
        return match.group(1).replace("''", "'")
    return ""


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
    return datetime.now(timezone.utc) - timedelta(days=random.randint(0, days_back_max), hours=random.randint(0, 23))


def generate_comments(num_comments: int, post_date: datetime) -> list:
    comments = []
    for _ in range(num_comments):
        commenter = random.choice(DEMO_USERS)
        comment_date = post_date + timedelta(hours=random.randint(1, 72))
        lang = random.choice(["de", "en", "fr"])
        comments.append({
            "id": str(uuid.uuid4()),
            "author_name": commenter["name"],
            "author_id": commenter["id"],
            "content": random.choice(COMMENT_TEMPLATES[lang]),
            "created_at": comment_date.isoformat()
        })
    return comments


def build_experience(loc, occ, desc):
    if not desc:
        return ""
    if loc and occ:
        return f"📍 {loc} | 🎉 {occ}\n\n{desc}"
    elif loc:
        return f"📍 {loc}\n\n{desc}"
    elif occ:
        return f"🎉 {occ}\n\n{desc}"
    return desc


async def import_with_regex(csv_path: str):
    """Import all posts using regex extraction"""
    
    print("🍷 Final Import v2: Regex-based Extraction\n")
    print("=" * 60)
    
    # Clear existing posts
    deleted = await db.feed_posts.delete_many({})
    print(f"🗑️  Cleared {deleted.deleted_count} existing posts")
    
    posts_to_insert = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"📊 Processing {len(lines) - 1} lines...")
    
    for i, line in enumerate(lines[1:], start=2):
        try:
            # Extract UUID
            id_match = re.search(r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}", line)
            post_id = id_match.group() if id_match else str(uuid.uuid4())
            
            # Extract wine name
            wine_name = extract_field(line, 'wine')
            if not wine_name:
                continue
            
            # German fields
            dish_de = extract_field(line, 'dish_de') or extract_field(line, 'dish')
            description_de = extract_field(line, 'description_de') or extract_field(line, 'description')
            location_de = extract_field(line, 'location_de') or extract_field(line, 'location')
            occasion_de = extract_field(line, 'occasion_de') or extract_field(line, 'occasion')
            
            # English fields
            dish_en = extract_field(line, 'dish_en')
            description_en = extract_field(line, 'description_en')
            location_en = extract_field(line, 'location_en')
            occasion_en = extract_field(line, 'occasion_en')
            
            # French fields
            dish_fr = extract_field(line, 'dish_fr')
            description_fr = extract_field(line, 'description_fr')
            location_fr = extract_field(line, 'location_fr')
            occasion_fr = extract_field(line, 'occasion_fr')
            
            if not dish_de:
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
            
            post = {
                "id": post_id,
                "author_name": author["name"],
                "author_id": author["id"],
                "wine_name": wine_name,
                "wine_type": wine_type,
                "rating": random.randint(4, 5),
                "image_base64": None,
                "likes": likes,
                "comments": generate_comments(num_comments, post_date),
                "created_at": post_date.isoformat(),
                # German
                "dish": dish_de,
                "experience": experience_de,
                "location": location_de,
                "occasion": occasion_de,
                # English
                "dish_en": dish_en,
                "experience_en": experience_en,
                "description_en": description_en,
                # French
                "dish_fr": dish_fr,
                "experience_fr": experience_fr,
                "description_fr": description_fr,
            }
            
            posts_to_insert.append(post)
            
        except Exception as e:
            print(f"  Line {i}: Error - {str(e)[:40]}")
    
    print(f"\n📝 Parsed {len(posts_to_insert)} posts")
    
    if posts_to_insert:
        await db.feed_posts.insert_many(posts_to_insert)
        print(f"✅ Inserted {len(posts_to_insert)} posts")
    
    # Statistics
    with_en_dish = await db.feed_posts.count_documents({"dish_en": {"$ne": ""}})
    with_en_exp = await db.feed_posts.count_documents({"experience_en": {"$ne": ""}})
    print(f"\n📊 Statistics:")
    print(f"   Posts with dish_en: {with_en_dish}/{len(posts_to_insert)}")
    print(f"   Posts with experience_en: {with_en_exp}/{len(posts_to_insert)}")
    
    # Sample
    sample = await db.feed_posts.find_one(
        {"dish_en": {"$ne": ""}},
        {"_id": 0, "dish": 1, "dish_en": 1, "dish_fr": 1, "experience": 1, "experience_en": 1}
    )
    if sample:
        print(f"\n📍 Sample:")
        print(f"   dish DE: {sample.get('dish', '')}")
        print(f"   dish EN: {sample.get('dish_en', '')}")
        print(f"   dish FR: {sample.get('dish_fr', '')}")
        print(f"   exp EN: {sample.get('experience_en', '')[:80]}...")


async def main():
    csv_path = '/tmp/community.csv'
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found")
        return
    await import_with_regex(csv_path)
    print("\n" + "=" * 60)
    print("✅ Import Complete!")


if __name__ == '__main__':
    asyncio.run(main())
