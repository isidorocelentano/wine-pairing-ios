"""
Final Import: Community Feed Posts with JSON parsing
Uses json.loads instead of ast.literal_eval for better Unicode handling
"""
import asyncio
import os
import json
import random
import re
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


def convert_python_dict_to_json(s: str) -> str:
    """Convert Python dict literal to JSON string"""
    # Replace single quotes with double quotes, but be careful with apostrophes
    # This is a simplified approach
    result = s
    # Replace Python-style quotes with JSON-style
    result = re.sub(r"'([^']*)'(\s*:)", r'"\1"\2', result)  # Keys
    result = re.sub(r":\s*'([^']*)'", r': "\1"', result)  # String values
    return result


async def final_import(csv_path: str):
    """Import all posts with proper JSON parsing"""
    
    print("🍷 Final Import: Community Feed with Translations\n")
    print("=" * 60)
    
    # Clear existing posts
    deleted = await db.feed_posts.delete_many({})
    print(f"🗑️  Cleared {deleted.deleted_count} existing posts")
    
    posts_to_insert = []
    errors = []
    
    # Read file content
    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Skip header
    header = lines[0].strip()
    print(f"📊 Header: {header[:80]}...")
    
    # Process each line
    for i, line in enumerate(lines[1:], start=2):
        try:
            # Extract the content dict using regex
            # The content is a Python dict starting with {' and ending with '}
            match = re.search(r"\{'wine':\s*'[^}]+\}", line)
            if not match:
                # Try to find JSON-like dict
                match = re.search(r'\{["\']wine["\']:\s*["\'][^}]+\}', line)
            
            if not match:
                errors.append(f"Line {i}: No content dict found")
                continue
            
            content_str = match.group()
            
            # Convert to proper JSON
            try:
                # First try direct json parse (if it's already JSON)
                content = json.loads(content_str)
            except json.JSONDecodeError:
                # Convert Python dict literal to JSON
                json_str = content_str.replace("'", '"')
                try:
                    content = json.loads(json_str)
                except json.JSONDecodeError:
                    # More aggressive conversion
                    json_str = convert_python_dict_to_json(content_str)
                    content = json.loads(json_str)
            
            # Extract UUID from line
            id_match = re.search(r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}", line)
            post_id = id_match.group() if id_match else str(uuid.uuid4())
            
            # Get translations
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
                errors.append(f"Line {i}: Missing wine or dish")
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
                # French
                "dish_fr": dish_fr,
                "experience_fr": experience_fr,
                "description_fr": description_fr,
            }
            
            posts_to_insert.append(post)
            
        except Exception as e:
            errors.append(f"Line {i}: {str(e)[:50]}")
            continue
    
    print(f"📝 Parsed {len(posts_to_insert)} posts")
    print(f"⚠️ Errors: {len(errors)}")
    
    if errors[:5]:
        print(f"   First errors: {errors[:5]}")
    
    if posts_to_insert:
        await db.feed_posts.insert_many(posts_to_insert)
        print(f"✅ Inserted {len(posts_to_insert)} posts")
    
    # Statistics
    with_en = await db.feed_posts.count_documents({"dish_en": {"$ne": "", "$exists": True}})
    print(f"\n📊 Posts with English dish: {with_en}/{len(posts_to_insert)}")
    
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


async def main():
    csv_path = '/tmp/community.csv'
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found")
        return
    await final_import(csv_path)
    print("\n" + "=" * 60)
    print("✅ Import Complete!")


if __name__ == '__main__':
    asyncio.run(main())
