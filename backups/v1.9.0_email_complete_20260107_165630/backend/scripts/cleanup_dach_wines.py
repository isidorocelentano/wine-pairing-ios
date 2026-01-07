#!/usr/bin/env python3
"""
Cleanup-Script für D/A/CH Weindaten
- Bereinigt Regionen (entfernt Sub-Regionen, korrigiert Tippfehler)
- Bereinigt Appellationen (entfernt Prädikatsstufen, Punkte-Bewertungen)
- Füllt leere Regionen basierend auf Appellation wenn möglich

Autor: Agent
Datum: 18.12.2025
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "test_database"

# === DEUTSCHLAND MAPPINGS ===
DE_REGION_CORRECTIONS = {
    # Tippfehler korrigieren
    "Wuejrttemberg": "Württemberg",
    "Wuerttenberg": "Württemberg",
    "Rheinessen": "Rheinhessen",
    "Deutschland": None,  # Will be filled from appellation
    "Mosel-Saar-Ruwer": "Mosel",
}

DE_MAIN_REGIONS = [
    "Ahr", "Baden", "Franken", "Hessische Bergstraße", "Mittelrhein",
    "Mosel", "Nahe", "Pfalz", "Rheingau", "Rheinhessen", "Saale-Unstrut",
    "Sachsen", "Württemberg"
]

# Prädikatsstufen und andere Nicht-Appellationen für Deutschland
DE_INVALID_APPELLATIONS = [
    "Kabinett", "Spätlese", "Auslese", "Beerenauslese", "Trockenbeerenauslese",
    "Eiswein", "Prädikatswein"
]

# === ÖSTERREICH MAPPINGS ===
AT_REGION_CORRECTIONS = {
    "Österreichischer Sekt": None,  # Not a region
}

AT_MAIN_REGIONS = [
    "Wachau", "Kamptal", "Kremstal", "Traisental", "Wagram", "Weinviertel",
    "Carnuntum", "Thermenregion", "Neusiedlersee", "Leithaberg", "Mittelburgenland",
    "Eisenberg", "Südsteiermark", "Weststeiermark", "Vulkanland Steiermark",
    "Wien", "Burgenland"
]

# Nicht-Appellationen für Österreich
AT_INVALID_APPELLATIONS = [
    "Steinfeder", "Federspiel", "Smaragd",  # Wachauer Kategorien
    "Prädikatswein", "Beerenauslese", "Trockenbeerenauslese", "Eiswein",
    "Punkte", "87 Punkte", "88 Punkte", "89 Punkte", "90 Punkte", "91 Punkte",
    "92 Punkte", "93 Punkte", "94 Punkte", "95 Punkte"
]

# === SCHWEIZ MAPPINGS ===
CH_REGION_CORRECTIONS = {
    "Graubuenden": "Graubünden",
}

CH_MAIN_REGIONS = [
    "Wallis", "Waadt", "Genf", "Tessin", "Neuenburg", "Graubünden",
    "Zürich", "Schaffhausen", "Bern", "Luzern", "St. Gallen", "Lavaux",
    "Thurgau", "Aargau"
]


async def cleanup_germany(db):
    """Bereinigt deutsche Weindaten"""
    print("\n" + "="*60)
    print("=== DEUTSCHLAND CLEANUP ===")
    print("="*60)
    
    wines = await db.public_wines.find({"country": "Deutschland"}).to_list(2000)
    print(f"Total deutsche Weine: {len(wines)}")
    
    updates = []
    
    for wine in wines:
        wine_id = wine["_id"]
        region = wine.get("region", "")
        appellation = wine.get("appellation", "")
        changes = {}
        
        # 1. Region korrigieren
        new_region = region
        
        # Tippfehler korrigieren
        if region in DE_REGION_CORRECTIONS:
            new_region = DE_REGION_CORRECTIONS[region]
        
        # Sub-Region zu Hauptregion konvertieren (z.B. "Pfalz - Gimmeldingen" -> "Pfalz")
        if new_region and " - " in new_region:
            main_region = new_region.split(" - ")[0]
            if main_region in DE_MAIN_REGIONS:
                new_region = main_region
        
        # Leere Region aus Appellation füllen
        if not new_region and appellation:
            for main_region in DE_MAIN_REGIONS:
                if main_region.lower() in appellation.lower():
                    new_region = main_region
                    break
        
        if new_region != region:
            changes["region"] = new_region
        
        # 2. Appellation bereinigen
        new_appellation = appellation
        if appellation in DE_INVALID_APPELLATIONS:
            new_appellation = ""  # Remove invalid appellation
        
        if new_appellation != appellation:
            changes["appellation"] = new_appellation
        
        if changes:
            updates.append({
                "_id": wine_id,
                "changes": changes,
                "old_region": region,
                "old_appellation": appellation
            })
    
    # Apply updates
    if updates:
        print(f"\nÄnderungen: {len(updates)} Weine")
        
        # Show sample changes
        print("\nBeispiel-Änderungen (erste 10):")
        for u in updates[:10]:
            print(f"  Region: '{u['old_region']}' -> '{u['changes'].get('region', u['old_region'])}'")
            if 'appellation' in u['changes']:
                print(f"  Appellation: '{u['old_appellation']}' -> '{u['changes']['appellation']}'")
        
        # Apply
        for u in updates:
            await db.public_wines.update_one(
                {"_id": u["_id"]},
                {"$set": u["changes"]}
            )
        print(f"\n✅ {len(updates)} deutsche Weine aktualisiert")
    else:
        print("✅ Keine Änderungen nötig")
    
    return len(updates)


async def cleanup_austria(db):
    """Bereinigt österreichische Weindaten"""
    print("\n" + "="*60)
    print("=== ÖSTERREICH CLEANUP ===")
    print("="*60)
    
    wines = await db.public_wines.find({"country": "Österreich"}).to_list(2000)
    print(f"Total österreichische Weine: {len(wines)}")
    
    updates = []
    
    for wine in wines:
        wine_id = wine["_id"]
        region = wine.get("region", "")
        appellation = wine.get("appellation", "")
        changes = {}
        
        # 1. Region korrigieren
        new_region = region
        
        if region in AT_REGION_CORRECTIONS:
            new_region = AT_REGION_CORRECTIONS[region]
        
        # Leere Region aus Appellation füllen (z.B. "Kamptal DAC" -> Region "Kamptal")
        if not new_region and appellation:
            for main_region in AT_MAIN_REGIONS:
                if main_region.lower() in appellation.lower():
                    new_region = main_region
                    break
        
        if new_region != region:
            changes["region"] = new_region
        
        # 2. Appellation bereinigen
        new_appellation = appellation
        if appellation in AT_INVALID_APPELLATIONS:
            new_appellation = ""
        
        if new_appellation != appellation:
            changes["appellation"] = new_appellation
        
        if changes:
            updates.append({
                "_id": wine_id,
                "changes": changes,
                "old_region": region,
                "old_appellation": appellation
            })
    
    # Apply updates
    if updates:
        print(f"\nÄnderungen: {len(updates)} Weine")
        
        print("\nBeispiel-Änderungen (erste 10):")
        for u in updates[:10]:
            print(f"  Region: '{u['old_region']}' -> '{u['changes'].get('region', u['old_region'])}'")
            if 'appellation' in u['changes']:
                print(f"  Appellation: '{u['old_appellation']}' -> '{u['changes']['appellation']}'")
        
        for u in updates:
            await db.public_wines.update_one(
                {"_id": u["_id"]},
                {"$set": u["changes"]}
            )
        print(f"\n✅ {len(updates)} österreichische Weine aktualisiert")
    else:
        print("✅ Keine Änderungen nötig")
    
    return len(updates)


async def cleanup_switzerland(db):
    """Bereinigt Schweizer Weindaten"""
    print("\n" + "="*60)
    print("=== SCHWEIZ CLEANUP ===")
    print("="*60)
    
    wines = await db.public_wines.find({"country": "Schweiz"}).to_list(2000)
    print(f"Total Schweizer Weine: {len(wines)}")
    
    updates = []
    
    for wine in wines:
        wine_id = wine["_id"]
        region = wine.get("region", "")
        appellation = wine.get("appellation", "")
        changes = {}
        
        # 1. Region korrigieren
        new_region = region
        
        # Tippfehler korrigieren
        if region in CH_REGION_CORRECTIONS:
            new_region = CH_REGION_CORRECTIONS[region]
        
        # Sub-Region zu Hauptregion konvertieren (z.B. "Wallis - Sion" -> "Wallis")
        if new_region and " - " in new_region:
            main_region = new_region.split(" - ")[0]
            if main_region in CH_MAIN_REGIONS:
                new_region = main_region
        
        # Leere Region aus Appellation füllen
        if not new_region and appellation:
            # Try to extract region from AOC names
            for main_region in CH_MAIN_REGIONS:
                if main_region.lower() in appellation.lower():
                    new_region = main_region
                    break
            # Special mappings
            if "Valais" in appellation:
                new_region = "Wallis"
            elif "Vaud" in appellation:
                new_region = "Waadt"
            elif "Genève" in appellation:
                new_region = "Genf"
            elif "Neuchâtel" in appellation:
                new_region = "Neuenburg"
            elif "Ticino" in appellation:
                new_region = "Tessin"
        
        if new_region != region:
            changes["region"] = new_region
        
        if changes:
            updates.append({
                "_id": wine_id,
                "changes": changes,
                "old_region": region
            })
    
    # Apply updates
    if updates:
        print(f"\nÄnderungen: {len(updates)} Weine")
        
        print("\nBeispiel-Änderungen (erste 15):")
        for u in updates[:15]:
            print(f"  Region: '{u['old_region']}' -> '{u['changes'].get('region', u['old_region'])}'")
        
        for u in updates:
            await db.public_wines.update_one(
                {"_id": u["_id"]},
                {"$set": u["changes"]}
            )
        print(f"\n✅ {len(updates)} Schweizer Weine aktualisiert")
    else:
        print("✅ Keine Änderungen nötig")
    
    return len(updates)


async def verify_results(db):
    """Verifiziert die Ergebnisse nach dem Cleanup"""
    print("\n" + "="*60)
    print("=== VERIFIZIERUNG ===")
    print("="*60)
    
    for country in ["Deutschland", "Österreich", "Schweiz"]:
        print(f"\n--- {country} ---")
        
        # Count empty regions
        empty_count = await db.public_wines.count_documents({
            "country": country,
            "$or": [{"region": ""}, {"region": None}, {"region": {"$exists": False}}]
        })
        
        # Get unique regions
        regions = await db.public_wines.distinct("region", {"country": country})
        regions = [r for r in regions if r]
        
        # Get unique appellations
        appellations = await db.public_wines.distinct("appellation", {"country": country})
        appellations = [a for a in appellations if a]
        
        print(f"  Weine ohne Region: {empty_count}")
        print(f"  Einzigartige Regionen: {len(regions)}")
        print(f"  Einzigartige Appellationen: {len(appellations)}")
        
        # Show regions
        print(f"  Regionen: {', '.join(sorted(regions)[:10])}...")


async def main():
    print("🍷 D/A/CH Wein-Daten Cleanup")
    print("="*60)
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Run cleanups
    de_count = await cleanup_germany(db)
    at_count = await cleanup_austria(db)
    ch_count = await cleanup_switzerland(db)
    
    # Verify
    await verify_results(db)
    
    print("\n" + "="*60)
    print("=== ZUSAMMENFASSUNG ===")
    print("="*60)
    print(f"Deutschland: {de_count} Weine aktualisiert")
    print(f"Österreich: {at_count} Weine aktualisiert")
    print(f"Schweiz: {ch_count} Weine aktualisiert")
    print(f"TOTAL: {de_count + at_count + ch_count} Weine aktualisiert")
    print("\n✅ Cleanup abgeschlossen!")


if __name__ == "__main__":
    asyncio.run(main())
