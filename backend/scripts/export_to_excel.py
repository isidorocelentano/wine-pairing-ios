#!/usr/bin/env python3
"""
Exportiert alle Datenbank-Collections als Excel-Dateien
"""
import asyncio
import os
from datetime import datetime
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import pandas as pd

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

COLLECTIONS = [
    'public_wines',
    'wine_database', 
    'grape_varieties',
    'regional_pairings',
    'blog_posts',
    'feed_posts',
    'dishes',
    'seo_pairings',
    'users',
    'wines',
    'coupons'
]

async def export_all():
    client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
    db = client[os.environ.get('DB_NAME')]
    
    export_dir = ROOT_DIR / 'data' / 'excel_exports'
    export_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print(f"📊 Exportiere nach: {export_dir}")
    print()
    
    for coll_name in COLLECTIONS:
        try:
            docs = await db[coll_name].find({}, {'_id': 0}).to_list(None)
            if docs:
                df = pd.DataFrame(docs)
                filename = f"{coll_name}_{timestamp}.xlsx"
                filepath = export_dir / filename
                df.to_excel(filepath, index=False)
                print(f"   ✅ {coll_name}: {len(docs)} Zeilen → {filename}")
            else:
                print(f"   ⚠️ {coll_name}: leer")
        except Exception as e:
            print(f"   ❌ {coll_name}: {e}")
    
    client.close()
    print()
    print(f"✅ Export abgeschlossen: {export_dir}")

if __name__ == '__main__':
    asyncio.run(export_all())
