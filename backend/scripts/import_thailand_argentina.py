#!/usr/bin/env python3
"""
Import Thai and Argentinian dishes from Sommelier Kompass document
with wine pairings and translations.
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

# Thailand dishes with wine pairings
THAILAND_DISHES = [
    # === ZENTRAL-THAILAND ===
    {
        "dish": "Green Curry (Kaeng Khiao Wan, แกงเขียวหวาน)",
        "region": "Zentral-Thailand",
        "dish_description": "Scharfes, cremiges Curry mit grünen Chilis, Kokosmilch, Hühnchen oder Rind.",
        "wine_name": "Riesling Spätlese halbtrocken",
        "wine_type": "weiss",
        "wine_description": "Die elegante Restsüße des deutschen Rieslings ist wie ein kühler Wasserfall gegen die Schärfe des Green Curry. Die Fruchtnoten tanzen mit der Kokosmilch, während die Säure das Fett ausbalanciert."
    },
    {
        "dish": "Red Curry (Kaeng Phet, แกงเผ็ด)",
        "region": "Zentral-Thailand",
        "dish_description": "Scharfes Curry mit roten Chilis, Kokosmilch, Fleisch und Gemüse.",
        "wine_name": "Gewürztraminer",
        "wine_type": "weiss",
        "wine_description": "Der aromatische Gewürztraminer mit seinen exotischen Litschi- und Rosennoten ist ein mutiger Partner für das feurige Red Curry. Die leichte Süße zähmt die Chilis sanft."
    },
    {
        "dish": "Panang Curry (Kaeng Phanaeng, แกงพะแนง)",
        "region": "Zentral-Thailand",
        "dish_description": "Dicker, nussiger Curry mit Kokosmilch, Fleisch und Kaffir-Limettenblättern.",
        "wine_name": "Viognier",
        "wine_type": "weiss",
        "wine_description": "Der opulente Viognier mit seinen Aprikosen- und Blütennoten verschmilzt mit dem nussigen Panang Curry zu einem tropischen Traum. Die cremige Textur beider Partner harmoniert perfekt."
    },
    {
        "dish": "Yellow Curry (Kaeng Kari, แกงกะหรี่)",
        "region": "Zentral-Thailand",
        "dish_description": "Mildes, gelbes Curry mit Kurkuma, Kartoffeln und Hühnchen oder Rind.",
        "wine_name": "Chenin Blanc",
        "wine_type": "weiss",
        "wine_description": "Der vielseitige Chenin Blanc mit seiner lebendigen Säure und Honignoten ist der ideale Partner für dieses milde, erdige Curry. Die Kartoffeln finden im Wein einen würdigen Begleiter."
    },
    {
        "dish": "Pad Thai (ผัดไทย)",
        "region": "Bangkok",
        "dish_description": "Gebratene Reisnudeln mit Ei, Tofu, Garnelen, Erdnüssen und Tamarindensoße.",
        "wine_name": "Grüner Veltliner",
        "wine_type": "weiss",
        "wine_description": "Der pfeffrige Grüne Veltliner mit seiner lebendigen Säure ist wie gemacht für Pad Thai. Die Erdnüsse und die süß-saure Tamarinde werden von der Würze des Weins perfekt ergänzt."
    },
    {
        "dish": "Tom Yum Goong (ต้มยำกุ้ง)",
        "region": "Zentral-Thailand",
        "dish_description": "Scharfe, saure Suppe mit Garnelen, Pilzen, Lemongras und Kaffir-Limettenblättern.",
        "wine_name": "Sauvignon Blanc (Marlborough)",
        "wine_type": "weiss",
        "wine_description": "Der knackige Sauvignon Blanc aus Neuseeland mit seinen grasigen Noten und der Zitrusfrische ist der perfekte Partner für die aromatische Tom Yum. Lemongras trifft auf Limette – eine himmlische Begegnung."
    },
    {
        "dish": "Tom Kha Gai (ต้มข่าไก่)",
        "region": "Zentral-Thailand",
        "dish_description": "Kokosmilch-Suppe mit Hähnchen, Pilzen, Lemongras und Kaffir-Limettenblättern.",
        "wine_name": "Chardonnay (unoaked)",
        "wine_type": "weiss",
        "wine_description": "Ein frischer, ungehobelter Chardonnay mit seinen Apfel- und Zitrusnoten begleitet die cremige Kokosmilch-Suppe elegant. Die Säure bringt Frische in die reichhaltige Suppe."
    },
    {
        "dish": "Khao Kha Moo (ข้าวขาหมู)",
        "region": "Zentral-Thailand",
        "dish_description": "Langsam gekochtes Schweinebein mit Reis, oft mit Ei und Soße.",
        "wine_name": "Pinot Noir",
        "wine_type": "rot",
        "wine_description": "Der elegante Pinot Noir mit seinen Kirschnoten und seidigen Tanninen umschmeichelt das butterzarte Schweinebein. Ein Wein, der die Tiefe des Gerichts würdigt."
    },
    {
        "dish": "Khao Man Gai (ข้าวมันไก่)",
        "region": "Bangkok",
        "dish_description": "Gekochtes Hähnchen mit duftendem Reis, oft mit Ingwer-Soße und Suppe.",
        "wine_name": "Riesling Kabinett",
        "wine_type": "weiss",
        "wine_description": "Der elegante deutsche Riesling Kabinett mit seiner feinen Frucht und lebendigen Säure ist der perfekte Partner für dieses zarte Hähnchengericht. Der Ingwer findet im Wein sein Echo."
    },
    
    # === SÜDEN (Malaiisch beeinflusst) ===
    {
        "dish": "Massaman Curry (Kaeng Massaman, แกงมัสมั่น)",
        "region": "Südthailand",
        "dish_description": "Mildes, süß-scharfes Curry mit Kartoffeln, Erdnüssen, Zimt und Fleisch.",
        "wine_name": "Moscato d'Asti",
        "wine_type": "weiss",
        "wine_description": "Der süße, leicht perlende Moscato ist ein Traum mit dem würzigen Massaman Curry. Die Erdnüsse und der Zimt finden in den Traubennoten einen harmonischen Partner."
    },
    {
        "dish": "Satay (สะเต๊ะ)",
        "region": "Südthailand",
        "dish_description": "Marinierte Fleischspieße (Huhn, Rind) mit Erdnusssoße.",
        "wine_name": "Torrontés",
        "wine_type": "weiss",
        "wine_description": "Der aromatische argentinische Torrontés mit seinen floralen Noten ist ein überraschend passender Partner für Satay. Die Erdnusssoße und die Blütennoten des Weins verschmelzen harmonisch."
    },
    {
        "dish": "Gaeng Som (แกงส้ม)",
        "region": "Südthailand",
        "dish_description": "Scharfe, saure Fischsuppe mit Gemüse, oft mit Tamarinde und Chili.",
        "wine_name": "Vinho Verde",
        "wine_type": "weiss",
        "wine_description": "Der spritzige Vinho Verde mit seinem leichten Prickeln ist erfrischend und belebend zu dieser säurebetonten Fischsuppe. Wie eine Meeresbrise an der Andamanenküste."
    },
    
    # === NORDOSTEN (Isaan) ===
    {
        "dish": "Som Tum (ส้มตำ)",
        "region": "Isaan (Nordosten)",
        "dish_description": "Grüner Papayasalat mit Chili, Fischsoße, Limette, Tomaten und Erdnüssen.",
        "wine_name": "Riesling trocken",
        "wine_type": "weiss",
        "wine_description": "Der trockene Riesling mit seiner kristallinen Säure ist der klassische Partner für Som Tum. Die Limette und die Schärfe werden von der Eleganz des Weins aufgefangen."
    },
    {
        "dish": "Larb (ลาบ)",
        "region": "Isaan (Nordosten)",
        "dish_description": "Hackfleischsalat (Huhn, Rind, Schwein) mit Chili, Limette, Koriander und geröstetem Reis.",
        "wine_name": "Côtes du Rhône Rosé",
        "wine_type": "rose",
        "wine_description": "Ein frischer Côtes du Rhône Rosé mit seinen roten Beerennoten ist ein erfrischender Partner für den würzigen Larb. Der geröstete Reis findet in den nussigen Untertönen sein Echo."
    },
    {
        "dish": "Nam Prik (น้ำพริก)",
        "region": "Isaan (Nordosten)",
        "dish_description": "Chili-Dip mit Gemüse, Fisch, Tofu oder Ei – oft mit Reis oder Gemüse.",
        "wine_name": "Albariño",
        "wine_type": "weiss",
        "wine_description": "Der mineralische Albariño mit seiner salzigen Brise und Zitrusnoten ist ein eleganter Kontrast zum feurigen Nam Prik. Die Frische des Weins beruhigt den Gaumen."
    },
    
    # === NORDTHAILAND (Chiang Mai) ===
    {
        "dish": "Khao Soi (ข้าวซอย)",
        "region": "Chiang Mai (Norden)",
        "dish_description": "Kokosmilch-Curry-Nudeln mit knusprigen Nudeln oben, oft mit Hähnchen oder Rind.",
        "wine_name": "Gewürztraminer Elsass",
        "wine_type": "weiss",
        "wine_description": "Der aromatische elsässische Gewürztraminer mit seinen exotischen Noten ist wie geschaffen für Khao Soi. Die cremige Kokosmilch und die knusprigen Nudeln werden von der Fülle des Weins umarmt."
    },
    
    # === ÜBERALL ===
    {
        "dish": "Pad Kra Pao (ผัดกระเพรา)",
        "region": "Überall",
        "dish_description": "Gebratener Reis oder Nudeln mit Schweinefleisch, Chili und heiligem Basilikum.",
        "wine_name": "Lambrusco",
        "wine_type": "rot",
        "wine_description": "Der leicht perlende, fruchtige Lambrusco ist ein erfrischender Kontrast zum feurigen Pad Kra Pao. Seine Kühle und Süße beruhigen den Gaumen zwischen den würzigen Bissen."
    },
    {
        "dish": "Khao Pad (ข้าวผัด)",
        "region": "Überall",
        "dish_description": "Gebratener Reis mit Ei, Gemüse, Fleisch oder Meeresfrüchten.",
        "wine_name": "Cava Brut",
        "wine_type": "schaumwein",
        "wine_description": "Der spanische Cava mit seinen feinen Perlen und Zitrusnoten ist universell und flexibel – genau wie der gebratene Reis selbst. Eine fröhliche Kombination für jeden Anlass."
    },
    {
        "dish": "Drunken Noodles (Pad Kee Mao, ผัดขี้เมา)",
        "region": "Überall",
        "dish_description": "Scharfe, breite Reisnudeln mit Fleisch, Chili, Basilikum und Sojasauce.",
        "wine_name": "Off-Dry Riesling",
        "wine_type": "weiss",
        "wine_description": "Ein halbtrocken Riesling mit seiner Balance aus Frucht und Säure ist der perfekte Partner für die feurigen Drunken Noodles. Die Restsüße mildert die Schärfe."
    },
    {
        "dish": "Spring Rolls (Poh Pia Tod, ปอเปี๊ยะทอด)",
        "region": "Überall",
        "dish_description": "Frittierte Teigrollen mit Gemüse, Fleisch oder Glasnudeln.",
        "wine_name": "Prosecco",
        "wine_type": "schaumwein",
        "wine_description": "Der erfrischende Prosecco mit seinen zarten Perlen ist der ideale Aperitif-Partner für knusprige Spring Rolls. Die Leichtigkeit beider Partner harmoniert wunderbar."
    }
]

# Argentina dishes with wine pairings
ARGENTINA_DISHES = [
    # === ÜBERALL ===
    {
        "dish": "Asado (Argentinisches Grillfleisch)",
        "region": "Überall",
        "dish_description": "Traditionelles Grillen von Rindfleisch (Vacío, Entraña, Costilla) über Holzkohle. Die Kultur des Asado ist zentral für Argentinien.",
        "wine_name": "Malbec (Mendoza)",
        "wine_type": "rot",
        "wine_description": "Der legendäre argentinische Malbec aus Mendoza mit seinen dunklen Beeren, Pflaumen und einem Hauch von Rauch ist DER Partner für Asado. Ein Wein, der die Seele Argentiniens verkörpert."
    },
    {
        "dish": "Choripán",
        "region": "Überall",
        "dish_description": "Gegrillte Chorizo-Wurst in Brötchen, oft mit Chimichurri-Sauce.",
        "wine_name": "Bonarda",
        "wine_type": "rot",
        "wine_description": "Der fruchtige Bonarda mit seinen Kirsch- und Pflaumennoten ist der perfekte Streetfood-Wein für Choripán. Die würzige Chimichurri findet im Wein einen ebenbürtigen Partner."
    },
    {
        "dish": "Morcilla (Argentinische Blutwurst)",
        "region": "Überall",
        "dish_description": "Gegrillte oder gebratene Blutwurst, oft mit Zwiebeln und Chimichurri.",
        "wine_name": "Cabernet Sauvignon (Mendoza)",
        "wine_type": "rot",
        "wine_description": "Der kraftvolle Cabernet Sauvignon mit seiner dunklen Frucht und seinen Tanninen ist mutig genug für die intensive Morcilla. Eine Kombination für Fleischliebhaber."
    },
    {
        "dish": "Vacío (Rinderbauch)",
        "region": "Überall",
        "dish_description": "Zartes, fettreiches Rindfleisch vom Grill oder aus der Pfanne.",
        "wine_name": "Malbec Reserve",
        "wine_type": "rot",
        "wine_description": "Ein gereifter Malbec Reserve mit seiner samtigen Textur und den Noten von Veilchen und dunkler Schokolade umschmeichelt das fettreiche Vacío perfekt."
    },
    {
        "dish": "Entraña (Zwerchfell)",
        "region": "Überall",
        "dish_description": "Zartes, saftiges Rindfleisch, oft mit Chimichurri serviert.",
        "wine_name": "Malbec-Cabernet Blend",
        "wine_type": "rot",
        "wine_description": "Eine elegante Cuvée aus Malbec und Cabernet Sauvignon vereint Frucht und Struktur – perfekt für das saftige Entraña mit seiner intensiven Fleischigkeit."
    },
    {
        "dish": "Empanadas (Argentinische Teigtaschen)",
        "region": "Überall",
        "dish_description": "Gefüllte Teigtaschen mit Rind, Huhn, Käse, Oliven oder Ei – jede Region hat ihre eigene Variante.",
        "wine_name": "Torrontés",
        "wine_type": "weiss",
        "wine_description": "Der aromatische Torrontés mit seinen Blüten- und Zitrusnoten ist ein erfrischender Partner für die herzhaften Empanadas. Ein Wein, der die Vielfalt Argentiniens feiert."
    },
    {
        "dish": "Provoleta (Gegrillter Käse)",
        "region": "Überall",
        "dish_description": "Gegrillter Provolone-Käse, oft mit Oregano und Chili – ein klassischer Asado-Starter.",
        "wine_name": "Malbec Rosé",
        "wine_type": "rose",
        "wine_description": "Ein frischer Malbec Rosé mit seinen roten Beerennoten und der lebendigen Säure durchschneidet die Reichhaltigkeit des gegrillten Käses perfekt."
    },
    {
        "dish": "Chimichurri (als Beilage)",
        "region": "Überall",
        "dish_description": "Die legendäre grüne Sauce aus Petersilie, Knoblauch, Oregano, Essig und Öl – unverzichtbar zum Asado.",
        "wine_name": "Malbec Clásico",
        "wine_type": "rot",
        "wine_description": "Ein klassischer Malbec mit seiner Frucht und mittleren Tanninen ist der traditionelle Partner für alles, was mit Chimichurri serviert wird."
    },
    
    # === BUENOS AIRES (italienisch beeinflusst) ===
    {
        "dish": "Milanesa (Argentinisches Schnitzel)",
        "region": "Buenos Aires",
        "dish_description": "Paniertes Schnitzel (meist Rind oder Huhn), oft mit Pommes oder Salat.",
        "wine_name": "Sangiovese (Argentinien)",
        "wine_type": "rot",
        "wine_description": "Der argentinische Sangiovese mit seinen Kirschnoten und lebendiger Säure ist ein eleganter Partner für die knusprige Milanesa. Italienisches Erbe trifft auf argentinische Seele."
    },
    {
        "dish": "Milanesa a la Napolitana",
        "region": "Buenos Aires",
        "dish_description": "Milanesa mit Tomatensoße, Käse und Schinken – wie Schnitzel auf Napolitaner Art.",
        "wine_name": "Syrah (Mendoza)",
        "wine_type": "rot",
        "wine_description": "Der würzige Syrah mit seinen dunklen Beeren und Pfeffernoten ist ein kraftvoller Partner für dieses reichhaltige Gericht. Die Tomatensoße und der Käse werden von der Intensität des Weins umspielt."
    },
    {
        "dish": "Canelones (Argentinische Cannelloni)",
        "region": "Buenos Aires",
        "dish_description": "Gefüllte Nudelröllchen mit Hackfleisch und Käse, überbacken mit Béchamel.",
        "wine_name": "Merlot (Mendoza)",
        "wine_type": "rot",
        "wine_description": "Der samtige Merlot mit seinen Pflaumennoten und weichen Tanninen umschmeichelt die cremige Béchamel und das würzige Hackfleisch. Comfort Food mit passendem Comfort Wine."
    },
    {
        "dish": "Matambre Arrollado",
        "region": "Buenos Aires",
        "dish_description": "Gefülltes Rindfleisch (mit Karotten, Zwiebeln, Ei), gerollt und gekocht.",
        "wine_name": "Cabernet Franc",
        "wine_type": "rot",
        "wine_description": "Der elegante Cabernet Franc mit seinen grünen Paprika- und Beerennoten ist ein raffinierter Partner für das gefüllte Matambre. Die Gemüsefüllung findet im Wein ihr Echo."
    },
    {
        "dish": "Carbonada (Süßer Fleischeintopf)",
        "region": "Buenos Aires",
        "dish_description": "Süßer Eintopf aus Rindfleisch, Obst (Apfel, Birne), Gemüse und Milch.",
        "wine_name": "Malbec Late Harvest",
        "wine_type": "rot",
        "wine_description": "Ein süßer Malbec Late Harvest mit seinen Aromen von getrockneten Früchten ist ein unkonventioneller, aber perfekter Partner für diesen süß-herzhaften Eintopf."
    },
    {
        "dish": "Puchero (Sonntagseintopf)",
        "region": "Buenos Aires",
        "dish_description": "Eintopf aus Rindfleisch, Gemüse, Kartoffeln und Mais – traditionell sonntags serviert.",
        "wine_name": "Petit Verdot",
        "wine_type": "rot",
        "wine_description": "Der intensive Petit Verdot mit seiner dunklen Frucht und seinen kräftigen Tanninen ist ein würdiger Partner für den herzhaften Sonntagseintopf. Ein Wein für die Familie."
    },
    
    # === NORDWESTEN (Salta, Jujuy) ===
    {
        "dish": "Locro (Argentinischer Nationaleintopf)",
        "region": "Nordwesten (Salta)",
        "dish_description": "Eintopf aus Mais, Bohnen, Fleisch und Gemüse – traditionell zu Nationalfeiertagen serviert.",
        "wine_name": "Torrontés (Salta)",
        "wine_type": "weiss",
        "wine_description": "Der Torrontés aus den Höhenlagen von Salta mit seinen intensiven Blütennoten ist der authentische lokale Partner für Locro. Ein Wein aus derselben Heimat wie das Gericht."
    },
    {
        "dish": "Humita (Maisfüllung in Maisblättern)",
        "region": "Nordwesten (Jujuy)",
        "dish_description": "Gekochte Maisfüllung in Maisblättern, oft als Beilage oder Hauptgericht.",
        "wine_name": "Chardonnay (Salta)",
        "wine_type": "weiss",
        "wine_description": "Ein frischer Chardonnay aus den Höhenlagen von Salta mit seiner knackigen Säure und Steinobstnoten ist ein wunderbarer Partner für die süße, erdige Humita."
    },
    
    # === PATAGONIEN ===
    {
        "dish": "Cordero Patagónico (Patagonisches Lamm)",
        "region": "Patagonien",
        "dish_description": "Langsam gegrilltes oder geschmortes Lamm aus Patagonien – das Fleisch hat einen einzigartigen Geschmack durch die wilden Kräuter der Region.",
        "wine_name": "Pinot Noir (Patagonien)",
        "wine_type": "rot",
        "wine_description": "Der elegante Pinot Noir aus Patagonien mit seinen Kräuter- und Kirschnoten ist wie geschaffen für das würzige patagonische Lamm. Terroir trifft auf Terroir."
    },
    {
        "dish": "Trucha Patagónica (Patagonische Forelle)",
        "region": "Patagonien",
        "dish_description": "Frische Forelle aus den kristallklaren Seen Patagoniens, oft gegrillt oder geräuchert.",
        "wine_name": "Sauvignon Blanc (Patagonien)",
        "wine_type": "weiss",
        "wine_description": "Der frische Sauvignon Blanc aus Patagonien mit seinen Zitrus- und Kräuternoten ist der natürliche Partner für die zarte Forelle. Reinheit trifft auf Reinheit."
    }
]


async def import_all():
    """Import all Thai and Argentinian dishes."""
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'wine_pairing')]
    
    total_imported = 0
    total_skipped = 0
    
    # Import Thailand
    print("🇹🇭 Importing Thailand dishes...")
    for dish_data in THAILAND_DISHES:
        exists = await db.regional_pairings.find_one({
            "dish": dish_data["dish"],
            "country": "Thailand"
        })
        if exists:
            print(f"  ⏭️ Skipping: {dish_data['dish']}")
            total_skipped += 1
            continue
        
        doc = {
            "id": str(uuid4()),
            "dish": dish_data["dish"],
            "dish_description": dish_data["dish_description"],
            "dish_description_en": dish_data["dish_description"],
            "dish_description_fr": dish_data["dish_description"],
            "country": "Thailand",
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
        total_imported += 1
    
    thailand_count = await db.regional_pairings.count_documents({"country": "Thailand"})
    print(f"\n  📊 Thailand total: {thailand_count}\n")
    
    # Import Argentina
    print("🇦🇷 Importing Argentina dishes...")
    for dish_data in ARGENTINA_DISHES:
        exists = await db.regional_pairings.find_one({
            "dish": dish_data["dish"],
            "country": "Argentinien"
        })
        if exists:
            print(f"  ⏭️ Skipping: {dish_data['dish']}")
            total_skipped += 1
            continue
        
        doc = {
            "id": str(uuid4()),
            "dish": dish_data["dish"],
            "dish_description": dish_data["dish_description"],
            "dish_description_en": dish_data["dish_description"],
            "dish_description_fr": dish_data["dish_description"],
            "country": "Argentinien",
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
        total_imported += 1
    
    argentina_count = await db.regional_pairings.count_documents({"country": "Argentinien"})
    print(f"\n  📊 Argentinien total: {argentina_count}")
    
    print("\n" + "="*60)
    print(f"🎉 IMPORT COMPLETE!")
    print(f"   ✅ Imported: {total_imported}")
    print(f"   ⏭️ Skipped: {total_skipped}")
    print(f"   🇹🇭 Thailand: {thailand_count}")
    print(f"   🇦🇷 Argentinien: {argentina_count}")
    print("="*60)
    
    client.close()


if __name__ == "__main__":
    asyncio.run(import_all())
