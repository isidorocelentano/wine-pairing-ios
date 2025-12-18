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
    "Südafrika": "🇿🇦",
    "Japan": "🇯🇵",
    "Italien": "🇮🇹",
    "Frankreich": "🇫🇷",
    "Spanien": "🇪🇸",
    "Deutschland": "🇩🇪",
    "Österreich": "🇦🇹",
    "Schweiz": "🇨🇭",
    "Portugal": "🇵🇹",
    "USA": "🇺🇸",
    "Türkei": "🇹🇷",
    "International": "🌍"
}

# South Africa dishes
SOUTH_AFRICA_DISHES = [
    {
        "dish": "Braai (Südafrikanisches Grillfleisch)",
        "region": "Überall",
        "dish_description": "Traditionelles Grillen von Rind, Schwein, Lamm, Würstchen (Boerewors) und Huhn über Holzkohle. Die Kultur des Braai ist zentral für Südafrika.",
        "wine_name": "Pinotage",
        "wine_type": "rot",
        "wine_description": "Der legendäre südafrikanische Pinotage mit seinen rauchigen, erdigen Noten und reifen Beerenaromen ist DER Partner für ein Braai. Ein Wein, der die Seele des Kaps verkörpert."
    },
    {
        "dish": "Boerewors (Bauernwurst)",
        "region": "Überall",
        "dish_description": "Gewürzte Rind- oder Schweinewurst, oft in Spiralen gegrillt, mit Brot oder Pommes.",
        "wine_name": "Shiraz (Stellenbosch)",
        "wine_type": "rot",
        "wine_description": "Der würzige Shiraz aus Stellenbosch mit seinen Pfeffernoten und dunklen Beeren ist der perfekte Partner für die aromatische Boerewors. Südafrikanische Würze trifft auf südafrikanischen Wein."
    },
    {
        "dish": "Bobotie (Gewürzter Hackfleischauflauf)",
        "region": "Kapstadt",
        "dish_description": "Hackfleisch mit Curry, Trockenobst, Eierguss und Brot - oft mit Reis serviert. Ein Klassiker der Cape Malay Küche.",
        "wine_name": "Chenin Blanc",
        "wine_type": "weiss",
        "wine_description": "Der vielseitige südafrikanische Chenin Blanc mit seiner Honig- und Aprikosennote ist perfekt für das süß-würzige Bobotie. Die Frucht des Weins harmoniert mit den Trockenfrüchten."
    },
    {
        "dish": "Potjiekos (Eintopf im Gusseisentopf)",
        "region": "Überall",
        "dish_description": "Langsam gegartes Fleisch (Rind, Lamm) mit Gemüse in einem Eisenkessel über offenem Feuer.",
        "wine_name": "Cabernet Sauvignon (Paarl)",
        "wine_type": "rot",
        "wine_description": "Der kraftvolle Cabernet Sauvignon aus Paarl mit seinen Cassis- und Zedernnoten ist ein würdiger Partner für den reichhaltigen Potjiekos. Stunden der Geduld verdienen einen großen Wein."
    },
    {
        "dish": "Biltong (Luftgetrocknetes Fleisch)",
        "region": "Überall",
        "dish_description": "Gewürztes, luftgetrocknetes Rind- oder Wildfleisch - ähnlich Jerky, aber weicher und aromatischer.",
        "wine_name": "Merlot (Robertson)",
        "wine_type": "rot",
        "wine_description": "Ein samtiger Merlot aus Robertson mit seinen weichen Pflaumennoten ist ein überraschend guter Snack-Begleiter für das würzige Biltong."
    },
    {
        "dish": "Pap en Vleis (Maisbrei mit Fleisch)",
        "region": "Überall",
        "dish_description": "Maisbrei (Pap) mit Fleisch-Eintopf (oft Rind oder Huhn) - ein südafrikanisches Grundnahrungsmittel.",
        "wine_name": "Pinotage Rosé",
        "wine_type": "rose",
        "wine_description": "Ein frischer Pinotage Rosé mit seinen roten Beerennoten und der lebendigen Säure ist ein vielseitiger Partner für dieses herzhafte Alltagsgericht."
    },
    {
        "dish": "Sosaties (Marinierte Fleischspieße)",
        "region": "Kapstadt",
        "dish_description": "Lamm- oder Hühnerfleisch mit Trockenobst, Gewürzen und Kokosmilch mariniert, gegrillt.",
        "wine_name": "Gewürztraminer (Elgin)",
        "wine_type": "weiss",
        "wine_description": "Der aromatische Gewürztraminer aus dem kühlen Elgin mit seinen exotischen Noten ist wie geschaffen für die süß-würzigen Sosaties. Cape Malay trifft auf Elsässer Eleganz."
    },
    {
        "dish": "Chakalaka (Scharfer Gemüsesalat)",
        "region": "Johannesburg",
        "dish_description": "Gemüse (Tomaten, Karotten, Zwiebeln) mit Chili und Gewürzen - oft als Beilage zu Braai.",
        "wine_name": "Sauvignon Blanc (Constantia)",
        "wine_type": "weiss",
        "wine_description": "Der knackige Sauvignon Blanc aus Constantia mit seinen grasigen Noten und der lebendigen Säure ist ein erfrischender Kontrast zum feurigen Chakalaka."
    },
    {
        "dish": "Bunny Chow (Brot mit Curry)",
        "region": "Durban",
        "dish_description": "Hohles Brot mit Curry (Huhn, Lamm, Kichererbsen) gefüllt - der legendäre Street Food-Klassiker aus Durban.",
        "wine_name": "Viognier",
        "wine_type": "weiss",
        "wine_description": "Der opulente Viognier mit seinen Aprikosen- und Blütennoten ist ein mutiger Partner für das würzige Bunny Chow. Die Frucht des Weins zähmt die Schärfe des Currys."
    },
    {
        "dish": "Cape Malay Curry",
        "region": "Kapstadt",
        "dish_description": "Süßer, würziger Curry mit Huhn, Lamm oder Gemüse, oft mit Reis - ein Erbe der kapmalaiischen Küche.",
        "wine_name": "Riesling (Elgin)",
        "wine_type": "weiss",
        "wine_description": "Ein eleganter Riesling aus dem kühlen Elgin mit seiner feinen Restsüße und lebendigen Säure ist der perfekte Partner für den süß-scharfen Cape Malay Curry."
    },
    {
        "dish": "Umngqusho (Mais-Bohnen-Eintopf)",
        "region": "Ostkap",
        "dish_description": "Mais und Bohnen langsam gekocht, oft mit Speck oder Fleisch - ein traditionelles Xhosa-Gericht.",
        "wine_name": "Cinsault",
        "wine_type": "rot",
        "wine_description": "Der leichte, fruchtige Cinsault mit seinen Erdbeernoten ist ein zugänglicher Partner für diesen erdigen Eintopf. Ein unterschätzter Wein für ein unterschätztes Gericht."
    },
    {
        "dish": "Samosas (Gefüllte Teigtaschen)",
        "region": "Durban",
        "dish_description": "Frittierte Teigtaschen mit Fleisch, Gemüse oder Kichererbsen - indisch beeinflusst.",
        "wine_name": "Méthode Cap Classique Brut",
        "wine_type": "schaumwein",
        "wine_description": "Der elegante südafrikanische Schaumwein mit seinen feinen Perlen ist der ideale Aperitif-Partner für knusprige Samosas. Festlich und erfrischend."
    },
    {
        "dish": "Snoek (Atlantikfisch)",
        "region": "Kapstadt",
        "dish_description": "Gegrillter oder geräucherter Fisch, typisch für die Kapregion, oft mit Kartoffeln oder Salat.",
        "wine_name": "Sauvignon Blanc (Darling)",
        "wine_type": "weiss",
        "wine_description": "Der mineralische Sauvignon Blanc aus Darling mit seiner salzigen Brise und Zitrusnoten ist der natürliche Partner für den Snoek vom Grill."
    },
    {
        "dish": "Seafood Potjie (Meeresfrüchte-Eintopf)",
        "region": "Küstenregionen",
        "dish_description": "Fisch, Garnelen, Muscheln in Eintopf mit Gemüse und Gewürzen - die Küstenversion des Potjiekos.",
        "wine_name": "Chardonnay (Walker Bay)",
        "wine_type": "weiss",
        "wine_description": "Der elegante Chardonnay aus Walker Bay mit seiner cremigen Textur und mineralischen Tiefe ist der perfekte Partner für den reichhaltigen Seafood Potjie."
    },
    {
        "dish": "Malva Pudding (Dessert)",
        "region": "Kapstadt",
        "dish_description": "Süßer, klebriger Pudding mit Aprikosenmarmelade, oft mit Vanillesoße serviert.",
        "wine_name": "Vin de Constance",
        "wine_type": "weiss",
        "wine_description": "Der legendäre Vin de Constance - einst der Lieblingswein von Napoleon - mit seinen Honig- und Aprikosennoten ist ein historisches Pairing für den Malva Pudding."
    }
]

# Japan dishes
JAPAN_DISHES = [
    {
        "dish": "Nigiri Sushi (握り寿司)",
        "region": "Tokio",
        "dish_description": "Reis mit dünn geschnittenem rohem Fisch (z.B. Thunfisch, Lachs) darauf - der Edo-Stil Klassiker.",
        "wine_name": "Champagner Brut",
        "wine_type": "schaumwein",
        "wine_description": "Der elegante Champagner mit seinen feinen Perlen und der knackigen Säure ist der klassische Luxus-Partner für feinstes Nigiri Sushi. Die Mineralität des Weins spiegelt die Reinheit des Fischs."
    },
    {
        "dish": "Maki Sushi (巻き寿司)",
        "region": "Überall",
        "dish_description": "Reis und Füllung (Fisch, Gemüse) in Nori (Seetang) gerollt.",
        "wine_name": "Grüner Veltliner",
        "wine_type": "weiss",
        "wine_description": "Der pfeffrige Grüne Veltliner mit seiner lebendigen Säure und mineralischen Tiefe ist ein hervorragender Partner für die Vielfalt der Maki-Rollen."
    },
    {
        "dish": "Sashimi (刺身)",
        "region": "Überall",
        "dish_description": "Dünn geschnittener roher Fisch (z.B. Thunfisch, Makrele, Aal) ohne Reis - pure Reinheit.",
        "wine_name": "Chablis Premier Cru",
        "wine_type": "weiss",
        "wine_description": "Der mineralische Chablis mit seiner stahligen Präzision und den Noten von Austernschalen ist der perfekte Partner für feinstes Sashimi. Reinheit trifft auf Reinheit."
    },
    {
        "dish": "Ramen (ラーメン)",
        "region": "Überall",
        "dish_description": "Nudeln in Brühe (Soja, Miso, Salz, Tonkotsu) mit Fleisch, Ei, Nori - Japans Seelenfutter.",
        "wine_name": "Beaujolais-Villages",
        "wine_type": "rot",
        "wine_description": "Der frische, fruchtige Beaujolais mit seinen Kirschnoten ist ein überraschend guter Partner für eine dampfende Schüssel Ramen. Leicht gekühlt serviert - perfekt!"
    },
    {
        "dish": "Tonkotsu Ramen (豚骨ラーメン)",
        "region": "Fukuoka",
        "dish_description": "Reichhaltige Schweineknochen-Brühe, cremig und intensiv - der Stolz von Kyushu.",
        "wine_name": "Côtes du Rhône Rouge",
        "wine_type": "rot",
        "wine_description": "Der würzige Côtes du Rhône mit seinen erdigen Noten und weichen Tanninen ist mutig genug für die intensive Tonkotsu-Brühe."
    },
    {
        "dish": "Udon (うどん)",
        "region": "Osaka",
        "dish_description": "Dicke Weizennudeln in klare Brühe, oft mit Tempura oder Gemüse.",
        "wine_name": "Muscadet sur Lie",
        "wine_type": "weiss",
        "wine_description": "Der mineralische Muscadet mit seiner salzigen Frische ist ein eleganter Partner für die schlichte Perfektion der Udon-Nudeln."
    },
    {
        "dish": "Soba (そば)",
        "region": "Tokio",
        "dish_description": "Buchweizennudeln, heiß oder kalt, mit Dipping-Soße oder in Brühe.",
        "wine_name": "Sake (Junmai)",
        "wine_type": "weiss",
        "wine_description": "Ein hochwertiger Junmai Sake mit seinen reinen, erdigen Noten ist der authentische Partner für Soba. Japanische Tradition in Perfektion."
    },
    {
        "dish": "Tempura (天ぷら)",
        "region": "Tokio",
        "dish_description": "Frittierte Meeresfrüchte und Gemüse in leichtem, knusprigem Teig.",
        "wine_name": "Franciacorta Brut",
        "wine_type": "schaumwein",
        "wine_description": "Der elegante italienische Schaumwein mit seinen feinen Perlen durchschneidet die knusprige Tempura-Kruste perfekt. Leichtigkeit trifft auf Knusprigkeit."
    },
    {
        "dish": "Sukiyaki (すき焼き)",
        "region": "Osaka",
        "dish_description": "Dünnes Rindfleisch, Gemüse, Tofu in süßer Sojabrühe, am Tisch gegart.",
        "wine_name": "Pinot Noir (Burgund)",
        "wine_type": "rot",
        "wine_description": "Der elegante Burgunder Pinot Noir mit seinen Kirschnoten und seidigen Tanninen ist der klassische Partner für das zarte Rindfleisch im Sukiyaki."
    },
    {
        "dish": "Shabu-Shabu (しゃぶしゃぶ)",
        "region": "Osaka",
        "dish_description": "Dünnes Rindfleisch, im Topf kurz in Brühe gewirbelt, mit Dipping-Soße.",
        "wine_name": "Riesling Kabinett",
        "wine_type": "weiss",
        "wine_description": "Der elegante Riesling Kabinett mit seiner feinen Frucht und lebendigen Säure begleitet das zarte Shabu-Shabu mit Finesse. Die Dipping-Soßen werden vom Wein aufgenommen."
    },
    {
        "dish": "Okonomiyaki (お好み焼き)",
        "region": "Osaka",
        "dish_description": "Wie du willst gebacken - herzhafter Pfannkuchen mit Gemüse, Fleisch, Meeresfruechten und spezieller Sosse.",
        "wine_name": "Lambrusco",
        "wine_type": "rot",
        "wine_description": "Der leicht perlende, fruchtige Lambrusco ist ein spielerischer Partner für den vielseitigen Okonomiyaki. Die süße Soße und der Wein tanzen zusammen."
    },
    {
        "dish": "Katsudon (カツ丼)",
        "region": "Überall",
        "dish_description": "Reis mit paniertem Schweinefleisch (Tonkatsu) und Ei - Comfort Food pur.",
        "wine_name": "Grauburgunder",
        "wine_type": "weiss",
        "wine_description": "Der vollmundige Grauburgunder mit seinen Birnen- und Nussnoten ist ein hervorragender Partner für das knusprige, reichhaltige Katsudon."
    },
    {
        "dish": "Gyudon (牛丼)",
        "region": "Überall",
        "dish_description": "Reis mit dünn geschnittenem Rindfleisch und Zwiebeln in süß-saurer Soße.",
        "wine_name": "Merlot",
        "wine_type": "rot",
        "wine_description": "Der samtige Merlot mit seinen weichen Pflaumennoten harmoniert wunderbar mit dem süß-scharfen Rindfleisch auf dem Gyudon."
    },
    {
        "dish": "Oyakodon (親子丼)",
        "region": "Tokio",
        "dish_description": "Reis mit Hähnchen und Ei in süß-saurer Soße - "Eltern-Kind-Gericht".",
        "wine_name": "Vouvray Demi-Sec",
        "wine_type": "weiss",
        "wine_description": "Der halbtrocken Vouvray mit seiner Honignote und lebendigen Säure ist ein eleganter Partner für die süß-herzhafte Kombination von Hähnchen und Ei."
    },
    {
        "dish": "Chirashizushi (ちらし寿司)",
        "region": "Osaka",
        "dish_description": "Reis mit buntem Gemisch aus rohem Fisch, Ei, Gemüse und Soße - festlich und farbenfroh.",
        "wine_name": "Rosé Champagner",
        "wine_type": "schaumwein",
        "wine_description": "Der elegante Rosé Champagner mit seinen roten Beerennoten und feinen Perlen ist ein festlicher Partner für das bunte Chirashizushi."
    },
    {
        "dish": "Tsukemen (つけ麺)",
        "region": "Tokio",
        "dish_description": "Nudeln zum Eintauchen in konzentrierter, kalter oder warmer Brühe.",
        "wine_name": "Albariño",
        "wine_type": "weiss",
        "wine_description": "Der mineralische Albariño mit seiner salzigen Note und Zitrusfrische ist ein erfrischender Partner für die intensiven Dipping-Brühen des Tsukemen."
    },
    {
        "dish": "Monjayaki (もんじゃ焼き)",
        "region": "Tokio",
        "dish_description": "Flüssigerer, klebrigerer Bratenteig mit Gemüse und Fleisch, oft mit einem kleinen Löffel direkt von der Platte gegessen.",
        "wine_name": "Prosecco",
        "wine_type": "schaumwein",
        "wine_description": "Der erfrischende Prosecco mit seinen leichten Perlen ist ein fröhlicher Begleiter für das gesellige Monjayaki-Erlebnis."
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
            "country": "Südafrika"
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
            "country": "Südafrika",
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
    
    sa_count = await db.regional_pairings.count_documents({"country": "Südafrika"})
    print(f"\n  📊 Südafrika total: {sa_count}")
    
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
    print(f"   🇿🇦 Südafrika: {sa_count} dishes (imported: {imported_sa})")
    print(f"   🇯🇵 Japan: {jp_count} dishes (imported: {imported_jp})")
    print(f"   📊 Total Sommelier Kompass: {total}")
    print("="*60)
    
    client.close()


if __name__ == "__main__":
    asyncio.run(fix_and_import())
