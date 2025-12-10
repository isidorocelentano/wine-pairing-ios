"""
Import Community Feed Posts from CSV
Creates demo users and imports wine pairing posts with simulated engagement
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

# Demo Users - Wine enthusiasts from different backgrounds
DEMO_USERS = [
    {"id": "claude_sommelier", "name": "Claude Sommelier", "avatar": "sommelier", "bio": "Master of Wine & leidenschaftlicher Koch"},
    {"id": "maria_veneto", "name": "Maria aus Veneto", "avatar": "user1", "bio": "Weinliebhaberin aus Italien"},
    {"id": "hans_rheingau", "name": "Hans vom Rheingau", "avatar": "user2", "bio": "Winzer in 4. Generation"},
    {"id": "sophie_bordeaux", "name": "Sophie de Bordeaux", "avatar": "user3", "bio": "Sommelière & Food Blogger"},
    {"id": "marco_toscana", "name": "Marco Toscana", "avatar": "user4", "bio": "Koch & Weinkenner"},
    {"id": "lisa_wien", "name": "Lisa aus Wien", "avatar": "user5", "bio": "Weinakademikerin"},
    {"id": "pierre_bourgogne", "name": "Pierre Bourgogne", "avatar": "user6", "bio": "Négociant & Gourmet"},
    {"id": "anna_piemont", "name": "Anna Piemonte", "avatar": "user7", "bio": "Nebbiolo-Liebhaberin"},
    {"id": "thomas_mosel", "name": "Thomas Mosel", "avatar": "user8", "bio": "Riesling-Enthusiast"},
    {"id": "elena_rioja", "name": "Elena Rioja", "avatar": "user9", "bio": "Spanische Weinexpertin"},
]

# Comment templates for simulated engagement
COMMENT_TEMPLATES_DE = [
    "Tolle Kombination! Das muss ich probieren. 🍷",
    "Genau mein Geschmack! Danke für den Tipp.",
    "Hab ich letzte Woche auch gemacht - fantastisch!",
    "Der Wein ist einer meiner Favoriten!",
    "Perfektes Pairing für den Sommer!",
    "Das klingt himmlisch! 😍",
    "Muss ich unbedingt nachkochen!",
    "Klassiker! Immer wieder gut.",
    "Interessante Wahl, hätte ich nicht gedacht.",
    "Danke für die Inspiration!",
]

COMMENT_TEMPLATES_EN = [
    "Great pairing! I need to try this. 🍷",
    "Exactly my taste! Thanks for the tip.",
    "Did this last week too - fantastic!",
    "That wine is one of my favorites!",
    "Perfect pairing for summer!",
    "Sounds heavenly! 😍",
    "I definitely need to recreate this!",
    "Classic! Always a good choice.",
    "Interesting choice, wouldn't have thought of it.",
    "Thanks for the inspiration!",
]


def determine_wine_type(wine_name: str, description: str) -> str:
    """Determine wine type from name and description"""
    context = f"{wine_name} {description}".lower()
    
    if any(w in context for w in ['bianco', 'blanc', 'white', 'weiss', 'weiß', 'grillo', 'chardonnay', 'riesling', 'sauvignon']):
        return 'weiss'
    if any(w in context for w in ['rosé', 'rose', 'rosato', 'rosado']):
        return 'rose'
    if any(w in context for w in ['spumante', 'champagne', 'prosecco', 'cava', 'sekt', 'schaumwein', 'brut']):
        return 'schaumwein'
    if any(w in context for w in ['passito', 'süßwein', 'dessert', 'sauternes']):
        return 'suesswein'
    
    return 'rot'  # Default to red


def parse_content(content_str: str) -> dict:
    """Parse the content string which is a Python dict literal"""
    try:
        # The content is a Python dict literal, use ast.literal_eval
        return ast.literal_eval(content_str)
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing content: {e}")
        return {}


def generate_random_date(days_back_max: int = 60) -> datetime:
    """Generate a random date within the last N days"""
    days_ago = random.randint(0, days_back_max)
    hours_ago = random.randint(0, 23)
    return datetime.now(timezone.utc) - timedelta(days=days_ago, hours=hours_ago)


def generate_comments(num_comments: int, post_date: datetime) -> list:
    """Generate random comments for a post"""
    comments = []
    for i in range(num_comments):
        commenter = random.choice(DEMO_USERS)
        comment_date = post_date + timedelta(hours=random.randint(1, 72))
        
        # 70% German, 30% English comments
        if random.random() < 0.7:
            content = random.choice(COMMENT_TEMPLATES_DE)
        else:
            content = random.choice(COMMENT_TEMPLATES_EN)
        
        comments.append({
            "id": str(uuid.uuid4()),
            "author_name": commenter["name"],
            "author_id": commenter["id"],
            "content": content,
            "created_at": comment_date.isoformat()
        })
    
    return comments


async def import_community_posts(csv_path: str):
    """Import posts from CSV file"""
    
    # Clear existing feed posts (optional - comment out to append)
    existing_count = await db.feed_posts.count_documents({})
    print(f"📊 Existing posts in database: {existing_count}")
    
    # Read CSV
    posts_to_insert = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Parse content
            content = parse_content(row['content'])
            if not content:
                continue
            
            # Get wine and dish info
            wine_name = content.get('wine', '')
            dish_de = content.get('dish_de', content.get('dish', ''))
            description_de = content.get('description_de', content.get('description', ''))
            location = content.get('location_de', content.get('location', ''))
            occasion = content.get('occasion_de', content.get('occasion', ''))
            
            if not wine_name or not dish_de:
                continue
            
            # Select random author
            author = random.choice(DEMO_USERS)
            
            # Determine wine type
            wine_type = determine_wine_type(wine_name, description_de)
            
            # Generate random engagement
            num_likes = random.randint(0, 25)
            num_comments = random.randint(0, 5) if random.random() < 0.4 else 0
            
            # Generate random date
            post_date = generate_random_date(60)
            
            # Generate likes (random user IDs)
            likes = [random.choice(DEMO_USERS)["id"] for _ in range(num_likes)]
            likes = list(set(likes))  # Remove duplicates
            
            # Generate comments
            comments = generate_comments(num_comments, post_date)
            
            # Build experience text with location and occasion
            experience = description_de
            if location and occasion:
                experience = f"📍 {location} | 🎉 {occasion}\n\n{description_de}"
            elif location:
                experience = f"📍 {location}\n\n{description_de}"
            elif occasion:
                experience = f"🎉 {occasion}\n\n{description_de}"
            
            # Create post document
            post = {
                "id": row['id'],  # Keep original ID
                "author_name": author["name"],
                "author_id": author["id"],
                "dish": dish_de,
                "wine_name": wine_name,
                "wine_type": wine_type,
                "rating": random.randint(4, 5),  # High ratings for curated content
                "experience": experience,
                "image_base64": None,  # No images for now
                "likes": likes,
                "comments": comments,
                "created_at": post_date.isoformat(),
                # Additional multilingual fields for future use
                "dish_en": content.get('dish_en', ''),
                "dish_fr": content.get('dish_fr', ''),
                "description_en": content.get('description_en', ''),
                "description_fr": content.get('description_fr', ''),
                "location": location,
                "occasion": occasion,
            }
            
            posts_to_insert.append(post)
    
    print(f"📝 Parsed {len(posts_to_insert)} posts from CSV")
    
    if posts_to_insert:
        # Check for duplicates and only insert new ones
        existing_ids = set(await db.feed_posts.distinct("id"))
        new_posts = [p for p in posts_to_insert if p["id"] not in existing_ids]
        
        if new_posts:
            await db.feed_posts.insert_many(new_posts)
            print(f"✅ Inserted {len(new_posts)} new posts")
        else:
            print("ℹ️ All posts already exist in database")
    
    # Print statistics
    total_posts = await db.feed_posts.count_documents({})
    total_likes = sum([len(p.get('likes', [])) for p in await db.feed_posts.find({}, {"likes": 1}).to_list(1000)])
    total_comments = sum([len(p.get('comments', [])) for p in await db.feed_posts.find({}, {"comments": 1}).to_list(1000)])
    
    print(f"\n📊 Feed Statistics:")
    print(f"   Total posts: {total_posts}")
    print(f"   Total likes: {total_likes}")
    print(f"   Total comments: {total_comments}")
    
    # Show sample posts
    print(f"\n📍 Sample Posts:")
    samples = await db.feed_posts.find({}, {"_id": 0, "author_name": 1, "wine_name": 1, "dish": 1, "likes": 1}).limit(5).to_list(5)
    for s in samples:
        print(f"   {s['author_name']}: {s['wine_name'][:30]} + {s['dish'][:25]} ({len(s.get('likes', []))} likes)")


async def main():
    print("🍷 Community Feed Import\n")
    print("=" * 60)
    
    csv_path = '/tmp/community.csv'
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        print("   Please download the file first.")
        return
    
    await import_community_posts(csv_path)
    
    print("\n" + "=" * 60)
    print("✅ Import Complete!")


if __name__ == '__main__':
    asyncio.run(main())
