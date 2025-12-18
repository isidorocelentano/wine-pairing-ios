#!/usr/bin/env python3
"""
Update ALL grape varieties with high-quality wine images.
Uses diverse, beautiful Unsplash images for each wine type.
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import random

# High-quality, diverse wine images from Unsplash
WINE_IMAGES = {
    "rot": [
        # Red wine glasses and bottles
        "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800&q=80",  # Red wine glass elegant
        "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=800&q=80",  # Red wine pouring
        "https://images.unsplash.com/photo-1586370434639-0fe43b2d32e6?w=800&q=80",  # Red wine bottle
        "https://images.unsplash.com/photo-1567696911980-2eed69a46042?w=800&q=80",  # Red wine glass dark
        "https://images.unsplash.com/photo-1474722883778-792e7990302f?w=800&q=80",  # Red grapes vineyard
        "https://images.unsplash.com/photo-1560148271-00b5e5850812?w=800&q=80",  # Red wine tasting
        "https://images.unsplash.com/photo-1598306442928-4d90f32c6866?w=800&q=80",  # Red wine bottle elegant
        "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800&q=80",  # Wine glass sunset
        "https://images.unsplash.com/photo-1423483641154-5411ec9c0ddf?w=800&q=80",  # Red wine decanting
        "https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=800&q=80",  # Wine cellar red
        "https://images.unsplash.com/photo-1516594915307-8f71bcaed47e?w=800&q=80",  # Red wine romantic
        "https://images.unsplash.com/photo-1566754436522-64a8d07a1c4d?w=800&q=80",  # Red wine barrel
        "https://images.unsplash.com/photo-1568213816046-0ee1c42bd559?w=800&q=80",  # Red wine glass close
        "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800&q=80",  # Wine glass light
        "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=800&q=80",  # Wine abstract
    ],
    "weiss": [
        # White wine glasses and bottles
        "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800&q=80",  # White wine glass
        "https://images.unsplash.com/photo-1566995541428-f2246c17cda1?w=800&q=80",  # White wine elegant
        "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800&q=80",  # White wine pouring
        "https://images.unsplash.com/photo-1507434965515-61970f2bd7c6?w=800&q=80",  # White grapes
        "https://images.unsplash.com/photo-1569919659476-f0852f6834b7?w=800&q=80",  # White wine bottle
        "https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=800&q=80",  # White wine glass side
        "https://images.unsplash.com/photo-1560148218-1a83060f7b32?w=800&q=80",  # White wine outdoor
        "https://images.unsplash.com/photo-1584916201218-f4242ceb4809?w=800&q=80",  # Wine setting
        "https://images.unsplash.com/photo-1561461056-77634126673a?w=800&q=80",  # Chardonnay
        "https://images.unsplash.com/photo-1585553616435-2dc0a54e271d?w=800&q=80",  # White wine cellar
        "https://images.unsplash.com/photo-1528823872057-9c018a7a7553?w=800&q=80",  # Wine tasting white
        "https://images.unsplash.com/photo-1471253794676-0f039a6aae9d?w=800&q=80",  # Wine glasses white
        "https://images.unsplash.com/photo-1486947799489-3fabdd7d32a6?w=800&q=80",  # White wine bright
        "https://images.unsplash.com/photo-1544776193-52a2d4a3cf9d?w=800&q=80",  # Wine glass light
        "https://images.unsplash.com/photo-1559620192-032c4bc4674e?w=800&q=80",  # Wine picnic
    ],
    "rosé": [
        # Rosé wine
        "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80",  # Rosé wine glass
        "https://images.unsplash.com/photo-1560148218-1a83060f7b32?w=800&q=80",  # Rosé elegant
        "https://images.unsplash.com/photo-1573062337052-54ad71b70402?w=800&q=80",  # Rosé bottle
        "https://images.unsplash.com/photo-1516594915307-8f71bcaed47e?w=800&q=80",  # Rosé summer
        "https://images.unsplash.com/photo-1544776193-52a2d4a3cf9d?w=800&q=80",  # Rosé glass light
        "https://images.unsplash.com/photo-1598306442928-4d90f32c6866?w=800&q=80",  # Rosé bottle elegant
        "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=800&q=80",  # Wine pouring pink
        "https://images.unsplash.com/photo-1571613316887-6f8d5cbf7ef7?w=800&q=80",  # Rosé outdoor
        "https://images.unsplash.com/photo-1559620192-032c4bc4674e?w=800&q=80",  # Wine picnic rosé
        "https://images.unsplash.com/photo-1528823872057-9c018a7a7553?w=800&q=80",  # Wine tasting rosé
    ],
    "schaumwein": [
        # Sparkling wine / Champagne
        "https://images.unsplash.com/photo-1549918864-48ac978761a4?w=800&q=80",  # Champagne glasses
        "https://images.unsplash.com/photo-1578911373434-0cb395d2cbfb?w=800&q=80",  # Sparkling wine
        "https://images.unsplash.com/photo-1548690596-f1722c190938?w=800&q=80",  # Champagne bottle
        "https://images.unsplash.com/photo-1546171753-97d7676e4602?w=800&q=80",  # Prosecco
        "https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=800&q=80",  # Sparkling celebration
        "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=800&q=80",  # Champagne toast
        "https://images.unsplash.com/photo-1503095396549-807759245b35?w=800&q=80",  # Champagne bubbles
        "https://images.unsplash.com/photo-1559620192-032c4bc4674e?w=800&q=80",  # Celebration
        "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&q=80",  # Sparkling elegance
        "https://images.unsplash.com/photo-1570598912132-0ba1dc952b7d?w=800&q=80",  # Champagne pour
    ],
}


def get_wine_type(grape):
    """Determine wine type from color or type field"""
    color = (grape.get('color') or grape.get('type') or '').lower()
    
    if 'rot' in color or 'red' in color:
        return 'rot'
    elif 'weiß' in color or 'weiss' in color or 'white' in color:
        return 'weiss'
    elif 'rosé' in color or 'rose' in color or 'pink' in color:
        return 'rosé'
    elif 'schaum' in color or 'spark' in color or 'champagne' in color or 'sekt' in color:
        return 'schaumwein'
    else:
        # Default based on common grape names
        name = grape.get('name', '').lower()
        red_grapes = ['cabernet', 'merlot', 'pinot noir', 'syrah', 'shiraz', 'tempranillo', 
                      'sangiovese', 'nebbiolo', 'grenache', 'malbec', 'zinfandel']
        if any(rg in name for rg in red_grapes):
            return 'rot'
        return 'weiss'  # Default to white


async def update_all_images():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client['test_database']
    
    # Get all grapes
    grapes = await db.grape_varieties.find({}).to_list(500)
    
    print(f"🍇 Aktualisiere ALLE {len(grapes)} Rebsorten mit neuen Bildern...")
    
    # Track usage to ensure variety
    counters = {k: 0 for k in WINE_IMAGES.keys()}
    by_type = {"rot": 0, "weiss": 0, "rosé": 0, "schaumwein": 0}
    
    for grape in grapes:
        wine_type = get_wine_type(grape)
        images = WINE_IMAGES.get(wine_type, WINE_IMAGES['weiss'])
        
        # Rotate through images to distribute evenly
        idx = counters.get(wine_type, 0) % len(images)
        image_url = images[idx]
        counters[wine_type] = counters.get(wine_type, 0) + 1
        by_type[wine_type] = by_type.get(wine_type, 0) + 1
        
        # Update database
        await db.grape_varieties.update_one(
            {"_id": grape["_id"]},
            {"$set": {"image_url": image_url}}
        )
    
    print(f"\n✅ {len(grapes)} Rebsorten aktualisiert:")
    for wine_type, count in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"   🍷 {wine_type}: {count} Rebsorten")
    
    # Verify
    print(f"\n📊 Verifizierung:")
    with_image = await db.grape_varieties.count_documents({"image_url": {"$exists": True, "$ne": None, "$ne": ""}})
    print(f"   Rebsorten mit Bild: {with_image}/{len(grapes)}")


if __name__ == "__main__":
    asyncio.run(update_all_images())
