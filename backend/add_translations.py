import asyncio
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient
import uuid
from emergentintegrations.llm.chat import LlmChat, UserMessage
import json
import re

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'wine_pairing_db')]

# LLM API Key
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')


async def add_translations():
    """Add English and French translations to all wines in the database."""
    
    # Get all wines without translations
    wines = await db.wines_db.find({
        "$or": [
            {"description_en": {"$in": [None, ""]}},
            {"description_fr": {"$in": [None, ""]}}
        ]
    }, {"_id": 0}).to_list(1000)
    
    print(f"🌍 Found {len(wines)} wines needing translations\n")
    
    for idx, wine in enumerate(wines, 1):
        print(f"[{idx}/{len(wines)}] {wine['name']}")
        
        try:
            # Generate English translation
            if not wine.get('description_en'):
                chat_en = LlmChat(
                    api_key=EMERGENT_LLM_KEY,
                    session_id=str(uuid.uuid4()),
                    system_message="You are an expert wine translator. Translate wine descriptions from German to English, preserving the emotional and poetic tone. Always respond with valid JSON."
                )
                
                pairings_text = ', '.join(wine.get('food_pairings_de', [])) if wine.get('food_pairings_de') else 'None'
                
                prompt_en = f"""Translate to English and return ONLY a JSON object:

German Description: {wine['description_de']}
Food Pairings (DE): {pairings_text}

JSON format:
{{
  "description_en": "translated description",
  "food_pairings_en": ["pairing1", "pairing2"]
}}"""
                
                user_message_en = UserMessage(text=prompt_en)
                response_en = await chat_en.send_message(user_message_en)
                
                # Extract JSON
                json_match = re.search(r'\{.*\}', response_en, re.DOTALL)
                if json_match:
                    data_en = json.loads(json_match.group())
                    wine['description_en'] = data_en.get('description_en', wine['description_de'])
                    wine['food_pairings_en'] = data_en.get('food_pairings_en', wine.get('food_pairings_de', []))
                else:
                    wine['description_en'] = wine['description_de']
                    wine['food_pairings_en'] = wine.get('food_pairings_de', [])
                
                print(f"  ✅ EN translation added")
            
            # Generate French translation
            if not wine.get('description_fr'):
                chat_fr = LlmChat(
                    api_key=EMERGENT_LLM_KEY,
                    session_id=str(uuid.uuid4()),
                    system_message="Tu es un expert en traduction de vins. Traduis les descriptions de vin de l'allemand au français, en préservant le ton émotionnel et poétique. Réponds toujours avec un JSON valide."
                )
                
                pairings_text = ', '.join(wine.get('food_pairings_de', [])) if wine.get('food_pairings_de') else 'None'
                
                prompt_fr = f"""Traduis en français et retourne SEULEMENT un objet JSON:

Description allemande: {wine['description_de']}
Food Pairings (DE): {pairings_text}

Format JSON:
{{
  "description_fr": "description traduite",
  "food_pairings_fr": ["pairing1", "pairing2"]
}}"""
                
                user_message_fr = UserMessage(text=prompt_fr)
                response_fr = await chat_fr.send_message(user_message_fr)
                
                # Extract JSON
                json_match = re.search(r'\{.*\}', response_fr, re.DOTALL)
                if json_match:
                    data_fr = json.loads(json_match.group())
                    wine['description_fr'] = data_fr.get('description_fr', wine['description_de'])
                    wine['food_pairings_fr'] = data_fr.get('food_pairings_fr', wine.get('food_pairings_de', []))
                else:
                    wine['description_fr'] = wine['description_de']
                    wine['food_pairings_fr'] = wine.get('food_pairings_de', [])
                
                print(f"  ✅ FR translation added")
            
            # Update database
            await db.wines_db.update_one(
                {"id": wine['id']},
                {"$set": {
                    "description_en": wine['description_en'],
                    "description_fr": wine['description_fr'],
                    "food_pairings_en": wine['food_pairings_en'],
                    "food_pairings_fr": wine['food_pairings_fr']
                }}
            )
            print(f"  💾 Updated in database\n")
            
        except Exception as e:
            print(f"  ⚠️  Error: {str(e)}\n")
            continue
    
    print("🎉 All translations complete!")


if __name__ == '__main__':
    asyncio.run(add_translations())
