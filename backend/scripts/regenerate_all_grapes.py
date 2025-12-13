"""
Regenerate ALL European grape varieties
Based on the original structure from generate_italian_grapes.py and generate_spanish_grapes.py
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
db = client[os.environ.get('DB_NAME', 'wine_pairing_db')]

EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

# ===================== GRAPE LISTS BY COUNTRY =====================

ITALIAN_GRAPES = [
    # Red grapes
    ("Barbera", "rot", "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800"),
    ("Primitivo", "rot", "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800"),
    ("Nero d'Avola", "rot", "https://images.unsplash.com/photo-1474722883778-792e7990302f?w=800"),
    ("Montepulciano", "rot", "https://images.unsplash.com/photo-1567696911980-2eed69a46042?w=800"),
    ("Dolcetto", "rot", "https://images.unsplash.com/photo-1558346489-19413928158b?w=800"),
    ("Corvina", "rot", "https://images.unsplash.com/photo-1516594915697-87eb3b1c14ea?w=800"),
    ("Aglianico", "rot", "https://images.unsplash.com/photo-1560148218-1a83060f7b32?w=800"),
    ("Nerello Mascalese", "rot", "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=800"),
    ("Lagrein", "rot", "https://images.unsplash.com/photo-1566754436808-0fddc0c0c4c6?w=800"),
    ("Cannonau", "rot", "https://images.unsplash.com/photo-1584916201218-f4242ceb4809?w=800"),
    ("Sagrantino", "rot", "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800"),
    ("Teroldego", "rot", "https://images.unsplash.com/photo-1568213214202-3e582bc02fd5?w=800"),
    ("Negroamaro", "rot", "https://images.unsplash.com/photo-1507434965515-61970f2bd7c6?w=800"),
    ("Schiava", "rot", "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=800"),
    ("Refosco", "rot", "https://images.unsplash.com/photo-1571950006920-a8621a6d8c4e?w=800"),
    # White grapes
    ("Trebbiano", "weiss", "https://images.unsplash.com/photo-1528823872057-9c018a7a7553?w=800"),
    ("Garganega", "weiss", "https://images.unsplash.com/photo-1566995541428-f2246c17cda1?w=800"),
    ("Verdicchio", "weiss", "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800"),
    ("Fiano", "weiss", "https://images.unsplash.com/photo-1568213214202-3e582bc02fd5?w=800"),
    ("Greco", "weiss", "https://images.unsplash.com/photo-1507434965515-61970f2bd7c6?w=800"),
    ("Falanghina", "weiss", "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=800"),
    ("Arneis", "weiss", "https://images.unsplash.com/photo-1571950006920-a8621a6d8c4e?w=800"),
    ("Cortese", "weiss", "https://images.unsplash.com/photo-1528823872057-9c018a7a7553?w=800"),
    ("Vermentino", "weiss", "https://images.unsplash.com/photo-1566995541428-f2246c17cda1?w=800"),
    ("Friulano", "weiss", "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800"),
    ("Ribolla Gialla", "weiss", "https://images.unsplash.com/photo-1568213214202-3e582bc02fd5?w=800"),
    ("Glera", "weiss", "https://images.unsplash.com/photo-1507434965515-61970f2bd7c6?w=800"),
    ("Moscato Bianco", "weiss", "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=800"),
    ("Malvasia", "weiss", "https://images.unsplash.com/photo-1571950006920-a8621a6d8c4e?w=800"),
    ("Pecorino", "weiss", "https://images.unsplash.com/photo-1528823872057-9c018a7a7553?w=800"),
]

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

FRENCH_GRAPES = [
    # Red grapes
    ("Grenache", "rot", "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800"),
    ("Mourvèdre", "rot", "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800"),
    ("Carignan", "rot", "https://images.unsplash.com/photo-1474722883778-792e7990302f?w=800"),
    ("Cinsault", "rot", "https://images.unsplash.com/photo-1567696911980-2eed69a46042?w=800"),
    ("Gamay", "rot", "https://images.unsplash.com/photo-1558346489-19413928158b?w=800"),
    ("Cabernet Franc", "rot", "https://images.unsplash.com/photo-1516594915697-87eb3b1c14ea?w=800"),
    ("Malbec", "rot", "https://images.unsplash.com/photo-1560148218-1a83060f7b32?w=800"),
    ("Petit Verdot", "rot", "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=800"),
    ("Tannat", "rot", "https://images.unsplash.com/photo-1566754436808-0fddc0c0c4c6?w=800"),
    # White grapes
    ("Chenin Blanc", "weiss", "https://images.unsplash.com/photo-1566995541428-f2246c17cda1?w=800"),
    ("Viognier", "weiss", "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800"),
    ("Marsanne", "weiss", "https://images.unsplash.com/photo-1568213214202-3e582bc02fd5?w=800"),
    ("Roussanne", "weiss", "https://images.unsplash.com/photo-1507434965515-61970f2bd7c6?w=800"),
    ("Sémillon", "weiss", "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=800"),
    ("Muscadet", "weiss", "https://images.unsplash.com/photo-1571950006920-a8621a6d8c4e?w=800"),
    ("Picpoul", "weiss", "https://images.unsplash.com/photo-1528823872057-9c018a7a7553?w=800"),
    ("Ugni Blanc", "weiss", "https://images.unsplash.com/photo-1566995541428-f2246c17cda1?w=800"),
]

PORTUGUESE_GRAPES = [
    # Red grapes
    ("Touriga Nacional", "rot", "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800"),
    ("Touriga Franca", "rot", "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800"),
    ("Tinta Roriz", "rot", "https://images.unsplash.com/photo-1474722883778-792e7990302f?w=800"),
    ("Baga", "rot", "https://images.unsplash.com/photo-1567696911980-2eed69a46042?w=800"),
    ("Castelão", "rot", "https://images.unsplash.com/photo-1558346489-19413928158b?w=800"),
    ("Trincadeira", "rot", "https://images.unsplash.com/photo-1516594915697-87eb3b1c14ea?w=800"),
    ("Tinta Barroca", "rot", "https://images.unsplash.com/photo-1560148218-1a83060f7b32?w=800"),
    # White grapes
    ("Alvarinho", "weiss", "https://images.unsplash.com/photo-1566995541428-f2246c17cda1?w=800"),
    ("Loureiro", "weiss", "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800"),
    ("Arinto", "weiss", "https://images.unsplash.com/photo-1568213214202-3e582bc02fd5?w=800"),
    ("Encruzado", "weiss", "https://images.unsplash.com/photo-1507434965515-61970f2bd7c6?w=800"),
    ("Fernão Pires", "weiss", "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=800"),
    ("Verdelho", "weiss", "https://images.unsplash.com/photo-1571950006920-a8621a6d8c4e?w=800"),
]

GERMAN_GRAPES = [
    # Red grapes
    ("Spätburgunder", "rot", "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800"),
    ("Dornfelder", "rot", "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800"),
    ("Trollinger", "rot", "https://images.unsplash.com/photo-1474722883778-792e7990302f?w=800"),
    ("Lemberger", "rot", "https://images.unsplash.com/photo-1567696911980-2eed69a46042?w=800"),
    ("Portugieser", "rot", "https://images.unsplash.com/photo-1558346489-19413928158b?w=800"),
    ("Schwarzriesling", "rot", "https://images.unsplash.com/photo-1516594915697-87eb3b1c14ea?w=800"),
    # White grapes
    ("Müller-Thurgau", "weiss", "https://images.unsplash.com/photo-1566995541428-f2246c17cda1?w=800"),
    ("Silvaner", "weiss", "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800"),
    ("Weißburgunder", "weiss", "https://images.unsplash.com/photo-1568213214202-3e582bc02fd5?w=800"),
    ("Grauburgunder", "weiss", "https://images.unsplash.com/photo-1507434965515-61970f2bd7c6?w=800"),
    ("Scheurebe", "weiss", "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=800"),
    ("Kerner", "weiss", "https://images.unsplash.com/photo-1571950006920-a8621a6d8c4e?w=800"),
    ("Bacchus", "weiss", "https://images.unsplash.com/photo-1528823872057-9c018a7a7553?w=800"),
    ("Elbling", "weiss", "https://images.unsplash.com/photo-1566995541428-f2246c17cda1?w=800"),
]

AUSTRIAN_GRAPES = [
    # Red grapes
    ("Blaufränkisch", "rot", "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800"),
    ("Zweigelt", "rot", "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800"),
    ("St. Laurent", "rot", "https://images.unsplash.com/photo-1474722883778-792e7990302f?w=800"),
    ("Blauer Portugieser", "rot", "https://images.unsplash.com/photo-1567696911980-2eed69a46042?w=800"),
    # White grapes
    ("Welschriesling", "weiss", "https://images.unsplash.com/photo-1566995541428-f2246c17cda1?w=800"),
    ("Neuburger", "weiss", "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800"),
    ("Rotgipfler", "weiss", "https://images.unsplash.com/photo-1568213214202-3e582bc02fd5?w=800"),
    ("Zierfandler", "weiss", "https://images.unsplash.com/photo-1507434965515-61970f2bd7c6?w=800"),
    ("Roter Veltliner", "weiss", "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=800"),
    ("Frühroter Veltliner", "weiss", "https://images.unsplash.com/photo-1571950006920-a8621a6d8c4e?w=800"),
]

SWISS_GRAPES = [
    # Red grapes
    ("Pinot Noir Suisse", "rot", "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800"),
    ("Gamaret", "rot", "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800"),
    ("Garanoir", "rot", "https://images.unsplash.com/photo-1474722883778-792e7990302f?w=800"),
    ("Cornalin", "rot", "https://images.unsplash.com/photo-1567696911980-2eed69a46042?w=800"),
    ("Humagne Rouge", "rot", "https://images.unsplash.com/photo-1558346489-19413928158b?w=800"),
    # White grapes
    ("Chasselas", "weiss", "https://images.unsplash.com/photo-1566995541428-f2246c17cda1?w=800"),
    ("Petite Arvine", "weiss", "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800"),
    ("Amigne", "weiss", "https://images.unsplash.com/photo-1568213214202-3e582bc02fd5?w=800"),
    ("Heida", "weiss", "https://images.unsplash.com/photo-1507434965515-61970f2bd7c6?w=800"),
    ("Completer", "weiss", "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=800"),
    ("Räuschling", "weiss", "https://images.unsplash.com/photo-1571950006920-a8621a6d8c4e?w=800"),
]

# ===================== SYSTEM PROMPTS =====================

def get_system_prompt(country: str) -> str:
    """Get country-specific system prompt for grape generation"""
    country_context = {
        "Italien": "wie ein leidenschaftlicher italienischer Winzer unter der toskanischen Sonne. Evoziere la dolce vita, die Terrassen am Gardasee, die vulkanische Kraft des Ätna.",
        "Spanien": "wie ein spanischer Winzer unter der glühenden Sonne Kastiliens. Evoziere die Hitze, Flamenco, Tapas-Bars und die stolze Geschichte.",
        "Frankreich": "wie ein französischer vigneron im Herzen der Champagne oder Burgunds. Evoziere Eleganz, Terroir, jahrhundertealte Tradition.",
        "Portugal": "wie ein portugiesischer Quinta-Besitzer am Douro. Evoziere die steilen Terrassen, den Atlantik, Saudade und Porto.",
        "Deutschland": "wie ein deutscher Winzer an der Mosel oder im Rheingau. Evoziere die steilen Schieferhänge, die kühle Eleganz, Präzision.",
        "Österreich": "wie ein österreichischer Heuriger-Wirt in der Wachau. Evoziere Gemütlichkeit, die Donau, Wiener Schnitzel und Kaffeehauskultur.",
        "Schweiz": "wie ein Schweizer Winzer im Wallis. Evoziere die Alpen, Präzision, Reinheit und die einzigartige Höhenlage."
    }
    
    return f"""Du bist ein Wein-Experte und Sommelier mit besonderer Expertise für {country}er Weine. Erzeuge einen vollständigen, poetischen Datensatz für Rebsorten.

STIL: Poetisch, emotional, leidenschaftlich - {country_context.get(country, 'wie ein erfahrener Sommelier')}

ANTWORTFORMAT (STRICT JSON, KEIN ERKLÄRTEXT):
{{
  "slug": "kebab-case-slug-ohne-umlaute",
  "name": "Name der Rebsorte",
  "type": "rot" oder "weiss",
  "description": "Poetische deutsche Beschreibung (4-6 Sätze). Beschreibe Farbe, Duft, Geschmack und Charakter der Traube wie ein Dichter.",
  "description_en": "Poetic English description (4-6 sentences). Same passionate style.",
  "description_fr": "Description poétique en français (4-6 phrases). Même style passionné.",
  "synonyms": ["Alternative Namen oder regionale Bezeichnungen"],
  "body": "leicht" oder "mittel" oder "vollmundig",
  "acidity": "niedrig" oder "mittel" oder "hoch",
  "tannin": "niedrig" oder "mittel" oder "hoch",
  "aging": "Typischer Ausbau: Edelstahl, Holz, etc.",
  "primary_aromas": ["5-7 deutsche Aroma-Tags in Kleinschreibung"],
  "tertiary_aromas": ["3-5 Reife-/Alterungsaromen in Kleinschreibung"],
  "perfect_pairings": ["5-7 passende Gerichte aus {country} auf Deutsch"],
  "perfect_pairings_en": ["Same dishes in English"],
  "perfect_pairings_fr": ["Mêmes plats en français"],
  "main_regions": ["3-5 wichtigste Anbaugebiete in {country}"]
}}

WICHTIG:
- Beschreibungen müssen POETISCH und EMOTIONAL sein, nicht technisch
- Alle drei Sprachen müssen denselben Inhalt in unterschiedlichen Worten vermitteln
- Speisepaarungen speziell auf {country}er Küche abstimmen
"""


async def get_existing_grapes():
    """Get list of existing grape names to avoid duplicates"""
    grapes = await db.grape_varieties.find({}, {"name": 1, "slug": 1, "_id": 0}).to_list(500)
    existing_names = set(g['name'].lower() for g in grapes)
    # Auch Varianten ohne Sonderzeichen hinzufügen
    for g in grapes:
        name = g['name'].lower()
        # Varianten hinzufügen
        existing_names.add(name.replace('ñ', 'n'))
        existing_names.add(name.replace('·', ''))
    existing_slugs = set(g['slug'] for g in grapes)
    return existing_names, existing_slugs


async def generate_grape(grape_name: str, grape_type: str, image_url: str, country: str, existing_names: set, existing_slugs: set):
    """Generate a single grape variety entry using AI"""
    
    # Check for duplicate
    if grape_name.lower() in existing_names:
        print(f"  ⚠️  {grape_name} bereits vorhanden - überspringe")
        return None
    
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=str(uuid.uuid4()),
        system_message=get_system_prompt(country)
    ).with_model("openai", "gpt-5.1")
    
    prompt = f"""Erzeuge einen vollständigen Datensatz für die {country}er Rebsorte '{grape_name}' (Typ: {grape_type}).

Beachte:
- Diese Traube stammt aus {country}
- Beschreibe sie poetisch und emotional
- Füge typisch {country}er Speisepaarungen hinzu
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
    slug = data.get("slug") or grape_name.lower().replace(" ", "-").replace("'", "").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
    
    # Check slug duplicate
    if slug in existing_slugs:
        slug = f"{slug}-{country.lower()}"
    
    # Build grape entry
    grape_entry = {
        "id": str(uuid.uuid4()),
        "slug": slug,
        "name": data.get("name", grape_name),
        "type": grape_type,
        "description": data.get("description", ""),
        "description_en": data.get("description_en", ""),
        "description_fr": data.get("description_fr", ""),
        "synonyms": data.get("synonyms", []),
        "body": data.get("body", "mittel"),
        "acidity": data.get("acidity", "mittel"),
        "tannin": data.get("tannin", "mittel" if grape_type == "rot" else "niedrig"),
        "aging": data.get("aging", ""),
        "primary_aromas": data.get("primary_aromas", []),
        "tertiary_aromas": data.get("tertiary_aromas", []),
        "perfect_pairings": data.get("perfect_pairings", []),
        "perfect_pairings_en": data.get("perfect_pairings_en", []),
        "perfect_pairings_fr": data.get("perfect_pairings_fr", []),
        "main_regions": data.get("main_regions", []),
        "image_url": image_url,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    # Save to database
    await db.grape_varieties.insert_one(grape_entry)
    existing_names.add(grape_name.lower())
    existing_slugs.add(slug)
    
    return grape_entry


async def generate_country_grapes(country: str, grapes: list, existing_names: set, existing_slugs: set):
    """Generate all grapes for a country"""
    print(f"\n🍇 Generiere {country}er Rebsorten ({len(grapes)} Stück)...")
    
    created = 0
    for grape_name, grape_type, image_url in grapes:
        print(f"  → {grape_name}...", end=" ")
        result = await generate_grape(grape_name, grape_type, image_url, country, existing_names, existing_slugs)
        if result:
            print("✓")
            created += 1
        await asyncio.sleep(1)  # Rate limiting
    
    print(f"  ✅ {created}/{len(grapes)} {country}er Rebsorten erstellt")
    return created


async def main():
    """Main function to regenerate all European grape varieties"""
    print("=" * 60)
    print("🍷 REBSORTEN-REGENERATION FÜR EUROPÄISCHE WEINLÄNDER")
    print("=" * 60)
    
    # Get existing grapes
    existing_names, existing_slugs = await get_existing_grapes()
    print(f"\n📊 Bereits vorhanden: {len(existing_names)} Rebsorten")
    
    total_created = 0
    
    # Generate by country
    countries = [
        ("Italien", ITALIAN_GRAPES),
        ("Spanien", SPANISH_GRAPES),
        ("Frankreich", FRENCH_GRAPES),
        ("Portugal", PORTUGUESE_GRAPES),
        ("Deutschland", GERMAN_GRAPES),
        ("Österreich", AUSTRIAN_GRAPES),
        ("Schweiz", SWISS_GRAPES),
    ]
    
    for country, grapes in countries:
        created = await generate_country_grapes(country, grapes, existing_names, existing_slugs)
        total_created += created
    
    # Final count
    final_count = await db.grape_varieties.count_documents({})
    
    print("\n" + "=" * 60)
    print(f"🎉 FERTIG! {total_created} neue Rebsorten erstellt")
    print(f"📊 Gesamt in Datenbank: {final_count} Rebsorten")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
