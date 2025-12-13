#!/usr/bin/env python3
"""
🍷 Automatische Blog-Generierung für Weinregionen
Erstellt hochwertige, SEO-optimierte Blog-Beiträge mit Übersetzungen
"""

import asyncio
import os
import json
import re
from uuid import uuid4
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, List
from motor.motor_asyncio import AsyncIOMotorClient

# Lade Umgebungsvariablen
env_path = Path('/app/backend/.env')
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value.strip('"').strip("'")

from emergentintegrations.llm.chat import LlmChat, UserMessage

EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY")

# Wichtige Weinregionen für Blog-Erstellung (Priorität)
PRIORITY_REGIONS = [
    # Frankreich
    {"name": "Châteauneuf-du-Pape", "country": "Frankreich", "type": "appellation"},
    {"name": "Bordeaux", "country": "Frankreich", "type": "region"},
    {"name": "Burgund", "country": "Frankreich", "type": "region"},
    {"name": "Champagne", "country": "Frankreich", "type": "region"},
    {"name": "Elsass", "country": "Frankreich", "type": "region"},
    {"name": "Loire", "country": "Frankreich", "type": "region"},
    {"name": "Rhône", "country": "Frankreich", "type": "region"},
    {"name": "Provence", "country": "Frankreich", "type": "region"},
    
    # Italien
    {"name": "Toskana", "country": "Italien", "type": "region"},
    {"name": "Piemont", "country": "Italien", "type": "region"},
    {"name": "Venetien", "country": "Italien", "type": "region"},
    {"name": "Sizilien", "country": "Italien", "type": "region"},
    {"name": "Südtirol", "country": "Italien", "type": "region"},
    
    # Spanien
    {"name": "Rioja", "country": "Spanien", "type": "region"},
    {"name": "Ribera del Duero", "country": "Spanien", "type": "region"},
    {"name": "Priorat", "country": "Spanien", "type": "region"},
    {"name": "Jerez", "country": "Spanien", "type": "region"},
    
    # Deutschland
    {"name": "Mosel", "country": "Deutschland", "type": "region"},
    {"name": "Rheingau", "country": "Deutschland", "type": "region"},
    {"name": "Pfalz", "country": "Deutschland", "type": "region"},
    {"name": "Franken", "country": "Deutschland", "type": "region"},
    {"name": "Baden", "country": "Deutschland", "type": "region"},
    {"name": "Nahe", "country": "Deutschland", "type": "region"},
    {"name": "Ahr", "country": "Deutschland", "type": "region"},
    
    # Schweiz
    {"name": "Wallis", "country": "Schweiz", "type": "region"},
    {"name": "Waadt", "country": "Schweiz", "type": "region"},
    {"name": "Genf", "country": "Schweiz", "type": "region"},
    {"name": "Tessin", "country": "Schweiz", "type": "region"},
    {"name": "Graubünden", "country": "Schweiz", "type": "region"},
    
    # Österreich
    {"name": "Wachau", "country": "Österreich", "type": "region"},
    {"name": "Burgenland", "country": "Österreich", "type": "region"},
    {"name": "Steiermark", "country": "Österreich", "type": "region"},
    
    # Neue Welt
    {"name": "Napa Valley", "country": "USA", "type": "region"},
    {"name": "Sonoma", "country": "USA", "type": "region"},
    {"name": "Mendoza", "country": "Argentinien", "type": "region"},
    {"name": "Barossa Valley", "country": "Australien", "type": "region"},
    {"name": "Marlborough", "country": "Neuseeland", "type": "region"},
    {"name": "Stellenbosch", "country": "Südafrika", "type": "region"},
    
    # Portugal
    {"name": "Douro", "country": "Portugal", "type": "region"},
    {"name": "Alentejo", "country": "Portugal", "type": "region"},
    
    # Ungarn
    {"name": "Tokaj", "country": "Ungarn", "type": "region"},
]

BLOG_PROMPT_TEMPLATE = """Du bist ein leidenschaftlicher Wein-Journalist und Sommelier. Erstelle einen hochwertigen, emotionalen und SEO-optimierten Blog-Beitrag über die Weinregion/Appellation "{region}" in {country}.

WICHTIGE ANWEISUNGEN:
1. Der Text soll ca. 1200-1500 Wörter haben
2. Tonalität: Emotional, leidenschaftlich, inspirierend
3. Zielgruppe: Anspruchsvolle Weinliebhaber und Geniesser
4. SEO-Keywords natürlich einbauen

STRUKTUR (bitte einhalten):

## [Emotionaler Titel mit Region]

**Meta-Description:** [Max 155 Zeichen, verlockend]

### Einleitung: [Emotionaler Hook]
[Sinnliche Beschreibung, die den Leser in die Region versetzt. Gerüche, Landschaft, Atmosphäre.]

### Das Terroir: Boden und Klima
[Beschreibung der Böden, des Klimas, was die Region einzigartig macht]

### Die Rebsorten
[Hauptrebsorten der Region, ihre Charakteristiken]

### Geschichte und Tradition
[Historischer Hintergrund, wichtige Ereignisse, Persönlichkeiten]

### Typischer Stil und Aromen
[Sensorische Beschreibung der Weine, Aromaprofil]

### Food Pairing
[Passende Speisen, regionale Küche]

### FAQ – Häufige Fragen

**1. Was macht {region} Weine besonders?**
[Prägnante Antwort]

**2. Welche Rebsorten dominieren in {region}?**
[Prägnante Antwort]

**3. Wie lange sollte man {region} Weine lagern?**
[Prägnante Antwort]

**4. Welche Speisen passen zu {region} Weinen?**
[Prägnante Antwort]

**5. Was ist die beste Jahreszeit für einen Besuch in {region}?**
[Prägnante Antwort]

### Fazit
[Emotionaler Abschluss mit Call-to-Action]

---

Antworte NUR mit dem Blog-Text, keine zusätzlichen Erklärungen."""


async def generate_region_blog(region: str, country: str) -> Optional[Dict]:
    """Generiert einen dreisprachigen Blog-Beitrag für eine Weinregion"""
    
    try:
        print(f"  📝 Generiere deutschen Blog für {region}...")
        
        # Deutscher Blog
        chat_de = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=str(uuid4()),
            system_message="Du bist ein erfahrener Wein-Journalist. Schreibe auf Deutsch."
        ).with_model("openai", "gpt-5.1")
        
        prompt_de = BLOG_PROMPT_TEMPLATE.format(region=region, country=country)
        content_de = await chat_de.send_message(UserMessage(text=prompt_de))
        
        # Extrahiere Titel aus dem deutschen Content
        title_match = re.search(r'^##\s*(.+)$', content_de, re.MULTILINE)
        title_de = title_match.group(1).strip() if title_match else f"Entdecke {region} – Ein Weinparadies in {country}"
        
        # Meta-Description extrahieren
        meta_match = re.search(r'\*\*Meta-Description:\*\*\s*(.+)', content_de)
        excerpt_de = meta_match.group(1).strip()[:200] if meta_match else f"Entdecken Sie die faszinierende Weinregion {region} in {country}. Geschichte, Terroir, Rebsorten und die besten Weine."
        
        print(f"  🇬🇧 Generiere englische Übersetzung...")
        
        # Englische Übersetzung
        chat_en = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=str(uuid4()),
            system_message="You are a professional wine journalist. Translate to English while keeping the emotional and engaging tone."
        ).with_model("openai", "gpt-5.1")
        
        translate_en_prompt = f"""Translate this German wine blog post to English. Keep the same structure, headings (##, ###), and emotional tone:

{content_de}"""
        
        content_en = await chat_en.send_message(UserMessage(text=translate_en_prompt))
        
        title_en_match = re.search(r'^##\s*(.+)$', content_en, re.MULTILINE)
        title_en = title_en_match.group(1).strip() if title_en_match else f"Discover {region} – A Wine Paradise in {country}"
        
        meta_en_match = re.search(r'\*\*Meta-Description:\*\*\s*(.+)', content_en)
        excerpt_en = meta_en_match.group(1).strip()[:200] if meta_en_match else f"Discover the fascinating wine region {region} in {country}. History, terroir, grape varieties and the best wines."
        
        print(f"  🇫🇷 Generiere französische Übersetzung...")
        
        # Französische Übersetzung
        chat_fr = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=str(uuid4()),
            system_message="Vous êtes un journaliste vinicole professionnel. Traduisez en français en gardant le ton émotionnel et engageant."
        ).with_model("openai", "gpt-5.1")
        
        translate_fr_prompt = f"""Traduisez ce blog sur le vin en français. Gardez la même structure, les titres (##, ###), et le ton émotionnel:

{content_de}"""
        
        content_fr = await chat_fr.send_message(UserMessage(text=translate_fr_prompt))
        
        title_fr_match = re.search(r'^##\s*(.+)$', content_fr, re.MULTILINE)
        title_fr = title_fr_match.group(1).strip() if title_fr_match else f"Découvrez {region} – Un Paradis Viticole en {country}"
        
        meta_fr_match = re.search(r'\*\*Meta-Description:\*\*\s*(.+)', content_fr)
        excerpt_fr = meta_fr_match.group(1).strip()[:200] if meta_fr_match else f"Découvrez la fascinante région viticole de {region} en {country}. Histoire, terroir, cépages et les meilleurs vins."
        
        # Slug erstellen
        slug = re.sub(r'[^a-z0-9]+', '-', region.lower())
        slug = f"weinregion-{slug}"
        
        # Bild-URL (Unsplash Weinberg)
        image_keywords = {
            "Frankreich": "french-vineyard",
            "Italien": "italian-vineyard-tuscany",
            "Spanien": "spanish-vineyard-rioja",
            "Deutschland": "german-vineyard-mosel",
            "Schweiz": "swiss-vineyard-alps",
            "Österreich": "austrian-vineyard",
            "USA": "napa-valley-vineyard",
            "Portugal": "portuguese-vineyard-douro",
        }
        img_keyword = image_keywords.get(country, "vineyard-wine")
        image_url = f"https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80"
        
        blog_post = {
            "id": str(uuid4()),
            "slug": slug,
            "title": title_de,
            "title_en": title_en,
            "title_fr": title_fr,
            "excerpt": excerpt_de,
            "excerpt_en": excerpt_en,
            "excerpt_fr": excerpt_fr,
            "content": content_de,
            "content_en": content_en,
            "content_fr": content_fr,
            "image_url": image_url,
            "category": "regionen",
            "tags": [region, country, "Weinregion", "Terroir"],
            "author": "VinExplorer Sommelier",
            "published": True,
            "region": region,
            "country": country,
            "auto_generated": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        
        return blog_post
        
    except Exception as e:
        print(f"  ❌ Fehler bei {region}: {e}")
        return None


async def main():
    """Hauptfunktion: Generiert Blogs für alle Prioritäts-Regionen"""
    
    mongo_url = os.environ.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME", "test_database")
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("=" * 70)
    print("🍷 AUTOMATISCHE WEINREGION-BLOG GENERIERUNG")
    print("=" * 70)
    print(f"📊 Regionen zu verarbeiten: {len(PRIORITY_REGIONS)}")
    print()
    
    # Prüfe bereits existierende Region-Blogs
    existing_slugs = await db.blog_posts.distinct("slug", {"category": "regionen"})
    print(f"📝 Bereits existierende Region-Blogs: {len(existing_slugs)}")
    
    generated = 0
    skipped = 0
    failed = 0
    
    for i, region_info in enumerate(PRIORITY_REGIONS, 1):
        region = region_info["name"]
        country = region_info["country"]
        slug = f"weinregion-{re.sub(r'[^a-z0-9]+', '-', region.lower())}"
        
        print(f"\n[{i}/{len(PRIORITY_REGIONS)}] {region} ({country})")
        
        # Prüfe ob Blog bereits existiert
        if slug in existing_slugs:
            print(f"  ⏭️  Übersprungen (existiert bereits)")
            skipped += 1
            continue
        
        # Generiere Blog
        blog_post = await generate_region_blog(region, country)
        
        if blog_post:
            await db.blog_posts.insert_one(blog_post)
            print(f"  ✅ Blog erstellt: {blog_post['title'][:50]}...")
            generated += 1
        else:
            print(f"  ❌ Fehlgeschlagen")
            failed += 1
        
        # Pause zwischen Anfragen (Rate Limiting)
        await asyncio.sleep(2)
    
    print()
    print("=" * 70)
    print(f"🎉 FERTIG!")
    print(f"   ✅ Generiert: {generated}")
    print(f"   ⏭️  Übersprungen: {skipped}")
    print(f"   ❌ Fehlgeschlagen: {failed}")
    print("=" * 70)
    
    # Aktualisierte Statistik
    total = await db.blog_posts.count_documents({})
    region_blogs = await db.blog_posts.count_documents({"category": "regionen"})
    print(f"\n📊 Blog-Statistik:")
    print(f"   Total Blogs: {total}")
    print(f"   Region-Blogs: {region_blogs}")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
