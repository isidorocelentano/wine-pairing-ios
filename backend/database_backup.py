"""
Database Backup Script
Exports all important MongoDB collections to JSON files for easy restoration
"""
import asyncio
import json
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Load environment manually
ROOT_DIR = Path(__file__).parent
env_path = ROOT_DIR / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                # Remove quotes if present
                value = value.strip('"').strip("'")
                os.environ[key] = value

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'wine_pairing_db')]

DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


async def export_collection(collection_name: str, filename: str):
    """Export a collection to JSON file"""
    try:
        docs = await db[collection_name].find({}, {"_id": 0}).to_list(10000)
        if docs:
            filepath = DATA_DIR / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(docs, f, ensure_ascii=False, indent=2, default=str)
            print(f"✅ {collection_name}: {len(docs)} Dokumente → {filename}")
            return len(docs)
        else:
            print(f"⚠️  {collection_name}: Leer (nicht exportiert)")
            return 0
    except Exception as e:
        print(f"❌ {collection_name}: Fehler - {e}")
        return 0


async def import_collection(collection_name: str, filename: str, clear_first: bool = True):
    """Import a collection from JSON file"""
    try:
        filepath = DATA_DIR / filename
        if not filepath.exists():
            print(f"⚠️  {filename} nicht gefunden")
            return 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            docs = json.load(f)
        
        if not docs:
            print(f"⚠️  {filename} ist leer")
            return 0
        
        if clear_first:
            await db[collection_name].delete_many({})
        
        await db[collection_name].insert_many(docs)
        print(f"✅ {collection_name}: {len(docs)} Dokumente importiert")
        return len(docs)
    except Exception as e:
        print(f"❌ {collection_name}: Import-Fehler - {e}")
        return 0


async def backup_all():
    """Backup all important collections"""
    print("=" * 60)
    print("🗄️  DATENBANK-BACKUP ERSTELLEN")
    print("=" * 60)
    print(f"📁 Zielverzeichnis: {DATA_DIR}")
    print()
    
    # List all collections
    collections = await db.list_collection_names()
    print(f"📋 Gefundene Collections: {collections}")
    print()
    
    total = 0
    
    # Export each important collection
    exports = [
        ("grape_varieties", "grape_varieties.json"),
        ("regional_pairings", "regional_pairings.json"),
        ("blog_posts", "blog_posts.json"),
        ("dishes", "dishes.json"),
        ("wine_database", "wine_database.json"),
        ("public_wines", "public_wines.json"),
        ("feed_posts", "feed_posts.json"),
    ]
    
    for coll_name, filename in exports:
        if coll_name in collections:
            count = await export_collection(coll_name, filename)
            total += count
    
    print()
    print("=" * 60)
    print(f"🎉 BACKUP FERTIG! {total} Dokumente exportiert")
    print("=" * 60)
    
    # List created files
    print("\n📁 Erstellte Backup-Dateien:")
    for f in sorted(DATA_DIR.glob("*.json")):
        size = f.stat().st_size / 1024
        print(f"   {f.name}: {size:.1f} KB")


async def restore_all():
    """Restore all collections from JSON backups"""
    print("=" * 60)
    print("🔄 DATENBANK-WIEDERHERSTELLUNG")
    print("=" * 60)
    print(f"📁 Quellverzeichnis: {DATA_DIR}")
    print()
    
    total = 0
    
    # Import each collection
    imports = [
        ("grape_varieties", "grape_varieties.json"),
        ("regional_pairings", "regional_pairings.json"),
        ("blog_posts", "blog_posts.json"),
        ("dishes", "dishes.json"),
        ("wine_database", "wine_database.json"),
        ("public_wines", "public_wines.json"),
        ("feed_posts", "feed_posts.json"),
    ]
    
    for coll_name, filename in imports:
        filepath = DATA_DIR / filename
        if filepath.exists():
            count = await import_collection(coll_name, filename)
            total += count
    
    print()
    print("=" * 60)
    print(f"🎉 WIEDERHERSTELLUNG FERTIG! {total} Dokumente importiert")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        asyncio.run(restore_all())
    else:
        asyncio.run(backup_all())
