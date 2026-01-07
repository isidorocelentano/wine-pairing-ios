"""
Generate Spanish grape varieties using Claude GPT-5.1
With consistency check, duplicate detection, and image URLs
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

# The most important Spanish grape varieties (excluding Tempranillo which already exists)
SPANISH_GRAPES = [
    # Red grapes
    ("Garnacha", "rot", "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800"),
    ("Monastrell", "rot", "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800"),
    ("Mencía", "rot", "https://images.unsplash.com/photo-1474722883778-792e7990302f?w=800"),
    ("Bobal", "rot", "https://images.unsplash.com/photo-1567696911980-2eed69a46042?w=800"),
    ("Graciano", "rot", "https://images.unsplash.com/photo-1558346489-19413928158b?w=800"),
    ("Cariñena", "rot", "https://images.unsplash.com/photo-1516594915697-87eb3b1c14ea?w=800"),
    ("Tinta de Toro", "rot", "https://images.unsplash.com/photo-1560148218-1a83060f7b32?w=800"),
    ("Prieto Picudo", "rot", "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=800"),
    # White grapes
    ("Albariño", "weiss", "https://images.unsplash.com/photo-1566754436808-0fddc0c0c4c6?w=800"),
    ("Verdejo", "weiss", "https://images.unsplash.com/photo-1584916201218-f4242ceb4809?w=800"),
    ("Godello", "weiss", "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800"),
    ("Macabeo", "weiss", "https://images.unsplash.com/photo-1568213214202-3e582bc02fd5?w=800"),
    ("Xarel·lo", "weiss", "https://images.unsplash.com/photo-1507434965515-61970f2bd7c6?w=800"),
    ("Parellada", "weiss", "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=800"),
    ("Pedro Ximénez", "weiss", "https://images.unsplash.com/photo-1571950006920-a8621a6d8c4e?w=800"),
    ("Palomino Fino", "weiss", "https://images.unsplash.com/photo-1528823872057-9c018a7a7553?w=800"),
]

GRAPE_GENERATOR_SYSTEM = """Du bist ein Wein-Experte und Sommelier mit besonderer Expertise für spanische Weine. Erzeuge einen vollständigen, poetischen Datensatz für spanische Rebsorten.

STIL: Poetisch, emotional, leidenschaftlich - wie ein spanischer Winzer, der von seiner Traube unter der glühenden Sonne Kastiliens erzählt. Verwende Metaphern, Bilder und evoziere die Hitze, die Landschaft und die Seele Spaniens.

ANTWORTFORMAT (STRICT JSON, KEIN ERKLÄRTEXT):
{
  "slug": "kebab-case-slug",
  "name": "Name der Rebsorte",
  "type": "rot" oder "weiss",
  "description": "Poetische deutsche Beschreibung (4-6 Sätze). Beschreibe Farbe, Duft, Geschmack und Charakter der Traube wie ein Dichter. Evoziere die spanische Landschaft.",
  "description_en": "Poetic English description (4-6 sentences). Same passionate style.",
  "description_fr": "Description poétique en français (4-6 phrases). Même style passionné.",
  "synonyms": ["Alternative Namen oder regionale Bezeichnungen"],
  "body": "leicht" oder "mittel" oder "vollmundig",
  "acidity": "niedrig" oder "mittel" oder "hoch",
  "tannin": "niedrig" oder "mittel" oder "hoch",
  "aging": "Typischer Ausbau: Edelstahl, amerikanische Eiche, französische Eiche, Solera etc.",
  "primary_aromas": ["5-7 deutsche Aroma-Tags in Kleinschreibung"],
  "tertiary_aromas": ["3-5 Reife-/Alterungsaromen in Kleinschreibung"],
  "perfect_pairings": ["5-7 passende spanische Gerichte auf Deutsch"],
  "perfect_pairings_en": ["Same dishes in English"],
  "perfect_pairings_fr": ["Mêmes plats en français"],
  "main_regions": ["3-5 wichtigste spanische Anbaugebiete mit DO/DOCa"]
}

WICHTIG:
- Beschreibungen müssen POETISCH und EMOTIONAL sein, nicht technisch
- Evoziere die spanische Kultur: Flamenco, Stierkampf, Siesta, Tapas-Bars...
- Alle drei Sprachen müssen denselben Inhalt in unterschiedlichen Worten vermitteln
- Speisepaarungen speziell auf spanische Küche abstimmen (Tapas, Paella, Jamón, etc.)
"""


async def get_existing_grapes():
    """Get list of existing grape names to avoid duplicates"""
    grapes = await db.grape_varieties.find({}, {"name": 1, "slug": 1, "_id": 0}).to_list(100)
    existing_names = set(g['name'].lower() for g in grapes)
    existing_slugs = set(g['slug'] for g in grapes)
    return existing_names, existing_slugs


async def generate_grape(grape_name: str, grape_type: str, image_url: str, existing_names: set, existing_slugs: set):
    """Generate a single grape variety entry using Claude"""
    
    # Check for duplicate
    if grape_name.lower() in existing_names:
        print(f"⚠️  bereits vorhanden - überspringe")
        return None
    
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=str(uuid.uuid4()),
        system_message=GRAPE_GENERATOR_SYSTEM
    ).with_model("openai", "gpt-5.1")
    
    prompt = f"""Erzeuge einen vollständigen Datensatz für die spanische Rebsorte '{grape_name}'.
Diese Traube ist vom Typ: {grape_type}

Beachte:
- Diese Traube stammt aus Spanien
- Beschreibe sie poetisch und leidenschaftlich wie ein spanischer Winzer
- Füge typisch spanische Speisepaarungen hinzu (Tapas, Jamón, Paella, Chorizo, etc.)
- Alle drei Sprachen (DE/EN/FR) müssen hochwertige, emotionale Texte haben

Gib NUR das JSON zurück, keine Erklärungen."""

    user_message = UserMessage(text=prompt)
    response = await chat.send_message(user_message)
    
    if not response or not response.strip():
        print("❌ Leere Antwort")
        return None
    
    # Extract JSON
    json_match = re.search(r"\{[\s\S]*\}", response)
    if not json_match:
        print("❌ Kein JSON gefunden")
        return None
    
    try:
        data = json.loads(json_match.group())
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse-Fehler: {e}")
        return None
    
    # Validate and normalize
    slug = data.get("slug") or grape_name.lower().replace(" ", "-").replace("·", "-")
    
    # Check slug duplicate
    if slug in existing_slugs:
        slug = f"{slug}-espana"
    
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
        "image_url": image_url,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    return grape_doc


async def consistency_check(grapes: list):
    """Use Claude to check consistency of generated grapes"""
    
    print("\n🔍 Konsistenzprüfung mit Claude...")
    
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=str(uuid.uuid4()),
        system_message="Du bist ein spanischer Wein-Experte. Prüfe die Daten auf Konsistenz und Korrektheit."
    ).with_model("openai", "gpt-5.1")
    
    # Summary for check
    summary = []
    for g in grapes:
        summary.append({
            "name": g["name"],
            "type": g["type"],
            "body": g["body"],
            "acidity": g["acidity"],
            "tannin": g["tannin"],
            "regions": g.get("main_regions", [])[:2],
            "aromas": g.get("primary_aromas", [])[:3]
        })
    
    prompt = f"""Prüfe diese spanischen Rebsorten auf Korrektheit und Konsistenz:

{json.dumps(summary, indent=2, ensure_ascii=False)}

Prüfe kritisch:
1. Sind die Rebsorten-Typen (rot/weiss) alle korrekt?
2. Sind Body/Säure/Tannin für jede spanische Sorte plausibel?
3. Stimmen die angegebenen spanischen Regionen (DO/DOCa)?
4. Gibt es Duplikate oder sehr ähnliche Einträge?
5. Gibt es offensichtliche Fehler bei den Aromen?

Antworte KURZ und strukturiert:
✅ KORREKT: [Anzahl] Rebsorten
⚠️ ZU PRÜFEN: [Liste mit Begründung falls nötig]
❌ FEHLER: [Liste mit Korrektur falls nötig]"""

    user_message = UserMessage(text=prompt)
    response = await chat.send_message(user_message)
    
    print(response)
    return response


async def main():
    print("🍇 Generiere spanische Rebsorten")
    print("=" * 60)
    
    # Get existing grapes
    existing_names, existing_slugs = await get_existing_grapes()
    print(f"📋 {len(existing_names)} bestehende Rebsorten gefunden")
    print(f"   Überspringe: Tempranillo (bereits vorhanden)")
    
    # Filter out already existing
    grapes_to_generate = [(name, t, img) for name, t, img in SPANISH_GRAPES 
                         if name.lower() not in existing_names]
    
    print(f"\n🎯 Generiere {len(grapes_to_generate)} neue spanische Rebsorten:\n")
    
    generated = []
    
    for i, (grape_name, grape_type, image_url) in enumerate(grapes_to_generate, 1):
        print(f"[{i}/{len(grapes_to_generate)}] {grape_name}...", end=" ", flush=True)
        
        try:
            grape_doc = await generate_grape(grape_name, grape_type, image_url, existing_names, existing_slugs)
            
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
