"""
Update Regional Pairings with detailed descriptions
Adds country intros, images, and detailed dish/wine descriptions
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

# Country data
COUNTRY_IMAGES = {
    "Italien": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/gzi6i1r1_WINE-PAIRING.ONLINE%20SOMMELIER%20CLAUDE%20%20IN%20ITALIEN.png",
    "Frankreich": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/2yyo7i5z_WINE-PAIRING.ONLINE%20SOMMELIER%20CLAUDE%20%20IN%20PARIS.png",
    "Spanien": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/nq1s1lxe_WINE-PAIRING.ONLINE%20SOMMELIER%20CLAUDE%20%20IN%20SPANIEN.png",
    "Österreich": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/p9jyplfk_WINE-PAIRING.ONLINE%20SOMMELIER%20CLAUDE%20%20IN%20AUSTRIA.png",
    "Schweiz": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/z46212mx_WINE-PAIRING.ONLINE%20SOMMELIER%20CLAUDE%20%20IN%20DER%20SCHWEIZ.png",
    "Griechenland": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/egu4qtad_GRIECHENLAND.png",
    "Türkei": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/8fnlvn47_WINE-PAIRING.ONLINE%20SOMMELIER%20CLAUDE%20%20IN%20T%C3%9CRKEI.png",
    "Japan": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/3w62amis_JAPAN.png",
    "Deutschland": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/udlwr19h_WINE-PAIRING.ONLINE%20SOMMELIER%20CLAUDE%20%20IN%20DEUTSCHLAND.png"
}

COUNTRY_INTROS = {
    "Italien": "🍝 Aperitivo all'italiana: Die Passion auf dem Teller. Italien ist mehr als Pizza und Pasta – es ist die Geburtsstätte der regionalen Küche, wo jede Stadt, jedes Dorf eine eigene, oft jahrhundertealte Spezialität hütet.",
    "Frankreich": "🥐 Cuisine Bourgeoise: Die Eleganz der Terroirs. Frankreich ist das unangefochtene Epizentrum der klassischen Küche und der Weinwelt. Hier treffen kulturelle Monumente wie eine Bresse-Poularde auf die größten Weine der Erde.",
    "Spanien": "💃 Fiesta del Sabor: Sonne, Tapas und intensive Aromen. Spanien ist ein Fest für die Sinne, das auf dem Teller die Hitze der Sonne und die Vielfalt der Regionen vereint.",
    "Österreich": "🏔️ Alpen-Eleganz: Knusprige Panade und lebendige Säure. Österreich bietet eine einzigartige Mischung aus alpiner Bodenständigkeit und kaiserlicher Eleganz.",
    "Schweiz": "🧀 Alpine Richesse: Bergkäse, Schmelz und verborgene Schätze. Die Schweiz ist ein Mosaik aus kulinarischen Einflüssen – geprägt von den Bergen, der Herzlichkeit und der Vielfalt ihrer Kulturen.",
    "Griechenland": "☀️ Ode an die Ägäis: Salzigkeit, Olivenöl und antike Aromen. Griechenland ist die Wiege der mediterranen Diät, eine Küche, die von der Salzigkeit des Meeres, dem duftenden Oregano und dem satten Olivenöl der Sonne lebt.",
    "Türkei": "🍢 Anatolische Glut: Rauch, Gewürz und die Brücke der Kulturen. Die Türkei ist ein kulinarisches Kraftwerk, das die reichen Aromen des Orients mit der Frische der Ägäis verbindet.",
    "Japan": "🥢 Umami-Meister: Präzision, Subtilität und die Kunst der Textur. Japan ist ein kulinarisches Universum der Subtilität und Perfektion. Die Küche lebt von der Magie des Umami.",
    "Deutschland": "🌲 Von der Riesling-Steillage zum Wirtshaus: Würze, Textur und Klarheit. Die deutsche Küche ist ein Fest der regionalen Identitäten."
}

# Detailed dish and wine descriptions
DISH_DESCRIPTIONS = {
    # Italien
    "Tartufo d'Alba (Weißer Trüffel)": "Der weiße Trüffel aus Alba ist eine der teuersten und begehrtesten Zutaten der Welt. Sein intensives, erdiges Aroma mit nussigen und knoblauchartigen Noten macht jedes Gericht zu einem außergewöhnlichen Erlebnis.",
    "Bistecca alla Fiorentina": "Ein mindestens 3cm dickes T-Bone-Steak vom Chianina-Rind, gegrillt über Holzkohle. Außen knusprig, innen saftig und rosa – ein Klassiker der toskanischen Küche.",
    "Pizza Napoletana": "Die neapolitanische Pizza mit ihrem luftigen, leicht verkohlten Rand und dem einfachen Belag aus Tomatensauce, Mozzarella und Basilikum ist UNESCO-Weltkulturerbe.",
    "Cannoli": "Knusprige, frittierte Teigrollen gefüllt mit süßer Ricotta-Creme, oft verfeinert mit Pistazien oder kandierten Früchten – ein sizilianischer Dessertklassiker.",
    "Polenta": "Cremiger Maisgriess, der als Beilage zu Schmorgerichten oder als eigenständiges Gericht serviert wird. In Venetien eine Institution.",
    "Carbonara": "Pasta mit einer Sauce aus Ei, Pecorino Romano, Guanciale (Schweinebacke) und schwarzem Pfeffer – römische Einfachheit in Perfektion.",
    "Parmigiano Reggiano": "Der 'König der Käse' reift mindestens 12 Monate und entwickelt kristalline Strukturen und komplexe nussige Aromen.",
    "Pesto alla Genovese": "Basilikum, Piniennüsse, Knoblauch, Parmigiano und Olivenöl – die grüne Seele Liguriens.",
    
    # Frankreich
    "Boeuf Bourguignon": "Rindfleisch geschmort in Burgunder-Rotwein mit Zwiebeln, Karotten, Speck und Champignons. Ein Gericht, das die Seele Burgunds einfängt.",
    "Bouillabaisse": "Die berühmte provenzalische Fischsuppe mit Safran, Fenchel und verschiedenen Mittelmeerfischen. Serviert mit Rouille und Baguette.",
    "Choucroute Garnie": "Elsässer Sauerkraut mit verschiedenen Fleischsorten und Würsten – ein herzhaftes Wintergericht.",
    "Confit de Canard": "Langsam in eigenem Fett gegarte Entenkeule – zart, saftig und voller Geschmack.",
    "Tarte Tatin": "Karamellisierter umgestürzter Apfelkuchen, warm serviert – eine süße Verführung aus der Loire.",
    
    # Spanien
    "Gazpacho": "Kalte andalusische Gemüsesuppe aus Tomaten, Paprika, Gurke und Knoblauch – erfrischend an heißen Sommertagen.",
    "Bacalao a la Vizcaína": "Baskischer Kabeljau in einer samtigen Paprikasauce – ein Meisterwerk der Meeresküche.",
    "Pulpo a la Gallega": "Galizischer Oktopus auf Kartoffeln mit Paprikapulver und Olivenöl – einfach und brillant.",
    "Suquet de Peix": "Katalanischer Fischeintopf mit Kartoffeln, Tomaten und Safran.",
    "Patatas a la Riojana": "Rioja-Kartoffel-Eintopf mit Chorizo und Paprika.",
    
    # Österreich
    "Wiener Schnitzel": "Hauchdünn geklopftes Kalbfleisch in goldbrauner Panade – knusprig, zart und eine Wiener Institution.",
    "Salzburger Nockerl": "Luftige Süßspeise aus Eischnee, die an die Salzburger Berge erinnert – eine süße Wolke.",
    "Steirisches Backhendl": "Knusprig gebratenes Huhn nach steirischer Art.",
    "Ganslbraten": "Festlicher Gänsebraten, traditionell zu Martini serviert.",
    
    # Schweiz
    "Walliser Raclette": "Geschmolzener Käse über Pellkartoffeln – alpiner Genuss pur.",
    "Bündner Gerstensuppe": "Kräftige Suppe mit Gerste und Gemüse aus Graubünden.",
    "Zürcher Geschnetzeltes": "Zartes Kalbfleisch in cremiger Rahmsauce mit Pilzen.",
    "Polenta Ticinese": "Tessin-Polenta, oft mit Schmorfleisch serviert.",
    
    # Griechenland
    "Tomatokeftedes": "Knusprige Tomatenpuffer aus Santorini mit Kräutern.",
    "Dakos": "Kretischer Gerstenzwieback mit Tomaten, Feta und Olivenöl.",
    "Moussaka": "Geschichteter Auflauf aus Auberginen, Hackfleisch und Béchamelsauce.",
    "Souvlaki": "Gegrillte Fleischspieße – griechisches Street Food.",
    
    # Japan
    "Edo-mae Sushi": "Traditionelles Tokio-Sushi mit frischem Fisch und perfekt gewürztem Reis.",
    "Okonomiyaki": "Herzhafter japanischer Pfannkuchen mit Kohl und verschiedenen Toppings.",
    "Miso Ramen": "Reichhaltige Nudelsuppe mit Miso-Brühe und verschiedenen Toppings.",
    
    # Deutschland
    "Pfälzer Saumagen": "Pfälzer Spezialität aus Schweinmagen gefüllt mit Kartoffeln und Fleisch.",
    "Fränkische Bratwurst": "Grobkörnige Bratwurst aus Franken, oft über Buchenholz gegrillt.",
    "Schweinshaxe": "Knusprige bayerische Schweinshaxe mit krosse Kruste.",
    "Himmel un Ääd": "Rheinische Spezialität aus Kartoffelpüree, Apfelmus und Blutwurst.",
    
    # Türkei
    "İskender Kebap": "Döner auf Fladenbrot mit Tomatensoße, Joghurt und zerlassener Butter.",
    "Zeytinyağlı Enginar": "In Olivenöl geschmorte Artischocken – ein Klassiker der türkischen Meze-Küche.",
    "Adana Kebap": "Scharfer Hackfleischspieß aus Adana, über Holzkohle gegrillt."
}

WINE_DESCRIPTIONS = {
    # Italien
    "Barolo oder Barbaresco": "Die beiden großen Nebbiolo-Weine des Piemonts. Kraftvoll, tanninreich und langlebig mit Aromen von Rosen, Teer und roten Früchten.",
    "Chianti Classico": "Sangiovese-Rotwein aus der Toskana mit Kirsch-Aromen, lebendiger Säure und eleganten Tanninen.",
    "Fiano di Avellino": "Mineralischer Weißwein aus Kampanien mit Noten von Haselnuss und Honig.",
    "Marsala Dolce": "Süßer Likörwein aus Sizilien, perfekt zu Desserts.",
    "Prosecco oder Amarone": "Prosecco: perlender Weißwein. Amarone: kraftvoller, getrockneter Rotwein aus Valpolicella.",
    "Frascati": "Frischer, unkomplizierter Weißwein aus Latium.",
    "Lambrusco": "Leicht schäumender, halbtrockener Rotwein aus der Emilia-Romagna.",
    "Pigato": "Aromatischer ligurischer Weißwein mit salziger Meeresnote.",
    
    # Frankreich
    "Pinot Noir aus Burgund": "Eleganter, komplexer Rotwein mit Aromen von roten Beeren, Erde und Gewürzen.",
    "Bandol Rosé": "Kraftvoller provenzalischer Rosé mit Struktur und Tiefe.",
    "Riesling": "Trockener Elsässer Riesling mit präziser Säure und mineralischen Noten.",
    "Saint-Émilion": "Bordeaux-Rotwein von der rechten Ufer, Merlot-dominiert, samtig und fruchtbetont.",
    "Vouvray Moelleux": "Süßer Chenin Blanc aus der Loire mit Honig- und Aprikosen-Aromen.",
    
    # Spanien
    "Fino Sherry": "Trockener, oxidativer Weißwein aus Jerez mit Mandel- und Hefenoten.",
    "Txakoli": "Leichter, leicht perlender baskischer Weißwein mit frischer Säure.",
    "Albariño": "Aromatischer galizischer Weißwein mit Pfirsich und Zitrus-Noten.",
    "Cava": "Spanischer Schaumwein nach traditioneller Methode.",
    "Rioja Crianza": "Tempranillo-Rotwein mit Eichenfass-Reifung, ausgewogen und zugänglich.",
    
    # Österreich
    "Grüner Veltliner": "Österreichs Klassiker – frisch, pfeffrig, mit guter Säure.",
    "Muskateller": "Aromatischer Weißwein mit Rosenduft.",
    "Sauvignon Blanc": "Steirischer Sauvignon mit Stachelbeere und Gras-Aromen.",
    "Blaufränkisch": "Kräftiger österreichischer Rotwein mit Kirsch und Gewürznoten.",
    
    # Schweiz
    "Fendant oder Petite Arvine": "Walliser Chasselas bzw. seltene alpine Weißwein-Rarität.",
    "Pinot Noir": "Schweizer Pinot Noir aus der Bündner Herrschaft.",
    "Chardonnay": "Eleganter Schweizer Chardonnay.",
    "Merlot del Ticino": "Tessiner Merlot mit südlicher Frucht.",
    
    # Griechenland
    "Assyrtiko": "Mineralischer Weißwein von Santorini mit salziger Note.",
    "Vidiano": "Aromatischer kretischer Weißwein.",
    "Xinomavro": "Tanninreicher griechischer Rotwein mit Alterungspotential.",
    "Agiorgitiko": "Samtiger Rotwein aus dem Peloponnes.",
    
    # Japan
    "Koshu": "Japanischer Weißwein, mineralisch und delikat.",
    "Prosecco oder Cava": "Perlweine, die zu herzhaften Pfannkuchen passen.",
    "Junmai Sake": "Vollmundiger Sake aus nur Reis, Wasser und Koji.",
    
    # Deutschland
    "Riesling": "Deutscher Riesling mit Steinobst, Zitrus und markanter Säure.",
    "Silvaner": "Erdiger, zurückhaltender fränkischer Weißwein.",
    "Spätburgunder": "Deutscher Pinot Noir mit Eleganz und Finesse.",
    
    # Türkei
    "Öküzgözü": "Mittelschwerer türkischer Rotwein mit Säure und Frucht.",
    "Emir": "Klarer, mineralischer türkischer Weißwein.",
    "Bornova Misketi": "Aromatischer türkischer Weißwein oder Rosé."
}


async def update_pairings():
    """Update all pairings with country intros, images, and descriptions"""
    
    print("🔄 Updating Regional Pairings with Details\n")
    print("=" * 60)
    
    # Update each country
    for country in COUNTRY_INTROS.keys():
        result = await db.regional_pairings.update_many(
            {"country": country},
            {
                "$set": {
                    "country_intro": COUNTRY_INTROS[country],
                    "country_image_url": COUNTRY_IMAGES.get(country)
                },
                "$unset": {"image_url": ""}  # Remove old field
            }
        )
        print(f"✓ Updated {result.modified_count} {country} pairings with intro & image")
    
    # Update dish descriptions
    updated_dishes = 0
    for dish_name, description in DISH_DESCRIPTIONS.items():
        result = await db.regional_pairings.update_many(
            {"dish": {"$regex": dish_name.split('(')[0].strip(), "$options": "i"}},
            {"$set": {"dish_description": description}}
        )
        if result.modified_count > 0:
            updated_dishes += result.modified_count
            print(f"  ✓ Added description to: {dish_name}")
    
    print(f"\n✅ Updated {updated_dishes} dishes with descriptions")
    
    # Update wine descriptions
    updated_wines = 0
    for wine_name, description in WINE_DESCRIPTIONS.items():
        result = await db.regional_pairings.update_many(
            {"wine_name": {"$regex": wine_name.split('(')[0].strip(), "$options": "i"}},
            {"$set": {"wine_description": description}}
        )
        if result.modified_count > 0:
            updated_wines += result.modified_count
            print(f"  ✓ Added wine description to: {wine_name}")
    
    print(f"\n✅ Updated {updated_wines} wines with descriptions")
    
    # Sample check
    sample = await db.regional_pairings.find_one({"dish": {"$regex": "Tartufo"}}, {"_id": 0})
    if sample:
        print(f"\n📍 Sample (Tartufo d'Alba):")
        print(f"   Dish Description: {sample.get('dish_description', 'N/A')[:80]}...")
        print(f"   Wine Description: {sample.get('wine_description', 'N/A')[:80]}...")
        print(f"   Country Intro: {sample.get('country_intro', 'N/A')[:80]}...")


async def main():
    await update_pairings()
    print("\n" + "=" * 60)
    print("✅ Update Complete!")


if __name__ == '__main__':
    asyncio.run(main())
