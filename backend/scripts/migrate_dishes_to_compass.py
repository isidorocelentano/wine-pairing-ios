"""
MIGRATION SCRIPT: Speisen aus Rebsorten in den Sommelier-Kompass übertragen
============================================================================
Dieses Script:
1. Sammelt alle Speisen aus den Rebsorten (perfect_pairings)
2. Verwendet Claude um jede Speise einem Land zuzuordnen
3. Erstellt neue Einträge im Sommelier-Kompass (regional_pairings)
4. Speichert Übersetzungen (DE/EN/FR)

Ausführung: python scripts/migrate_dishes_to_compass.py
"""

import asyncio
import os
import sys
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

load_dotenv(Path(__file__).parent.parent / '.env')

# Konfiguration
BATCH_SIZE = 20  # Speisen pro Claude-Anfrage
MAX_DISHES = None  # None = alle, oder Zahl für Test

# Bekannte Länder im Kompass mit Emoji
KNOWN_COUNTRIES = {
    'Deutschland': {'en': 'Germany', 'fr': 'Allemagne', 'emoji': '🇩🇪'},
    'Frankreich': {'en': 'France', 'fr': 'France', 'emoji': '🇫🇷'},
    'Italien': {'en': 'Italy', 'fr': 'Italie', 'emoji': '🇮🇹'},
    'Spanien': {'en': 'Spain', 'fr': 'Espagne', 'emoji': '🇪🇸'},
    'Österreich': {'en': 'Austria', 'fr': 'Autriche', 'emoji': '🇦🇹'},
    'Schweiz': {'en': 'Switzerland', 'fr': 'Suisse', 'emoji': '🇨🇭'},
    'Griechenland': {'en': 'Greece', 'fr': 'Grèce', 'emoji': '🇬🇷'},
    'Portugal': {'en': 'Portugal', 'fr': 'Portugal', 'emoji': '🇵🇹'},
    'China': {'en': 'China', 'fr': 'Chine', 'emoji': '🇨🇳'},
    'Japan': {'en': 'Japan', 'fr': 'Japon', 'emoji': '🇯🇵'},
    'Türkei': {'en': 'Turkey', 'fr': 'Turquie', 'emoji': '🇹🇷'},
    'USA': {'en': 'USA', 'fr': 'États-Unis', 'emoji': '🇺🇸'},
    'Mexiko': {'en': 'Mexico', 'fr': 'Mexique', 'emoji': '🇲🇽'},
    'Thailand': {'en': 'Thailand', 'fr': 'Thaïlande', 'emoji': '🇹🇭'},
    'Indien': {'en': 'India', 'fr': 'Inde', 'emoji': '🇮🇳'},
    'Marokko': {'en': 'Morocco', 'fr': 'Maroc', 'emoji': '🇲🇦'},
    'Argentinien': {'en': 'Argentina', 'fr': 'Argentine', 'emoji': '🇦🇷'},
    'Brasilien': {'en': 'Brazil', 'fr': 'Brésil', 'emoji': '🇧🇷'},
    'Großbritannien': {'en': 'United Kingdom', 'fr': 'Royaume-Uni', 'emoji': '🇬🇧'},
    'Belgien': {'en': 'Belgium', 'fr': 'Belgique', 'emoji': '🇧🇪'},
    'Niederlande': {'en': 'Netherlands', 'fr': 'Pays-Bas', 'emoji': '🇳🇱'},
    'Polen': {'en': 'Poland', 'fr': 'Pologne', 'emoji': '🇵🇱'},
    'Ungarn': {'en': 'Hungary', 'fr': 'Hongrie', 'emoji': '🇭🇺'},
    'Tschechien': {'en': 'Czech Republic', 'fr': 'Tchéquie', 'emoji': '🇨🇿'},
    'Russland': {'en': 'Russia', 'fr': 'Russie', 'emoji': '🇷🇺'},
    'Korea': {'en': 'Korea', 'fr': 'Corée', 'emoji': '🇰🇷'},
    'Vietnam': {'en': 'Vietnam', 'fr': 'Vietnam', 'emoji': '🇻🇳'},
    'Indonesien': {'en': 'Indonesia', 'fr': 'Indonésie', 'emoji': '🇮🇩'},
    'Libanon': {'en': 'Lebanon', 'fr': 'Liban', 'emoji': '🇱🇧'},
    'Israel': {'en': 'Israel', 'fr': 'Israël', 'emoji': '🇮🇱'},
    'Australien': {'en': 'Australia', 'fr': 'Australie', 'emoji': '🇦🇺'},
    'Neuseeland': {'en': 'New Zealand', 'fr': 'Nouvelle-Zélande', 'emoji': '🇳🇿'},
    'Südafrika': {'en': 'South Africa', 'fr': 'Afrique du Sud', 'emoji': '🇿🇦'},
    'International': {'en': 'International', 'fr': 'International', 'emoji': '🌍'},
}


async def get_llm_client():
    """Erstellt einen LLM-Client für Claude"""
    api_key = os.environ.get('EMERGENT_LLM_KEY')
    if not api_key:
        raise ValueError("EMERGENT_LLM_KEY nicht gesetzt!")
    
    return LlmChat(
        api_key=api_key,
        session_id=str(uuid.uuid4()),
        system_message="""Du bist ein kulinarischer Experte. Deine Aufgabe ist es, Gerichte ihrem Ursprungsland zuzuordnen.

Antworte IMMER im JSON-Format mit folgendem Schema:
{
  "dishes": [
    {
      "dish": "Name des Gerichts",
      "country": "Land auf Deutsch",
      "region": "Region oder Stadt (optional)",
      "confidence": "high/medium/low"
    }
  ]
}

Wichtige Regeln:
- Verwende NUR diese Länder: Deutschland, Frankreich, Italien, Spanien, Österreich, Schweiz, Griechenland, Portugal, China, Japan, Türkei, USA, Mexiko, Thailand, Indien, Marokko, Argentinien, Brasilien, Großbritannien, Belgien, Niederlande, Polen, Ungarn, Tschechien, Russland, Korea, Vietnam, Indonesien, Libanon, Israel, Australien, Neuseeland, Südafrika, International
- "International" für Gerichte ohne klares Ursprungsland oder moderne Fusion-Küche
- Bei regionalen Gerichten (z.B. "Wiener Schnitzel") die Region angeben
- Antworte NUR mit dem JSON, keine Erklärungen"""
    ).with_model("openai", "gpt-5.1")


async def classify_dishes_with_claude(dishes: list, llm: LlmChat) -> list:
    """Klassifiziert eine Liste von Speisen mit Claude"""
    
    # Erstelle Anfrage
    dishes_text = "\n".join([f"- {d['de']}" for d in dishes])
    
    prompt = f"""Ordne folgende Gerichte ihrem Ursprungsland zu:

{dishes_text}

Antworte im JSON-Format."""

    try:
        response = await llm.send_async(UserMessage(prompt))
        
        # Parse JSON aus Response
        response_text = response.strip()
        
        # Extrahiere JSON falls in Markdown-Block
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        result = json.loads(response_text)
        return result.get('dishes', [])
        
    except Exception as e:
        print(f"  ❌ Fehler bei Claude-Anfrage: {e}")
        return []


async def main():
    print("=" * 60)
    print("MIGRATION: Speisen → Sommelier-Kompass")
    print("=" * 60)
    print()
    
    # Verbinde mit DB
    client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
    db = client[os.environ.get('DB_NAME')]
    
    # 1. Sammle alle Speisen aus Rebsorten
    print("📋 Sammle Speisen aus Rebsorten...")
    grapes = await db.grape_varieties.find({}, {
        '_id': 0, 
        'name': 1, 
        'perfect_pairings': 1, 
        'perfect_pairings_en': 1, 
        'perfect_pairings_fr': 1
    }).to_list(200)
    
    # Sammle unique Speisen mit Übersetzungen
    dish_data = {}  # DE -> {en, fr, grapes}
    
    for g in grapes:
        de_dishes = g.get('perfect_pairings', []) or []
        en_dishes = g.get('perfect_pairings_en', []) or []
        fr_dishes = g.get('perfect_pairings_fr', []) or []
        grape_name = g.get('name', 'Unknown')
        
        for i, de_dish in enumerate(de_dishes):
            if not de_dish:
                continue
            
            if de_dish not in dish_data:
                dish_data[de_dish] = {
                    'de': de_dish,
                    'en': en_dishes[i] if i < len(en_dishes) else de_dish,
                    'fr': fr_dishes[i] if i < len(fr_dishes) else de_dish,
                    'grapes': []
                }
            
            if grape_name not in dish_data[de_dish]['grapes']:
                dish_data[de_dish]['grapes'].append(grape_name)
    
    # 2. Filtere bereits existierende
    existing = await db.regional_pairings.distinct('dish')
    existing_set = set(existing)
    
    new_dishes = [d for d in dish_data.values() if d['de'] not in existing_set]
    
    print(f"   Gesamt: {len(dish_data)} unique Speisen")
    print(f"   Bereits im Kompass: {len(existing_set)}")
    print(f"   Neue Speisen: {len(new_dishes)}")
    print()
    
    if not new_dishes:
        print("✅ Keine neuen Speisen zu migrieren!")
        return
    
    # Limitiere für Test
    if MAX_DISHES:
        new_dishes = new_dishes[:MAX_DISHES]
        print(f"   (Limitiert auf {MAX_DISHES} für Test)")
    
    # 3. Klassifiziere mit Claude in Batches
    print(f"🤖 Klassifiziere {len(new_dishes)} Speisen mit Claude...")
    print()
    
    llm = await get_llm_client()
    classified = []
    
    for i in range(0, len(new_dishes), BATCH_SIZE):
        batch = new_dishes[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        total_batches = (len(new_dishes) + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"   Batch {batch_num}/{total_batches} ({len(batch)} Speisen)...")
        
        results = await classify_dishes_with_claude(batch, llm)
        
        # Merge results mit Original-Daten
        for result in results:
            dish_name = result.get('dish', '')
            # Finde passendes Original
            for orig in batch:
                if orig['de'] == dish_name or dish_name in orig['de']:
                    classified.append({
                        **orig,
                        'country': result.get('country', 'International'),
                        'region': result.get('region', ''),
                        'confidence': result.get('confidence', 'medium')
                    })
                    break
        
        # Rate-Limiting
        await asyncio.sleep(1)
    
    print()
    print(f"   ✅ {len(classified)} Speisen klassifiziert")
    print()
    
    # 4. Erstelle neue Kompass-Einträge
    print("💾 Erstelle Kompass-Einträge...")
    
    new_entries = []
    country_stats = {}
    
    for dish in classified:
        country_de = dish.get('country', 'International')
        country_info = KNOWN_COUNTRIES.get(country_de, KNOWN_COUNTRIES['International'])
        
        # Statistik
        if country_de not in country_stats:
            country_stats[country_de] = 0
        country_stats[country_de] += 1
        
        entry = {
            'id': str(uuid.uuid4()),
            'country': country_de,
            'country_en': country_info['en'],
            'country_fr': country_info['fr'],
            'country_emoji': country_info['emoji'],
            'region': dish.get('region', ''),
            'dish': dish['de'],
            'dish_en': dish.get('en', dish['de']),
            'dish_fr': dish.get('fr', dish['de']),
            'wine_name': '',  # Wird später gefüllt
            'wine_type': '',
            'dish_description': f"Passt zu: {', '.join(dish.get('grapes', [])[:3])}",
            'dish_description_en': f"Pairs with: {', '.join(dish.get('grapes', [])[:3])}",
            'dish_description_fr': f"S'accorde avec: {', '.join(dish.get('grapes', [])[:3])}",
            'wine_description': '',
            'wine_description_en': '',
            'wine_description_fr': '',
            'source': 'grape_migration',
            'confidence': dish.get('confidence', 'medium'),
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        
        new_entries.append(entry)
    
    # 5. In DB speichern
    if new_entries:
        await db.regional_pairings.insert_many(new_entries)
        print(f"   ✅ {len(new_entries)} neue Einträge erstellt")
    
    # 6. Statistik ausgeben
    print()
    print("=" * 60)
    print("📊 MIGRATION ABGESCHLOSSEN")
    print("=" * 60)
    print()
    print("Neue Gerichte pro Land:")
    for country, count in sorted(country_stats.items(), key=lambda x: -x[1]):
        emoji = KNOWN_COUNTRIES.get(country, {}).get('emoji', '🌍')
        print(f"   {emoji} {country}: {count}")
    
    print()
    print(f"Gesamt: {len(new_entries)} neue Einträge im Sommelier-Kompass")


if __name__ == "__main__":
    asyncio.run(main())
