#!/usr/bin/env python3
"""
🍷 Automatische Blog-Generierung für Weinregionen V2
Erstellt hochwertige, SEO-optimierte Blog-Beiträge mit 10 FAQ und Übersetzungen
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

# Weinbilder von Unsplash nach Region/Land
WINE_IMAGES = {
    # Frankreich
    "Châteauneuf-du-Pape": "https://images.unsplash.com/photo-1566903451935-7e8835ed3e97?w=1200",
    "Bordeaux": "https://images.unsplash.com/photo-1597916829826-02e5bb4a54a0?w=1200",
    "Burgund": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200",
    "Champagne": "https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=1200",
    "Elsass": "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=1200",
    "Loire": "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=1200",
    "Rhône": "https://images.unsplash.com/photo-1566903451935-7e8835ed3e97?w=1200",
    "Provence": "https://images.unsplash.com/photo-1523741543316-beb7fc7023d8?w=1200",
    # Italien
    "Toskana": "https://images.unsplash.com/photo-1523528283115-9bf9b1699245?w=1200",
    "Piemont": "https://images.unsplash.com/photo-1552751753-d0c8f1f5c5cc?w=1200",
    "Venetien": "https://images.unsplash.com/photo-1534531173927-aeb928d54385?w=1200",
    "Sizilien": "https://images.unsplash.com/photo-1498579809087-ef1e558fd1da?w=1200",
    "Südtirol": "https://images.unsplash.com/photo-1566903451935-7e8835ed3e97?w=1200",
    # Spanien
    "Rioja": "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=1200",
    "Ribera del Duero": "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=1200",
    "Priorat": "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=1200",
    "Jerez": "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=1200",
    # Deutschland
    "Mosel": "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=1200",
    "Rheingau": "https://images.unsplash.com/photo-1566903451935-7e8835ed3e97?w=1200",
    "Pfalz": "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=1200",
    "Franken": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200",
    "Baden": "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=1200",
    "Nahe": "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=1200",
    "Ahr": "https://images.unsplash.com/photo-1566903451935-7e8835ed3e97?w=1200",
    # Schweiz
    "Wallis": "https://images.unsplash.com/photo-1464638681273-0962e9b53566?w=1200",
    "Waadt": "https://images.unsplash.com/photo-1523528283115-9bf9b1699245?w=1200",
    "Genf": "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=1200",
    "Tessin": "https://images.unsplash.com/photo-1534531173927-aeb928d54385?w=1200",
    "Graubünden": "https://images.unsplash.com/photo-1464638681273-0962e9b53566?w=1200",
    # Österreich
    "Wachau": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200",
    "Burgenland": "https://images.unsplash.com/photo-1566903451935-7e8835ed3e97?w=1200",
    "Steiermark": "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=1200",
    # Neue Welt
    "Napa Valley": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1200",
    "Sonoma": "https://images.unsplash.com/photo-1474722883778-792e7990302f?w=1200",
    "Mendoza": "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=1200",
    "Barossa Valley": "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=1200",
    "Marlborough": "https://images.unsplash.com/photo-1523528283115-9bf9b1699245?w=1200",
    "Stellenbosch": "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=1200",
    "Douro": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200",
    "Alentejo": "https://images.unsplash.com/photo-1566903451935-7e8835ed3e97?w=1200",
    "Tokaj": "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=1200",
}
DEFAULT_IMAGE = "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=1200"

# Regionen die noch verarbeitet werden müssen
REMAINING_REGIONS = [
    # Spanien (fehlend)
    {"name": "Rioja", "country": "Spanien", "type": "region"},
    {"name": "Ribera del Duero", "country": "Spanien", "type": "region"},
    {"name": "Priorat", "country": "Spanien", "type": "region"},
    {"name": "Jerez", "country": "Spanien", "type": "region"},
    
    # Deutschland (fehlend)
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

# Der detaillierte Prompt nach Ihren Vorgaben
DETAILED_BLOG_PROMPT = """Du bist ein leidenschaftlicher Wein-Journalist, Master of Wine und Terroir-Experte. Erstelle einen hochwertigen, emotionalen und SEO-optimierten Blog-Beitrag über die Weinregion "{region}" in {country}.

🎯 ZIELGRUPPE & TONALITÄT:
- Zielgruppe: Anspruchsvolle Weinliebhaber, Geniesser, Sommeliers in Ausbildung
- Tonalität: Emotional, leidenschaftlich, inspirierend, respektvoll gegenüber der Tradition
- Der Text soll ein Gefühl von Sehnsucht und Exklusivität vermitteln

📝 STRUKTUR (BITTE EXAKT EINHALTEN):

## [Emotionaler, klickstarker Titel mit Region und zentralem Gefühl]

**Meta-Description:** [Max 155 Zeichen, verlockend mit Keywords]

**Keywords:** {region}, [weitere relevante Keywords zur Region]

---

### Einleitung: Der erste Schluck Ewigkeit

[Sinnliche Beschreibung mit Geruch, Geschmack, Visuellem - versetze den Leser in die Region. Stelle die Region als Mythos und Legende vor. Gib einen Ausblick auf Geschichte, Böden, Rebsorten.]

---

### Das Unverwechselbare Terroir und Klima

**Der Boden:**
[Erkläre die Bodentypen der Region und ihre Auswirkung auf den Wein. Was macht sie einzigartig?]

**Das Klima:**
[Beschreibe Sonnenstunden, Niederschlag, Wind, Temperaturunterschiede und deren Einfluss auf die Trauben.]

---

### Die Rebsorten: Das Herzstück der Region

**Die Hauptakteure:**
[Detaillierte Darstellung der wichtigsten Rebsorten mit ihren Charakteristiken]

**Die weißen/roten Sorten:**
[Weitere wichtige Rebsorten der Region]

---

### Geschichte & Tradition

[Historischer Kontext: Wie entstand die Weinkultur in dieser Region? Wichtige Persönlichkeiten, Ereignisse, Klassifikationen. Was macht die Region historisch bedeutsam?]

---

### Genuss & Perfekte Kombinationen

**Sensorische Beschreibung:**
[Typische Aromen, Geschmacksprofile, Mundgefühl der Weine]

**Food-Pairing:**
[Anspruchsvolle Vorschläge für Speisenkombinationen, regionale Küche]

---

### FAQ – Die 10 wichtigsten Fragen zu {region}

**1. Was macht {region} Weine so besonders?**
[Prägnante, faktische Antwort in 2-3 Sätzen]

**2. Welche Rebsorten dominieren in {region}?**
[Prägnante Antwort]

**3. Wie schmeckt ein typischer {region} Wein?**
[Aromaprofil beschreiben]

**4. Wie lange sollte man {region} Weine lagern?**
[Lagerempfehlung]

**5. Welche Speisen passen zu {region} Weinen?**
[Food-Pairing Empfehlungen]

**6. Was ist das Besondere am Terroir von {region}?**
[Boden und Klima]

**7. Welche Weingüter in {region} sind besonders empfehlenswert?**
[3-5 bekannte Produzenten nennen]

**8. Was kostet ein guter {region} Wein?**
[Preiskategorien: Einstieg, Mittel, Premium]

**9. Wann ist die beste Zeit für einen Besuch in {region}?**
[Reiseempfehlung]

**10. Welche Alternativen gibt es zu {region} Weinen?**
[Ähnliche Regionen oder Stile]

---

### Fazit: Ein Wein, der die Seele berührt

[Emotionaler Abschluss mit Call-to-Action: Ermutigung eine Flasche zu entkorken und die Geschichte zu erleben]

---

WICHTIGE ANWEISUNGEN:
- Länge: 1200-1500 Wörter
- Schreibe auf Deutsch
- Verwende die Keywords natürlich im Text
- Mache den Text SEO-optimiert für Featured Snippets
- Füge authentische, recherchierte Fakten ein
- Antworte NUR mit dem Blog-Text, keine zusätzlichen Erklärungen"""


async def generate_region_blog_v2(region: str, country: str) -> Optional[Dict]:
    """Generiert einen dreisprachigen Blog-Beitrag mit dem detaillierten Prompt"""
    
    try:
        print(f"  📝 Generiere deutschen Blog für {region}...")
        
        # Deutscher Blog mit detailliertem Prompt
        chat_de = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=str(uuid4()),
            system_message="Du bist ein erfahrener Wein-Journalist und Master of Wine. Schreibe leidenschaftlich und faktenbasiert auf Deutsch."
        ).with_model("openai", "gpt-5.1")
        
        prompt_de = DETAILED_BLOG_PROMPT.format(region=region, country=country)
        content_de = await chat_de.send_message(UserMessage(text=prompt_de))
        
        # Extrahiere Titel
        title_match = re.search(r'^##\s*(.+)$', content_de, re.MULTILINE)
        title_de = title_match.group(1).strip() if title_match else f"{region} – Ein Weinparadies in {country}"
        
        # Meta-Description
        meta_match = re.search(r'\*\*Meta-Description:\*\*\s*(.+)', content_de)
        excerpt_de = meta_match.group(1).strip()[:200] if meta_match else f"Entdecken Sie {region} in {country}. Geschichte, Terroir, Rebsorten und die besten Weine der Region."
        
        print(f"  🇬🇧 Generiere englische Übersetzung...")
        
        # Englische Übersetzung
        chat_en = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=str(uuid4()),
            system_message="You are a professional wine journalist. Translate to English while keeping the emotional, passionate tone and all formatting (##, ###, **bold**)."
        ).with_model("openai", "gpt-5.1")
        
        content_en = await chat_en.send_message(UserMessage(text=f"Translate this German wine blog post to English. Keep all Markdown formatting:\n\n{content_de}"))
        
        title_en_match = re.search(r'^##\s*(.+)$', content_en, re.MULTILINE)
        title_en = title_en_match.group(1).strip() if title_en_match else f"{region} – A Wine Paradise in {country}"
        
        meta_en_match = re.search(r'\*\*Meta-Description:\*\*\s*(.+)', content_en)
        excerpt_en = meta_en_match.group(1).strip()[:200] if meta_en_match else f"Discover {region} in {country}. History, terroir, grape varieties and the best wines."
        
        print(f"  🇫🇷 Generiere französische Übersetzung...")
        
        # Französische Übersetzung
        chat_fr = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=str(uuid4()),
            system_message="Vous êtes un journaliste vinicole professionnel. Traduisez en français en gardant le ton émotionnel et passionné ainsi que tout le formatage (##, ###, **gras**)."
        ).with_model("openai", "gpt-5.1")
        
        content_fr = await chat_fr.send_message(UserMessage(text=f"Traduisez ce blog sur le vin en français. Gardez tout le formatage Markdown:\n\n{content_de}"))
        
        title_fr_match = re.search(r'^##\s*(.+)$', content_fr, re.MULTILINE)
        title_fr = title_fr_match.group(1).strip() if title_fr_match else f"{region} – Un Paradis Viticole en {country}"
        
        meta_fr_match = re.search(r'\*\*Meta-Description:\*\*\s*(.+)', content_fr)
        excerpt_fr = meta_fr_match.group(1).strip()[:200] if meta_fr_match else f"Découvrez {region} en {country}. Histoire, terroir, cépages et les meilleurs vins."
        
        # Slug erstellen
        slug = re.sub(r'[^a-z0-9]+', '-', region.lower())
        slug = f"weinregion-{slug}"
        
        # Bild auswählen
        image_url = WINE_IMAGES.get(region, DEFAULT_IMAGE)
        
        # Keywords extrahieren
        keywords_match = re.search(r'\*\*Keywords:\*\*\s*(.+)', content_de)
        tags = [region, country, "Weinregion", "Terroir"]
        if keywords_match:
            extra_tags = [t.strip() for t in keywords_match.group(1).split(',')][:5]
            tags.extend(extra_tags)
        
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
            "tags": tags,
            "author": "VinExplorer Sommelier",
            "published": True,
            "region": region,
            "country": country,
            "auto_generated": True,
            "version": "v2",  # Markierung für den neuen Prompt
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        
        return blog_post
        
    except Exception as e:
        print(f"  ❌ Fehler bei {region}: {e}")
        return None


async def main():
    """Hauptfunktion: Generiert Blogs für verbleibende Regionen"""
    
    mongo_url = os.environ.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME", "test_database")
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("=" * 70)
    print("🍷 WEINREGION-BLOG GENERIERUNG V2 (Detaillierter Prompt)")
    print("=" * 70)
    print(f"📊 Regionen zu verarbeiten: {len(REMAINING_REGIONS)}")
    print()
    
    # Prüfe bereits existierende Region-Blogs
    existing_slugs = await db.blog_posts.distinct("slug", {"category": "regionen"})
    print(f"📝 Bereits existierende Region-Blogs: {len(existing_slugs)}")
    
    generated = 0
    skipped = 0
    failed = 0
    
    for i, region_info in enumerate(REMAINING_REGIONS, 1):
        region = region_info["name"]
        country = region_info["country"]
        slug = f"weinregion-{re.sub(r'[^a-z0-9]+', '-', region.lower())}"
        
        print(f"\n[{i}/{len(REMAINING_REGIONS)}] {region} ({country})")
        
        # Prüfe ob Blog bereits existiert
        if slug in existing_slugs:
            print(f"  ⏭️  Übersprungen (existiert bereits)")
            skipped += 1
            continue
        
        # Generiere Blog
        blog_post = await generate_region_blog_v2(region, country)
        
        if blog_post:
            await db.blog_posts.insert_one(blog_post)
            print(f"  ✅ Blog erstellt: {blog_post['title'][:50]}...")
            generated += 1
            
            # Backup alle 5 Blogs
            if generated % 5 == 0:
                print(f"\n  💾 Zwischenbackup nach {generated} Blogs...")
        else:
            print(f"  ❌ Fehlgeschlagen")
            failed += 1
        
        # Pause zwischen Anfragen
        await asyncio.sleep(2)
    
    print()
    print("=" * 70)
    print(f"🎉 FERTIG!")
    print(f"   ✅ Generiert: {generated}")
    print(f"   ⏭️  Übersprungen: {skipped}")
    print(f"   ❌ Fehlgeschlagen: {failed}")
    print("=" * 70)
    
    # Statistik
    total = await db.blog_posts.count_documents({})
    region_blogs = await db.blog_posts.count_documents({"category": "regionen"})
    print(f"\n📊 Blog-Statistik:")
    print(f"   Total Blogs: {total}")
    print(f"   Region-Blogs: {region_blogs}")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
