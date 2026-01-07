#!/usr/bin/env python3
"""
Aktualisiert die AGENT_HANDOFF.md mit aktuellen Datenbank-Statistiken.
Sollte vor jedem Fork/Deployment ausgeführt werden.

Verwendung:
    python3 /app/backend/scripts/update_handoff_stats.py
"""

import asyncio
import os
from datetime import datetime, timezone
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import re

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

COLLECTIONS = [
    ('public_wines', 'Öffentliche Wein-Datenbank (wächst dynamisch)'),
    ('wine_database', 'Erweiterte Wein-Infos'),
    ('grape_varieties', 'Rebsorten-Lexikon'),
    ('regional_pairings', 'Sommelier Kompass'),
    ('blog_posts', 'Blog-Artikel'),
    ('feed_posts', 'Community-Beiträge'),
    ('dishes', 'Gerichte für Pairing'),
    ('seo_pairings', 'SEO-optimierte Pairings'),
    ('users', 'Benutzerkonten'),
    ('wines', 'Persönliche Weinkeller (user_id!)'),
    ('coupons', 'Gutscheine'),
]

async def get_stats():
    """Hole aktuelle Statistiken aus der Datenbank"""
    client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
    db = client[os.environ.get('DB_NAME')]
    
    stats = {}
    total = 0
    
    for coll_name, desc in COLLECTIONS:
        count = await db[coll_name].count_documents({})
        stats[coll_name] = {'count': count, 'description': desc}
        total += count
    
    stats['_total'] = total
    client.close()
    return stats

def update_handoff_file(stats):
    """Aktualisiere AGENT_HANDOFF.md mit neuen Statistiken"""
    handoff_path = Path("/app/AGENT_HANDOFF.md")
    
    if not handoff_path.exists():
        print("❌ AGENT_HANDOFF.md nicht gefunden!")
        return False
    
    with open(handoff_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Erstelle neue Tabelle
    table_lines = ["| Collection | Anzahl | Beschreibung |", "|------------|--------|--------------|"]
    for coll_name, desc in COLLECTIONS:
        count = stats[coll_name]['count']
        # Formatiere Anzahl mit Tilde für variable Werte
        if coll_name in ['users', 'wines']:
            count_str = f"~{count}"
        else:
            count_str = f"{count:,}"
        table_lines.append(f"| `{coll_name}` | {count_str} | {desc} |")
    
    table_lines.append(f"| **GESAMT** | **~{stats['_total']:,}** | |")
    new_table = "\n".join(table_lines)
    
    # Ersetze alte Tabelle
    pattern = r'\| Collection \| Anzahl \| Beschreibung \|.*?\| \*\*GESAMT\*\* \|[^\n]*\|'
    content = re.sub(pattern, new_table, content, flags=re.DOTALL)
    
    # Aktualisiere Datum
    now = datetime.now(timezone.utc).strftime('%d.%m.%Y %H:%M UTC')
    content = re.sub(
        r'\*Letzte Aktualisierung:.*\*',
        f'*Letzte Aktualisierung: {now}*',
        content
    )
    
    # Aktualisiere Stand-Datum im Header
    today = datetime.now(timezone.utc).strftime('%d.%m.%Y')
    content = re.sub(
        r'## 📊 AKTUELLER STAND \([^)]+\)',
        f'## 📊 AKTUELLER STAND ({today})',
        content
    )
    
    with open(handoff_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

async def main():
    print("🔄 AKTUALISIERE AGENT HANDOFF STATISTIKEN")
    print("=" * 50)
    
    # Hole Statistiken
    print("\n📊 Hole Datenbank-Statistiken...")
    stats = await get_stats()
    
    # Zeige Statistiken
    print("\nAktuelle Werte:")
    for coll_name, desc in COLLECTIONS:
        count = stats[coll_name]['count']
        print(f"   {coll_name}: {count:,}")
    print(f"\n   GESAMT: {stats['_total']:,}")
    
    # Aktualisiere Datei
    print("\n📝 Aktualisiere AGENT_HANDOFF.md...")
    if update_handoff_file(stats):
        print("✅ AGENT_HANDOFF.md erfolgreich aktualisiert!")
    else:
        print("❌ Fehler beim Aktualisieren!")
    
    # Aktualisiere auch die Dokumentation
    doc_path = Path("/app/docs/APP_DOKUMENTATION_KOMPLETT.md")
    if doc_path.exists():
        print("\n📝 Aktualisiere APP_DOKUMENTATION_KOMPLETT.md...")
        with open(doc_path, 'r', encoding='utf-8') as f:
            doc_content = f.read()
        
        # Update Weine
        doc_content = re.sub(r'\| `public_wines` \| [\d,]+ \|', f'| `public_wines` | {stats["public_wines"]["count"]:,} |', doc_content)
        doc_content = re.sub(r'\| `grape_varieties` \| [\d,]+ \|', f'| `grape_varieties` | {stats["grape_varieties"]["count"]:,} |', doc_content)
        
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        print("✅ Dokumentation aktualisiert!")
    
    print("\n" + "=" * 50)
    print("✅ FERTIG!")

if __name__ == '__main__':
    asyncio.run(main())
