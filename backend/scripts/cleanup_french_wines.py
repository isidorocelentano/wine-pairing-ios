#!/usr/bin/env python3
"""
Bereinigungsscript für französische Weine in der public_wines Collection.

Dieses Script:
1. Normalisiert Appellations-Schreibweisen (Akzente, Leerzeichen, Bindestriche)
2. Entfernt Duplikate durch Zusammenführung ähnlicher Namen
3. Korrigiert Fälle, wo Region als Appellation eingetragen ist
4. Setzt korrekte Regionen für bekannte Appellationen
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

# Mapping: Appellation -> korrigierte Appellation
APPELLATION_CORRECTIONS = {
    # Leerzeichen am Ende entfernen
    "Pauillac ": "Pauillac",
    "Margaux ": "Margaux",
    "Haut-Medoc ": "Haut-Médoc",
    "Haut Medoc": "Haut-Médoc",
    "Haut-Medoc": "Haut-Médoc",
    "Medoc": "Médoc",
    "Medoc ": "Médoc",
    "Pomerol ": "Pomerol",
    "Fronsac ": "Fronsac",
    
    # Saint-Émilion Varianten
    "Saint-Emilion": "Saint-Émilion",
    "Saint-Emilion ": "Saint-Émilion",
    "St. Emilion": "Saint-Émilion",
    "St.-Emilion": "Saint-Émilion",
    "St-Emilion": "Saint-Émilion",
    "Saint-Emilion Grand Cru ": "Saint-Émilion Grand Cru",
    "St. Emilion Grand Cru": "Saint-Émilion Grand Cru",
    "Saint-Emilion Grand Cru Classe": "Saint-Émilion Grand Cru Classé",
    "Saint-Emilion Grand Cru Classe ": "Saint-Émilion Grand Cru Classé",
    "Saint-Emilion Premier Grand Cru Classe ": "Saint-Émilion Premier Grand Cru Classé",
    "Saint-Georges Saint-Emilion ": "Saint-Georges-Saint-Émilion",
    
    # Saint-Estèphe Varianten
    "Saint-Estèphe ": "Saint-Estèphe",
    "St. Estephe": "Saint-Estèphe",
    "St-Estèphe": "Saint-Estèphe",
    
    # Pessac-Léognan Varianten
    "Pessac-Leognan ": "Pessac-Léognan",
    "Graves/Pessac-Leognan": "Pessac-Léognan",
    
    # Châteauneuf-du-Pape Varianten
    "Chateauneuf-du-Pape": "Châteauneuf-du-Pape",
    
    # Côtes Varianten
    "Côte-Rôtie": "Côte-Rôtie",
    "Côtes de Provence": "Côtes de Provence",
    "Côtes de Castillon ": "Côtes de Castillon",
    "Côtes de Bourg ": "Côtes de Bourg",
    "Côtes de Francs ": "Côtes de Francs",
    "Côtes-du-Rhône Villages": "Côtes du Rhône Villages",
    "Côte de Languedoc": "Coteaux du Languedoc",
    
    # Premières Côtes Varianten
    "Premières Côtes de Blaye ": "Premières Côtes de Blaye",
    "Premières Côtes de Bordeaux ": "Premières Côtes de Bordeaux",
    
    # Bordeaux Varianten
    "Bordeaux Superieur ": "Bordeaux Supérieur",
    "Bordeaux Superieur": "Bordeaux Supérieur",
    "Bordeaux A.C. ": "Bordeaux AOC",
    
    # Médoc Varianten
    "Medoc/Haut-Medoc": "Médoc",
    "Moulis-en-Medoc": "Moulis-en-Médoc",
    "Listrac-Medoc": "Listrac-Médoc",
    
    # Fronsac Varianten
    "Fronsac/Canon-Fronsac": "Fronsac",
    "Canon-Fronsac ": "Canon-Fronsac",
    
    # Lalande de Pomerol
    "Lalande de Pomerol ": "Lalande-de-Pomerol",
    
    # Sauternes Varianten
    "Sauternes / Barsac": "Sauternes",
    "Sauternes/Barsac": "Sauternes",
    
    # Provence
    "Côteaux d' Aix en Provence": "Coteaux d'Aix-en-Provence",
    
    # Südwest
    "Suedwest-Frankreich": "Südwest-Frankreich",
    "Suedwesten": "Südwest-Frankreich",
    
    # Cru Klassifizierungen (sollten nicht als Appellation stehen)
    "cru bourgeois": None,  # Entfernen, da keine echte Appellation
    "cru classe": None,
    "grand cru classe": None,
    "grand cru": None,
    "2ème cru classe": None,
    "2è grand cru classe": None,
    "3ème grand cru classe": None,
    "3è grand cru classe  Magn.": None,
    "4ème grand cru classe": None,
    "5ème grand cru classe": None,
    "5ème grand cru classe  Magn.": None,
    "Cru Bourgeois,": None,
    "2e vin de Cos": None,
    "A": None,  # Das ist keine Appellation
    
    # Region als Appellation -> wird später behandelt
}

# Mapping: Appellation -> korrekte Region (wenn falsch oder fehlend)
APPELLATION_TO_REGION = {
    # Bordeaux Appellationen
    "Pauillac": "Bordeaux",
    "Margaux": "Bordeaux", 
    "Pomerol": "Bordeaux",
    "Saint-Émilion": "Bordeaux",
    "Saint-Émilion Grand Cru": "Bordeaux",
    "Saint-Émilion Grand Cru Classé": "Bordeaux",
    "Saint-Émilion Premier Grand Cru Classé": "Bordeaux",
    "Saint-Georges-Saint-Émilion": "Bordeaux",
    "Saint-Julien": "Bordeaux",
    "Saint-Estèphe": "Bordeaux",
    "Sauternes": "Bordeaux",
    "Barsac": "Bordeaux",
    "Pessac-Léognan": "Bordeaux",
    "Haut-Médoc": "Bordeaux",
    "Médoc": "Bordeaux",
    "Moulis": "Bordeaux",
    "Moulis-en-Médoc": "Bordeaux",
    "Listrac": "Bordeaux",
    "Listrac-Médoc": "Bordeaux",
    "Graves": "Bordeaux",
    "Fronsac": "Bordeaux",
    "Canon-Fronsac": "Bordeaux",
    "Lalande-de-Pomerol": "Bordeaux",
    "Côtes de Castillon": "Bordeaux",
    "Côtes de Bourg": "Bordeaux",
    "Côtes de Francs": "Bordeaux",
    "Premières Côtes de Blaye": "Bordeaux",
    "Premières Côtes de Bordeaux": "Bordeaux",
    "Bordeaux Supérieur": "Bordeaux",
    "Bordeaux AOC": "Bordeaux",
    
    # Burgund Appellationen
    "Bourgogne": "Burgund",
    "Corton Grand Cru": "Burgund",
    "Romanée-Conti Grand Cru": "Burgund",
    "La Tâche Grand Cru": "Burgund",
    "Richebourg Grand Cru": "Burgund",
    "Romanée-Saint-Vivant Grand Cru": "Burgund",
    "Échezeaux Grand Cru": "Burgund",
    "Grands-Échezeaux Grand Cru": "Burgund",
    "Clos de Vougeot Grand Cru": "Burgund",
    "Chambertin Grand Cru": "Burgund",
    "Chambertin-Clos de Bèze Grand Cru": "Burgund",
    "Charmes-Chambertin Grand Cru": "Burgund",
    "Clos de la Roche Grand Cru": "Burgund",
    "Clos Saint-Denis Grand Cru": "Burgund",
    "Bonnes-Mares Grand Cru": "Burgund",
    "Musigny Grand Cru": "Burgund",
    "Montrachet Grand Cru": "Burgund",
    "Chevalier-Montrachet Grand Cru": "Burgund",
    "Bâtard-Montrachet Grand Cru": "Burgund",
    "Bienvenues-Bâtard-Montrachet Grand Cru": "Burgund",
    "Criots-Bâtard-Montrachet Grand Cru": "Burgund",
    "Corton-Charlemagne Grand Cru": "Burgund",
    "Chablis Grand Cru Les Clos Grand Cru": "Burgund",
    "Chablis Grand Cru Vaudésir Grand Cru": "Burgund",
    "Chablis Grand Cru Grenouilles Grand Cru": "Burgund",
    "Pouilly-Fuissé": "Burgund",
    "Vosne-Romanée": "Burgund",
    "Meursault 1er Cru": "Burgund",
    "Meursault / Puligny-Montrachet": "Burgund",
    "Côte de Beaune": "Burgund",
    "Chambolle-Musigny": "Burgund",
    "Côtes d'Auxerre": "Burgund",
    
    # Rhône Appellationen
    "Châteauneuf-du-Pape": "Rhône",
    "Côte-Rôtie": "Rhône",
    "Hermitage": "Rhône",
    "Crozes-Hermitage": "Rhône",
    "Cornas": "Rhône",
    "Saint-Joseph": "Rhône",
    "Condrieu": "Rhône",
    "Gigondas": "Rhône",
    "Vacqueyras": "Rhône",
    "Tavel Rosé": "Rhône",
    "Côtes du Rhône Villages": "Rhône",
    "Tal der Rhône": "Rhône",
    "Nördliche Rhône": "Rhône",
    
    # Loire Appellationen
    "Sancerre": "Loire",
    "Pouilly Fume": "Loire",
    "Vouvray": "Loire",
    "Chinon": "Loire",
    "Saumur": "Loire",
    "Anjou": "Loire",
    "Touraine": "Loire",
    
    # Elsass
    "Alsace Grand Cru": "Elsass",
    
    # Beaujolais
    "Moulin-à-Vent": "Beaujolais",
    "Morgon": "Beaujolais",
    "Fleurie": "Beaujolais",
    "Juliénas": "Beaujolais",
    "Saint-Amour": "Beaujolais",
    "Chénas": "Beaujolais",
    "Chiroubles": "Beaujolais",
    "Brouilly": "Beaujolais",
    "Régnié": "Beaujolais",
    "Côte de Brouilly": "Beaujolais",
    
    # Languedoc-Roussillon
    "Corbières": "Languedoc-Roussillon",
    "Coteaux du Languedoc": "Languedoc-Roussillon",
    "Languedoc": "Languedoc-Roussillon",
    "Roussillon": "Languedoc-Roussillon",
    "Montperoux": "Languedoc-Roussillon",
    
    # Provence
    "Côtes de Provence": "Provence",
    "Coteaux d'Aix-en-Provence": "Provence",
}

# Regionen, die als Appellation entfernt werden sollen
REGIONS_AS_APPELLATIONS = {
    "Burgund",
    "Rhône",
    "Bordeaux",
    "Elsass",
    "Loire",
    "Champagne",
    "Provence",
    "Beaujolais",
}

async def cleanup_french_wines():
    """Hauptfunktion für die Bereinigung"""
    client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
    db = client[os.environ.get('DB_NAME')]
    
    print("=" * 60)
    print("🍷 FRANZÖSISCHE WEINE BEREINIGUNG")
    print("=" * 60)
    
    # Statistiken vor der Bereinigung
    total_french = await db.public_wines.count_documents({'country': 'Frankreich'})
    print(f"\n📊 Französische Weine gesamt: {total_french}")
    
    # 1. Appellation-Korrekturen anwenden
    print("\n--- SCHRITT 1: Appellation-Korrekturen ---")
    corrections_count = 0
    
    for old_app, new_app in APPELLATION_CORRECTIONS.items():
        count = await db.public_wines.count_documents({
            'country': 'Frankreich',
            'appellation': old_app
        })
        
        if count > 0:
            if new_app is None:
                # Appellation entfernen (auf leer setzen)
                result = await db.public_wines.update_many(
                    {'country': 'Frankreich', 'appellation': old_app},
                    {'$set': {'appellation': ''}}
                )
                print(f"  ❌ '{old_app}' entfernt: {result.modified_count} Weine")
            else:
                result = await db.public_wines.update_many(
                    {'country': 'Frankreich', 'appellation': old_app},
                    {'$set': {'appellation': new_app}}
                )
                print(f"  ✏️ '{old_app}' → '{new_app}': {result.modified_count} Weine")
            corrections_count += count
    
    print(f"\n✅ Appellation-Korrekturen: {corrections_count} Weine aktualisiert")
    
    # 2. Region als Appellation behandeln
    print("\n--- SCHRITT 2: Region als Appellation korrigieren ---")
    region_corrections = 0
    
    for region in REGIONS_AS_APPELLATIONS:
        count = await db.public_wines.count_documents({
            'country': 'Frankreich',
            'appellation': region
        })
        
        if count > 0:
            # Appellation leeren, Region beibehalten
            result = await db.public_wines.update_many(
                {'country': 'Frankreich', 'appellation': region},
                {'$set': {'appellation': ''}}
            )
            print(f"  🔄 '{region}' als Appellation entfernt: {result.modified_count} Weine")
            region_corrections += count
    
    print(f"\n✅ Region-Korrekturen: {region_corrections} Weine aktualisiert")
    
    # 3. Fehlende Regionen basierend auf Appellation ergänzen
    print("\n--- SCHRITT 3: Fehlende Regionen ergänzen ---")
    region_additions = 0
    
    for appellation, region in APPELLATION_TO_REGION.items():
        # Weine mit dieser Appellation aber falscher/fehlender Region
        result = await db.public_wines.update_many(
            {
                'country': 'Frankreich',
                'appellation': appellation,
                '$or': [
                    {'region': {'$exists': False}},
                    {'region': ''},
                    {'region': None},
                    {'region': {'$ne': region}}
                ]
            },
            {'$set': {'region': region}}
        )
        
        if result.modified_count > 0:
            print(f"  📍 '{appellation}' → Region '{region}': {result.modified_count} Weine")
            region_additions += result.modified_count
    
    print(f"\n✅ Regionen ergänzt: {region_additions} Weine aktualisiert")
    
    # 4. "Unbekannt" Appellationen bereinigen
    print("\n--- SCHRITT 4: 'Unbekannt' Appellationen bereinigen ---")
    result = await db.public_wines.update_many(
        {'country': 'Frankreich', 'appellation': 'Unbekannt'},
        {'$set': {'appellation': ''}}
    )
    print(f"  🗑️ 'Unbekannt' entfernt: {result.modified_count} Weine")
    
    # Finale Statistiken
    print("\n" + "=" * 60)
    print("📊 FINALE STATISTIKEN")
    print("=" * 60)
    
    # Regionen nach Bereinigung
    french_wines = await db.public_wines.find(
        {'country': 'Frankreich'},
        {'_id': 0, 'region': 1, 'appellation': 1}
    ).to_list(None)
    
    regions = {}
    appellations = {}
    empty_appellations = 0
    
    for w in french_wines:
        r = w.get('region') or 'KEINE_REGION'
        a = w.get('appellation') or ''
        regions[r] = regions.get(r, 0) + 1
        if a:
            appellations[a] = appellations.get(a, 0) + 1
        else:
            empty_appellations += 1
    
    print(f"\n🗺️ REGIONEN ({len(regions)}):")
    for r, c in sorted(regions.items(), key=lambda x: -x[1]):
        print(f"  {r}: {c}")
    
    print(f"\n🏷️ TOP 30 APPELLATIONEN ({len(appellations)} unique):")
    for a, c in sorted(appellations.items(), key=lambda x: -x[1])[:30]:
        print(f"  {a}: {c}")
    
    print(f"\n⚠️ Weine ohne Appellation: {empty_appellations}")
    
    print("\n" + "=" * 60)
    print("✅ BEREINIGUNG ABGESCHLOSSEN")
    print("=" * 60)
    
    return {
        'total_french': total_french,
        'corrections': corrections_count,
        'region_corrections': region_corrections,
        'region_additions': region_additions,
        'unique_regions': len(regions),
        'unique_appellations': len(appellations)
    }

if __name__ == "__main__":
    result = asyncio.run(cleanup_french_wines())
    print(f"\n📋 Zusammenfassung: {result}")
