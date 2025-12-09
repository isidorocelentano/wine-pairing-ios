"""
Generate EN and FR translations for all wines in public_wines collection
Using GPT-5.1 for high-quality, emotional translations
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from emergentintegrations.llm.chat import LlmChat, UserMessage
import json
import re
from datetime import datetime

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# LLM API Key
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

# Stats
stats = {
    'total': 0,
    'translated': 0,
    'skipped': 0,
    'failed': 0,
    'start_time': None
}


async def translate_wine(wine):
    """Generate EN and FR translations for a single wine"""
    wine_id = wine['id']
    wine_name = wine['name']
    
    # Skip if already translated
    if wine.get('description_en') and wine.get('description_en') != wine.get('description_de'):
        if wine.get('description_fr') and wine.get('description_fr') != wine.get('description_de'):
            print(f"  ⏭️  Already translated: {wine_name}")
            stats['skipped'] += 1
            return True
    
    description_de = wine.get('description_de', '')
    pairings_de = wine.get('food_pairings_de', [])
    
    if not description_de:
        print(f"  ⚠️  No German description: {wine_name}")
        stats['skipped'] += 1
        return False
    
    try:
        # Generate ENGLISH translation
        chat_en = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"translate_en_{wine_id}",
            system_message="You are an expert wine translator. Translate wine descriptions from German to English, preserving the poetic, emotional tone. Keep the same style and feeling."
        )
        
        pairings_text = ', '.join(pairings_de) if pairings_de else ''
        
        prompt_en = f"""Translate this emotional German wine description to English. Keep the same poetic, evocative style.

German Description: {description_de}

German Food Pairings: {pairings_text}

Return ONLY a JSON object (no markdown, no extra text):
{{
  "description_en": "your English translation here",
  "food_pairings_en": ["pairing 1", "pairing 2"]
}}"""
        
        msg_en = UserMessage(text=prompt_en)
        response_en = await chat_en.send_message(msg_en)
        
        # Parse English response
        json_match = re.search(r'\{.*\}', response_en, re.DOTALL)
        if json_match:
            data_en = json.loads(json_match.group())
            description_en = data_en.get('description_en', description_de)
            pairings_en = data_en.get('food_pairings_en', pairings_de)
        else:
            description_en = description_de
            pairings_en = pairings_de
        
        # Generate FRENCH translation
        chat_fr = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"translate_fr_{wine_id}",
            system_message="Tu es un expert en traduction de vins. Traduis les descriptions de vin de l'allemand au français, en préservant le ton poétique et émotionnel."
        )
        
        prompt_fr = f"""Traduis cette description émotionnelle de vin de l'allemand au français. Garde le même style poétique et évocateur.

Description allemande: {description_de}

Accords mets-vins (allemand): {pairings_text}

Retourne SEULEMENT un objet JSON (pas de markdown, pas de texte supplémentaire):
{{
  "description_fr": "ta traduction en français ici",
  "food_pairings_fr": ["accord 1", "accord 2"]
}}"""
        
        msg_fr = UserMessage(text=prompt_fr)
        response_fr = await chat_fr.send_message(msg_fr)
        
        # Parse French response
        json_match = re.search(r'\{.*\}', response_fr, re.DOTALL)
        if json_match:
            data_fr = json.loads(json_match.group())
            description_fr = data_fr.get('description_fr', description_de)
            pairings_fr = data_fr.get('food_pairings_fr', pairings_de)
        else:
            description_fr = description_de
            pairings_fr = pairings_de
        
        # Update database
        await db.public_wines.update_one(
            {"id": wine_id},
            {"$set": {
                "description_en": description_en,
                "description_fr": description_fr,
                "food_pairings_en": pairings_en,
                "food_pairings_fr": pairings_fr
            }}
        )
        
        print(f"  ✅ Translated: {wine_name}")
        stats['translated'] += 1
        return True
        
    except Exception as e:
        print(f"  ❌ Error for {wine_name}: {str(e)[:100]}")
        stats['failed'] += 1
        return False


async def main():
    print("🌍 Wine Translation Service")
    print("=" * 60)
    
    stats['start_time'] = datetime.now()
    
    # Get all wines
    wines = await db.public_wines.find({}, {"_id": 0}).to_list(1000)
    stats['total'] = len(wines)
    
    print(f"📊 Found {stats['total']} wines to process\n")
    
    # Process each wine
    for idx, wine in enumerate(wines, 1):
        print(f"[{idx}/{stats['total']}] {wine['name']}")
        await translate_wine(wine)
        
        # Progress update every 10 wines
        if idx % 10 == 0:
            elapsed = (datetime.now() - stats['start_time']).total_seconds()
            avg_time = elapsed / idx
            remaining = (stats['total'] - idx) * avg_time
            print(f"\n📊 Progress: {idx}/{stats['total']} ({idx/stats['total']*100:.1f}%)")
            print(f"⏱️  Estimated remaining: {remaining/60:.1f} minutes\n")
    
    # Final stats
    elapsed = (datetime.now() - stats['start_time']).total_seconds()
    print("\n" + "=" * 60)
    print("🎉 Translation Complete!")
    print(f"✅ Translated: {stats['translated']}")
    print(f"⏭️  Skipped: {stats['skipped']}")
    print(f"❌ Failed: {stats['failed']}")
    print(f"⏱️  Total time: {elapsed/60:.1f} minutes")
    print("=" * 60)


if __name__ == '__main__':
    asyncio.run(main())
