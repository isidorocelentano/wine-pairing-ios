#!/usr/bin/env python3
"""
1. Fix country emojis for all existing entries
2. Import South Africa and Japan dishes
"""

import asyncio
import os
import sys
from datetime import datetime, timezone
from uuid import uuid4

sys.path.insert(0, '/app/backend')

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')

# Country emoji mapping
COUNTRY_EMOJIS = {
    "Griechenland": "🇬🇷",
    "China": "🇨🇳",
    "Thailand": "🇹🇭",
    "Argentinien": "🇦🇷",
    "Suedafrika": "🇿🇦",
    "Japan": "🇯🇵",
    "Italien": "🇮🇹",
    "Frankreich": "🇫🇷",
    "Spanien": "🇪🇸",
    "Deutschland": "🇩🇪",
    "Österreich": "🇦🇹",
    "Schweiz": "🇨🇭",
    "Portugal": "🇵🇹",
    "USA": "🇺🇸",
    "Tuerkei": "🇹🇷",
    "International": "🌍"
}

# South Africa dishes
SOUTH_AFRICA_DISHES = [
    {
        "dish": "Braai (Suedafrikanisches Grillfleisch)",
        "region": "Überall",
        "dish_description": "Traditionelles Grillen von Rind, Schwein, Lamm, Wuerstchen (Boerewors) und Huhn ueber Holzkohle. Die Kultur des Braai ist zentral fuer Suedafrika.",
        "wine_name": "Pinotage",
        "wine_type": "rot",
        "wine_description": "Der legendaere suedafrikanische Pinotage mit seinen rauchigen, erdigen Noten und reifen Beerenaromen ist DER Partner fuer ein Braai. Ein Wein, der die Seele des Kaps verkoerpert."
    },
    {
        "dish": "Boerewors (Bauernwurst)",
        "region": "Überall",
        "dish_description": "Gewuerzte Rind- oder Schweinewurst, oft in Spiralen gegrillt, mit Brot oder Pommes.",
        "wine_name": "Shiraz (Stellenbosch)",
        "wine_type": "rot",
        "wine_description": "Der wuerzige Shiraz aus Stellenbosch mit seinen Pfeffernoten und dunklen Beeren ist der perfekte Partner fuer die aromatische Boerewors. Suedafrikanische Wuerze trifft auf suedafrikanischen Wein."
    },
    {
        "dish": "Bobotie (Gewuerzter Hackfleischauflauf)",
        "region": "Kapstadt",
        "dish_description": "Hackfleisch mit Curry, Trockenobst, Eierguss und Brot - oft mit Reis serviert. Ein Klassiker der Cape Malay Kueche.",
        "wine_name": "Chenin Blanc",
        "wine_type": "weiss",
        "wine_description": "Der vielseitige suedafrikanische Chenin Blanc mit seiner Honig- und Aprikosennote ist perfekt fuer das suess-wuerzige Bobotie. Die Frucht des Weins harmoniert mit den Trockenfruechten."
    },
    {
        "dish": "Potjiekos (Eintopf im Gusseisentopf)",
        "region": "Überall",
        "dish_description": "Langsam gegartes Fleisch (Rind, Lamm) mit Gemuese in einem Eisenkessel ueber offenem Feuer.",
        "wine_name": "Cabernet Sauvignon (Paarl)",
        "wine_type": "rot",
        "wine_description": "Der kraftvolle Cabernet Sauvignon aus Paarl mit seinen Cassis- und Zedernnoten ist ein wuerdiger Partner fuer den reichhaltigen Potjiekos. Stunden der Geduld verdienen einen grossen Wein."
    },
    {
        "dish": "Biltong (Luftgetrocknetes Fleisch)",
        "region": "Überall",
        "dish_description": "Gewuerztes, luftgetrocknetes Rind- oder Wildfleisch - aehnlich Jerky, aber weicher und aromatischer.",
        "wine_name": "Merlot (Robertson)",
        "wine_type": "rot",
        "wine_description": "Ein samtiger Merlot aus Robertson mit seinen weichen Pflaumennoten ist ein ueberraschend guter Snack-Begleiter fuer das wuerzige Biltong."
    },
    {
        "dish": "Pap en Vleis (Maisbrei mit Fleisch)",
        "region": "Überall",
        "dish_description": "Maisbrei (Pap) mit Fleisch-Eintopf (oft Rind oder Huhn) - ein suedafrikanisches Grundnahrungsmittel.",
        "wine_name": "Pinotage Rosé",
        "wine_type": "rose",
        "wine_description": "Ein frischer Pinotage Rosé mit seinen roten Beerennoten und der lebendigen Saeure ist ein vielseitiger Partner fuer dieses herzhafte Alltagsgericht."
    },
    {
        "dish": "Sosaties (Marinierte Fleischspiesse)",
        "region": "Kapstadt",
        "dish_description": "Lamm- oder Huehnerfleisch mit Trockenobst, Gewuerzen und Kokosmilch mariniert, gegrillt.",
        "wine_name": "Gewuerztraminer (Elgin)",
        "wine_type": "weiss",
        "wine_description": "Der aromatische Gewuerztraminer aus dem kuehlen Elgin mit seinen exotischen Noten ist wie geschaffen fuer die suess-wuerzigen Sosaties. Cape Malay trifft auf Elsaesser Eleganz."
    },
    {
        "dish": "Chakalaka (Scharfer Gemuesesalat)",
        "region": "Johannesburg",
        "dish_description": "Gemuese (Tomaten, Karotten, Zwiebeln) mit Chili und Gewuerzen - oft als Beilage zu Braai.",
        "wine_name": "Sauvignon Blanc (Constantia)",
        "wine_type": "weiss",
        "wine_description": "Der knackige Sauvignon Blanc aus Constantia mit seinen grasigen Noten und der lebendigen Saeure ist ein erfrischender Kontrast zum feurigen Chakalaka."
    },
    {
        "dish": "Bunny Chow (Brot mit Curry)",
        "region": "Durban",
        "dish_description": "Hohles Brot mit Curry (Huhn, Lamm, Kichererbsen) gefuellt - der legendaere Street Food-Klassiker aus Durban.",
        "wine_name": "Viognier",
        "wine_type": "weiss",
        "wine_description": "Der opulente Viognier mit seinen Aprikosen- und Bluetennoten ist ein mutiger Partner fuer das wuerzige Bunny Chow. Die Frucht des Weins zaehmt die Schaerfe des Currys."
    },
    {
        "dish": "Cape Malay Curry",
        "region": "Kapstadt",
        "dish_description": "Suesser, wuerziger Curry mit Huhn, Lamm oder Gemuese, oft mit Reis - ein Erbe der kapmalaiischen Kueche.",
        "wine_name": "Riesling (Elgin)",
        "wine_type": "weiss",
        "wine_description": "Ein eleganter Riesling aus dem kuehlen Elgin mit seiner feinen Restsuesse und lebendigen Saeure ist der perfekte Partner fuer den suess-scharfen Cape Malay Curry."
    },
    {
        "dish": "Umngqusho (Mais-Bohnen-Eintopf)",
        "region": "Ostkap",
        "dish_description": "Mais und Bohnen langsam gekocht, oft mit Speck oder Fleisch - ein traditionelles Xhosa-Gericht.",
        "wine_name": "Cinsault",
        "wine_type": "rot",
        "wine_description": "Der leichte, fruchtige Cinsault mit seinen Erdbeernoten ist ein zugaenglicher Partner fuer diesen erdigen Eintopf. Ein unterschaetzter Wein fuer ein unterschaetztes Gericht."
    },
    {
        "dish": "Samosas (Gefuellte Teigtaschen)",
        "region": "Durban",
        "dish_description": "Frittierte Teigtaschen mit Fleisch, Gemuese oder Kichererbsen - indisch beeinflusst.",
        "wine_name": "Méthode Cap Classique Brut",
        "wine_type": "schaumwein",
        "wine_description": "Der elegante suedafrikanische Schaumwein mit seinen feinen Perlen ist der ideale Aperitif-Partner fuer knusprige Samosas. Festlich und erfrischend."
    },
    {
        "dish": "Snoek (Atlantikfisch)",
        "region": "Kapstadt",
        "dish_description": "Gegrillter oder geraeucherter Fisch, typisch fuer die Kapregion, oft mit Kartoffeln oder Salat.",
        "wine_name": "Sauvignon Blanc (Darling)",
        "wine_type": "weiss",
        "wine_description": "Der mineralische Sauvignon Blanc aus Darling mit seiner salzigen Brise und Zitrusnoten ist der natuerliche Partner fuer den Snoek vom Grill."
    },
    {
        "dish": "Seafood Potjie (Meeresfruechte-Eintopf)",
        "region": "Kuestenregionen",
        "dish_description": "Fisch, Garnelen, Muscheln in Eintopf mit Gemuese und Gewuerzen - die Kuestenversion des Potjiekos.",
        "wine_name": "Chardonnay (Walker Bay)",
        "wine_type": "weiss",
        "wine_description": "Der elegante Chardonnay aus Walker Bay mit seiner cremigen Textur und mineralischen Tiefe ist der perfekte Partner fuer den reichhaltigen Seafood Potjie."
    },
    {
        "dish": "Malva Pudding (Dessert)",
        "region": "Kapstadt",
        "dish_description": "Suesser, klebriger Pudding mit Aprikosenmarmelade, oft mit Vanillesosse serviert.",
        "wine_name": "Vin de Constance",
        "wine_type": "weiss",
        "wine_description": "Der legendaere Vin de Constance - einst der Lieblingswein von Napoleon - mit seinen Honig- und Aprikosennoten ist ein historisches Pairing fuer den Malva Pudding."
    }
]

# Japan dishes
JAPAN_DISHES = [
    {
        "dish": "Nigiri Sushi (握り寿司)",
        "region": "Tokio",
        "dish_description": "Reis mit duenn geschnittenem rohem Fisch (z.B. Thunfisch, Lachs) darauf - der Edo-Stil Klassiker.",
        "wine_name": "Champagner Brut",
        "wine_type": "schaumwein",
        "wine_description": "Der elegante Champagner mit seinen feinen Perlen und der knackigen Saeure ist der klassische Luxus-Partner fuer feinstes Nigiri Sushi. Die Mineralitaet des Weins spiegelt die Reinheit des Fischs."
    },
    {
        "dish": "Maki Sushi (巻き寿司)",
        "region": "Überall",
        "dish_description": "Reis und Fuellung (Fisch, Gemuese) in Nori (Seetang) gerollt.",
        "wine_name": "Gruener Veltliner",
        "wine_type": "weiss",
        "wine_description": "Der pfeffrige Gruene Veltliner mit seiner lebendigen Saeure und mineralischen Tiefe ist ein hervorragender Partner fuer die Vielfalt der Maki-Rollen."
    },
    {
        "dish": "Sashimi (刺身)",
        "region": "Überall",
        "dish_description": "Duenn geschnittener roher Fisch (z.B. Thunfisch, Makrele, Aal) ohne Reis - pure Reinheit.",
        "wine_name": "Chablis Premier Cru",
        "wine_type": "weiss",
        "wine_description": "Der mineralische Chablis mit seiner stahligen Praezision und den Noten von Austernschalen ist der perfekte Partner fuer feinstes Sashimi. Reinheit trifft auf Reinheit."
    },
    {
        "dish": "Ramen (ラーメン)",
        "region": "Überall",
        "dish_description": "Nudeln in Bruehe (Soja, Miso, Salz, Tonkotsu) mit Fleisch, Ei, Nori - Japans Seelenfutter.",
        "wine_name": "Beaujolais-Villages",
        "wine_type": "rot",
        "wine_description": "Der frische, fruchtige Beaujolais mit seinen Kirschnoten ist ein ueberraschend guter Partner fuer eine dampfende Schuessel Ramen. Leicht gekuehlt serviert - perfekt!"
    },
    {
        "dish": "Tonkotsu Ramen (豚骨ラーメン)",
        "region": "Fukuoka",
        "dish_description": "Reichhaltige Schweineknochen-Bruehe, cremig und intensiv - der Stolz von Kyushu.",
        "wine_name": "Côtes du Rhône Rouge",
        "wine_type": "rot",
        "wine_description": "Der wuerzige Côtes du Rhône mit seinen erdigen Noten und weichen Tanninen ist mutig genug fuer die intensive Tonkotsu-Bruehe."
    },
    {
        "dish": "Udon (うどん)",
        "region": "Osaka",
        "dish_description": "Dicke Weizennudeln in klare Bruehe, oft mit Tempura oder Gemuese.",
        "wine_name": "Muscadet sur Lie",
        "wine_type": "weiss",
        "wine_description": "Der mineralische Muscadet mit seiner salzigen Frische ist ein eleganter Partner fuer die schlichte Perfektion der Udon-Nudeln."
    },
    {
        "dish": "Soba (そば)",
        "region": "Tokio",
        "dish_description": "Buchweizennudeln, heiss oder kalt, mit Dipping-Sosse oder in Bruehe.",
        "wine_name": "Sake (Junmai)",
        "wine_type": "weiss",
        "wine_description": "Ein hochwertiger Junmai Sake mit seinen reinen, erdigen Noten ist der authentische Partner fuer Soba. Japanische Tradition in Perfektion."
    },
    {
        "dish": "Tempura (天ぷら)",
        "region": "Tokio",
        "dish_description": "Frittierte Meeresfruechte und Gemuese in leichtem, knusprigem Teig.",
        "wine_name": "Franciacorta Brut",
        "wine_type": "schaumwein",
        "wine_description": "Der elegante italienische Schaumwein mit seinen feinen Perlen durchschneidet die knusprige Tempura-Kruste perfekt. Leichtigkeit trifft auf Knusprigkeit."
    },
    {
        "dish": "Sukiyaki (すき焼き)",
        "region": "Osaka",
        "dish_description": "Duennes Rindfleisch, Gemuese, Tofu in suesser Sojabruehe, am Tisch gegart.",
        "wine_name": "Pinot Noir (Burgund)",
        "wine_type": "rot",
        "wine_description": "Der elegante Burgunder Pinot Noir mit seinen Kirschnoten und seidigen Tanninen ist der klassische Partner fuer das zarte Rindfleisch im Sukiyaki."
    },
    {
        "dish": "Shabu-Shabu (しゃぶしゃぶ)",
        "region": "Osaka",
        "dish_description": "Duennes Rindfleisch, im Topf kurz in Bruehe gewirbelt, mit Dipping-Sosse.",
        "wine_name": "Riesling Kabinett",
        "wine_type": "weiss",
        "wine_description": "Der elegante Riesling Kabinett mit seiner feinen Frucht und lebendigen Saeure begleitet das zarte Shabu-Shabu mit Finesse. Die Dipping-Sossen werden vom Wein aufgenommen."
    },
    {
        "dish": "Okonomiyaki (お好み焼き)",
        "region": "Osaka",
        "dish_description": "Wie du willst gebacken - herzhafter Pfannkuchen mit Gemuese, Fleisch, Meeresfruechten und spezieller Sosse.",
        "wine_name": "Lambrusco",
        "wine_type": "rot",
        "wine_description": "Der leicht perlende, fruchtige Lambrusco ist ein spielerischer Partner fuer den vielseitigen Okonomiyaki. Die suesse Sosse und der Wein tanzen zusammen."
    },
    {
        "dish": "Katsudon (カツ丼)",
        "region": "Überall",
        "dish_description": "Reis mit paniertem Schweinefleisch (Tonkatsu) und Ei - Comfort Food pur.",
        "wine_name": "Grauburgunder",
        "wine_type": "weiss",
        "wine_description": "Der vollmundige Grauburgunder mit seinen Birnen- und Nussnoten ist ein hervorragender Partner fuer das knusprige, reichhaltige Katsudon."
    },
    {
        "dish": "Gyudon (牛丼)",
        "region": "Überall",
        "dish_description": "Reis mit duenn geschnittenem Rindfleisch und Zwiebeln in suess-saurer Sosse.",
        "wine_name": "Merlot",
        "wine_type": "rot",
        "wine_description": "Der samtige Merlot mit seinen weichen Pflaumennoten harmoniert wunderbar mit dem suess-scharfen Rindfleisch auf dem Gyudon."
    },
    {
        "dish": "Oyakodon (親子丼)",
        "region": "Tokio",
        "dish_description": "Reis mit Haehnchen und Ei in suess-saurer Sosse - Eltern-Kind-Gericht.",
        "wine_name": "Vouvray Demi-Sec",
        "wine_type": "weiss",
        "wine_description": "Der halbtrocken Vouvray mit seiner Honignote und lebendigen Saeure ist ein eleganter Partner fuer die suess-herzhafte Kombination von Haehnchen und Ei."
    },
    {
        "dish": "Chirashizushi (ちらし寿司)",
        "region": "Osaka",
        "dish_description": "Reis mit buntem Gemisch aus rohem Fisch, Ei, Gemuese und Sosse - festlich und farbenfroh.",
        "wine_name": "Rosé Champagner",
        "wine_type": "schaumwein",
        "wine_description": "Der elegante Rosé Champagner mit seinen roten Beerennoten und feinen Perlen ist ein festlicher Partner fuer das bunte Chirashizushi."
    },
    {
        "dish": "Tsukemen (つけ麺)",
        "region": "Tokio",
        "dish_description": "Nudeln zum Eintauchen in konzentrierter, kalter oder warmer Bruehe.",
        "wine_name": "Albariño",
        "wine_type": "weiss",
        "wine_description": "Der mineralische Albariño mit seiner salzigen Note und Zitrusfrische ist ein erfrischender Partner fuer die intensiven Dipping-Bruehen des Tsukemen."
    },
    {
        "dish": "Monjayaki (もんじゃ焼き)",
        "region": "Tokio",
        "dish_description": "Fluessigerer, klebrigerer Bratenteig mit Gemuese und Fleisch, oft mit einem kleinen Loeffel direkt von der Platte gegessen.",
        "wine_name": "Prosecco",
        "wine_type": "schaumwein",
        "wine_description": "Der erfrischende Prosecco mit seinen leichten Perlen ist ein froehlicher Begleiter fuer das gesellige Monjayaki-Erlebnis."
    }
]


async def fix_and_import():
    """Fix country emojis and import new dishes."""
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'wine_pairing')]
    
    print("="*60)
    print("PHASE 1: Fixing country emojis for all entries")
    print("="*60)
    
    # Fix emojis for all countries
    for country, emoji in COUNTRY_EMOJIS.items():
        result = await db.regional_pairings.update_many(
            {"country": country},
            {"$set": {"country_emoji": emoji}}
        )
        if result.modified_count > 0:
            print(f"  ✅ {country}: {emoji} - Updated {result.modified_count} entries")
    
    print("\n" + "="*60)
    print("PHASE 2: Importing South Africa dishes")
    print("="*60)
    
    imported_sa = 0
    for dish_data in SOUTH_AFRICA_DISHES:
        exists = await db.regional_pairings.find_one({
            "dish": dish_data["dish"],
            "country": "Suedafrika"
        })
        if exists:
            print(f"  ⏭️ Skipping: {dish_data['dish']}")
            continue
        
        doc = {
            "id": str(uuid4()),
            "dish": dish_data["dish"],
            "dish_description": dish_data["dish_description"],
            "dish_description_en": dish_data["dish_description"],
            "dish_description_fr": dish_data["dish_description"],
            "country": "Suedafrika",
            "country_emoji": "🇿🇦",
            "region": dish_data["region"],
            "wine_name": dish_data["wine_name"],
            "wine_type": dish_data["wine_type"],
            "wine_description": dish_data["wine_description"],
            "wine_description_en": f"[EN] {dish_data['wine_description'][:100]}...",
            "wine_description_fr": f"[FR] {dish_data['wine_description'][:100]}...",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.regional_pairings.insert_one(doc)
        print(f"  ✅ Imported: {dish_data['dish']}")
        imported_sa += 1
    
    sa_count = await db.regional_pairings.count_documents({"country": "Suedafrika"})
    print(f"\n  📊 Suedafrika total: {sa_count}")
    
    print("\n" + "="*60)
    print("PHASE 3: Importing Japan dishes")
    print("="*60)
    
    imported_jp = 0
    for dish_data in JAPAN_DISHES:
        exists = await db.regional_pairings.find_one({
            "dish": dish_data["dish"],
            "country": "Japan"
        })
        if exists:
            print(f"  ⏭️ Skipping: {dish_data['dish']}")
            continue
        
        doc = {
            "id": str(uuid4()),
            "dish": dish_data["dish"],
            "dish_description": dish_data["dish_description"],
            "dish_description_en": dish_data["dish_description"],
            "dish_description_fr": dish_data["dish_description"],
            "country": "Japan",
            "country_emoji": "🇯🇵",
            "region": dish_data["region"],
            "wine_name": dish_data["wine_name"],
            "wine_type": dish_data["wine_type"],
            "wine_description": dish_data["wine_description"],
            "wine_description_en": f"[EN] {dish_data['wine_description'][:100]}...",
            "wine_description_fr": f"[FR] {dish_data['wine_description'][:100]}...",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.regional_pairings.insert_one(doc)
        print(f"  ✅ Imported: {dish_data['dish']}")
        imported_jp += 1
    
    jp_count = await db.regional_pairings.count_documents({"country": "Japan"})
    print(f"\n  📊 Japan total: {jp_count}")
    
    # Final summary
    total = await db.regional_pairings.count_documents({})
    
    print("\n" + "="*60)
    print("🎉 COMPLETE!")
    print(f"   🇿🇦 Suedafrika: {sa_count} dishes (imported: {imported_sa})")
    print(f"   🇯🇵 Japan: {jp_count} dishes (imported: {imported_jp})")
    print(f"   📊 Total Sommelier Kompass: {total}")
    print("="*60)
    
    client.close()


if __name__ == "__main__":
    asyncio.run(fix_and_import())
