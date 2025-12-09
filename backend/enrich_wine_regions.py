"""
Enrich wine database with correct regions and appellations using GPT-5.1
Claude knows French wines very well!
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from emergentintegrations.llm.chat import LlmChat, UserMessage
import json
import re
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# LLM API Key
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

# Stats
stats = {
    'total': 0,
    'enriched': 0,
    'skipped': 0,
    'failed': 0,
    'start_time': None
}


async def enrich_wine_region(wine):
    """Get correct region and appellation for a wine using Claude's expertise"""
    wine_id = wine['id']
    wine_name = wine['name']
    country = wine.get('country', 'Frankreich')
    current_region = wine.get('region', 'Unbekannt')
    current_appellation = wine.get('appellation', 'Unbekannt')
    grape_variety = wine.get('grape_variety', '')
    
    # Skip if already has proper region and appellation
    if current_region and current_region != 'Unbekannt' and current_appellation and current_appellation != 'Unbekannt':
        print(f"  ⏭️  Already complete: {wine_name}")
        stats['skipped'] += 1
        return True
    
    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"enrich_{wine_id}",
            system_message="You are a Master of Wine with expert knowledge of French wine regions and appellations. Provide accurate, specific region and appellation information for wines based on their names."
        )
        
        prompt = f"""Based on the wine name and details, provide the correct REGION and APPELLATION.

Wine Name: {wine_name}
Country: {country}
Current Region: {current_region}
Current Appellation: {current_appellation}
Grape Variety: {grape_variety}

Please provide the most accurate and specific information. For example:
- For "Château Margaux": Region = "Bordeaux", Appellation = "Margaux"
- For "Romanée-Conti": Region = "Burgund", Appellation = "Vosne-Romanée"
- For "Barolo Cannubi": Region = "Piemont", Appellation = "Barolo"

Return ONLY a JSON object (no markdown, no extra text):
{{
  "region": "correct region name in German",
  "appellation": "specific appellation/sub-region"
}}"""
        
        msg = UserMessage(text=prompt)
        response = await chat.send_message(msg)
        
        # Parse response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            new_region = data.get('region', current_region)
            new_appellation = data.get('appellation', current_appellation)
            
            # Update database
            await db.public_wines.update_one(
                {"id": wine_id},
                {"$set": {
                    "region": new_region,
                    "appellation": new_appellation
                }}
            )
            
            print(f"  ✅ Enriched: {wine_name}")
            print(f"     Region: {new_region}, Appellation: {new_appellation}")
            stats['enriched'] += 1
            return True
        else:
            print(f"  ⚠️  No JSON in response for {wine_name}")
            stats['failed'] += 1
            return False
        
    except Exception as e:
        print(f"  ❌ Error for {wine_name}: {str(e)[:100]}")
        stats['failed'] += 1
        return False


async def main():
    print("🍷 Wine Region Enrichment Service")
    print("=" * 60)
    
    stats['start_time'] = datetime.now()
    
    # Get all wines
    wines = await db.public_wines.find({}, {"_id": 0}).to_list(1000)
    stats['total'] = len(wines)
    
    print(f"📊 Found {stats['total']} wines to process\n")
    
    # Process each wine with rate limiting
    for idx, wine in enumerate(wines, 1):
        print(f"[{idx}/{stats['total']}] {wine['name']}")
        await enrich_wine_region(wine)
        
        # Small delay to avoid rate limits
        if idx < stats['total']:
            await asyncio.sleep(0.5)
        
        # Progress update every 20 wines
        if idx % 20 == 0:
            elapsed = (datetime.now() - stats['start_time']).total_seconds()
            avg_time = elapsed / idx
            remaining = (stats['total'] - idx) * avg_time
            print(f"\n📊 Progress: {idx}/{stats['total']} ({idx/stats['total']*100:.1f}%)")
            print(f"⏱️  Estimated remaining: {remaining/60:.1f} minutes\n")
    
    # Final stats
    elapsed = (datetime.now() - stats['start_time']).total_seconds()
    print("\n" + "=" * 60)
    print("🎉 Region Enrichment Complete!")
    print(f"✅ Enriched: {stats['enriched']}")
    print(f"⏭️  Skipped: {stats['skipped']}")
    print(f"❌ Failed: {stats['failed']}")
    print(f"⏱️  Total time: {elapsed/60:.1f} minutes")
    print("=" * 60)


if __name__ == '__main__':
    asyncio.run(main())
