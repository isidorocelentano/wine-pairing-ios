#!/usr/bin/env python3
"""
Script to add wine-specific images to grape varieties based on their color.
Uses high-quality Unsplash images for each wine type.
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import random

# High-quality wine images from Unsplash - organized by wine type
WINE_IMAGES = {
    "rot": [
        "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800",  # Red wine glass elegant
        "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=800",  # Red wine pouring
        "https://images.unsplash.com/photo-1586370434639-0fe43b2d32e6?w=800",  # Red wine bottle
        "https://images.unsplash.com/photo-1567696911980-2eed69a46042?w=800",  # Red wine glass dark
        "https://images.unsplash.com/photo-1584916201218-f4242ceb4809?w=800",  # Red wine cellar
        "https://images.unsplash.com/photo-1474722883778-792e7990302f?w=800",  # Red wine grapes
        "https://images.unsplash.com/photo-1560148271-00b5e5850812?w=800",  # Red wine tasting
        "https://images.unsplash.com/photo-1598306442928-4d90f32c6866?w=800",  # Red wine bottle elegant
    ],
    "weiß": [
        "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800",  # White wine glass
        "https://images.unsplash.com/photo-1566995541428-f2246c17cda1?w=800",  # White wine elegant
        "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800",  # White wine pouring
        "https://images.unsplash.com/photo-1507434965515-61970f2bd7c6?w=800",  # White wine grapes
        "https://images.unsplash.com/photo-1584916201218-f4242ceb4809?w=800",  # White wine setting
        "https://images.unsplash.com/photo-1569919659476-f0852f6834b7?w=800",  # White wine bottle
        "https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=800",  # White wine glass side
        "https://images.unsplash.com/photo-1560148218-1a83060f7b32?w=800",  # White wine outdoor
    ],
    "rosé": [
        "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",  # Rosé wine glass
        "https://images.unsplash.com/photo-1560148218-1a83060f7b32?w=800",  # Rosé elegant
        "https://images.unsplash.com/photo-1573062337052-54ad71b70402?w=800",  # Rosé bottle
        "https://images.unsplash.com/photo-1560148271-00b5e5850812?w=800",  # Rosé tasting
        "https://images.unsplash.com/photo-1516594915307-8f71bcaed47e?w=800",  # Rosé summer
        "https://images.unsplash.com/photo-1544776193-52a2d4a3cf9d?w=800",  # Rosé glass light
    ],
    "schaumwein": [
        "https://images.unsplash.com/photo-1549918864-48ac978761a4?w=800",  # Champagne glasses
        "https://images.unsplash.com/photo-1578911373434-0cb395d2cbfb?w=800",  # Sparkling wine
        "https://images.unsplash.com/photo-1548690596-f1722c190938?w=800",  # Champagne bottle
        "https://images.unsplash.com/photo-1546171753-97d7676e4602?w=800",  # Prosecco
        "https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=800",  # Sparkling celebration
        "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=800",  # Champagne toast
    ],
}

# Default fallback for unknown types
DEFAULT_IMAGES = [
    "https://images.unsplash.com/photo-1474722883778-792e7990302f?w=800",
    "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800",
    "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800",
]


def get_wine_type(grape):
    """Determine wine type from color or type field"""
    color = (grape.get('color') or grape.get('type') or '').lower()
    
    if 'rot' in color or 'red' in color:
        return 'rot'
    elif 'weiß' in color or 'weiss' in color or 'white' in color:
        return 'weiß'
    elif 'rosé' in color or 'rose' in color or 'pink' in color:
        return 'rosé'
    elif 'schaum' in color or 'spark' in color or 'champagne' in color or 'sekt' in color:
        return 'schaumwein'
    else:
        return None


async def add_images():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client['test_database']
    
    # Find grapes without images
    grapes = await db.grape_varieties.find(
        {"$or": [{"image_url": {"$exists": False}}, {"image_url": None}, {"image_url": ""}]}
    ).to_list(500)
    
    print(f"🍇 Rebsorten ohne Bild: {len(grapes)}")
    
    # Track image usage to distribute evenly
    image_counters = {k: 0 for k in WINE_IMAGES.keys()}
    
    updated = 0
    by_type = {"rot": 0, "weiß": 0, "rosé": 0, "schaumwein": 0, "default": 0}
    
    for grape in grapes:
        wine_type = get_wine_type(grape)
        
        if wine_type and wine_type in WINE_IMAGES:
            images = WINE_IMAGES[wine_type]
            # Rotate through images to distribute evenly
            idx = image_counters[wine_type] % len(images)
            image_url = images[idx]
            image_counters[wine_type] += 1
            by_type[wine_type] += 1
        else:
            # Use default images
            idx = updated % len(DEFAULT_IMAGES)
            image_url = DEFAULT_IMAGES[idx]
            by_type["default"] += 1
        
        # Update database
        await db.grape_varieties.update_one(
            {"_id": grape["_id"]},
            {"$set": {"image_url": image_url}}
        )
        updated += 1
    
    print(f"\n✅ {updated} Rebsorten aktualisiert:")
    for wine_type, count in by_type.items():
        if count > 0:
            print(f"   - {wine_type}: {count}")
    
    # Verify
    total = await db.grape_varieties.count_documents({})
    with_image = await db.grape_varieties.count_documents({"image_url": {"$exists": True, "$ne": None, "$ne": ""}})
    print(f"\n📊 Ergebnis: {with_image}/{total} Rebsorten haben jetzt Bilder")


if __name__ == "__main__":
    asyncio.run(add_images())
