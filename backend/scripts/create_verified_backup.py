#!/usr/bin/env python3
"""
VERIFIZIERTES BACKUP-SKRIPT
============================
Erstellt ein vollständiges Backup mit Verifizierung.
Kann jederzeit manuell ausgeführt werden.

Verwendung:
    python3 /app/backend/scripts/create_verified_backup.py
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Lade Umgebungsvariablen
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

# Alle Collections die gesichert werden müssen
COLLECTIONS_TO_BACKUP = [
    # Content-Daten
    ('public_wines', 'Öffentliche Weine'),
    ('wine_database', 'Wein-Datenbank'),
    ('grape_varieties', 'Rebsorten'),
    ('regional_pairings', 'Sommelier Kompass'),
    ('blog_posts', 'Blog-Artikel'),
    ('feed_posts', 'Community Feed'),
    ('dishes', 'Gerichte'),
    ('seo_pairings', 'SEO Pairings'),
    ('coupons', 'Gutscheine'),
    # User-Daten
    ('users', 'Benutzer'),
    ('wines', 'Persönliche Weinkeller'),
    ('pairings', 'Pairing-History'),
    ('chats', 'Chat-Verläufe'),
    ('wine_favorites', 'Favoriten'),
    ('payment_transactions', 'Zahlungen'),
]

async def create_verified_backup():
    """Erstellt ein vollständiges, verifiziertes Backup."""
    
    print("=" * 60)
    print("🔐 VERIFIZIERTES BACKUP")
    print("=" * 60)
    print()
    
    # Verbinde zur Datenbank
    client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
    db = client[os.environ.get('DB_NAME')]
    
    # Erstelle Backup-Ordner
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = ROOT_DIR / 'data' / 'backups' / f'verified_backup_{timestamp}'
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Backup-Ordner: {backup_dir}")
    print()
    
    # Backup-Manifest
    manifest = {
        'created_at': datetime.now().isoformat(),
        'version': '3.1',
        'collections': {},
        'verification': 'PENDING'
    }
    
    total_docs = 0
    errors = []
    
    # Sichere jede Collection
    for collection_name, description in COLLECTIONS_TO_BACKUP:
        try:
            # Hole alle Dokumente
            docs = await db[collection_name].find({}, {'_id': 0}).to_list(None)
            count = len(docs)
            total_docs += count
            
            # Speichere als JSON
            backup_file = backup_dir / f'{collection_name}.json'
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(docs, f, ensure_ascii=False, indent=2, default=str)
            
            # Verifiziere
            with open(backup_file, 'r', encoding='utf-8') as f:
                verified_data = json.load(f)
            
            if len(verified_data) == count:
                print(f"   ✅ {collection_name}: {count:,} Dokumente ({description})")
                manifest['collections'][collection_name] = {
                    'count': count,
                    'verified': True,
                    'file': f'{collection_name}.json'
                }
            else:
                print(f"   ❌ {collection_name}: VERIFIZIERUNG FEHLGESCHLAGEN!")
                errors.append(collection_name)
                manifest['collections'][collection_name] = {
                    'count': count,
                    'verified': False,
                    'error': 'Count mismatch after save'
                }
                
        except Exception as e:
            print(f"   ❌ {collection_name}: FEHLER - {e}")
            errors.append(collection_name)
            manifest['collections'][collection_name] = {
                'count': 0,
                'verified': False,
                'error': str(e)
            }
    
    # Speichere Manifest
    manifest['total_documents'] = total_docs
    manifest['verification'] = 'SUCCESS' if not errors else 'FAILED'
    manifest['errors'] = errors
    
    manifest_file = backup_dir / 'manifest.json'
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    # Kopiere auch in Haupt-Backup-Ordner
    main_backup_dir = ROOT_DIR / 'data'
    for collection_name, _ in COLLECTIONS_TO_BACKUP:
        src = backup_dir / f'{collection_name}.json'
        dst = main_backup_dir / f'{collection_name}.json'
        if src.exists():
            with open(src, 'r', encoding='utf-8') as f:
                data = f.read()
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(data)
    
    # Zusammenfassung
    print()
    print("=" * 60)
    if not errors:
        print(f"✅ BACKUP ERFOLGREICH!")
        print(f"   Gesamt: {total_docs:,} Dokumente")
        print(f"   Ordner: {backup_dir}")
    else:
        print(f"⚠️ BACKUP MIT FEHLERN!")
        print(f"   Fehlerhafte Collections: {', '.join(errors)}")
    print("=" * 60)
    
    client.close()
    return not errors

if __name__ == '__main__':
    success = asyncio.run(create_verified_backup())
    exit(0 if success else 1)
