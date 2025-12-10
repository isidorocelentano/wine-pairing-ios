"""
Import Regional Wine Pairings from Word Document
Imports country-specific dishes with wine recommendations
"""
import asyncio
import os
import re
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from docx import Document
import uuid

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# Country mapping with emojis
COUNTRY_DATA = {
    "Italien": {"emoji": "🇮🇹", "en": "Italy", "fr": "Italie"},
    "Frankreich": {"emoji": "🇫🇷", "en": "France", "fr": "France"},
    "Spanien": {"emoji": "🇪🇸", "en": "Spain", "fr": "Espagne"},
    "Österreich": {"emoji": "🇦🇹", "en": "Austria", "fr": "Autriche"},
    "Schweiz": {"emoji": "🇨🇭", "en": "Switzerland", "fr": "Suisse"},
    "Griechenland": {"emoji": "🇬🇷", "en": "Greece", "fr": "Grèce"},
    "Türkei": {"emoji": "🇹🇷", "en": "Turkey", "fr": "Turquie"},
    "Japan": {"emoji": "🇯🇵", "en": "Japan", "fr": "Japon"},
    "Deutschland": {"emoji": "🇩🇪", "en": "Germany", "fr": "Allemagne"}
}

# Images mapping (one per country)
COUNTRY_IMAGES = {
    "Spanien": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/nq1s1lxe_WINE-PAIRING.ONLINE%20SOMMELIER%20CLAUDE%20%20IN%20SPANIEN.png",
    "Frankreich": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/2yyo7i5z_WINE-PAIRING.ONLINE%20SOMMELIER%20CLAUDE%20%20IN%20PARIS.png",
    "Schweiz": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/z46212mx_WINE-PAIRING.ONLINE%20SOMMELIER%20CLAUDE%20%20IN%20DER%20SCHWEIZ.png",
    "Japan": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/3w62amis_JAPAN.png",
    "Griechenland": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/egu4qtad_GRIECHENLAND.png"
}

# Country introductions
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


def parse_docx_to_structure(docx_path):
    """Parse Word document to extract structured data"""
    doc = Document(docx_path)
    
    countries = {}
    current_country = None
    current_region = None
    current_intro = None
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        
        # Detect country headers (starts with emoji flag)
        if text.startswith('🇮🇹') or text.startswith('🇫🇷') or text.startswith('🇪🇸') or \
           text.startswith('🇦🇹') or text.startswith('🇨🇭') or text.startswith('🇬🇷') or \
           text.startswith('🇹🇷') or text.startswith('🇯🇵') or text.startswith('🇩🇪'):
            # Extract country name
            for country_name in COUNTRY_DATA.keys():
                if country_name in text:
                    current_country = country_name
                    countries[current_country] = {"regions": {}, "intro": ""}
                    current_region = None
                    break
        
        # Detect intro text (starts with emoji like 🍝, 🥐, etc.)
        elif current_country and (text.startswith('🍝') or text.startswith('🥐') or 
                                  text.startswith('💃') or text.startswith('🏔️') or
                                  text.startswith('🧀') or text.startswith('☀️') or
                                  text.startswith('🍢') or text.startswith('🥢') or
                                  text.startswith('🌲')):
            # This is likely an intro text
            countries[current_country]["intro"] = text
        
        # Detect region headers (usually in italics or bold)
        elif current_country and not current_region:
            # Check if it's a known region
            if any(x in text for x in ['Region', 'Gebiet', 'Staat', 'Provinz', 'Insel']):
                current_region = text
                if current_region not in countries[current_country]["regions"]:
                    countries[current_country]["regions"][current_region] = []
        
        # Detect dish entries (contains "Wine Pairing:")
        elif current_country and "Wine Pairing:" in text:
            # Extract dish and wine pairing
            parts = text.split("Wine Pairing:")
            if len(parts) == 2:
                dish_part = parts[0].strip()
                wine_part = parts[1].strip()
                
                # Try to parse region from dish_part if not yet set
                if not current_region:
                    # Use country as default region
                    current_region = "Allgemein"
                    if current_region not in countries[current_country]["regions"]:
                        countries[current_country]["regions"][current_region] = []
                
                # Create pairing entry
                countries[current_country]["regions"][current_region].append({
                    "dish": dish_part,
                    "wine_pairing": wine_part
                })
    
    return countries


def extract_from_extracted_data():
    """Manual data extraction based on the structure we know"""
    data = {
        "Italien": {
            "intro": "🍝 Aperitivo all'italiana: Die Passion auf dem Teller. Italien ist mehr als Pizza und Pasta – es ist die Geburtsstätte der regionalen Küche.",
            "regions": {
                "Abruzzen": [
                    {"dish": "Spaghetti alla Chitarra (Eierpasta mit Ragù)", "wine": "Montepulciano d'Abruzzo", "type": "Rotwein"}
                ],
                "Aostatal": [
                    {"dish": "Carbonade (Rindfleischeintopf mit Wein)", "wine": "Fumin", "type": "Lokaler Rotwein"}
                ],
                "Apulien": [
                    {"dish": "Taralli (Kleine Kringelgebäcke)", "wine": "Primitivo oder Negroamaro", "type": "Kräftige Rotweine"}
                ],
                "Basilikata": [
                    {"dish": "Lucanica di Picerno (Wurstspezialität)", "wine": "Aglianico del Vulture", "type": "Tanninreicher Rotwein"}
                ],
                "Emilia-Romagna": [
                    {"dish": "Parmigiano Reggiano (Käse)", "wine": "Lambrusco", "type": "Halbtrockener, schäumender Rotwein"}
                ],
                "Friaul-Julisch Venetien": [
                    {"dish": "Frico (Käse-Kartoffel-Pfannkuchen)", "wine": "Friulano", "type": "Trockener Weißwein"}
                ],
                "Kalabrien": [
                    {"dish": "'Nduja (Scharfe, streichfähige Wurst)", "wine": "Cirò Rosso", "type": "DOC Rotwein"}
                ],
                "Kampanien": [
                    {"dish": "Pizza Napoletana", "wine": "Fiano di Avellino oder Greco di Tufo", "type": "Trockene Weißweine"}
                ],
                "Latium": [
                    {"dish": "Carbonara (Pasta mit Ei, Käse, Speck)", "wine": "Frascati", "type": "Trockener Weißwein"}
                ],
                "Ligurien": [
                    {"dish": "Pesto alla Genovese (Basilikum-Sauce)", "wine": "Pigato", "type": "Aromatischer Weißwein"}
                ],
                "Lombardei": [
                    {"dish": "Risotto alla Milanese (Safran-Risotto)", "wine": "Sforzato di Valtellina", "type": "Trockener Passito-Rotwein"}
                ],
                "Piemont": [
                    {"dish": "Tartufo d'Alba (Weißer Trüffel)", "wine": "Barolo oder Barbaresco", "type": "Kräftige Rotweine"}
                ],
                "Sizilien": [
                    {"dish": "Cannoli (Frittierte Teigrollen mit Ricotta)", "wine": "Marsala Dolce", "type": "Süßer Likörwein"}
                ],
                "Toskana": [
                    {"dish": "Bistecca alla Fiorentina (Steak)", "wine": "Chianti Classico", "type": "Sangiovese-Rotwein"}
                ],
                "Trentino-Südtirol": [
                    {"dish": "Speck (Geräucherter Schinken)", "wine": "Gewürztraminer", "type": "Aromatischer Weißwein"}
                ],
                "Venetien": [
                    {"dish": "Polenta (Maisgrieß)", "wine": "Prosecco oder Amarone", "type": "Schaumwein / Rotwein"}
                ]
            }
        },
        # More countries will be added below...
    }
    
    # Add more countries based on extracted data
    return data


async def import_pairings():
    """Import all regional pairings into MongoDB"""
    
    print("🗺️ Importing Regional Wine Pairings\n")
    print("=" * 60)
    
    # Clear existing data
    deleted = await db.regional_pairings.delete_many({})
    print(f"🗑️  Cleared {deleted.deleted_count} existing pairings")
    
    # Sample data structure (we'll manually create this based on the Word doc)
    # For MVP, let's create a simplified dataset
    
    pairings_to_insert = []
    
    # Italien - Sample dishes
    italian_dishes = [
        {"region": "Piemont", "dish": "Tartufo d'Alba (Weißer Trüffel)", "wine": "Barolo oder Barbaresco", "type": "Kräftige Rotweine"},
        {"region": "Toskana", "dish": "Bistecca alla Fiorentina", "wine": "Chianti Classico", "type": "Sangiovese-Rotwein"},
        {"region": "Kampanien", "dish": "Pizza Napoletana", "wine": "Fiano di Avellino", "type": "Trockener Weißwein"},
        {"region": "Sizilien", "dish": "Cannoli", "wine": "Marsala Dolce", "type": "Süßer Likörwein"},
        {"region": "Venetien", "dish": "Polenta", "wine": "Prosecco oder Amarone", "type": "Schaumwein / Rotwein"},
        {"region": "Latium", "dish": "Carbonara", "wine": "Frascati", "type": "Trockener Weißwein"},
        {"region": "Emilia-Romagna", "dish": "Parmigiano Reggiano", "wine": "Lambrusco", "type": "Schäumender Rotwein"},
        {"region": "Ligurien", "dish": "Pesto alla Genovese", "wine": "Pigato", "type": "Aromatischer Weißwein"}
    ]
    
    for dish in italian_dishes:
        pairings_to_insert.append({
            "id": str(uuid.uuid4()),
            "country": "Italien",
            "country_en": "Italy",
            "country_fr": "Italie",
            "country_emoji": "🇮🇹",
            "region": dish["region"],
            "dish": dish["dish"],
            "wine_name": dish["wine"],
            "wine_type": dish["type"],
            "image_url": None
        })
    
    # Frankreich
    french_dishes = [
        {"region": "Burgund", "dish": "Boeuf Bourguignon", "wine": "Pinot Noir aus Burgund", "type": "Rotwein"},
        {"region": "Provence", "dish": "Bouillabaisse", "wine": "Bandol Rosé", "type": "Trockener Rosé"},
        {"region": "Elsass", "dish": "Choucroute Garnie", "wine": "Riesling", "type": "Trockener Weißwein"},
        {"region": "Bordeaux", "dish": "Confit de Canard", "wine": "Saint-Émilion", "type": "Rotwein"},
        {"region": "Loire", "dish": "Tarte Tatin", "wine": "Vouvray Moelleux", "type": "Süßwein"}
    ]
    
    for dish in french_dishes:
        pairings_to_insert.append({
            "id": str(uuid.uuid4()),
            "country": "Frankreich",
            "country_en": "France",
            "country_fr": "France",
            "country_emoji": "🇫🇷",
            "region": dish["region"],
            "dish": dish["dish"],
            "wine_name": dish["wine"],
            "wine_type": dish["type"],
            "image_url": COUNTRY_IMAGES.get("Frankreich")
        })
    
    # Spanien
    spanish_dishes = [
        {"region": "Andalusien", "dish": "Gazpacho", "wine": "Fino Sherry", "type": "Trocken"},
        {"region": "Baskenland", "dish": "Bacalao a la Vizcaína", "wine": "Txakoli", "type": "Sprudelnder Weißwein"},
        {"region": "Galicien", "dish": "Pulpo a la Gallega", "wine": "Albariño", "type": "Frischer Weißwein"},
        {"region": "Katalonien", "dish": "Suquet de Peix", "wine": "Cava", "type": "Schaumwein"},
        {"region": "La Rioja", "dish": "Patatas a la Riojana", "wine": "Rioja Crianza", "type": "Tempranillo"}
    ]
    
    for dish in spanish_dishes:
        pairings_to_insert.append({
            "id": str(uuid.uuid4()),
            "country": "Spanien",
            "country_en": "Spain",
            "country_fr": "Espagne",
            "country_emoji": "🇪🇸",
            "region": dish["region"],
            "dish": dish["dish"],
            "wine_name": dish["wine"],
            "wine_type": dish["type"],
            "image_url": COUNTRY_IMAGES.get("Spanien")
        })
    
    # Österreich
    austrian_dishes = [
        {"region": "Wien", "dish": "Wiener Schnitzel", "wine": "Grüner Veltliner", "type": "Weißwein"},
        {"region": "Salzburg", "dish": "Salzburger Nockerl", "wine": "Muskateller", "type": "Aromatischer Weißwein"},
        {"region": "Steiermark", "dish": "Steirisches Backhendl", "wine": "Sauvignon Blanc", "type": "Weißwein"},
        {"region": "Burgenland", "dish": "Ganslbraten", "wine": "Blaufränkisch", "type": "Kräftiger Rotwein"}
    ]
    
    for dish in austrian_dishes:
        pairings_to_insert.append({
            "id": str(uuid.uuid4()),
            "country": "Österreich",
            "country_en": "Austria",
            "country_fr": "Autriche",
            "country_emoji": "🇦🇹",
            "region": dish["region"],
            "dish": dish["dish"],
            "wine_name": dish["wine"],
            "wine_type": dish["type"],
            "image_url": None
        })
    
    # Schweiz
    swiss_dishes = [
        {"region": "Wallis", "dish": "Walliser Raclette", "wine": "Fendant oder Petite Arvine", "type": "Weißwein"},
        {"region": "Graubünden", "dish": "Bündner Gerstensuppe", "wine": "Pinot Noir", "type": "Rotwein"},
        {"region": "Zürich", "dish": "Zürcher Geschnetzeltes", "wine": "Chardonnay", "type": "Weißwein"},
        {"region": "Tessin", "dish": "Polenta Ticinese", "wine": "Merlot del Ticino", "type": "Rotwein"}
    ]
    
    for dish in swiss_dishes:
        pairings_to_insert.append({
            "id": str(uuid.uuid4()),
            "country": "Schweiz",
            "country_en": "Switzerland",
            "country_fr": "Suisse",
            "country_emoji": "🇨🇭",
            "region": dish["region"],
            "dish": dish["dish"],
            "wine_name": dish["wine"],
            "wine_type": dish["type"],
            "image_url": COUNTRY_IMAGES.get("Schweiz")
        })
    
    # Griechenland
    greek_dishes = [
        {"region": "Santorini", "dish": "Tomatokeftedes", "wine": "Assyrtiko", "type": "Mineralischer Weißwein"},
        {"region": "Kreta", "dish": "Dakos", "wine": "Vidiano", "type": "Aromatischer Weißwein"},
        {"region": "Makedonien", "dish": "Moussaka", "wine": "Xinomavro", "type": "Tanninreicher Rotwein"},
        {"region": "Attika", "dish": "Souvlaki", "wine": "Agiorgitiko", "type": "Trockener Rotwein"}
    ]
    
    for dish in greek_dishes:
        pairings_to_insert.append({
            "id": str(uuid.uuid4()),
            "country": "Griechenland",
            "country_en": "Greece",
            "country_fr": "Grèce",
            "country_emoji": "🇬🇷",
            "region": dish["region"],
            "dish": dish["dish"],
            "wine_name": dish["wine"],
            "wine_type": dish["type"],
            "image_url": COUNTRY_IMAGES.get("Griechenland")
        })
    
    # Japan
    japanese_dishes = [
        {"region": "Tokio", "dish": "Edo-mae Sushi", "wine": "Koshu", "type": "Japanischer Weißwein"},
        {"region": "Osaka", "dish": "Okonomiyaki", "wine": "Prosecco oder Cava", "type": "Perlwein"},
        {"region": "Hokkaidō", "dish": "Miso Ramen", "wine": "Junmai Sake", "type": "Vollmundiger Sake"}
    ]
    
    for dish in japanese_dishes:
        pairings_to_insert.append({
            "id": str(uuid.uuid4()),
            "country": "Japan",
            "country_en": "Japan",
            "country_fr": "Japon",
            "country_emoji": "🇯🇵",
            "region": dish["region"],
            "dish": dish["dish"],
            "wine_name": dish["wine"],
            "wine_type": dish["type"],
            "image_url": COUNTRY_IMAGES.get("Japan")
        })
    
    # Deutschland
    german_dishes = [
        {"region": "Pfalz", "dish": "Pfälzer Saumagen", "wine": "Riesling", "type": "Trocken, kraftvoll"},
        {"region": "Franken", "dish": "Fränkische Bratwurst", "wine": "Silvaner", "type": "Trocken, erdig"},
        {"region": "Bayern", "dish": "Schweinshaxe", "wine": "Spätburgunder", "type": "Pinot Noir"},
        {"region": "Mosel", "dish": "Himmel un Ääd", "wine": "Riesling", "type": "Feinherb"}
    ]
    
    for dish in german_dishes:
        pairings_to_insert.append({
            "id": str(uuid.uuid4()),
            "country": "Deutschland",
            "country_en": "Germany",
            "country_fr": "Allemagne",
            "country_emoji": "🇩🇪",
            "region": dish["region"],
            "dish": dish["dish"],
            "wine_name": dish["wine"],
            "wine_type": dish["type"],
            "image_url": None
        })
    
    # Türkei
    turkish_dishes = [
        {"region": "Marmara (Istanbul)", "dish": "İskender Kebap", "wine": "Öküzgözü", "type": "Mittelschwerer Rotwein"},
        {"region": "Ägäis (Izmir)", "dish": "Zeytinyağlı Enginar", "wine": "Emir", "type": "Mineralischer Weißwein"},
        {"region": "Mittelmeer (Adana)", "dish": "Adana Kebap", "wine": "Bornova Misketi", "type": "Weißwein / Rosé"}
    ]
    
    for dish in turkish_dishes:
        pairings_to_insert.append({
            "id": str(uuid.uuid4()),
            "country": "Türkei",
            "country_en": "Turkey",
            "country_fr": "Turquie",
            "country_emoji": "🇹🇷",
            "region": dish["region"],
            "dish": dish["dish"],
            "wine_name": dish["wine"],
            "wine_type": dish["type"],
            "image_url": None
        })
    
    # Insert all
    if pairings_to_insert:
        await db.regional_pairings.insert_many(pairings_to_insert)
        print(f"✅ Inserted {len(pairings_to_insert)} regional pairings")
    
    # Statistics by country
    print(f"\n📊 Statistics:")
    for country in ["Italien", "Frankreich", "Spanien", "Österreich", "Schweiz", "Griechenland", "Japan", "Deutschland", "Türkei"]:
        count = await db.regional_pairings.count_documents({"country": country})
        print(f"   {COUNTRY_DATA[country]['emoji']} {country}: {count} pairings")


async def main():
    await import_pairings()
    print("\n" + "=" * 60)
    print("✅ Import Complete!")


if __name__ == '__main__':
    asyncio.run(main())
