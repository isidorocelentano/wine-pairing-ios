"""
Improve wine recommendations with more specific details
Make recommendations more actionable and educational
"""
import asyncio
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# Improved wine recommendations with specific details
IMPROVEMENTS = [
    # JAPAN - Make all more specific
    {
        "match": {"country": "Japan", "dish": {"$regex": "Edo-mae Sushi"}},
        "update": {
            "wine_name": "Koshu (Grace Winery oder Château Mercian)",
            "wine_type": "Japanischer Weißwein aus Yamanashi",
            "wine_description": "Koshu ist Japans bedeutendste Weißwein-Rebsorte. Der mineralische, leichte Wein mit zarten Zitrus- und weißen Blütennoten passt perfekt zu rohem Fisch. Top-Produzenten: Grace Winery, Château Mercian, Lumière.",
            "wine_description_en": "Koshu is Japan's most important white wine grape. The mineral, light wine with delicate citrus and white flower notes pairs perfectly with raw fish. Top producers: Grace Winery, Château Mercian, Lumière.",
            "wine_description_fr": "Le Koshu est le cépage blanc le plus important du Japon. Le vin minéral et léger aux notes délicates d'agrumes et de fleurs blanches s'accorde parfaitement avec le poisson cru. Meilleurs producteurs: Grace Winery, Château Mercian, Lumière."
        }
    },
    {
        "match": {"country": "Japan", "dish": {"$regex": "Okonomiyaki"}},
        "update": {
            "wine_name": "Cava (Brut Nature) oder leichter Junmai Sake",
            "wine_type": "Schaumwein oder Sake",
            "wine_description": "Zu herzhaftem Okonomiyaki eignen sich trockene Schaumweine wie Cava Brut Nature oder ein leichter, fruchtiger Junmai Sake. Die Perlage schneidet durch die reichhaltigen Aromen von Kohl, Ei und Okonomiyaki-Sauce.",
            "wine_description_en": "For savory okonomiyaki, dry sparkling wines like Cava Brut Nature or a light, fruity Junmai Sake work well. The bubbles cut through the rich flavors of cabbage, egg and okonomiyaki sauce.",
            "wine_description_fr": "Pour l'okonomiyaki salé, les vins mousseux secs comme le Cava Brut Nature ou un Junmai Sake léger et fruité conviennent bien. Les bulles coupent les saveurs riches du chou, de l'œuf et de la sauce okonomiyaki."
        }
    },
    {
        "match": {"country": "Japan", "dish": {"$regex": "Miso Ramen"}},
        "update": {
            "wine_name": "Junmai Sake (mitteltrocken, z.B. Hakkaisan oder Dassai)",
            "wine_type": "Vollmundiger Sake aus Reis",
            "wine_description": "Zu kräftiger Miso-Ramen passt ein vollmundiger Junmai Sake perfekt. Der Sake sollte mitteltrocken sein (nicht zu süß) und Umami-Noten haben, die mit der Miso-Brühe harmonieren. Empfehlung: Hakkaisan Tokubetsu Junmai oder Dassai 45.",
            "wine_description_en": "A full-bodied Junmai Sake pairs perfectly with rich miso ramen. The sake should be semi-dry (not too sweet) and have umami notes that harmonize with the miso broth. Recommendation: Hakkaisan Tokubetsu Junmai or Dassai 45.",
            "wine_description_fr": "Un Junmai Sake corsé s'accorde parfaitement avec des ramen miso riches. Le sake doit être demi-sec (pas trop sucré) et avoir des notes umami qui s'harmonisent avec le bouillon miso. Recommandation: Hakkaisan Tokubetsu Junmai ou Dassai 45."
        }
    },
    
    # ITALIEN - Polenta clarification
    {
        "match": {"country": "Italien", "dish": {"$regex": "Polenta"}},
        "update": {
            "wine_name": "Prosecco (zu einfacher Polenta) oder Amarone (zu Schmorgerichten)",
            "wine_type": "Je nach Zubereitung: Schaumwein oder kraftvoller Rotwein",
            "wine_description": "Die Weinwahl hängt von der Zubereitung ab: Zu einfacher, cremiger Polenta passt ein frischer Prosecco Superiore. Wird die Polenta mit kräftigen Schmorgerichten (z.B. Ossobuco) serviert, ist ein Amarone della Valpolicella ideal – seine Frucht und Struktur harmonieren mit den intensiven Aromen.",
            "wine_description_en": "Wine choice depends on preparation: Fresh Prosecco Superiore pairs with simple, creamy polenta. When polenta is served with hearty braised dishes (e.g. ossobuco), Amarone della Valpolicella is ideal – its fruit and structure harmonize with the intense flavors.",
            "wine_description_fr": "Le choix du vin dépend de la préparation: Le Prosecco Superiore frais s'accorde avec la polenta simple et crémeuse. Lorsque la polenta est servie avec des plats braisés copieux (par ex. ossobuco), l'Amarone della Valpolicella est idéal – son fruit et sa structure s'harmonisent avec les saveurs intenses."
        }
    },
    
    # TÜRKEI - Make more specific
    {
        "match": {"country": "Türkei", "dish": {"$regex": "İskender Kebap"}},
        "update": {
            "wine_name": "Öküzgözü (Kavaklidere oder Doluca)",
            "wine_type": "Mittelschwerer türkischer Rotwein",
            "wine_description": "Öküzgözü ('Ochsenauge') ist eine autochthone türkische Rebsorte aus Elazığ. Der mittelschwere Rotwein mit lebendiger Säure und Kirsch-Aromen passt hervorragend zu gegrilltem Fleisch mit Tomatensoße. Empfohlene Produzenten: Kavaklidere, Doluca.",
            "wine_description_en": "Öküzgözü ('ox eye') is an indigenous Turkish grape variety from Elazığ. The medium-bodied red wine with lively acidity and cherry aromas pairs excellently with grilled meat in tomato sauce. Recommended producers: Kavaklidere, Doluca.",
            "wine_description_fr": "L'Öküzgözü ('œil de bœuf') est un cépage turc autochtone d'Elazığ. Le vin rouge de corps moyen avec une acidité vive et des arômes de cerise s'accorde excellemment avec la viande grillée en sauce tomate. Producteurs recommandés: Kavaklidere, Doluca."
        }
    },
    {
        "match": {"country": "Türkei", "dish": {"$regex": "Zeytinyağlı Enginar"}},
        "update": {
            "wine_name": "Emir (Cappadocia) oder Narince",
            "wine_type": "Trockener türkischer Weißwein",
            "wine_description": "Emir aus Kappadokien ist eine indigene Rebsorte mit markanter Mineralität und Zitrus-Aromen. Perfekt zu kalten Olivenöl-Gerichten. Als Alternative eignet sich auch Narince aus Tokat – beide bringen die nötige Frische und Säure für das mediterrane Gemüse.",
            "wine_description_en": "Emir from Cappadocia is an indigenous variety with pronounced minerality and citrus aromas. Perfect with cold olive oil dishes. Narince from Tokat is also suitable – both bring the necessary freshness and acidity for Mediterranean vegetables.",
            "wine_description_fr": "L'Emir de Cappadoce est un cépage indigène à la minéralité prononcée et aux arômes d'agrumes. Parfait avec les plats froids à l'huile d'olive. Le Narince de Tokat convient également – les deux apportent la fraîcheur et l'acidité nécessaires pour les légumes méditerranéens."
        }
    },
    {
        "match": {"country": "Türkei", "dish": {"$regex": "Adana Kebap"}},
        "update": {
            "wine_name": "Boğazkere (rot) oder Kalecik Karası (leichter)",
            "wine_type": "Türkischer Rotwein oder Rosé",
            "wine_description": "Zu scharfem Adana Kebap empfiehlt sich ein kräftiger Boğazkere mit Tannin-Struktur oder ein fruchtiger Kalecik Karası. Alternativ ein gekühlter türkischer Rosé (Bornova Misketi), dessen Frische die Schärfe mildert.",
            "wine_description_en": "For spicy Adana Kebap, a robust Boğazkere with tannic structure or a fruity Kalecik Karası is recommended. Alternatively, a chilled Turkish rosé (Bornova Misketi) whose freshness tempers the heat.",
            "wine_description_fr": "Pour l'Adana Kebap épicé, un Boğazkere robuste avec structure tannique ou un Kalecik Karası fruité est recommandé. Alternativement, un rosé turc rafraîchi (Bornova Misketi) dont la fraîcheur tempère le piquant."
        }
    },
    
    # GRIECHENLAND - Add producer recommendations
    {
        "match": {"country": "Griechenland", "dish": {"$regex": "Tomatokeftedes"}},
        "update": {
            "wine_name": "Assyrtiko (Santorini PDO, z.B. Gaia oder Sigalas)",
            "wine_type": "Mineralischer Weißwein von Santorini",
            "wine_description": "Assyrtiko von Santorini ist einer der besten Weißweine Griechenlands. Die alten Rebstöcke in vulkanischem Boden produzieren Weine mit intensiver Mineralität, Zitrus und salziger Meeresnote. Top-Erzeuger: Gaia Thalassitis, Sigalas, Santo Wines.",
            "wine_description_en": "Assyrtiko from Santorini is one of Greece's finest white wines. Old vines in volcanic soil produce wines with intense minerality, citrus and salty sea notes. Top producers: Gaia Thalassitis, Sigalas, Santo Wines.",
            "wine_description_fr": "L'Assyrtiko de Santorin est l'un des meilleurs vins blancs de Grèce. Les vieilles vignes dans un sol volcanique produisent des vins à la minéralité intense, aux agrumes et aux notes salines marines. Meilleurs producteurs: Gaia Thalassitis, Sigalas, Santo Wines."
        }
    },
    
    # DEUTSCHLAND - More specific regions
    {
        "match": {"country": "Deutschland", "dish": {"$regex": "Pfälzer Saumagen"}},
        "update": {
            "wine_name": "Riesling Pfalz (trocken, z.B. von Reichsrat von Buhl)",
            "wine_type": "Kräftiger, trockener Weißwein",
            "wine_description": "Zu dieser deftigen pfälzischen Spezialität gehört ein kräftiger, trockener Riesling aus der Pfalz. Die Säure schneidet durch die Fülle des Gerichts. Empfohlene Erzeuger: Reichsrat von Buhl, Dr. Bürklin-Wolf, Bassermann-Jordan.",
            "wine_description_en": "This hearty Palatinate specialty requires a powerful, dry Riesling from the Pfalz. The acidity cuts through the richness of the dish. Recommended producers: Reichsrat von Buhl, Dr. Bürklin-Wolf, Bassermann-Jordan.",
            "wine_description_fr": "Cette spécialité copieuse du Palatinat nécessite un Riesling puissant et sec du Pfalz. L'acidité coupe la richesse du plat. Producteurs recommandés: Reichsrat von Buhl, Dr. Bürklin-Wolf, Bassermann-Jordan."
        }
    }
]


async def improve_recommendations():
    """Apply improvements to wine recommendations"""
    
    print("🍷 Improving Wine Recommendations\n")
    print("=" * 80)
    
    total_improved = 0
    
    for improvement in IMPROVEMENTS:
        match = improvement["match"]
        update = improvement["update"]
        
        # Get the dish name for display
        if "dish" in match and "$regex" in match["dish"]:
            dish_name = match["dish"]["$regex"]
        else:
            dish_name = "Multiple"
        
        result = await db.regional_pairings.update_many(
            match,
            {"$set": update}
        )
        
        if result.modified_count > 0:
            total_improved += result.modified_count
            country = match.get("country", "?")
            new_wine = update.get("wine_name", "?")
            print(f"✓ {country}: {dish_name}")
            print(f"  → New: {new_wine}")
            print()
    
    print("=" * 80)
    print(f"✅ Improved {total_improved} wine recommendations")
    
    # Show examples
    print("\n📊 Sample Improvements:\n")
    
    # Japan example
    sushi = await db.regional_pairings.find_one(
        {"dish": {"$regex": "Edo-mae Sushi"}},
        {"_id": 0, "dish": 1, "wine_name": 1, "wine_type": 1}
    )
    if sushi:
        print("🇯🇵 Edo-mae Sushi:")
        print(f"   Wine: {sushi['wine_name']}")
        print(f"   Type: {sushi['wine_type']}")
        print()
    
    # Turkey example
    iskender = await db.regional_pairings.find_one(
        {"dish": {"$regex": "İskender"}},
        {"_id": 0, "dish": 1, "wine_name": 1, "wine_description": 1}
    )
    if iskender:
        print("🇹🇷 İskender Kebap:")
        print(f"   Wine: {iskender['wine_name']}")
        print(f"   Desc: {iskender['wine_description'][:80]}...")


async def main():
    await improve_recommendations()
    print("\n" + "=" * 80)


if __name__ == '__main__':
    asyncio.run(main())
