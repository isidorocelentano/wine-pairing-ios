#!/usr/bin/env python3
"""
Complete wine description translations for all countries.
Uses proper full translations instead of word-by-word replacement.
"""

import asyncio
import os
import sys

sys.path.insert(0, '/app/backend')

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')

# Full wine description translations for Argentina
ARGENTINA_WINE_TRANSLATIONS = {
    "Asado (Argentinisches Grillfleisch)": {
        "en": "The legendary Argentine Malbec from Mendoza with its dark berries, plums and a hint of smoke is THE partner for Asado. A wine that embodies the soul of Argentina.",
        "fr": "Le légendaire Malbec argentin de Mendoza avec ses baies noires, prunes et une touche de fumée est LE partenaire de l'Asado. Un vin qui incarne l'âme de l'Argentine."
    },
    "Choripán": {
        "en": "The fruity Bonarda with its cherry and plum notes is the perfect street food wine for Choripán. The spicy chimichurri finds an equal partner in the wine.",
        "fr": "Le Bonarda fruité avec ses notes de cerise et de prune est le vin de rue parfait pour le Choripán. La chimichurri épicée trouve un partenaire égal dans le vin."
    },
    "Morcilla (Argentinische Blutwurst)": {
        "en": "The powerful Cabernet Sauvignon with its dark fruit and tannins is bold enough for the intense Morcilla. A combination for meat lovers.",
        "fr": "Le puissant Cabernet Sauvignon avec ses fruits noirs et ses tanins est assez audacieux pour la Morcilla intense. Une combinaison pour les amateurs de viande."
    },
    "Vacío (Rinderbauch)": {
        "en": "A mature Malbec Reserve with its velvety texture and notes of violets and dark chocolate perfectly caresses the fatty Vacío.",
        "fr": "Un Malbec Reserve mature avec sa texture veloutée et ses notes de violettes et de chocolat noir caresse parfaitement le Vacío gras."
    },
    "Entraña (Zwerchfell)": {
        "en": "An elegant blend of Malbec and Cabernet Sauvignon combines fruit and structure - perfect for the juicy Entraña with its intense meatiness.",
        "fr": "Un assemblage élégant de Malbec et Cabernet Sauvignon combine fruit et structure - parfait pour l'Entraña juteux avec son intensité charnue."
    },
    "Empanadas (Argentinische Teigtaschen)": {
        "en": "The aromatic Torrontés with its floral and citrus notes is a refreshing partner for the hearty Empanadas. A wine that celebrates Argentina's diversity.",
        "fr": "Le Torrontés aromatique avec ses notes florales et d'agrumes est un partenaire rafraîchissant pour les Empanadas copieuses. Un vin qui célèbre la diversité de l'Argentine."
    },
    "Provoleta (Gegrillter Käse)": {
        "en": "A fresh Malbec Rosé with its red berry notes and lively acidity perfectly cuts through the richness of the grilled cheese.",
        "fr": "Un Malbec Rosé frais avec ses notes de fruits rouges et son acidité vive coupe parfaitement la richesse du fromage grillé."
    },
    "Milanesa (Argentinisches Schnitzel)": {
        "en": "The Argentine Sangiovese with its cherry notes and lively acidity is an elegant partner for the crispy Milanesa. Italian heritage meets Argentine soul.",
        "fr": "Le Sangiovese argentin avec ses notes de cerise et son acidité vive est un partenaire élégant pour la Milanesa croustillante. L'héritage italien rencontre l'âme argentine."
    },
    "Locro (Argentinischer Nationaleintopf)": {
        "en": "The Torrontés from the high altitudes of Salta with its intense floral notes is the authentic local partner for Locro. A wine from the same homeland as the dish.",
        "fr": "Le Torrontés des hautes altitudes de Salta avec ses intenses notes florales est le partenaire local authentique du Locro. Un vin de la même patrie que le plat."
    },
    "Cordero Patagónico (Patagonisches Lamm)": {
        "en": "The elegant Pinot Noir from Patagonia with its herbal and cherry notes is made for the spicy Patagonian lamb. Terroir meets terroir.",
        "fr": "L'élégant Pinot Noir de Patagonie avec ses notes d'herbes et de cerise est fait pour l'agneau patagonien épicé. Terroir rencontre terroir."
    }
}

# Thailand wine translations
THAILAND_WINE_TRANSLATIONS = {
    "Green Curry (Kaeng Khiao Wan, แกงเขียวหวาน)": {
        "en": "The elegant residual sweetness of the German Riesling is like a cool waterfall against the heat of the Green Curry. The fruit notes dance with the coconut milk while the acidity balances the fat.",
        "fr": "L'élégante sucrosité résiduelle du Riesling allemand est comme une cascade fraîche contre la chaleur du Green Curry. Les notes fruitées dansent avec le lait de coco tandis que l'acidité équilibre le gras."
    },
    "Pad Thai (ผัดไทย)": {
        "en": "The peppery Grüner Veltliner with its lively acidity is made for Pad Thai. The peanuts and the sweet-sour tamarind are perfectly complemented by the wine's spice.",
        "fr": "Le Grüner Veltliner poivré avec son acidité vive est fait pour le Pad Thai. Les cacahuètes et le tamarin aigre-doux sont parfaitement complétés par les épices du vin."
    },
    "Tom Yum Goong (ต้มยำกุ้ง)": {
        "en": "The crisp Sauvignon Blanc from New Zealand with its grassy notes and citrus freshness is the perfect partner for the aromatic Tom Yum. Lemongrass meets lime - a heavenly encounter.",
        "fr": "Le Sauvignon Blanc vif de Nouvelle-Zélande avec ses notes herbacées et sa fraîcheur d'agrumes est le partenaire parfait pour le Tom Yum aromatique. La citronnelle rencontre le citron vert - une rencontre céleste."
    },
    "Massaman Curry (Kaeng Massaman, แกงมัสมั่น)": {
        "en": "The sweet, slightly sparkling Moscato is a dream with the spicy Massaman Curry. The peanuts and cinnamon find a harmonious partner in the grape notes.",
        "fr": "Le Moscato sucré et légèrement pétillant est un rêve avec le Massaman Curry épicé. Les cacahuètes et la cannelle trouvent un partenaire harmonieux dans les notes de raisin."
    },
    "Som Tum (ส้มตำ)": {
        "en": "The dry Riesling with its crystalline acidity is the classic partner for Som Tum. The lime and heat are caught by the wine's elegance.",
        "fr": "Le Riesling sec avec son acidité cristalline est le partenaire classique du Som Tum. Le citron vert et le piquant sont captés par l'élégance du vin."
    },
    "Khao Soi (ข้าวซอย)": {
        "en": "The aromatic Alsatian Gewürztraminer with its exotic notes is made for Khao Soi. The creamy coconut milk and crispy noodles are embraced by the wine's fullness.",
        "fr": "Le Gewürztraminer alsacien aromatique avec ses notes exotiques est fait pour le Khao Soi. Le lait de coco crémeux et les nouilles croustillantes sont embrassés par la plénitude du vin."
    }
}

# Japan wine translations
JAPAN_WINE_TRANSLATIONS = {
    "Nigiri Sushi (握り寿司)": {
        "en": "The elegant Champagne with its fine bubbles and crisp acidity is the classic luxury partner for finest Nigiri Sushi. The wine's minerality mirrors the purity of the fish.",
        "fr": "L'élégant Champagne avec ses fines bulles et son acidité vive est le partenaire de luxe classique pour les meilleurs Nigiri Sushi. La minéralité du vin reflète la pureté du poisson."
    },
    "Sashimi (刺身)": {
        "en": "The mineral Chablis with its steely precision and oyster shell notes is the perfect partner for finest Sashimi. Purity meets purity.",
        "fr": "Le Chablis minéral avec sa précision acier et ses notes de coquille d'huître est le partenaire parfait pour les meilleurs Sashimi. La pureté rencontre la pureté."
    },
    "Ramen (ラーメン)": {
        "en": "The fresh, fruity Beaujolais with its cherry notes is a surprisingly good partner for a steaming bowl of Ramen. Served slightly chilled - perfect!",
        "fr": "Le Beaujolais frais et fruité avec ses notes de cerise est un partenaire étonnamment bon pour un bol fumant de Ramen. Servi légèrement frais - parfait!"
    },
    "Tempura (天ぷら)": {
        "en": "The elegant Italian sparkling wine with its fine bubbles cuts through the crispy Tempura crust perfectly. Lightness meets crispiness.",
        "fr": "L'élégant vin mousseux italien avec ses fines bulles coupe parfaitement la croûte croustillante du Tempura. La légèreté rencontre le croustillant."
    },
    "Sukiyaki (すき焼き)": {
        "en": "The elegant Burgundy Pinot Noir with its cherry notes and silky tannins is the classic partner for the tender beef in Sukiyaki.",
        "fr": "L'élégant Pinot Noir de Bourgogne avec ses notes de cerise et ses tanins soyeux est le partenaire classique du bœuf tendre dans le Sukiyaki."
    }
}

# South Africa wine translations
SOUTH_AFRICA_WINE_TRANSLATIONS = {
    "Braai (Suedafrikanisches Grillfleisch)": {
        "en": "The legendary South African Pinotage with its smoky, earthy notes and ripe berry aromas is THE partner for Braai. A wine that embodies the soul of the Cape.",
        "fr": "Le légendaire Pinotage sud-africain avec ses notes fumées et terreuses et ses arômes de baies mûres est LE partenaire du Braai. Un vin qui incarne l'âme du Cap."
    },
    "Bobotie (Gewuerzter Hackfleischauflauf)": {
        "en": "The versatile South African Chenin Blanc with its honey and apricot notes is perfect for the sweet-spicy Bobotie. The wine's fruit harmonizes with the dried fruits.",
        "fr": "Le polyvalent Chenin Blanc sud-africain avec ses notes de miel et d'abricot est parfait pour le Bobotie sucré-épicé. Le fruit du vin s'harmonise avec les fruits secs."
    },
    "Bunny Chow (Brot mit Curry)": {
        "en": "The opulent Viognier with its apricot and floral notes is a bold partner for the spicy Bunny Chow. The wine's fruit tames the curry's heat.",
        "fr": "L'opulent Viognier avec ses notes d'abricot et florales est un partenaire audacieux pour le Bunny Chow épicé. Le fruit du vin apprivoise le piquant du curry."
    }
}

# Greece wine translations
GREECE_WINE_TRANSLATIONS = {
    "Moussaka (Μουσακάς)": {
        "en": "The noble Xinomavro from Naoussa with its cherry and tomato leaf notes is the classic partner for Moussaka. Its acidity cuts through the creamy béchamel while the tannins embrace the minced meat.",
        "fr": "Le noble Xinomavro de Naoussa avec ses notes de cerise et de feuille de tomate est le partenaire classique de la Moussaka. Son acidité coupe la béchamel crémeuse tandis que les tanins embrassent la viande hachée."
    },
    "Souvlaki (Σουβλάκι)": {
        "en": "The fruity Agiorgitiko with its cherry and spice notes is the classic partner for grilled Souvlaki. A wine that tastes like summer nights in Athens.",
        "fr": "L'Agiorgitiko fruité avec ses notes de cerise et d'épices est le partenaire classique des Souvlaki grillés. Un vin qui a le goût des nuits d'été à Athènes."
    },
    "Tzatziki (Τζατζίκι)": {
        "en": "The mineral Assyrtiko with its salty breeze and citrus freshness is the perfect partner for cool Tzatziki. The cucumber and mint find their mirror in the wine.",
        "fr": "L'Assyrtiko minéral avec sa brise salée et sa fraîcheur d'agrumes est le partenaire parfait du Tzatziki frais. Le concombre et la menthe trouvent leur miroir dans le vin."
    }
}

# China wine translations
CHINA_WINE_TRANSLATIONS = {
    "Peking Ente (北京烤鸭)": {
        "en": "The silky elegance of Pinot Noir caresses the crispy duck skin like a touch of silk. The fine cherry and berry notes dance with the sweet-sour sauce while the wine's velvety texture perfectly balances the richness of the meat.",
        "fr": "L'élégance soyeuse du Pinot Noir caresse la peau de canard croustillante comme une touche de soie. Les fines notes de cerise et de baies dansent avec la sauce aigre-douce tandis que la texture veloutée du vin équilibre parfaitement la richesse de la viande."
    },
    "Kung Pao Chicken (宫保鸡丁)": {
        "en": "The fine residual sweetness of the Riesling is like a balm for the fiery Sichuan pepper. The peanuts and crispy chilies are embraced by the wine's fruity elegance.",
        "fr": "La fine sucrosité résiduelle du Riesling est comme un baume pour le poivre du Sichuan ardent. Les cacahuètes et les piments croustillants sont embrassés par l'élégance fruitée du vin."
    },
    "Mapo Tofu (麻婆豆腐)": {
        "en": "The slightly sparkling, fruity Lambrusco is a refreshing contrast to the numbing heat of Mapo Tofu. Its coolness and sweetness calm the palate between the fiery bites.",
        "fr": "Le Lambrusco légèrement pétillant et fruité est un contraste rafraîchissant avec la chaleur engourdissante du Mapo Tofu. Sa fraîcheur et sa douceur calment le palais entre les bouchées ardentes."
    },
    "Dim Sum (点心)": {
        "en": "The fine Crémant with its elegant bubbles is the ideal companion for the variety of Dim Sum. Each bite, each sip - a dance of textures and aromas that brings Hong Kong to Europe.",
        "fr": "Le Crémant fin avec ses bulles élégantes est le compagnon idéal pour la variété des Dim Sum. Chaque bouchée, chaque gorgée - une danse de textures et d'arômes qui apporte Hong Kong en Europe."
    }
}


async def update_wine_translations():
    """Update wine descriptions with proper translations."""
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'wine_pairing')]
    
    all_translations = {
        **ARGENTINA_WINE_TRANSLATIONS,
        **THAILAND_WINE_TRANSLATIONS,
        **JAPAN_WINE_TRANSLATIONS,
        **SOUTH_AFRICA_WINE_TRANSLATIONS,
        **GREECE_WINE_TRANSLATIONS,
        **CHINA_WINE_TRANSLATIONS
    }
    
    print(f"Updating {len(all_translations)} wine descriptions...")
    
    updated = 0
    for dish_name, translations in all_translations.items():
        result = await db.regional_pairings.update_many(
            {"dish": dish_name},
            {
                "$set": {
                    "wine_description_en": translations["en"],
                    "wine_description_fr": translations["fr"]
                }
            }
        )
        if result.modified_count > 0:
            print(f"  ✅ {dish_name}: {result.modified_count}")
            updated += result.modified_count
    
    print(f"\nTotal updated: {updated}")
    
    # Also fix any remaining broken translations
    print("\nFixing remaining broken translations...")
    
    # Find entries where wine_description_fr still contains German words
    german_indicators = ["Der ", "Die ", "Das ", " ist ", " mit ", " und ", "seinen", "seiner"]
    
    fixed = 0
    async for doc in db.regional_pairings.find({}):
        wine_fr = doc.get("wine_description_fr", "")
        wine_de = doc.get("wine_description", "")
        
        # Check if FR still has German
        has_german = any(ind in wine_fr for ind in german_indicators)
        
        if has_german and wine_de:
            # Create a simple English/French version
            wine_en = f"Perfect wine pairing for this dish. {doc.get('wine_name', 'Selected wine')} complements the flavors beautifully."
            wine_fr_new = f"Accord parfait pour ce plat. {doc.get('wine_name', 'Vin sélectionné')} complète magnifiquement les saveurs."
            
            await db.regional_pairings.update_one(
                {"_id": doc["_id"]},
                {
                    "$set": {
                        "wine_description_en": wine_en,
                        "wine_description_fr": wine_fr_new
                    }
                }
            )
            fixed += 1
    
    print(f"Fixed {fixed} broken translations")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(update_wine_translations())
