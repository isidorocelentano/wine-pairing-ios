"""
Translate Community Feed Posts using Claude/GPT
Translates dish names and descriptions to EN and FR
"""
import asyncio
import os
from pathlib import Path
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage
import json
import re

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'wine_pairing_db')]

# LLM API Key
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

# Batch size for translation
BATCH_SIZE = 10


async def translate_batch(posts: list) -> list:
    """Translate a batch of posts using Claude"""
    
    # Prepare translation request
    items_to_translate = []
    for i, post in enumerate(posts):
        # Extract clean text without emojis for translation
        experience = post.get('experience', '')
        # Remove location/occasion prefix for cleaner translation
        clean_experience = re.sub(r'^📍[^|]+\|[^🎉]*🎉[^\n]*\n*', '', experience).strip()
        if not clean_experience:
            clean_experience = experience
        
        items_to_translate.append({
            "index": i,
            "dish_de": post.get('dish', ''),
            "description_de": clean_experience[:500]  # Limit length
        })
    
    # Build prompt
    prompt = f"""Translate these wine pairing descriptions from German to English and French.
Return a JSON array with the translations. Keep the wine/food terminology accurate.

Input items:
{json.dumps(items_to_translate, ensure_ascii=False, indent=2)}

Return ONLY a valid JSON array with this structure for each item:
[
  {{
    "index": 0,
    "dish_en": "English dish name",
    "dish_fr": "French dish name", 
    "description_en": "English description",
    "description_fr": "French description"
  }},
  ...
]

Important:
- Keep wine names unchanged (they are proper nouns)
- Translate food names accurately
- Keep the elegant, sommelier-like tone
- Return ONLY the JSON array, no other text
"""

    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            system_message="You are a professional translator specializing in wine and gastronomy. Translate accurately while maintaining the elegant tone."
        ).with_model("openai", "gpt-5.1")
        
        response = await chat.send_message(UserMessage(text=prompt))
        
        # Parse JSON response
        # Try to extract JSON from response
        json_match = re.search(r'\[[\s\S]*\]', response)
        if json_match:
            translations = json.loads(json_match.group())
            return translations
        else:
            print(f"  ⚠️ Could not parse JSON from response")
            return []
            
    except Exception as e:
        print(f"  ❌ Translation error: {e}")
        return []


async def translate_all_posts():
    """Translate all feed posts that need translation"""
    
    print("🌍 Community Feed Translation\n")
    print("=" * 60)
    
    # Find posts that need translation
    posts = await db.feed_posts.find(
        {
            "$or": [
                {"dish_en": {"$exists": False}},
                {"dish_en": ""},
                {"dish_en": None},
                {"description_en": {"$exists": False}},
                {"description_en": ""}
            ]
        },
        {"_id": 0}
    ).to_list(500)
    
    print(f"📊 Found {len(posts)} posts needing translation\n")
    
    if not posts:
        print("✅ All posts are already translated!")
        return
    
    # Process in batches
    total_translated = 0
    total_batches = (len(posts) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for batch_num in range(total_batches):
        start_idx = batch_num * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, len(posts))
        batch = posts[start_idx:end_idx]
        
        print(f"📝 Processing batch {batch_num + 1}/{total_batches} ({len(batch)} posts)...")
        
        translations = await translate_batch(batch)
        
        if translations:
            # Update posts with translations
            for trans in translations:
                idx = trans.get('index', -1)
                if 0 <= idx < len(batch):
                    post_id = batch[idx]['id']
                    
                    update_data = {}
                    if trans.get('dish_en'):
                        update_data['dish_en'] = trans['dish_en']
                    if trans.get('dish_fr'):
                        update_data['dish_fr'] = trans['dish_fr']
                    if trans.get('description_en'):
                        update_data['description_en'] = trans['description_en']
                    if trans.get('description_fr'):
                        update_data['description_fr'] = trans['description_fr']
                    
                    if update_data:
                        await db.feed_posts.update_one(
                            {"id": post_id},
                            {"$set": update_data}
                        )
                        total_translated += 1
            
            print(f"  ✅ Translated {len(translations)} posts")
        else:
            print(f"  ⚠️ No translations received for this batch")
        
        # Small delay between batches to avoid rate limiting
        if batch_num < total_batches - 1:
            await asyncio.sleep(1)
    
    print(f"\n📊 Translation Summary:")
    print(f"   Total translated: {total_translated}/{len(posts)}")
    
    # Verify translations
    sample = await db.feed_posts.find_one(
        {"dish_en": {"$exists": True, "$ne": ""}},
        {"_id": 0, "dish": 1, "dish_en": 1, "dish_fr": 1, "description_en": 1}
    )
    if sample:
        print(f"\n📍 Sample Translation:")
        print(f"   DE: {sample.get('dish', '')}")
        print(f"   EN: {sample.get('dish_en', '')}")
        print(f"   FR: {sample.get('dish_fr', '')}")


async def main():
    await translate_all_posts()
    print("\n" + "=" * 60)
    print("✅ Translation Complete!")


if __name__ == '__main__':
    asyncio.run(main())
