"""
Generate 30 Italian grape varieties using Claude GPT-5.1
With consistency check and duplicate detection
"""
import asyncio
import os
import json
import re
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage
import uuid
from datetime import datetime, timezone

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

# The 30 most important Italian grape varieties (excluding already existing ones)
ITALIAN_GRAPES = [
    # Red grapes (already have Nebbiolo, Sangiovese)
    "Barbera",
    "Primitivo",
    "Nero d'Avola",
    "Montepulciano",
    "Dolcetto",
    "Corvina",
    "Aglianico",
    "Nerello Mascalese",
    "Lagrein",
    "Cannonau",
    "Sagrantino",
    "Teroldego",
    "Negroamaro",
    "Schiava",
    "Refosco",
    # White grapes (already have Pinot Grigio)
    "Trebbiano",
    "Garganega",
    "Verdicchio",
    "Fiano",
    "Greco",
    "Falanghina",
    "Arneis",
    "Cortese",
    "Vermentino",
    "Friulano",
    "Ribolla Gialla",
    "Glera",
    "Moscato",
    "Malvasia",
    "Pecorino",
]

GRAPE_GENERATOR_SYSTEM = """Du bist ein Wein-Experte und Sommelier. Erzeuge einen vollständigen, poetischen Datensatz für italienische Rebsorten.

STIL: Poetisch, emotional, sinnlich - wie ein leidenschaftlicher italienischer Winzer, der von seiner Traube erzählt.
Verwende Metaphern, Bilder und evoziere Emotionen.

ANTWORTFORMAT (STRICT JSON, KEIN ERKLÄRTEXT):
{
  "slug": "kebab-case-slug",
  "name": "Name der Rebsorte",
  "type": "rot" oder "weiss",
  "description": "Poetische deutsche Beschreibung (4-6 Sätze). Beschreibe Farbe, Duft, Geschmack und Charakter der Traube wie ein Dichter.",
  "description_en": "Poetic English description (4-6 sentences). Same style.",
  "description_fr": "Description poétique en français (4-6 phrases). Même style.",
  "synonyms": ["Alternative Namen oder regionale Bezeichnungen"],
  "body": "leicht" oder "mittel" oder "vollmundig",
  "acidity": "niedrig" oder "mittel" oder "hoch",
  "tannin": "niedrig" oder "mittel" oder "hoch",
  "aging": "Typischer Ausbau: Edelstahl, großes Holz, Barrique, etc.",
  "primary_aromas": ["5-7 deutsche Aroma-Tags in Kleinschreibung"],
  "tertiary_aromas": ["3-5 Reife-/Alterungsaromen in Kleinschreibung"],
  "perfect_pairings": ["5-7 passende italienische Gerichte auf Deutsch"],
  "perfect_pairings_en": ["Same dishes in English"],
  "perfect_pairings_fr": ["Mêmes plats en français"],
  "main_regions": ["3-5 wichtigste italienische Anbaugebiete"]
}

WICHTIG:
- Beschreibungen müssen POETISCH und EMOTIONAL sein, nicht technisch
- Alle drei Sprachen müssen denselben Inhalt in unterschiedlichen Worten vermitteln
- Aromen und Pairings speziell auf italienische Küche abstimmen
"""


async def get_existing_grapes():
    """Get list of existing grape names to avoid duplicates"""
    grapes = await db.grape_varieties.find({}, {"name": 1, "slug": 1, "_id": 0}).to_list(100)
    existing_names = set(g['name'].lower() for g in grapes)
    existing_slugs = set(g['slug'] for g in grapes)
    return existing_names, existing_slugs


async def generate_grape(grape_name: str, existing_names: set, existing_slugs: set):
    """Generate a single grape variety entry using Claude"""
    
    # Check for duplicate
    if grape_name.lower() in existing_names:
        print(f"  ⚠️  {grape_name} bereits vorhanden - überspringe")
        return None
    
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=str(uuid.uuid4()),
        system_message=GRAPE_GENERATOR_SYSTEM
    ).with_model("openai", "gpt-5.1")
    
    prompt = f"""Erzeuge einen vollständigen Datensatz für die italienische Rebsorte '{grape_name}'.

Beachte:
- Diese Traube stammt aus Italien
- Beschreibe sie poetisch und emotional
- Füge typisch italienische Speisepaarungen hinzu
- Alle drei Sprachen (DE/EN/FR) müssen hochwertige, unterschiedliche Texte haben

Gib NUR das JSON zurück, keine Erklärungen."""

    user_message = UserMessage(text=prompt)
    response = await chat.send_message(user_message)
    
    if not response or not response.strip():
        print(f"  ❌ Leere Antwort für {grape_name}")
        return None
    
    # Extract JSON
    json_match = re.search(r"\{[\s\S]*\}", response)
    if not json_match:
        print(f"  ❌ Kein JSON gefunden für {grape_name}")
        return None
    
    try:
        data = json.loads(json_match.group())
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON Parse-Fehler für {grape_name}: {e}")
        return None
    
    # Validate and normalize
    slug = data.get("slug") or grape_name.lower().replace(" ", "-").replace("'", "")
    
    # Check slug duplicate
    if slug in existing_slugs:
        slug = f"{slug}-italiano"
    
    grape_type = data.get("type", "rot")
    if grape_type not in ["rot", "weiss"]:
        grape_type = "rot"
    
    def ensure_list(val):
        if not val:
            return []
        if isinstance(val, list):
            return val
        return [str(val)]
    
    grape_doc = {
        "id": str(uuid.uuid4()),
        "slug": slug,
        "name": data.get("name", grape_name),
        "type": grape_type,
        "description": data.get("description", ""),
        "description_en": data.get("description_en", ""),
        "description_fr": data.get("description_fr", ""),
        "synonyms": ensure_list(data.get("synonyms")),
        "body": data.get("body", "mittel"),
        "acidity": data.get("acidity", "mittel"),
        "tannin": data.get("tannin", "mittel"),
        "aging": data.get("aging", ""),
        "primary_aromas": ensure_list(data.get("primary_aromas")),
        "tertiary_aromas": ensure_list(data.get("tertiary_aromas")),
        "perfect_pairings": ensure_list(data.get("perfect_pairings")),
        "perfect_pairings_en": ensure_list(data.get("perfect_pairings_en")),
        "perfect_pairings_fr": ensure_list(data.get("perfect_pairings_fr")),
        "main_regions": ensure_list(data.get("main_regions")),
        "image_url": None,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    return grape_doc


async def consistency_check(grapes: list):
    """Use Claude to check consistency of generated grapes"""
    
    print("\n🔍 Konsistenzprüfung mit Claude...")
    
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=str(uuid.uuid4()),
        system_message="Du bist ein Wein-Experte. Prüfe die Daten auf Konsistenz und Korrektheit."
    ).with_model("openai", "gpt-5.1")
    
    # Prepare summary for check
    summary = []
    for g in grapes:
        summary.append({
            "name": g["name"],
            "type": g["type"],
            "body": g["body"],
            "acidity": g["acidity"],
            "tannin": g["tannin"],
            "regions": g["main_regions"][:2],
            "aromas": g["primary_aromas"][:3]
        })
    
    prompt = f"""Prüfe diese italienischen Rebsorten auf Korrektheit und Konsistenz:

{json.dumps(summary, indent=2, ensure_ascii=False)}

Prüfe:
1. Sind die Rebsorten-Typen (rot/weiss) korrekt?
2. Sind Body/Säure/Tannin für jede Sorte plausibel?
3. Stimmen die Regionen?
4. Gibt es offensichtliche Fehler?

Antworte kurz und prägnant. Format:
✅ Korrekt: [Liste]
⚠️ Zu prüfen: [Liste mit Grund]
❌ Fehler: [Liste mit Korrektur]"""

    user_message = UserMessage(text=prompt)
    response = await chat.send_message(user_message)
    
    print(response)
    return response


async def main():
    print("🍇 Generiere italienische Rebsorten")
    print("=" * 60)
    
    # Get existing grapes
    existing_names, existing_slugs = await get_existing_grapes()
    print(f"📋 {len(existing_names)} bestehende Rebsorten gefunden")
    print(f"   Überspringe: Nebbiolo, Sangiovese, Pinot Grigio (bereits vorhanden)")
    
    # Filter out already existing
    grapes_to_generate = [g for g in ITALIAN_GRAPES 
                         if g.lower() not in existing_names 
                         and g.lower().replace("'", "") not in existing_names]
    
    print(f"\n🎯 Generiere {len(grapes_to_generate)} neue Rebsorten:\n")
    
    generated = []
    
    for i, grape_name in enumerate(grapes_to_generate, 1):
        print(f"[{i}/{len(grapes_to_generate)}] {grape_name}...", end=" ", flush=True)
        
        try:
            grape_doc = await generate_grape(grape_name, existing_names, existing_slugs)
            
            if grape_doc:
                generated.append(grape_doc)
                existing_names.add(grape_doc['name'].lower())
                existing_slugs.add(grape_doc['slug'])
                print(f"✅ {grape_doc['type']}")
            else:
                print("⏭️ übersprungen")
                
        except Exception as e:
            print(f"❌ Fehler: {e}")
        
        # Small delay to avoid rate limiting
        await asyncio.sleep(0.5)
    
    print(f"\n{'=' * 60}")
    print(f"✅ {len(generated)} Rebsorten generiert")
    
    if generated:
        # Consistency check
        await consistency_check(generated)
        
        # Insert into database
        print(f"\n💾 Speichere in Datenbank...")
        result = await db.grape_varieties.insert_many(generated)
        print(f"✅ {len(result.inserted_ids)} Rebsorten gespeichert")
        
        # Final count
        total = await db.grape_varieties.count_documents({})
        print(f"\n📊 Gesamt: {total} Rebsorten in der Datenbank")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
