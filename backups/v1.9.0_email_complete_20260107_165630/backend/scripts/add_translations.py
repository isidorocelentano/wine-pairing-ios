#!/usr/bin/env python3
"""
Add proper English and French translations for all new country dishes.
"""

import asyncio
import os
import sys

sys.path.insert(0, '/app/backend')

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')

# Complete translations for all dishes
TRANSLATIONS = {
    # === ARGENTINIEN ===
    "Asado (Argentinisches Grillfleisch)": {
        "en": "Traditional Argentine barbecue of beef (Vacio, Entrana, Costilla) over charcoal. The Asado culture is central to Argentina.",
        "fr": "Barbecue argentin traditionnel de boeuf (Vacio, Entrana, Costilla) sur charbon de bois. La culture de l'Asado est centrale en Argentine."
    },
    "Choripan": {
        "en": "Grilled chorizo sausage in a bun, often served with chimichurri sauce.",
        "fr": "Saucisse chorizo grillée dans un petit pain, souvent servie avec de la sauce chimichurri."
    },
    "Morcilla (Argentinische Blutwurst)": {
        "en": "Grilled or fried blood sausage, often served with onions and chimichurri.",
        "fr": "Boudin noir grillé ou frit, souvent servi avec des oignons et du chimichurri."
    },
    "Vacio (Rinderbauch)": {
        "en": "Tender, fatty beef flank from the grill or pan.",
        "fr": "Flanc de boeuf tendre et gras du grill ou de la poêle."
    },
    "Entrana (Zwerchfell)": {
        "en": "Tender, juicy beef diaphragm, often served with chimichurri.",
        "fr": "Diaphragme de boeuf tendre et juteux, souvent servi avec du chimichurri."
    },
    "Empanadas (Argentinische Teigtaschen)": {
        "en": "Stuffed pastries with beef, chicken, cheese, olives or egg - each region has its own variant.",
        "fr": "Chaussons farcis au boeuf, poulet, fromage, olives ou oeuf - chaque région a sa propre variante."
    },
    "Provoleta (Gegrillter Kaese)": {
        "en": "Grilled provolone cheese, often with oregano and chili - a classic Asado starter.",
        "fr": "Provolone grillé, souvent avec de l'origan et du piment - un classique en entrée d'Asado."
    },
    "Chimichurri (als Beilage)": {
        "en": "The legendary green sauce made of parsley, garlic, oregano, vinegar and oil - essential for Asado.",
        "fr": "La légendaire sauce verte à base de persil, ail, origan, vinaigre et huile - indispensable pour l'Asado."
    },
    "Milanesa (Argentinisches Schnitzel)": {
        "en": "Breaded cutlet (usually beef or chicken), often served with fries or salad.",
        "fr": "Escalope panée (généralement boeuf ou poulet), souvent servie avec des frites ou une salade."
    },
    "Milanesa a la Napolitana": {
        "en": "Milanesa topped with tomato sauce, cheese and ham - Neapolitan style schnitzel.",
        "fr": "Milanesa garnie de sauce tomate, fromage et jambon - escalope à la napolitaine."
    },
    "Canelones (Argentinische Cannelloni)": {
        "en": "Stuffed pasta rolls with minced meat and cheese, baked with béchamel sauce.",
        "fr": "Rouleaux de pâtes farcis à la viande hachée et au fromage, gratinés avec de la sauce béchamel."
    },
    "Matambre Arrollado": {
        "en": "Stuffed beef flank (with carrots, onions, egg), rolled and cooked.",
        "fr": "Flanc de boeuf farci (avec carottes, oignons, oeuf), roulé et cuit."
    },
    "Carbonada (Suesser Fleischeintopf)": {
        "en": "Sweet stew made of beef, fruit (apple, pear), vegetables and milk.",
        "fr": "Ragoût sucré de boeuf, fruits (pomme, poire), légumes et lait."
    },
    "Puchero (Sonntagseintopf)": {
        "en": "Stew made of beef, vegetables, potatoes and corn - traditionally served on Sundays.",
        "fr": "Ragoût de boeuf, légumes, pommes de terre et maïs - traditionnellement servi le dimanche."
    },
    "Locro (Argentinischer Nationaleintopf)": {
        "en": "Stew made of corn, beans, meat and vegetables - traditionally served on national holidays.",
        "fr": "Ragoût de maïs, haricots, viande et légumes - traditionnellement servi lors des fêtes nationales."
    },
    "Humita (Maisfuellung in Maisblaettern)": {
        "en": "Cooked corn filling wrapped in corn leaves, often served as a side dish or main course.",
        "fr": "Farce de maïs cuite enveloppée dans des feuilles de maïs, souvent servie en accompagnement ou plat principal."
    },
    "Cordero Patagonico (Patagonisches Lamm)": {
        "en": "Slowly grilled or braised lamb from Patagonia - the meat has a unique flavor from the region's wild herbs.",
        "fr": "Agneau de Patagonie grillé lentement ou braisé - la viande a une saveur unique grâce aux herbes sauvages de la région."
    },
    "Trucha Patagonica (Patagonische Forelle)": {
        "en": "Fresh trout from the crystal-clear lakes of Patagonia, often grilled or smoked.",
        "fr": "Truite fraîche des lacs cristallins de Patagonie, souvent grillée ou fumée."
    },
    
    # === THAILAND ===
    "Green Curry (Kaeng Khiao Wan, แกงเขียวหวาน)": {
        "en": "Spicy, creamy curry with green chilies, coconut milk, chicken or beef.",
        "fr": "Curry épicé et crémeux avec des piments verts, du lait de coco, du poulet ou du boeuf."
    },
    "Red Curry (Kaeng Phet, แกงเผ็ด)": {
        "en": "Spicy curry with red chilies, coconut milk, meat and vegetables.",
        "fr": "Curry épicé avec des piments rouges, du lait de coco, de la viande et des légumes."
    },
    "Panang Curry (Kaeng Phanaeng, แกงพะแนง)": {
        "en": "Thick, nutty curry with coconut milk, meat and kaffir lime leaves.",
        "fr": "Curry épais et noisette avec du lait de coco, de la viande et des feuilles de combava."
    },
    "Yellow Curry (Kaeng Kari, แกงกะหรี่)": {
        "en": "Mild yellow curry with turmeric, potatoes and chicken or beef.",
        "fr": "Curry jaune doux avec du curcuma, des pommes de terre et du poulet ou du boeuf."
    },
    "Pad Thai (ผัดไทย)": {
        "en": "Stir-fried rice noodles with egg, tofu, shrimp, peanuts and tamarind sauce.",
        "fr": "Nouilles de riz sautées avec oeuf, tofu, crevettes, cacahuètes et sauce tamarin."
    },
    "Tom Yum Goong (ต้มยำกุ้ง)": {
        "en": "Spicy, sour soup with shrimp, mushrooms, lemongrass and kaffir lime leaves.",
        "fr": "Soupe épicée et aigre avec des crevettes, des champignons, de la citronnelle et des feuilles de combava."
    },
    "Tom Kha Gai (ต้มข่าไก่)": {
        "en": "Coconut milk soup with chicken, mushrooms, lemongrass and kaffir lime leaves.",
        "fr": "Soupe au lait de coco avec du poulet, des champignons, de la citronnelle et des feuilles de combava."
    },
    "Massaman Curry (Kaeng Massaman, แกงมัสมั่น)": {
        "en": "Mild, sweet-spicy curry with potatoes, peanuts, cinnamon and meat.",
        "fr": "Curry doux, sucré-épicé avec des pommes de terre, des cacahuètes, de la cannelle et de la viande."
    },
    "Som Tum (ส้มตำ)": {
        "en": "Green papaya salad with chili, fish sauce, lime, tomatoes and peanuts.",
        "fr": "Salade de papaye verte avec du piment, de la sauce de poisson, du citron vert, des tomates et des cacahuètes."
    },
    "Larb (ลาบ)": {
        "en": "Minced meat salad (chicken, beef, pork) with chili, lime, coriander and roasted rice.",
        "fr": "Salade de viande hachée (poulet, boeuf, porc) avec du piment, du citron vert, de la coriandre et du riz grillé."
    },
    "Khao Soi (ข้าวซอย)": {
        "en": "Coconut curry noodles with crispy noodles on top, often with chicken or beef.",
        "fr": "Nouilles au curry et lait de coco avec des nouilles croustillantes dessus, souvent avec du poulet ou du boeuf."
    },
    "Pad Kra Pao (ผัดกระเพรา)": {
        "en": "Stir-fried rice or noodles with pork, chili and holy basil.",
        "fr": "Riz ou nouilles sautés avec du porc, du piment et du basilic sacré."
    },
    
    # === JAPAN ===
    "Nigiri Sushi (握り寿司)": {
        "en": "Rice topped with thinly sliced raw fish (e.g., tuna, salmon) - the Edo-style classic.",
        "fr": "Riz garni de poisson cru finement tranché (thon, saumon) - le classique du style Edo."
    },
    "Maki Sushi (巻き寿司)": {
        "en": "Rice and filling (fish, vegetables) rolled in nori (seaweed).",
        "fr": "Riz et garniture (poisson, légumes) roulés dans du nori (algue)."
    },
    "Sashimi (刺身)": {
        "en": "Thinly sliced raw fish (e.g., tuna, mackerel, eel) without rice - pure essence.",
        "fr": "Poisson cru finement tranché (thon, maquereau, anguille) sans riz - l'essence pure."
    },
    "Ramen (ラーメン)": {
        "en": "Noodles in broth (soy, miso, salt, tonkotsu) with meat, egg, nori - Japan's soul food.",
        "fr": "Nouilles dans un bouillon (soja, miso, sel, tonkotsu) avec viande, oeuf, nori - le plat réconfortant du Japon."
    },
    "Tempura (天ぷら)": {
        "en": "Deep-fried seafood and vegetables in a light, crispy batter.",
        "fr": "Fruits de mer et légumes frits dans une pâte légère et croustillante."
    },
    "Sukiyaki (すき焼き)": {
        "en": "Thin beef slices, vegetables, tofu in sweet soy broth, cooked at the table.",
        "fr": "Fines tranches de boeuf, légumes, tofu dans un bouillon de soja sucré, cuisiné à table."
    },
    "Okonomiyaki (お好み焼き)": {
        "en": "As you like it pancake - savory pancake with vegetables, meat, seafood and special sauce.",
        "fr": "Crêpe comme vous l'aimez - crêpe salée avec légumes, viande, fruits de mer et sauce spéciale."
    },
    "Katsudon (カツ丼)": {
        "en": "Rice bowl with breaded pork cutlet (tonkatsu) and egg - pure comfort food.",
        "fr": "Bol de riz avec côtelette de porc panée (tonkatsu) et oeuf - pur plat réconfortant."
    },
    "Gyudon (牛丼)": {
        "en": "Rice bowl with thinly sliced beef and onions in sweet-savory sauce.",
        "fr": "Bol de riz avec du boeuf finement tranché et des oignons dans une sauce sucrée-salée."
    },
    
    # === SÜDAFRIKA ===
    "Braai (Suedafrikanisches Grillfleisch)": {
        "en": "Traditional South African barbecue of beef, pork, lamb, sausages (Boerewors) and chicken over charcoal. The Braai culture is central to South Africa.",
        "fr": "Barbecue sud-africain traditionnel de boeuf, porc, agneau, saucisses (Boerewors) et poulet sur charbon de bois. La culture du Braai est centrale en Afrique du Sud."
    },
    "Boerewors (Bauernwurst)": {
        "en": "Spiced beef or pork sausage, often grilled in spirals, served with bread or fries.",
        "fr": "Saucisse de boeuf ou de porc épicée, souvent grillée en spirales, servie avec du pain ou des frites."
    },
    "Bobotie (Gewuerzter Hackfleischauflauf)": {
        "en": "Minced meat with curry, dried fruit, egg custard and bread - often served with rice. A Cape Malay classic.",
        "fr": "Viande hachée avec du curry, des fruits secs, une crème aux oeufs et du pain - souvent servi avec du riz. Un classique de la cuisine Cape Malay."
    },
    "Potjiekos (Eintopf im Gusseisentopf)": {
        "en": "Slowly cooked meat (beef, lamb) with vegetables in a cast iron pot over an open fire.",
        "fr": "Viande (boeuf, agneau) cuite lentement avec des légumes dans une marmite en fonte sur feu ouvert."
    },
    "Biltong (Luftgetrocknetes Fleisch)": {
        "en": "Spiced, air-dried beef or game meat - similar to jerky, but softer and more flavorful.",
        "fr": "Viande de boeuf ou de gibier séchée et épicée - similaire au jerky, mais plus tendre et savoureux."
    },
    "Bunny Chow (Brot mit Curry)": {
        "en": "Hollow bread filled with curry (chicken, lamb, chickpeas) - the legendary street food classic from Durban.",
        "fr": "Pain évidé rempli de curry (poulet, agneau, pois chiches) - le légendaire classique de street food de Durban."
    },
    "Cape Malay Curry": {
        "en": "Sweet, spicy curry with chicken, lamb or vegetables, often served with rice - a heritage of Cape Malay cuisine.",
        "fr": "Curry sucré et épicé avec du poulet, de l'agneau ou des légumes, souvent servi avec du riz - un héritage de la cuisine Cape Malay."
    },
    
    # === GRIECHENLAND (neue Einträge) ===
    "Moussaka (Μουσακάς)": {
        "en": "The national dish: Layers of eggplant, minced meat and béchamel - hearty, spiced and warming.",
        "fr": "Le plat national: Couches d'aubergines, viande hachée et béchamel - copieux, épicé et réconfortant."
    },
    "Pastitsio (Παστίτσιο)": {
        "en": "Pasta bake with minced meat and béchamel, similar to lasagna.",
        "fr": "Gratin de pâtes avec viande hachée et béchamel, similaire aux lasagnes."
    },
    "Souvlaki (Σουβλάκι)": {
        "en": "Grilled meat skewers (mostly pork or chicken) - Greece's beloved street food.",
        "fr": "Brochettes de viande grillée (porc ou poulet) - le street food bien-aimé de la Grèce."
    },
    "Gyros (Γύρος)": {
        "en": "Rotisserie meat (pork or chicken) in flatbread with salad and tzatziki.",
        "fr": "Viande à la broche (porc ou poulet) dans du pain plat avec salade et tzatziki."
    },
    "Dolmades (Δολμάδες)": {
        "en": "Rice-stuffed vine leaves, often with herbs and lemon.",
        "fr": "Feuilles de vigne farcies au riz, souvent avec des herbes et du citron."
    },
    "Spanakopita (Σπανακόπιτα)": {
        "en": "Phyllo pastry with spinach and feta cheese.",
        "fr": "Pâte feuilletée aux épinards et à la feta."
    },
    "Tzatziki (Τζατζίκι)": {
        "en": "Yogurt dip with cucumber, garlic and mint - often served as a side.",
        "fr": "Sauce au yaourt avec concombre, ail et menthe - souvent servie en accompagnement."
    },
    
    # === CHINA (neue Einträge) ===
    "Peking Ente (北京烤鸭)": {
        "en": "Crispy duck, thinly sliced, served with pancakes, vegetables and sweet-sour sauce.",
        "fr": "Canard croustillant, finement tranché, servi avec des crêpes, des légumes et une sauce aigre-douce."
    },
    "Jiaozi (饺子)": {
        "en": "Steamed or fried dumplings with meat or vegetable filling.",
        "fr": "Raviolis cuits à la vapeur ou frits avec une garniture de viande ou de légumes."
    },
    "Xiaolongbao (小笼包)": {
        "en": "Steamed soup dumplings filled with meat and broth - a Shanghai specialty.",
        "fr": "Raviolis à la vapeur remplis de viande et de bouillon - une spécialité de Shanghai."
    },
    "Kung Pao Chicken (宫保鸡丁)": {
        "en": "Chicken with peanuts, chili and Sichuan pepper - a spicy classic.",
        "fr": "Poulet aux cacahuètes, piment et poivre du Sichuan - un classique épicé."
    },
    "Mapo Tofu (麻婆豆腐)": {
        "en": "Tofu with minced meat, chili and Sichuan pepper - numbing and spicy.",
        "fr": "Tofu avec viande hachée, piment et poivre du Sichuan - engourdissant et épicé."
    },
    "Dim Sum (点心)": {
        "en": "Small dishes like Har Gow, Siu Mai, Char Siu Bao - the art of Cantonese brunch.",
        "fr": "Petits plats comme Har Gow, Siu Mai, Char Siu Bao - l'art du brunch cantonais."
    }
}


async def add_translations():
    """Add proper translations to all dishes."""
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'wine_pairing')]
    
    print("Adding translations to dishes...")
    
    updated = 0
    for dish_name, trans in TRANSLATIONS.items():
        # Try exact match first
        result = await db.regional_pairings.update_many(
            {"dish": dish_name},
            {
                "$set": {
                    "dish_description_en": trans["en"],
                    "dish_description_fr": trans["fr"]
                }
            }
        )
        
        if result.modified_count > 0:
            print(f"  ✅ {dish_name}: {result.modified_count} updated")
            updated += result.modified_count
        else:
            # Try partial match
            result = await db.regional_pairings.update_many(
                {"dish": {"$regex": dish_name.split(" ")[0], "$options": "i"}},
                {
                    "$set": {
                        "dish_description_en": trans["en"],
                        "dish_description_fr": trans["fr"]
                    }
                }
            )
            if result.modified_count > 0:
                print(f"  ✅ {dish_name} (partial): {result.modified_count} updated")
                updated += result.modified_count
    
    print(f"\nTotal updated: {updated}")
    
    # Verify
    print("\n=== VERIFICATION ===")
    for country in ["Argentinien", "Thailand", "Japan", "Suedafrika"]:
        doc = await db.regional_pairings.find_one(
            {"country": country},
            {"_id": 0, "dish": 1, "dish_description_en": 1}
        )
        if doc:
            desc = doc.get("dish_description_en", "")[:50]
            print(f"{country}: {doc.get('dish', '?')} -> {desc}...")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(add_translations())
