#!/usr/bin/env python3
"""
🍷 Blog-Generierung für fehlende Weinregionen aus der Datenbank
"""

import asyncio
import os
import re
from uuid import uuid4
from datetime import datetime, timezone
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient

env_path = Path('/app/backend/.env')
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value.strip('"').strip("'")

from emergentintegrations.llm.chat import LlmChat, UserMessage

EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY")

# Wichtige fehlende Regionen (nach Weinanzahl und Bedeutung sortiert)
MISSING_REGIONS = [
    # Italien - Klassiker
    {"name": "Barolo", "country": "Italien"},
    {"name": "Barbaresco", "country": "Italien"},
    {"name": "Brunello di Montalcino", "country": "Italien"},
    {"name": "Chianti Classico", "country": "Italien"},
    {"name": "Bolgheri", "country": "Italien"},
    {"name": "Langhe", "country": "Italien"},
    {"name": "Trentino", "country": "Italien"},
    
    # Frankreich - Bordeaux Appellationen
    {"name": "Saint-Émilion", "country": "Frankreich"},
    {"name": "Pauillac", "country": "Frankreich"},
    {"name": "Pomerol", "country": "Frankreich"},
    {"name": "Pessac-Léognan", "country": "Frankreich"},
    {"name": "Saint-Julien", "country": "Frankreich"},
    {"name": "Saint-Estèphe", "country": "Frankreich"},
    {"name": "Margaux", "country": "Frankreich"},
    {"name": "Sauternes", "country": "Frankreich"},
    
    # Spanien
    {"name": "Toro", "country": "Spanien"},
    {"name": "Rías Baixas", "country": "Spanien"},
    {"name": "Penedès", "country": "Spanien"},
    {"name": "Rioja Alavesa", "country": "Spanien"},
    {"name": "Rueda", "country": "Spanien"},
    {"name": "Bierzo", "country": "Spanien"},
    {"name": "Montsant", "country": "Spanien"},
    {"name": "Ribeira Sacra", "country": "Spanien"},
    
    # Deutschland
    {"name": "Rheinhessen", "country": "Deutschland"},
    
    # Neue Welt
    {"name": "Eden Valley", "country": "Australien"},
    {"name": "Kalifornien", "country": "USA"},
]

WINE_IMAGES = {
    "Barolo": "https://images.unsplash.com/photo-1552751753-d0c8f1f5cc5cc?w=1200",
    "Barbaresco": "https://images.unsplash.com/photo-1552751753-d0c8f1f5cc5cc?w=1200",
    "Brunello di Montalcino": "https://images.unsplash.com/photo-1523528283115-9bf9b1699245?w=1200",
    "Chianti Classico": "https://images.unsplash.com/photo-1523528283115-9bf9b1699245?w=1200",
    "Bolgheri": "https://images.unsplash.com/photo-1498579809087-ef1e558fd1da?w=1200",
    "Langhe": "https://images.unsplash.com/photo-1552751753-d0c8f1f5cc5cc?w=1200",
    "Trentino": "https://images.unsplash.com/photo-1566903451935-7e8835ed3e97?w=1200",
    "Saint-Émilion": "https://images.unsplash.com/photo-1597916829826-02e5bb4a54a0?w=1200",
    "Pauillac": "https://images.unsplash.com/photo-1597916829826-02e5bb4a54a0?w=1200",
    "Pomerol": "https://images.unsplash.com/photo-1597916829826-02e5bb4a54a0?w=1200",
    "Pessac-Léognan": "https://images.unsplash.com/photo-1597916829826-02e5bb4a54a0?w=1200",
    "Saint-Julien": "https://images.unsplash.com/photo-1597916829826-02e5bb4a54a0?w=1200",
    "Saint-Estèphe": "https://images.unsplash.com/photo-1597916829826-02e5bb4a54a0?w=1200",
    "Margaux": "https://images.unsplash.com/photo-1597916829826-02e5bb4a54a0?w=1200",
    "Sauternes": "https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=1200",
    "Toro": "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=1200",
    "Rías Baixas": "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=1200",
    "Penedès": "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=1200",
    "Rioja Alavesa": "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=1200",
    "Rueda": "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=1200",
    "Bierzo": "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=1200",
    "Montsant": "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=1200",
    "Ribeira Sacra": "https://images.unsplash.com/photo-1566903451935-7e8835ed3e97?w=1200",
    "Rheinhessen": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200",
    "Eden Valley": "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=1200",
    "Kalifornien": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1200",
}

DETAILED_BLOG_PROMPT = """Du bist ein leidenschaftlicher Wein-Journalist, Master of Wine und Terroir-Experte. Erstelle einen hochwertigen, emotionalen und SEO-optimierten Blog-Beitrag über die Weinregion/Appellation "{region}" in {country}.

🎯 ZIELGRUPPE & TONALITÄT:
- Zielgruppe: Anspruchsvolle Weinliebhaber, Geniesser, Sommeliers
- Tonalität: Emotional, leidenschaftlich, inspirierend
- Der Text soll ein Gefühl von Sehnsucht und Exklusivität vermitteln

📝 STRUKTUR:

## [Emotionaler, klickstarker Titel mit Region]

**Meta-Description:** [Max 155 Zeichen, verlockend mit Keywords]

**Keywords:** {region}, [weitere relevante Keywords]

---

### Einleitung: Der erste Schluck Ewigkeit
[Sinnliche Beschreibung - versetze den Leser in die Region]

---

### Das Unverwechselbare Terroir und Klima
**Der Boden:** [Bodentypen und Auswirkung]
**Das Klima:** [Klimaeinflüsse]

---

### Die Rebsorten: Das Herzstück der Region
[Hauptrebsorten mit Charakteristiken]

---

### Geschichte & Tradition
[Historischer Kontext, wichtige Ereignisse]

---

### Genuss & Perfekte Kombinationen
**Sensorische Beschreibung:** [Aromen, Geschmack]
**Food-Pairing:** [Speisenkombinationen]

---

### FAQ – Die 10 wichtigsten Fragen zu {region}

**1. Was macht {region} Weine so besonders?**
[Antwort]

**2. Welche Rebsorten dominieren in {region}?**
[Antwort]

**3. Wie schmeckt ein typischer {region} Wein?**
[Antwort]

**4. Wie lange sollte man {region} Weine lagern?**
[Antwort]

**5. Welche Speisen passen zu {region} Weinen?**
[Antwort]

**6. Was ist das Besondere am Terroir von {region}?**
[Antwort]

**7. Welche Weingüter in {region} sind besonders empfehlenswert?**
[Antwort]

**8. Was kostet ein guter {region} Wein?**
[Antwort]

**9. Wann ist die beste Zeit für einen Besuch in {region}?**
[Antwort]

**10. Welche Alternativen gibt es zu {region} Weinen?**
[Antwort]

---

### Fazit: Ein Wein, der die Seele berührt
[Emotionaler Abschluss]

---

Länge: 1200-1500 Wörter. Antworte NUR mit dem Blog-Text."""

async def generate_blog(region, country):
    try:
        print(f"  📝 DE...")
        chat_de = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=str(uuid4()),
            system_message="Du bist ein erfahrener Wein-Journalist.").with_model("openai", "gpt-5.1")
        content_de = await chat_de.send_message(UserMessage(text=DETAILED_BLOG_PROMPT.format(region=region, country=country)))
        
        title_match = re.search(r'^##\s*(.+)$', content_de, re.MULTILINE)
        title_de = title_match.group(1).strip() if title_match else f"{region} – Weinparadies in {country}"
        meta_match = re.search(r'\*\*Meta-Description:\*\*\s*(.+)', content_de)
        excerpt_de = meta_match.group(1).strip()[:200] if meta_match else f"Entdecken Sie {region} in {country}."
        
        print(f"  🇬🇧 EN...")
        chat_en = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=str(uuid4()),
            system_message="Translate to English, keep formatting.").with_model("openai", "gpt-5.1")
        content_en = await chat_en.send_message(UserMessage(text=f"Translate to English:\n\n{content_de}"))
        title_en_match = re.search(r'^##\s*(.+)$', content_en, re.MULTILINE)
        title_en = title_en_match.group(1).strip() if title_en_match else f"{region} – Wine Paradise"
        meta_en_match = re.search(r'\*\*Meta-Description:\*\*\s*(.+)', content_en)
        excerpt_en = meta_en_match.group(1).strip()[:200] if meta_en_match else f"Discover {region}."
        
        print(f"  🇫🇷 FR...")
        chat_fr = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=str(uuid4()),
            system_message="Traduisez en français, gardez le formatage.").with_model("openai", "gpt-5.1")
        content_fr = await chat_fr.send_message(UserMessage(text=f"Traduisez en français:\n\n{content_de}"))
        title_fr_match = re.search(r'^##\s*(.+)$', content_fr, re.MULTILINE)
        title_fr = title_fr_match.group(1).strip() if title_fr_match else f"{region} – Paradis Viticole"
        meta_fr_match = re.search(r'\*\*Meta-Description:\*\*\s*(.+)', content_fr)
        excerpt_fr = meta_fr_match.group(1).strip()[:200] if meta_fr_match else f"Découvrez {region}."
        
        return {
            "id": str(uuid4()), "slug": f"weinregion-{re.sub(r'[^a-z0-9]+', '-', region.lower())}",
            "title": title_de, "title_en": title_en, "title_fr": title_fr,
            "excerpt": excerpt_de, "excerpt_en": excerpt_en, "excerpt_fr": excerpt_fr,
            "content": content_de, "content_en": content_en, "content_fr": content_fr,
            "image_url": WINE_IMAGES.get(region, "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=1200"),
            "category": "regionen", "tags": [region, country, "Weinregion", "Terroir"],
            "author": "VinExplorer Sommelier", "published": True,
            "region": region, "country": country, "auto_generated": True, "version": "v2",
            "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc),
        }
    except Exception as e:
        print(f"  ❌ Fehler: {e}")
        return None

async def main():
    client = AsyncIOMotorClient(os.environ.get("MONGO_URL"))
    db = client[os.environ.get("DB_NAME", "test_database")]
    
    print("=" * 60)
    print("🍷 FEHLENDE DB-REGIONEN GENERIEREN")
    print("=" * 60)
    print(f"📊 Regionen: {len(MISSING_REGIONS)}")
    
    existing = await db.blog_posts.distinct('region', {'category': 'regionen'})
    
    generated = 0
    for i, r in enumerate(MISSING_REGIONS, 1):
        if r['name'] in existing:
            print(f"\n[{i}/{len(MISSING_REGIONS)}] {r['name']} ⏭️ existiert")
            continue
            
        print(f"\n[{i}/{len(MISSING_REGIONS)}] {r['name']} ({r['country']})")
        blog = await generate_blog(r['name'], r['country'])
        if blog:
            await db.blog_posts.insert_one(blog)
            print(f"  ✅ {blog['title'][:45]}...")
            generated += 1
        await asyncio.sleep(1)
    
    print("\n" + "=" * 60)
    total = await db.blog_posts.count_documents({})
    region_count = await db.blog_posts.count_documents({'category': 'regionen'})
    print(f"🎉 FERTIG! +{generated} neue Blogs")
    print(f"📊 Total: {total} Blogs, {region_count} Regionen")
    client.close()

asyncio.run(main())
