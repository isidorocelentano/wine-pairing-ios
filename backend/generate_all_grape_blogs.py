"""
Generate Blog Posts for ALL Grape Varieties
Uses AI to create unique, poetic blog posts for each grape variety
"""
import asyncio
import os
import json
import re
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from emergentintegrations.llm.chat import LlmChat, UserMessage
import uuid
from datetime import datetime, timezone

# Load environment
ROOT_DIR = Path(__file__).parent
with open(ROOT_DIR / '.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value.strip('"')

# MongoDB connection
client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
db = client[os.environ.get('DB_NAME', 'test_database')]
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

# ===================== PROMPTS =====================

GENERATION_PROMPT = """Du bist ein leidenschaftlicher Sommelier und Weinautor. Schreibe einen ausführlichen, emotionalen Blog-Artikel über die Rebsorte "{grape_name}".

## REBSORTEN-INFORMATIONEN:
- Name: {grape_name}
- Typ: {grape_type}
- Hauptregionen: {regions}
- Aromen: {aromas}
- Körper: {body}
- Säure: {acidity}
- Beschreibung: {description}

## STRUKTUR (Halte dich strikt daran):

### 1. TITEL
Erstelle einen poetischen, einprägsamen Titel mit einem passenden Beinamen.
Format: "[Beiname] [Rebsorte]: [Untertitel]"

### 2. EINLEITUNG (2-3 Absätze)
- Emotionale Begrüßung ("Liebe Weinliebhaber...")
- Was macht diese Rebsorte besonders?
- Bildhafte Sprache und Metaphern

### 3. ANBAUGEBIETE
Überschrift: "## 1. Der Globetrotter im Glas: Wo der {grape_name} zu Hause ist"
- Beschreibe 3-5 wichtige Anbauregionen
- Charakteristischer Stil pro Region

### 4. AUSBAUSTUFEN
Überschrift: "## 2. [Passender Untertitel zum Ausbau]"
- Stahltank vs. Holzfass
- Geschmacksunterschiede

### 5. FOOD PAIRING (mit Tabelle)
Überschrift: "## 3. Pairing-Empfehlungen: Der perfekte Partner"
Markdown-Tabelle mit 3 Gerichten:
| Gericht | Wein-Stil | Warum es funktioniert |

### 6. FAQ (10 Fragen)
Überschrift: "## 4. FAQ – 10 Fragen für {grape_name}-Liebhaber"
Format: **❓ [Frage]** mit Antwort darunter

## STILRICHTLINIEN:
- Poetisch, leidenschaftlich, einladend
- Deutsch, Du-Form
- Ca. 1200-1500 Wörter
- Markdown-Formatierung

## OUTPUT:
Gib NUR den Artikel zurück (mit Titel), keine Erklärungen.
"""

TRANSLATION_PROMPT = """Übersetze den folgenden deutschen Weinblog-Artikel ins {target_language}.

REGELN:
1. Behalte Markdown-Formatierung und Emojis bei
2. Übersetze Weinnamen/Regionen NICHT
3. Tabellen-Format beibehalten
4. Ton: warm, leidenschaftlich

OUTPUT als JSON:
{{
  "title": "Übersetzter Titel",
  "excerpt": "Kurze Zusammenfassung (max 200 Zeichen)",
  "content": "Vollständiger Artikel"
}}

DEUTSCHER ARTIKEL:
{content}
"""

def create_slug(name: str) -> str:
    """Create URL-friendly slug from grape name"""
    slug = name.lower()
    # Replace special characters
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ô': 'o', 'î': 'i',
        'ñ': 'n', 'ç': 'c', '·': '', "'": '', ' ': '-',
        '/': '-', '.': ''
    }
    for old, new in replacements.items():
        slug = slug.replace(old, new)
    # Remove any remaining non-alphanumeric chars
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    slug = re.sub(r'-+', '-', slug)  # Remove multiple dashes
    return slug.strip('-')


async def generate_blog_content(grape: dict) -> str:
    """Generate German blog content for a grape variety"""
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=str(uuid.uuid4()),
        system_message="Du bist ein leidenschaftlicher Sommelier und Weinautor mit jahrzehntelanger Erfahrung."
    ).with_model("openai", "gpt-5.1")
    
    prompt = GENERATION_PROMPT.format(
        grape_name=grape.get('name', ''),
        grape_type='Rotwein' if grape.get('type') == 'rot' else 'Weißwein',
        regions=', '.join(grape.get('main_regions', [])[:5]),
        aromas=', '.join(grape.get('primary_aromas', [])[:7]),
        body=grape.get('body', 'mittel'),
        acidity=grape.get('acidity', 'mittel'),
        description=grape.get('description', '')[:500]
    )
    
    response = await chat.send_message(UserMessage(text=prompt))
    return response if response else ""


async def translate_content(content: str, target_language: str) -> dict:
    """Translate content to target language"""
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=str(uuid.uuid4()),
        system_message="Du bist ein professioneller Übersetzer für Wein-Content."
    ).with_model("openai", "gpt-5.1")
    
    prompt = TRANSLATION_PROMPT.format(
        target_language=target_language,
        content=content
    )
    
    response = await chat.send_message(UserMessage(text=prompt))
    
    # Extract JSON
    json_match = re.search(r"\{[\s\S]*\}", response)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            return {}
    return {}


def extract_title_and_excerpt(content: str) -> tuple:
    """Extract title and excerpt from generated content"""
    lines = content.strip().split('\n')
    
    # Title is first non-empty line
    title = ""
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            title = line
            break
        elif line.startswith('#'):
            title = line.lstrip('#').strip()
            break
    
    # Excerpt from first paragraph after title
    excerpt = ""
    in_content = False
    for line in lines[1:]:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('|'):
            if in_content or not excerpt:
                excerpt = line[:200]
                break
        if line.startswith('##'):
            in_content = True
    
    return title, excerpt


async def create_blog_post_for_grape(grape: dict, existing_slugs: set) -> bool:
    """Create a complete blog post for a single grape variety"""
    grape_name = grape.get('name', '')
    slug = f"rebsorte-{create_slug(grape_name)}"
    
    # Skip if already exists
    if slug in existing_slugs:
        print(f"  ⏭️  {grape_name} - bereits vorhanden")
        return False
    
    try:
        # Generate German content
        print(f"  📝 Generiere DE...", end=" ", flush=True)
        de_content = await generate_blog_content(grape)
        if not de_content:
            print("❌ Fehler bei DE")
            return False
        print("✓", end=" ", flush=True)
        
        # Extract title and excerpt
        de_title, de_excerpt = extract_title_and_excerpt(de_content)
        if not de_title:
            de_title = f"{grape_name}: Ein Porträt"
        if not de_excerpt:
            de_excerpt = grape.get('description', '')[:200]
        
        # Translate to English
        print("EN...", end=" ", flush=True)
        en_data = await translate_content(de_content, "Englisch")
        print("✓", end=" ", flush=True)
        
        # Translate to French
        print("FR...", end=" ", flush=True)
        fr_data = await translate_content(de_content, "Französisch")
        print("✓")
        
        # Create blog post document
        blog_post = {
            "id": str(uuid.uuid4()),
            "slug": slug,
            "grape_id": grape.get('id', ''),
            "grape_slug": grape.get('slug', ''),
            "title": de_title,
            "title_en": en_data.get('title', ''),
            "title_fr": fr_data.get('title', ''),
            "excerpt": de_excerpt,
            "excerpt_en": en_data.get('excerpt', ''),
            "excerpt_fr": fr_data.get('excerpt', ''),
            "content": de_content,
            "content_en": en_data.get('content', ''),
            "content_fr": fr_data.get('content', ''),
            "image_url": grape.get('image_url', 'https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=1200'),
            "category": "rebsorten",
            "tags": [create_slug(grape_name), grape.get('type', ''), "rebsorten", "weinwissen"],
            "author": "Sommelier Team",
            "published": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Insert into database
        await db.blog_posts.insert_one(blog_post)
        return True
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False


async def main():
    print("=" * 70)
    print("🍇 BLOG-POSTS FÜR ALLE REBSORTEN GENERIEREN")
    print("=" * 70)
    
    # Get all grape varieties
    grapes = await db.grape_varieties.find({}, {"_id": 0}).sort("name", 1).to_list(500)
    print(f"\n📊 Gefunden: {len(grapes)} Rebsorten")
    
    # Get existing blog post slugs
    existing_posts = await db.blog_posts.find({}, {"slug": 1, "_id": 0}).to_list(1000)
    existing_slugs = set(p['slug'] for p in existing_posts)
    print(f"📝 Existierende Blog-Posts: {len(existing_slugs)}")
    
    # Filter grapes that already have posts
    grapes_to_process = []
    for grape in grapes:
        slug = f"rebsorte-{create_slug(grape.get('name', ''))}"
        if slug not in existing_slugs:
            grapes_to_process.append(grape)
    
    print(f"🆕 Zu erstellen: {len(grapes_to_process)} Blog-Posts")
    print()
    
    if not grapes_to_process:
        print("✅ Alle Blog-Posts bereits vorhanden!")
        return
    
    # Process grapes
    created = 0
    failed = 0
    
    for i, grape in enumerate(grapes_to_process, 1):
        grape_name = grape.get('name', 'Unbekannt')
        print(f"[{i}/{len(grapes_to_process)}] {grape_name}")
        
        success = await create_blog_post_for_grape(grape, existing_slugs)
        if success:
            created += 1
            existing_slugs.add(f"rebsorte-{create_slug(grape_name)}")
        else:
            failed += 1
        
        # Rate limiting - wait between requests
        await asyncio.sleep(2)
        
        # Progress update every 10 posts
        if i % 10 == 0:
            print(f"\n📈 Fortschritt: {i}/{len(grapes_to_process)} ({created} erstellt, {failed} fehlgeschlagen)\n")
    
    # Final summary
    print()
    print("=" * 70)
    print("🎉 FERTIG!")
    print("=" * 70)
    print(f"✅ Erstellt: {created}")
    print(f"❌ Fehlgeschlagen: {failed}")
    print(f"⏭️  Übersprungen: {len(grapes) - len(grapes_to_process)}")
    
    # Update backup
    print("\n💾 Backup wird aktualisiert...")
    total_posts = await db.blog_posts.count_documents({})
    print(f"📝 Gesamt Blog-Posts: {total_posts}")


if __name__ == "__main__":
    asyncio.run(main())
