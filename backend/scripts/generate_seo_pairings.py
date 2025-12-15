"""
Programmatic SEO Pairing Generator
Generiert tausende einzigartige Wein-Speise-Paarungen für SEO-Landingpages
"""

import asyncio
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# Beliebte Gerichte für Pairings (erweiterte Liste)
POPULAR_DISHES = [
    # Deutsche Küche
    {"name_de": "Wiener Schnitzel", "name_en": "Wiener Schnitzel", "name_fr": "Escalope viennoise", "cuisine": "Österreichisch", "category": "Fleisch", "keywords": ["Kalb", "paniert", "Zitrone"]},
    {"name_de": "Sauerbraten", "name_en": "Sauerbraten", "name_fr": "Rôti mariné", "cuisine": "Deutsch", "category": "Fleisch", "keywords": ["Rind", "geschmort", "Soße"]},
    {"name_de": "Schweinebraten", "name_en": "Roast Pork", "name_fr": "Rôti de porc", "cuisine": "Deutsch", "category": "Fleisch", "keywords": ["Schwein", "Kruste", "Beilage"]},
    {"name_de": "Weißwurst", "name_en": "White Sausage", "name_fr": "Saucisse blanche", "cuisine": "Bayerisch", "category": "Fleisch", "keywords": ["Wurst", "Senf", "Brezel"]},
    
    # Italienische Küche
    {"name_de": "Spaghetti Carbonara", "name_en": "Spaghetti Carbonara", "name_fr": "Spaghetti Carbonara", "cuisine": "Italienisch", "category": "Pasta", "keywords": ["Pasta", "Speck", "Ei", "Parmesan"]},
    {"name_de": "Risotto Milanese", "name_en": "Risotto Milanese", "name_fr": "Risotto Milanais", "cuisine": "Italienisch", "category": "Reis", "keywords": ["Reis", "Safran", "Butter"]},
    {"name_de": "Ossobuco", "name_en": "Ossobuco", "name_fr": "Osso buco", "cuisine": "Italienisch", "category": "Fleisch", "keywords": ["Kalb", "geschmort", "Gremolata"]},
    {"name_de": "Lasagne", "name_en": "Lasagna", "name_fr": "Lasagnes", "cuisine": "Italienisch", "category": "Pasta", "keywords": ["Pasta", "Bolognese", "Béchamel"]},
    {"name_de": "Pizza Margherita", "name_en": "Pizza Margherita", "name_fr": "Pizza Margherita", "cuisine": "Italienisch", "category": "Pizza", "keywords": ["Tomate", "Mozzarella", "Basilikum"]},
    {"name_de": "Vitello Tonnato", "name_en": "Vitello Tonnato", "name_fr": "Vitello Tonnato", "cuisine": "Italienisch", "category": "Vorspeise", "keywords": ["Kalb", "Thunfisch", "Kapern"]},
    
    # Französische Küche
    {"name_de": "Coq au Vin", "name_en": "Coq au Vin", "name_fr": "Coq au Vin", "cuisine": "Französisch", "category": "Fleisch", "keywords": ["Huhn", "Rotwein", "Pilze"]},
    {"name_de": "Boeuf Bourguignon", "name_en": "Beef Bourguignon", "name_fr": "Boeuf Bourguignon", "cuisine": "Französisch", "category": "Fleisch", "keywords": ["Rind", "Rotwein", "geschmort"]},
    {"name_de": "Bouillabaisse", "name_en": "Bouillabaisse", "name_fr": "Bouillabaisse", "cuisine": "Französisch", "category": "Fisch", "keywords": ["Fisch", "Meeresfrüchte", "Safran"]},
    {"name_de": "Entenbrust", "name_en": "Duck Breast", "name_fr": "Magret de canard", "cuisine": "Französisch", "category": "Fleisch", "keywords": ["Ente", "rosa", "Sauce"]},
    {"name_de": "Ratatouille", "name_en": "Ratatouille", "name_fr": "Ratatouille", "cuisine": "Französisch", "category": "Vegetarisch", "keywords": ["Gemüse", "Provence", "Kräuter"]},
    
    # Spanische Küche
    {"name_de": "Paella", "name_en": "Paella", "name_fr": "Paella", "cuisine": "Spanisch", "category": "Reis", "keywords": ["Reis", "Meeresfrüchte", "Safran"]},
    {"name_de": "Tapas", "name_en": "Tapas", "name_fr": "Tapas", "cuisine": "Spanisch", "category": "Vorspeise", "keywords": ["Häppchen", "Oliven", "Schinken"]},
    {"name_de": "Gambas al Ajillo", "name_en": "Garlic Shrimp", "name_fr": "Gambas à l'ail", "cuisine": "Spanisch", "category": "Meeresfrüchte", "keywords": ["Garnelen", "Knoblauch", "Olivenöl"]},
    
    # Asiatische Küche
    {"name_de": "Sushi", "name_en": "Sushi", "name_fr": "Sushi", "cuisine": "Japanisch", "category": "Fisch", "keywords": ["Reis", "Fisch", "roh"]},
    {"name_de": "Pad Thai", "name_en": "Pad Thai", "name_fr": "Pad Thai", "cuisine": "Thailändisch", "category": "Nudeln", "keywords": ["Nudeln", "Erdnüsse", "süß-sauer"]},
    {"name_de": "Grünes Thai Curry", "name_en": "Green Thai Curry", "name_fr": "Curry vert thaï", "cuisine": "Thailändisch", "category": "Curry", "keywords": ["Kokosmilch", "scharf", "Kräuter"]},
    {"name_de": "Peking Ente", "name_en": "Peking Duck", "name_fr": "Canard laqué", "cuisine": "Chinesisch", "category": "Fleisch", "keywords": ["Ente", "knusprig", "Pfannkuchen"]},
    
    # Grill & BBQ
    {"name_de": "Ribeye Steak", "name_en": "Ribeye Steak", "name_fr": "Entrecôte", "cuisine": "International", "category": "Fleisch", "keywords": ["Rind", "gegrillt", "medium"]},
    {"name_de": "T-Bone Steak", "name_en": "T-Bone Steak", "name_fr": "T-Bone Steak", "cuisine": "International", "category": "Fleisch", "keywords": ["Rind", "gegrillt", "Knochen"]},
    {"name_de": "Lammkoteletts", "name_en": "Lamb Chops", "name_fr": "Côtelettes d'agneau", "cuisine": "Mediterran", "category": "Fleisch", "keywords": ["Lamm", "Rosmarin", "gegrillt"]},
    {"name_de": "Gegrillter Lachs", "name_en": "Grilled Salmon", "name_fr": "Saumon grillé", "cuisine": "International", "category": "Fisch", "keywords": ["Lachs", "gegrillt", "Zitrone"]},
    
    # Meeresfrüchte
    {"name_de": "Hummer", "name_en": "Lobster", "name_fr": "Homard", "cuisine": "International", "category": "Meeresfrüchte", "keywords": ["Hummer", "Butter", "Luxus"]},
    {"name_de": "Jakobsmuscheln", "name_en": "Scallops", "name_fr": "Coquilles Saint-Jacques", "cuisine": "Französisch", "category": "Meeresfrüchte", "keywords": ["Muscheln", "gebraten", "delikat"]},
    {"name_de": "Austern", "name_en": "Oysters", "name_fr": "Huîtres", "cuisine": "Französisch", "category": "Meeresfrüchte", "keywords": ["roh", "Zitrone", "Meer"]},
    {"name_de": "Calamari", "name_en": "Calamari", "name_fr": "Calamars", "cuisine": "Mediterran", "category": "Meeresfrüchte", "keywords": ["Tintenfisch", "frittiert", "Zitrone"]},
    
    # Käse
    {"name_de": "Käseplatte", "name_en": "Cheese Platter", "name_fr": "Plateau de fromages", "cuisine": "International", "category": "Käse", "keywords": ["Käse", "gemischt", "Trauben"]},
    {"name_de": "Fondue", "name_en": "Cheese Fondue", "name_fr": "Fondue au fromage", "cuisine": "Schweizer", "category": "Käse", "keywords": ["Käse", "geschmolzen", "Brot"]},
    {"name_de": "Raclette", "name_en": "Raclette", "name_fr": "Raclette", "cuisine": "Schweizer", "category": "Käse", "keywords": ["Käse", "Kartoffeln", "geschmolzen"]},
    
    # Vegetarisch
    {"name_de": "Gemüse-Risotto", "name_en": "Vegetable Risotto", "name_fr": "Risotto aux légumes", "cuisine": "Italienisch", "category": "Vegetarisch", "keywords": ["Reis", "Gemüse", "Parmesan"]},
    {"name_de": "Caprese Salat", "name_en": "Caprese Salad", "name_fr": "Salade Caprese", "cuisine": "Italienisch", "category": "Vegetarisch", "keywords": ["Tomate", "Mozzarella", "Basilikum"]},
    {"name_de": "Spinat-Ricotta Pasta", "name_en": "Spinach Ricotta Pasta", "name_fr": "Pâtes épinards ricotta", "cuisine": "Italienisch", "category": "Vegetarisch", "keywords": ["Pasta", "Spinat", "Ricotta"]},
    
    # Desserts
    {"name_de": "Tiramisu", "name_en": "Tiramisu", "name_fr": "Tiramisu", "cuisine": "Italienisch", "category": "Dessert", "keywords": ["Kaffee", "Mascarpone", "süß"]},
    {"name_de": "Crème Brûlée", "name_en": "Crème Brûlée", "name_fr": "Crème Brûlée", "cuisine": "Französisch", "category": "Dessert", "keywords": ["Vanille", "Karamell", "Sahne"]},
    {"name_de": "Schokoladenkuchen", "name_en": "Chocolate Cake", "name_fr": "Gâteau au chocolat", "cuisine": "International", "category": "Dessert", "keywords": ["Schokolade", "süß", "reichhaltig"]},
]

# Wein-Kategorien und ihre typischen Paarungen
WINE_PAIRING_RULES = {
    "Rotwein": {
        "ideal_for": ["Fleisch", "Pasta", "Käse", "Pizza"],
        "cuisines": ["Italienisch", "Französisch", "Spanisch", "Mediterran", "International"],
    },
    "Weißwein": {
        "ideal_for": ["Fisch", "Meeresfrüchte", "Vorspeise", "Vegetarisch", "Curry"],
        "cuisines": ["Französisch", "Japanisch", "Thailändisch", "Schweizer"],
    },
    "Roséwein": {
        "ideal_for": ["Vorspeise", "Vegetarisch", "Meeresfrüchte", "Pizza"],
        "cuisines": ["Französisch", "Spanisch", "Mediterran", "Italienisch"],
    },
    "Schaumwein": {
        "ideal_for": ["Meeresfrüchte", "Vorspeise", "Dessert"],
        "cuisines": ["Französisch", "International"],
    },
}

def create_slug(dish_name: str, wine_name: str) -> str:
    """Erstellt einen SEO-freundlichen Slug"""
    combined = f"{dish_name}-{wine_name}".lower()
    # Umlaute ersetzen
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'é': 'e', 'è': 'e', 'ê': 'e', 'à': 'a', 'â': 'a',
        'ô': 'o', 'î': 'i', 'ï': 'i', 'ç': 'c', 'ñ': 'n'
    }
    for old, new in replacements.items():
        combined = combined.replace(old, new)
    # Nur alphanumerische Zeichen und Bindestriche
    slug = re.sub(r'[^a-z0-9]+', '-', combined)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug[:100]  # Max 100 Zeichen

def get_wine_color_de(wine: dict) -> str:
    """Ermittelt die Weinfarbe auf Deutsch"""
    color = wine.get('wine_color', wine.get('type', '')).lower()
    if 'rot' in color or 'red' in color:
        return 'Rotwein'
    elif 'weiß' in color or 'weiss' in color or 'white' in color:
        return 'Weißwein'
    elif 'rosé' in color or 'rose' in color:
        return 'Roséwein'
    elif 'schaum' in color or 'sparkling' in color or 'sekt' in color or 'champagner' in color:
        return 'Schaumwein'
    return 'Rotwein'  # Default

def is_good_pairing(dish: dict, wine: dict) -> bool:
    """Prüft, ob Gericht und Wein gut zusammenpassen"""
    wine_color = get_wine_color_de(wine)
    rules = WINE_PAIRING_RULES.get(wine_color, {})
    
    dish_category = dish.get('category', '')
    dish_cuisine = dish.get('cuisine', '')
    
    # Prüfe ob die Kategorie oder Küche passt
    ideal_categories = rules.get('ideal_for', [])
    ideal_cuisines = rules.get('cuisines', [])
    
    category_match = any(cat in dish_category for cat in ideal_categories)
    cuisine_match = any(cuis in dish_cuisine for cuis in ideal_cuisines)
    
    return category_match or cuisine_match

def generate_pairing_description(dish: dict, wine: dict, lang: str = 'de') -> str:
    """Generiert eine Beschreibung für das Pairing"""
    wine_name = wine.get('name', wine.get('wine_name', 'Wein'))
    wine_region = wine.get('region', 'unbekannte Region')
    wine_color = get_wine_color_de(wine)
    dish_name = dish.get(f'name_{lang}', dish.get('name_de', ''))
    
    if lang == 'de':
        templates = [
            f"Der {wine_name} aus {wine_region} ist der perfekte Begleiter für {dish_name}. Die Aromen ergänzen sich harmonisch und schaffen ein unvergessliches Geschmackserlebnis.",
            f"Zu {dish_name} empfehlen wir diesen exzellenten {wine_color} aus {wine_region}. Die Kombination ist ein Klassiker der gehobenen Küche.",
            f"Ein {wine_name} passt hervorragend zu {dish_name}. Die Tannine und Fruchtaromen harmonieren perfekt mit den Geschmacksnoten des Gerichts.",
        ]
    elif lang == 'en':
        templates = [
            f"The {wine_name} from {wine_region} is the perfect companion for {dish_name}. The flavors complement each other harmoniously, creating an unforgettable taste experience.",
            f"For {dish_name}, we recommend this excellent wine from {wine_region}. This combination is a classic of fine dining.",
            f"A {wine_name} pairs beautifully with {dish_name}. The tannins and fruit aromas harmonize perfectly with the dish's flavor notes.",
        ]
    else:  # fr
        templates = [
            f"Le {wine_name} de {wine_region} est le compagnon parfait pour {dish_name}. Les saveurs se complètent harmonieusement, créant une expérience gustative inoubliable.",
            f"Pour {dish_name}, nous recommandons cet excellent vin de {wine_region}. Cette combinaison est un classique de la gastronomie.",
            f"Un {wine_name} s'accorde parfaitement avec {dish_name}. Les tanins et les arômes fruités s'harmonisent parfaitement avec les notes gustatives du plat.",
        ]
    
    import random
    return random.choice(templates)

async def generate_seo_pairings(limit: int = 500) -> list:
    """Generiert SEO-Paarungen aus Datenbank-Weinen und beliebten Gerichten"""
    
    print("🍷 Lade Weine aus der Datenbank...")
    
    # Lade Weine (nur mit Region und Name)
    wines = await db.public_wines.find(
        {"region": {"$exists": True, "$ne": ""}},
        {"_id": 0, "name": 1, "wine_name": 1, "region": 1, "country": 1, 
         "wine_color": 1, "type": 1, "grape_variety": 1, "grape": 1,
         "description_de": 1, "description_en": 1, "description_fr": 1}
    ).to_list(500)  # Max 500 Weine
    
    print(f"   Gefunden: {len(wines)} Weine")
    
    # Generiere Paarungen
    pairings = []
    used_slugs = set()
    
    for dish in POPULAR_DISHES:
        for wine in wines:
            # Prüfe ob gutes Pairing
            if not is_good_pairing(dish, wine):
                continue
            
            wine_name = wine.get('name', wine.get('wine_name', ''))
            if not wine_name:
                continue
            
            slug = create_slug(dish['name_de'], wine_name)
            
            # Überspringe Duplikate
            if slug in used_slugs:
                continue
            used_slugs.add(slug)
            
            # Erstelle Pairing-Objekt
            pairing = {
                "slug": slug,
                "dish": {
                    "name_de": dish['name_de'],
                    "name_en": dish['name_en'],
                    "name_fr": dish['name_fr'],
                    "cuisine": dish['cuisine'],
                    "category": dish['category'],
                    "keywords": dish['keywords']
                },
                "wine": {
                    "name": wine_name,
                    "region": wine.get('region', ''),
                    "country": wine.get('country', ''),
                    "color": get_wine_color_de(wine),
                    "grape": wine.get('grape_variety', wine.get('grape', '')),
                    "description_de": wine.get('description_de', ''),
                    "description_en": wine.get('description_en', ''),
                    "description_fr": wine.get('description_fr', '')
                },
                "pairing_description": {
                    "de": generate_pairing_description(dish, wine, 'de'),
                    "en": generate_pairing_description(dish, wine, 'en'),
                    "fr": generate_pairing_description(dish, wine, 'fr')
                },
                "seo": {
                    "title_de": f"{dish['name_de']} & {wine_name} - Perfektes Wein-Pairing",
                    "title_en": f"{dish['name_en']} & {wine_name} - Perfect Wine Pairing",
                    "title_fr": f"{dish['name_fr']} & {wine_name} - Accord Parfait",
                    "description_de": f"Entdecken Sie warum {wine_name} der ideale Weinbegleiter für {dish['name_de']} ist. Unser Sommelier erklärt die perfekte Kombination.",
                    "description_en": f"Discover why {wine_name} is the ideal wine pairing for {dish['name_en']}. Our sommelier explains the perfect combination.",
                    "description_fr": f"Découvrez pourquoi {wine_name} est l'accord parfait pour {dish['name_fr']}. Notre sommelier explique cette combinaison idéale.",
                    "keywords": dish['keywords'] + [wine_name, wine.get('region', ''), wine.get('country', '')]
                },
                "url": f"https://wine-pairing.online/pairing/{slug}",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "auto_generated": True
            }
            
            pairings.append(pairing)
            
            if len(pairings) >= limit:
                break
        
        if len(pairings) >= limit:
            break
    
    return pairings

async def save_pairings_to_db(pairings: list):
    """Speichert die generierten Paarungen in der Datenbank"""
    
    print(f"\n💾 Speichere {len(pairings)} Paarungen in der Datenbank...")
    
    # Lösche alte auto-generierte Pairings
    await db.seo_pairings.delete_many({"auto_generated": True})
    
    # Füge neue Pairings ein
    if pairings:
        result = await db.seo_pairings.insert_many(pairings)
        print(f"   ✅ {len(result.inserted_ids)} Paarungen gespeichert")
    
    # Erstelle Index für schnelle Suche
    await db.seo_pairings.create_index("slug", unique=True)
    await db.seo_pairings.create_index("dish.category")
    await db.seo_pairings.create_index("wine.region")
    
    print("   ✅ Indizes erstellt")

async def export_pairings_to_json(pairings: list):
    """Exportiert die Paarungen als JSON-Backup"""
    
    backup_path = ROOT_DIR / 'data' / 'seo_pairings.json'
    
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(pairings, f, ensure_ascii=False, indent=2)
    
    print(f"   ✅ Backup gespeichert: {backup_path}")

async def main():
    """Hauptfunktion"""
    
    print("=" * 60)
    print("🚀 PROGRAMMATIC SEO PAIRING GENERATOR")
    print("=" * 60)
    
    # Generiere Pairings
    pairings = await generate_seo_pairings(limit=500)
    
    print(f"\n📊 Generiert: {len(pairings)} einzigartige Paarungen")
    
    # Zeige Beispiele
    print("\n📋 Beispiele:")
    for p in pairings[:5]:
        print(f"   - /pairing/{p['slug']}")
        print(f"     {p['dish']['name_de']} + {p['wine']['name']}")
    
    # Speichere in DB
    await save_pairings_to_db(pairings)
    
    # Exportiere als JSON
    await export_pairings_to_json(pairings)
    
    print("\n" + "=" * 60)
    print("✅ FERTIG!")
    print(f"   {len(pairings)} SEO-Landingpages generiert")
    print("   URL-Muster: /pairing/{slug}")
    print("=" * 60)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
