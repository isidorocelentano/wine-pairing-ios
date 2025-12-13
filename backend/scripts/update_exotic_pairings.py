"""
Überarbeitung der exotischen Länder im Sommelier-Kompass
Mit internationalem Wein + lokaler Alternative
"""
import asyncio
import json
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment
ROOT_DIR = Path(__file__).parent
with open(ROOT_DIR / '.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value.strip('"')

client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
db = client[os.environ.get('DB_NAME', 'test_database')]

# ===================== NEUE EXOTISCHE PAIRINGS =====================

EXOTIC_PAIRINGS = [
    # ==================== GRIECHENLAND ====================
    {
        "country": "Griechenland",
        "country_en": "Greece",
        "country_fr": "Grèce",
        "country_emoji": "🇬🇷",
        "region": "Santorin",
        "dish": "Tomatokeftedes (Gebratene Tomatenbällchen)",
        "dish_description": "Knusprige Bällchen aus sonnengetrockneten Tomaten, Minze und Kräutern – eine Spezialität der Kykladen, die die intensive Süße der vulkanischen Tomaten Santorins einfängt.",
        "dish_description_en": "Crispy fritters made from sun-dried tomatoes, mint and herbs – a Cycladic specialty capturing the intense sweetness of Santorini's volcanic tomatoes.",
        "dish_description_fr": "Boulettes croustillantes de tomates séchées au soleil, menthe et herbes – une spécialité des Cyclades capturant la douceur intense des tomates volcaniques de Santorin.",
        
        # INTERNATIONALE EMPFEHLUNG (sichere Wahl)
        "wine_name": "Sauvignon Blanc (Sancerre oder Marlborough)",
        "wine_type": "Frischer Weißwein",
        "wine_description": "Die klassische sichere Wahl: Ein knackiger Sauvignon Blanc mit Zitrus und Kräuternoten passt perfekt zu den mediterranen Aromen. Die Säure schneidet durch die Frittierung.",
        "wine_description_en": "The classic safe choice: A crisp Sauvignon Blanc with citrus and herbal notes pairs perfectly with Mediterranean flavors. The acidity cuts through the frying.",
        "wine_description_fr": "Le choix sûr classique : Un Sauvignon Blanc vif aux notes d'agrumes et d'herbes s'accorde parfaitement avec les saveurs méditerranéennes.",
        
        # LOKALE ALTERNATIVE
        "local_wine_name": "Assyrtiko (Santorini PDO)",
        "local_wine_type": "Vulkanischer Weißwein",
        "local_wine_description": "🌋 Die Entdeckung: Assyrtiko von den vulkanischen Böden Santorins – mineralisch, salzig, mit Zitrus und einem Hauch Rauch. Der authentische Begleiter, der die Insel ins Glas bringt. Probieren Sie Gaia, Sigalas oder Argyros.",
        "local_wine_description_en": "🌋 The discovery: Assyrtiko from Santorini's volcanic soils – mineral, saline, with citrus and a hint of smoke. The authentic companion that brings the island into your glass. Try Gaia, Sigalas or Argyros.",
        "local_wine_description_fr": "🌋 La découverte : Assyrtiko des sols volcaniques de Santorin – minéral, salin, avec des agrumes et une touche de fumée. Le compagnon authentique qui amène l'île dans votre verre.",
        
        "country_intro": "🏛️ Hellas – Wiege des Weins: Griechenland ist eines der ältesten Weinländer der Welt. Von den vulkanischen Terrassen Santorins bis zu den kühlen Höhen Makedoniens warten einzigartige, autochthone Rebsorten darauf, entdeckt zu werden.",
        "country_intro_en": "🏛️ Hellas – Cradle of Wine: Greece is one of the oldest wine countries in the world. From Santorini's volcanic terraces to Macedonia's cool heights, unique indigenous grape varieties await discovery.",
        "country_intro_fr": "🏛️ Hellas – Berceau du Vin : La Grèce est l'un des plus anciens pays viticoles du monde. Des terrasses volcaniques de Santorin aux hauteurs fraîches de Macédoine, des cépages autochtones uniques attendent d'être découverts.",
        "country_image_url": "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=1200"
    },
    {
        "country": "Griechenland",
        "country_en": "Greece",
        "country_fr": "Grèce",
        "country_emoji": "🇬🇷",
        "region": "Kreta",
        "dish": "Dakos (Kretischer Zwieback-Salat)",
        "dish_description": "Gerstenzwieback getränkt mit frischen Tomaten, gekrönt mit Mizithra-Käse, Oliven und Oregano – die Essenz der kretischen Diät.",
        "dish_description_en": "Barley rusk soaked with fresh tomatoes, topped with Mizithra cheese, olives and oregano – the essence of the Cretan diet.",
        "dish_description_fr": "Biscotte d'orge imbibée de tomates fraîches, garnie de fromage Mizithra, olives et origan – l'essence du régime crétois.",
        
        "wine_name": "Grüner Veltliner oder Vermentino",
        "wine_type": "Frischer, würziger Weißwein",
        "wine_description": "Bekannte mediterrane Weißweine mit ähnlichem Charakter: würzig, frisch, mit guter Säure. Eine vertraute Wahl für den mediterranen Salat.",
        "wine_description_en": "Well-known Mediterranean whites with similar character: spicy, fresh, with good acidity. A familiar choice for this Mediterranean salad.",
        "wine_description_fr": "Blancs méditerranéens connus au caractère similaire : épicés, frais, avec une bonne acidité.",
        
        "local_wine_name": "Vidiano (Kreta)",
        "local_wine_type": "Kretischer Weißwein",
        "local_wine_description": "🏺 Die Entdeckung: Vidiano – Kretas wiederentdeckter Schatz. Aromatisch mit tropischen Früchten, Blüten und einer seidigen Textur. Fast ausgestorben, heute ein Star der griechischen Renaissance.",
        "local_wine_description_en": "🏺 The discovery: Vidiano – Crete's rediscovered treasure. Aromatic with tropical fruits, flowers and a silky texture. Nearly extinct, now a star of the Greek renaissance.",
        "local_wine_description_fr": "🏺 La découverte : Vidiano – le trésor redécouvert de Crète. Aromatique avec des fruits tropicaux, des fleurs et une texture soyeuse.",
        
        "country_intro": "🏛️ Hellas – Wiege des Weins: Griechenland ist eines der ältesten Weinländer der Welt.",
        "country_intro_en": "🏛️ Hellas – Cradle of Wine: Greece is one of the oldest wine countries in the world.",
        "country_intro_fr": "🏛️ Hellas – Berceau du Vin : La Grèce est l'un des plus anciens pays viticoles du monde.",
        "country_image_url": "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=1200"
    },
    {
        "country": "Griechenland",
        "country_en": "Greece",
        "country_fr": "Grèce",
        "country_emoji": "🇬🇷",
        "region": "Naoussa (Makedonien)",
        "dish": "Moussaka",
        "dish_description": "Das Nationalgericht: Schichten von Auberginen, Hackfleisch und Béchamel – herzhaft, würzig und wärmend.",
        "dish_description_en": "The national dish: Layers of eggplant, minced meat and béchamel – hearty, spicy and warming.",
        "dish_description_fr": "Le plat national : Couches d'aubergines, viande hachée et béchamel – copieux, épicé et réconfortant.",
        
        "wine_name": "Côtes du Rhône Rouge oder Chianti Classico",
        "wine_type": "Mittelschwerer Rotwein",
        "wine_description": "Klassische mediterrane Rotweine mit Würze und mittlerem Körper. Die Vertrautheit eines guten Rhône oder Chianti harmoniert wunderbar mit dem reichhaltigen Auflauf.",
        "wine_description_en": "Classic Mediterranean reds with spice and medium body. The familiarity of a good Rhône or Chianti harmonizes wonderfully with this rich casserole.",
        "wine_description_fr": "Rouges méditerranéens classiques avec épices et corps moyen. La familiarité d'un bon Rhône ou Chianti s'harmonise merveilleusement.",
        
        "local_wine_name": "Xinomavro (Naoussa PDO)",
        "local_wine_type": "Griechischer Nebbiolo",
        "local_wine_description": "🍇 Die Entdeckung: Xinomavro – 'saure Schwarze' – Griechenlands edelster Roter. Oft mit Barolo verglichen: tanninreich, komplex, mit Aromen von Tomaten, Oliven und getrockneten Blumen. Ein Wein für Entdecker!",
        "local_wine_description_en": "🍇 The discovery: Xinomavro – 'sour black' – Greece's noblest red. Often compared to Barolo: tannic, complex, with aromas of tomatoes, olives and dried flowers. A wine for explorers!",
        "local_wine_description_fr": "🍇 La découverte : Xinomavro – 'noir acide' – le plus noble rouge de Grèce. Souvent comparé au Barolo : tannique, complexe, avec des arômes de tomates, olives et fleurs séchées.",
        
        "country_intro": "🏛️ Hellas – Wiege des Weins: Griechenland ist eines der ältesten Weinländer der Welt.",
        "country_intro_en": "🏛️ Hellas – Cradle of Wine: Greece is one of the oldest wine countries in the world.",
        "country_intro_fr": "🏛️ Hellas – Berceau du Vin : La Grèce est l'un des plus anciens pays viticoles du monde.",
        "country_image_url": "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=1200"
    },
    {
        "country": "Griechenland",
        "country_en": "Greece",
        "country_fr": "Grèce",
        "country_emoji": "🇬🇷",
        "region": "Nemea (Peloponnes)",
        "dish": "Souvlaki & Gyros",
        "dish_description": "Gegrillte Fleischspieße oder das ikonische Gyros – mariniert mit Oregano, Zitrone und Olivenöl. Das ultimative Streetfood.",
        "dish_description_en": "Grilled meat skewers or iconic gyros – marinated with oregano, lemon and olive oil. The ultimate street food.",
        "dish_description_fr": "Brochettes de viande grillée ou gyros emblématiques – marinés à l'origan, citron et huile d'olive. L'ultime street food.",
        
        "wine_name": "Rosé aus der Provence oder Tempranillo Rosado",
        "wine_type": "Trockener Rosé",
        "wine_description": "Ein frischer Rosé ist die universelle Antwort auf gegrilltes Fleisch mit mediterranen Kräutern. Kühl serviert, ein Sommer-Klassiker.",
        "wine_description_en": "A fresh rosé is the universal answer to grilled meat with Mediterranean herbs. Served cool, a summer classic.",
        "wine_description_fr": "Un rosé frais est la réponse universelle aux viandes grillées aux herbes méditerranéennes. Servi frais, un classique d'été.",
        
        "local_wine_name": "Agiorgitiko (Nemea PDO)",
        "local_wine_type": "Samtiger Rotwein",
        "local_wine_description": "🍷 Die Entdeckung: Agiorgitiko – 'St. Georg' – Griechenlands beliebtester Roter. Samtig, fruchtig, mit Aromen von Kirschen und Pflaumen. Weniger tanninreich als Xinomavro, perfekt zum Streetfood!",
        "local_wine_description_en": "🍷 The discovery: Agiorgitiko – 'St. George' – Greece's most popular red. Velvety, fruity, with aromas of cherries and plums. Less tannic than Xinomavro, perfect for street food!",
        "local_wine_description_fr": "🍷 La découverte : Agiorgitiko – 'St. George' – le rouge le plus populaire de Grèce. Velouté, fruité, avec des arômes de cerises et prunes.",
        
        "country_intro": "🏛️ Hellas – Wiege des Weins: Griechenland ist eines der ältesten Weinländer der Welt.",
        "country_intro_en": "🏛️ Hellas – Cradle of Wine: Greece is one of the oldest wine countries in the world.",
        "country_intro_fr": "🏛️ Hellas – Berceau du Vin : La Grèce est l'un des plus anciens pays viticoles du monde.",
        "country_image_url": "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=1200"
    },
    
    # ==================== JAPAN ====================
    {
        "country": "Japan",
        "country_en": "Japan",
        "country_fr": "Japon",
        "country_emoji": "🇯🇵",
        "region": "Tokyo",
        "dish": "Edo-mae Sushi (Traditionelles Sushi)",
        "dish_description": "Die Kunst des Sushi: Frischester Fisch auf perfekt temperiertem Reis, gewürzt mit Wasabi und einem Hauch Sojasauce. Perfektion in Einfachheit.",
        "dish_description_en": "The art of sushi: Freshest fish on perfectly tempered rice, seasoned with wasabi and a hint of soy sauce. Perfection in simplicity.",
        "dish_description_fr": "L'art du sushi : Poisson ultra-frais sur riz parfaitement tempéré, assaisonné de wasabi et d'un soupçon de sauce soja. La perfection dans la simplicité.",
        
        "wine_name": "Champagner (Brut) oder Chablis",
        "wine_type": "Eleganter Schaumwein/Weißwein",
        "wine_description": "Die klassische Luxus-Kombination: Champagner mit seiner feinen Perlage und Mineralität oder ein stahltankvergorener Chablis. Beide respektieren die Delikatesse des Fischs.",
        "wine_description_en": "The classic luxury pairing: Champagne with its fine bubbles and minerality or a steel-fermented Chablis. Both respect the delicacy of the fish.",
        "wine_description_fr": "L'accord luxueux classique : Champagne avec ses fines bulles et minéralité ou un Chablis vinifié en cuve inox. Les deux respectent la délicatesse du poisson.",
        
        "local_wine_name": "Koshu (Yamanashi)",
        "local_wine_type": "Japanischer Weißwein",
        "local_wine_description": "🗻 Die Entdeckung: Koshu – Japans einzige Vinifera-Traube mit 1000-jähriger Geschichte. Dezent, elegant, mit Noten von weißem Pfirsich und einem Hauch Umami. Die perfekte Harmonie zu Sushi! Probieren Sie Grace Winery oder Château Mercian.",
        "local_wine_description_en": "🗻 The discovery: Koshu – Japan's only Vinifera grape with 1000 years of history. Subtle, elegant, with notes of white peach and a hint of umami. Perfect harmony with sushi! Try Grace Winery or Château Mercian.",
        "local_wine_description_fr": "🗻 La découverte : Koshu – l'unique cépage Vinifera du Japon avec 1000 ans d'histoire. Subtil, élégant, avec des notes de pêche blanche et une touche d'umami.",
        
        "country_intro": "🎌 Nihon – Land der aufgehenden Sonne und des feinen Geschmacks: Japan überrascht mit einer aufstrebenden Weinszene. In den kühlen Höhen von Yamanashi und Nagano entstehen Weine, die Eleganz und Präzision verkörpern – Spiegel der japanischen Ästhetik.",
        "country_intro_en": "🎌 Nihon – Land of the Rising Sun and Fine Taste: Japan surprises with an emerging wine scene. In the cool heights of Yamanashi and Nagano, wines embodying elegance and precision are born – mirrors of Japanese aesthetics.",
        "country_intro_fr": "🎌 Nihon – Pays du Soleil Levant et du Goût Raffiné : Le Japon surprend avec une scène viticole émergente. Dans les hauteurs fraîches de Yamanashi et Nagano naissent des vins incarnant élégance et précision.",
        "country_image_url": "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=1200"
    },
    {
        "country": "Japan",
        "country_en": "Japan",
        "country_fr": "Japon",
        "country_emoji": "🇯🇵",
        "region": "Osaka",
        "dish": "Okonomiyaki (Japanische Pfannkuchen)",
        "dish_description": "Der 'Koch-es-wie-du-magst' Pfannkuchen aus Osaka: Kohl, Fleisch oder Meeresfrüchte, getoppt mit süßer Sauce, Mayo und Bonito-Flocken.",
        "dish_description_en": "The 'cook-it-as-you-like' pancake from Osaka: Cabbage, meat or seafood, topped with sweet sauce, mayo and bonito flakes.",
        "dish_description_fr": "La crêpe 'cuisinez-comme-vous-voulez' d'Osaka : Chou, viande ou fruits de mer, garnie de sauce sucrée, mayo et flocons de bonite.",
        
        "wine_name": "Crémant d'Alsace oder Prosecco",
        "wine_type": "Frischer Schaumwein",
        "wine_description": "Ein fruchtiger, nicht zu trockener Schaumwein balanciert die süß-salzige Sauce perfekt. Die Bläschen erfrischen zwischen den reichhaltigen Bissen.",
        "wine_description_en": "A fruity, not too dry sparkling wine balances the sweet-salty sauce perfectly. The bubbles refresh between rich bites.",
        "wine_description_fr": "Un vin pétillant fruité, pas trop sec, équilibre parfaitement la sauce sucrée-salée. Les bulles rafraîchissent entre les bouchées riches.",
        
        "local_wine_name": "Junmai Sake (z.B. Hakkaisan oder Dassai)",
        "local_wine_type": "Premium-Reiswein",
        "local_wine_description": "🍶 Die Entdeckung: Sake ist kein Wein, aber der authentische Begleiter! Junmai (reiner Reis) ohne Zusatz von Braualkohol. Leicht gekühlt serviert, mit Umami und einer samtigen Textur – die lokale Wahl der Kenner.",
        "local_wine_description_en": "🍶 The discovery: Sake isn't wine, but the authentic companion! Junmai (pure rice) without added brewing alcohol. Served slightly chilled, with umami and a velvety texture – the local connoisseur's choice.",
        "local_wine_description_fr": "🍶 La découverte : Le saké n'est pas du vin, mais le compagnon authentique ! Junmai (riz pur) sans alcool de brassage ajouté. Servi légèrement frais, avec umami et texture veloutée.",
        
        "country_intro": "🎌 Nihon – Land der aufgehenden Sonne und des feinen Geschmacks.",
        "country_intro_en": "🎌 Nihon – Land of the Rising Sun and Fine Taste.",
        "country_intro_fr": "🎌 Nihon – Pays du Soleil Levant et du Goût Raffiné.",
        "country_image_url": "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=1200"
    },
    {
        "country": "Japan",
        "country_en": "Japan",
        "country_fr": "Japon",
        "country_emoji": "🇯🇵",
        "region": "Sapporo (Hokkaido)",
        "dish": "Miso Ramen",
        "dish_description": "Hokkaidos Signature: Reichhaltige Miso-Brühe mit Nudeln, Schweinefleisch, Mais und Butter. Wärmend, umami-reich und sättigend.",
        "dish_description_en": "Hokkaido's signature: Rich miso broth with noodles, pork, corn and butter. Warming, umami-rich and satisfying.",
        "dish_description_fr": "La signature d'Hokkaido : Bouillon miso riche avec nouilles, porc, maïs et beurre. Réchauffant, riche en umami et rassasiant.",
        
        "wine_name": "Gewürztraminer (Elsass) oder Riesling Spätlese",
        "wine_type": "Aromatischer Weißwein",
        "wine_description": "Die aromatische Intensität eines Gewürztraminers oder die leichte Süße einer Spätlese harmoniert überraschend gut mit der Umami-Bombe Miso.",
        "wine_description_en": "The aromatic intensity of Gewürztraminer or the slight sweetness of Spätlese harmonizes surprisingly well with the umami bomb miso.",
        "wine_description_fr": "L'intensité aromatique d'un Gewürztraminer ou la légère douceur d'une Spätlese s'harmonise étonnamment bien avec la bombe umami du miso.",
        
        "local_wine_name": "Kerner (Hokkaido) oder Junmai Daiginjo Sake",
        "local_wine_type": "Japanischer Weißwein / Premium-Sake",
        "local_wine_description": "🏔️ Die Entdeckung: Hokkaido produziert deutsche Rebsorten wie Kerner und Müller-Thurgau in kühlem Klima. Alternativ: Ein Junmai Daiginjo – der 'Grand Cru' des Sake – mit floralen Noten und kristalliner Reinheit.",
        "local_wine_description_en": "🏔️ The discovery: Hokkaido produces German grape varieties like Kerner and Müller-Thurgau in its cool climate. Alternatively: A Junmai Daiginjo – the 'Grand Cru' of sake – with floral notes and crystalline purity.",
        "local_wine_description_fr": "🏔️ La découverte : Hokkaido produit des cépages allemands comme le Kerner dans son climat frais. Alternative : Un Junmai Daiginjo – le 'Grand Cru' du saké – avec des notes florales et une pureté cristalline.",
        
        "country_intro": "🎌 Nihon – Land der aufgehenden Sonne und des feinen Geschmacks.",
        "country_intro_en": "🎌 Nihon – Land of the Rising Sun and Fine Taste.",
        "country_intro_fr": "🎌 Nihon – Pays du Soleil Levant et du Goût Raffiné.",
        "country_image_url": "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=1200"
    },
    
    # ==================== TÜRKEI ====================
    {
        "country": "Türkei",
        "country_en": "Turkey",
        "country_fr": "Turquie",
        "country_emoji": "🇹🇷",
        "region": "Bursa / Marmara",
        "dish": "İskender Kebap",
        "dish_description": "Das Meisterwerk aus Bursa: Zartes Döner-Fleisch auf Fladenbrot, übergossen mit Tomaten-Butter-Sauce und serviert mit Joghurt. Reichhaltig und unvergesslich.",
        "dish_description_en": "The masterpiece from Bursa: Tender döner meat on flatbread, drenched in tomato-butter sauce and served with yogurt. Rich and unforgettable.",
        "dish_description_fr": "Le chef-d'œuvre de Bursa : Viande de döner tendre sur pain plat, nappée de sauce tomate-beurre et servie avec du yaourt. Riche et inoubliable.",
        
        "wine_name": "Côtes du Rhône Rouge oder Primitivo",
        "wine_type": "Würziger Rotwein",
        "wine_description": "Ein fruchtbetonter, würziger Rotwein mit weichen Tanninen. Die Vertrautheit eines guten Rhône oder Primitivo steht dem reichhaltigen Fleisch gut.",
        "wine_description_en": "A fruit-forward, spicy red with soft tannins. The familiarity of a good Rhône or Primitivo stands up well to the rich meat.",
        "wine_description_fr": "Un rouge fruité et épicé aux tanins souples. La familiarité d'un bon Rhône ou Primitivo accompagne bien cette viande riche.",
        
        "local_wine_name": "Öküzgözü (Elazığ)",
        "local_wine_type": "Anatolischer Rotwein",
        "local_wine_description": "🌙 Die Entdeckung: Öküzgözü – 'Ochsenauge' – Ostanatoliens Star. Samtig, fruchtig, mit Aromen von Sauerkirschen und Gewürzen. Oft mit Syrah verglichen, aber einzigartig türkisch. Probieren Sie Kavaklidere oder Doluca!",
        "local_wine_description_en": "🌙 The discovery: Öküzgözü – 'Ox Eye' – Eastern Anatolia's star. Velvety, fruity, with aromas of sour cherries and spices. Often compared to Syrah, but uniquely Turkish. Try Kavaklidere or Doluca!",
        "local_wine_description_fr": "🌙 La découverte : Öküzgözü – 'Œil de bœuf' – la star de l'Anatolie orientale. Velouté, fruité, avec des arômes de cerises aigres et d'épices. Souvent comparé au Syrah, mais uniquement turc.",
        
        "country_intro": "🌙 Türkiye – Brücke zwischen Orient und Okzident: Die Türkei ist eines der ältesten Weinländer der Welt – hier wurden wilde Reben domestiziert! Heute erleben autochthone Rebsorten wie Öküzgözü und Boğazkere eine Renaissance.",
        "country_intro_en": "🌙 Türkiye – Bridge between East and West: Turkey is one of the oldest wine countries in the world – wild vines were domesticated here! Today, indigenous grape varieties like Öküzgözü and Boğazkere are experiencing a renaissance.",
        "country_intro_fr": "🌙 Türkiye – Pont entre Orient et Occident : La Turquie est l'un des plus anciens pays viticoles du monde – les vignes sauvages y ont été domestiquées ! Aujourd'hui, des cépages autochtones comme Öküzgözü et Boğazkere connaissent une renaissance.",
        "country_image_url": "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?w=1200"
    },
    {
        "country": "Türkei",
        "country_en": "Turkey",
        "country_fr": "Turquie",
        "country_emoji": "🇹🇷",
        "region": "Ägäis / Izmir",
        "dish": "Zeytinyağlı Enginar (Artischocken in Olivenöl)",
        "dish_description": "Ägäische Eleganz: Artischocken geschmort in bestem Olivenöl mit Dill, Zitrone und Kartoffeln. Ein Klassiker der türkischen Gemüseküche.",
        "dish_description_en": "Aegean elegance: Artichokes braised in finest olive oil with dill, lemon and potatoes. A classic of Turkish vegetable cuisine.",
        "dish_description_fr": "Élégance égéenne : Artichauts braisés dans la meilleure huile d'olive avec aneth, citron et pommes de terre. Un classique de la cuisine végétale turque.",
        
        "wine_name": "Vermentino (Sardinien) oder Albariño",
        "wine_type": "Mediterraner Weißwein",
        "wine_description": "Bekannte mediterrane Weißweine mit Kräuternoten und frischer Säure. Sie ergänzen die Artischocken ohne zu dominieren.",
        "wine_description_en": "Well-known Mediterranean whites with herbal notes and fresh acidity. They complement the artichokes without dominating.",
        "wine_description_fr": "Blancs méditerranéens connus aux notes herbacées et acidité fraîche. Ils complètent les artichauts sans dominer.",
        
        "local_wine_name": "Emir (Kappadokien) oder Narince",
        "local_wine_type": "Anatolischer Weißwein",
        "local_wine_description": "🏺 Die Entdeckung: Emir aus den Höhenweinbergen Kappadokiens – knackig, mineralisch, mit grünem Apfel und Zitrus. Oder Narince – aromatischer, mit Blüten und Steinobst. Authentisch anatolisch!",
        "local_wine_description_en": "🏺 The discovery: Emir from Cappadocia's high-altitude vineyards – crisp, mineral, with green apple and citrus. Or Narince – more aromatic, with flowers and stone fruit. Authentically Anatolian!",
        "local_wine_description_fr": "🏺 La découverte : Emir des vignobles d'altitude de Cappadoce – vif, minéral, avec pomme verte et agrumes. Ou Narince – plus aromatique, avec fleurs et fruits à noyau. Authentiquement anatolien !",
        
        "country_intro": "🌙 Türkiye – Brücke zwischen Orient und Okzident.",
        "country_intro_en": "🌙 Türkiye – Bridge between East and West.",
        "country_intro_fr": "🌙 Türkiye – Pont entre Orient et Occident.",
        "country_image_url": "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?w=1200"
    },
    {
        "country": "Türkei",
        "country_en": "Turkey",
        "country_fr": "Turquie",
        "country_emoji": "🇹🇷",
        "region": "Adana / Südostanatolien",
        "dish": "Adana Kebap",
        "dish_description": "Der feurige Klassiker: Würziges Hackfleisch am Spieß gegrillt über Holzkohle. Schärfer und intensiver als der Urfa Kebap – nichts für schwache Nerven!",
        "dish_description_en": "The fiery classic: Spicy minced meat grilled on skewers over charcoal. Spicier and more intense than Urfa Kebap – not for the faint-hearted!",
        "dish_description_fr": "Le classique ardent : Viande hachée épicée grillée sur brochettes au charbon de bois. Plus épicé et intense que l'Urfa Kebap – pas pour les âmes sensibles !",
        
        "wine_name": "Malbec (Argentinien) oder Shiraz (Australien)",
        "wine_type": "Kräftiger Rotwein",
        "wine_description": "Ein kraftvoller, fruchtbetonter Rotwein mit Rauch- und Gewürznoten. Die internationale Wahl für würziges Grillfleisch.",
        "wine_description_en": "A powerful, fruit-forward red with smoke and spice notes. The international choice for spicy grilled meat.",
        "wine_description_fr": "Un rouge puissant et fruité aux notes de fumée et d'épices. Le choix international pour les grillades épicées.",
        
        "local_wine_name": "Boğazkere (Diyarbakır)",
        "local_wine_type": "Tanninreicher Rotwein",
        "local_wine_description": "🔥 Die Entdeckung: Boğazkere – 'Rachenquäler' – der kraftvollste türkische Rote. Tanninreich, dunkel, mit Brombeeren und Gewürzen. Braucht Luft oder Dekantieren, belohnt dann mit Tiefe und Komplexität!",
        "local_wine_description_en": "🔥 The discovery: Boğazkere – 'throat gripper' – Turkey's most powerful red. Tannic, dark, with blackberries and spices. Needs air or decanting, then rewards with depth and complexity!",
        "local_wine_description_fr": "🔥 La découverte : Boğazkere – 'étrangleur de gorge' – le rouge turc le plus puissant. Tannique, sombre, avec mûres et épices. Nécessite de l'air ou un carafage, puis récompense avec profondeur et complexité !",
        
        "country_intro": "🌙 Türkiye – Brücke zwischen Orient und Okzident.",
        "country_intro_en": "🌙 Türkiye – Bridge between East and West.",
        "country_intro_fr": "🌙 Türkiye – Pont entre Orient et Occident.",
        "country_image_url": "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?w=1200"
    },
    {
        "country": "Türkei",
        "country_en": "Turkey",
        "country_fr": "Turquie",
        "country_emoji": "🇹🇷",
        "region": "Zentralanatolien / Ankara",
        "dish": "Mantı (Türkische Teigtaschen)",
        "dish_description": "Winzige Teigtaschen gefüllt mit gewürztem Hackfleisch, serviert mit Joghurt-Knoblauch-Sauce und Paprikabutter. Türkisches Soulfood par excellence.",
        "dish_description_en": "Tiny dumplings filled with spiced minced meat, served with yogurt-garlic sauce and paprika butter. Turkish soul food par excellence.",
        "dish_description_fr": "Minuscules raviolis farcis de viande hachée épicée, servis avec sauce yaourt-ail et beurre au paprika. Comfort food turc par excellence.",
        
        "wine_name": "Spätburgunder (Baden) oder Pinot Noir (Burgund)",
        "wine_type": "Eleganter Rotwein",
        "wine_description": "Ein eleganter, nicht zu schwerer Roter mit guter Säure. Die Finesse eines Pinot Noir harmoniert wunderbar mit der cremigen Joghurt-Sauce.",
        "wine_description_en": "An elegant, not too heavy red with good acidity. The finesse of a Pinot Noir harmonizes wonderfully with the creamy yogurt sauce.",
        "wine_description_fr": "Un rouge élégant, pas trop lourd, avec une bonne acidité. La finesse d'un Pinot Noir s'harmonise merveilleusement avec la sauce crémeuse au yaourt.",
        
        "local_wine_name": "Kalecik Karası (Ankara)",
        "local_wine_type": "Leichter Rotwein",
        "local_wine_description": "🏰 Die Entdeckung: Kalecik Karası – Ankaras eigene Traube, fast ausgestorben und wiederbelebt. Leicht, fruchtig, mit Aromen von Erdbeeren und Veilchen. Der 'türkische Pinot Noir' – perfekt zu Joghurt-Gerichten!",
        "local_wine_description_en": "🏰 The discovery: Kalecik Karası – Ankara's own grape, nearly extinct and revived. Light, fruity, with aromas of strawberries and violets. The 'Turkish Pinot Noir' – perfect with yogurt dishes!",
        "local_wine_description_fr": "🏰 La découverte : Kalecik Karası – le cépage propre d'Ankara, presque éteint et ressuscité. Léger, fruité, avec des arômes de fraises et violettes. Le 'Pinot Noir turc' – parfait avec les plats au yaourt !",
        
        "country_intro": "🌙 Türkiye – Brücke zwischen Orient und Okzident.",
        "country_intro_en": "🌙 Türkiye – Bridge between East and West.",
        "country_intro_fr": "🌙 Türkiye – Pont entre Orient et Occident.",
        "country_image_url": "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?w=1200"
    },
    
    # ==================== CHINA ====================
    {
        "country": "China",
        "country_en": "China",
        "country_fr": "Chine",
        "country_emoji": "🇨🇳",
        "region": "Peking",
        "dish": "Peking-Ente",
        "dish_description": "Das kaiserliche Gericht: Knusprige, lackierte Entenhaut mit zartem Fleisch, serviert mit Pfannkuchen, Frühlingszwiebeln und Hoisin-Sauce.",
        "dish_description_en": "The imperial dish: Crispy lacquered duck skin with tender meat, served with pancakes, spring onions and hoisin sauce.",
        "dish_description_fr": "Le plat impérial : Peau de canard laquée croustillante avec viande tendre, servie avec crêpes, oignons verts et sauce hoisin.",
        
        "wine_name": "Pinot Noir (Burgund oder Oregon)",
        "wine_type": "Eleganter Rotwein",
        "wine_description": "Die klassische Wahl: Ein eleganter Pinot Noir mit seiner Säure und roten Frucht ergänzt das fette Entenfleisch perfekt, ohne die süße Sauce zu erschlagen.",
        "wine_description_en": "The classic choice: An elegant Pinot Noir with its acidity and red fruit complements the fatty duck meat perfectly without overwhelming the sweet sauce.",
        "wine_description_fr": "Le choix classique : Un Pinot Noir élégant avec son acidité et ses fruits rouges complète parfaitement la viande grasse de canard sans écraser la sauce sucrée.",
        
        "local_wine_name": "Cabernet Sauvignon (Ningxia)",
        "local_wine_type": "Chinesischer Rotwein",
        "local_wine_description": "🐉 Die Entdeckung: Ningxia – Chinas 'Napa Valley' am Fuße der Helan-Berge. Die besten chinesischen Cabernets kommen von hier: kraftvoll, mit reifen Früchten und würzigen Noten. Probieren Sie Silver Heights, Ao Yun oder Helan Mountain!",
        "local_wine_description_en": "🐉 The discovery: Ningxia – China's 'Napa Valley' at the foot of the Helan Mountains. The best Chinese Cabernets come from here: powerful, with ripe fruits and spicy notes. Try Silver Heights, Ao Yun or Helan Mountain!",
        "local_wine_description_fr": "🐉 La découverte : Ningxia – le 'Napa Valley' de Chine au pied des montagnes Helan. Les meilleurs Cabernets chinois viennent d'ici : puissants, avec des fruits mûrs et des notes épicées.",
        
        "country_intro": "🐉 Zhōngguó – Das erwachende Weinland: China ist der fünftgrößte Weinproduzent der Welt! In Ningxia, Xinjiang und Shandong entstehen Weine, die internationale Wettbewerbe gewinnen. Eine Revolution im Glas.",
        "country_intro_en": "🐉 Zhōngguó – The Awakening Wine Country: China is the world's fifth-largest wine producer! In Ningxia, Xinjiang and Shandong, wines are being made that win international competitions. A revolution in the glass.",
        "country_intro_fr": "🐉 Zhōngguó – Le Pays du Vin qui s'Éveille : La Chine est le cinquième producteur mondial de vin ! À Ningxia, Xinjiang et Shandong, des vins qui remportent des concours internationaux voient le jour. Une révolution dans le verre.",
        "country_image_url": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=1200"
    },
    {
        "country": "China",
        "country_en": "China",
        "country_fr": "Chine",
        "country_emoji": "🇨🇳",
        "region": "Sichuan",
        "dish": "Mapo Tofu",
        "dish_description": "Die Schärfe Sichuans: Seidentofu in feuriger Sauce mit Hackfleisch, Sichuan-Pfeffer und Doubanjiang. Betäubend-scharf und süchtig machend.",
        "dish_description_en": "The heat of Sichuan: Silken tofu in fiery sauce with minced meat, Sichuan pepper and doubanjiang. Numbing-spicy and addictive.",
        "dish_description_fr": "La chaleur du Sichuan : Tofu soyeux dans une sauce ardente avec viande hachée, poivre du Sichuan et doubanjiang. Engourdissant-épicé et addictif.",
        
        "wine_name": "Riesling Spätlese (Mosel) oder Gewürztraminer",
        "wine_type": "Aromatischer Weißwein mit Restsüße",
        "wine_description": "Süße gegen Schärfe: Ein halbtrockener Riesling oder aromatischer Gewürztraminer kühlt den Gaumen und harmoniert überraschend gut mit dem Sichuan-Pfeffer.",
        "wine_description_en": "Sweetness against heat: A semi-dry Riesling or aromatic Gewürztraminer cools the palate and harmonizes surprisingly well with Sichuan pepper.",
        "wine_description_fr": "Douceur contre piquant : Un Riesling demi-sec ou Gewürztraminer aromatique rafraîchit le palais et s'harmonise étonnamment bien avec le poivre du Sichuan.",
        
        "local_wine_name": "Ice Wine (Liaoning) oder Chardonnay (Shandong)",
        "local_wine_type": "Chinesischer Süß-/Weißwein",
        "local_wine_description": "❄️ Die Entdeckung: Chinas Nordosten (Liaoning) produziert exzellente Eisweine, die die Schärfe perfekt ausbalancieren. Oder: Ein buttriger Chardonnay aus Shandong als cremiger Kontrast zum feurigen Tofu.",
        "local_wine_description_en": "❄️ The discovery: China's northeast (Liaoning) produces excellent ice wines that perfectly balance the heat. Or: A buttery Chardonnay from Shandong as a creamy contrast to the fiery tofu.",
        "local_wine_description_fr": "❄️ La découverte : Le nord-est de la Chine (Liaoning) produit d'excellents vins de glace qui équilibrent parfaitement le piquant. Ou : Un Chardonnay beurré du Shandong comme contraste crémeux au tofu ardent.",
        
        "country_intro": "🐉 Zhōngguó – Das erwachende Weinland.",
        "country_intro_en": "🐉 Zhōngguó – The Awakening Wine Country.",
        "country_intro_fr": "🐉 Zhōngguó – Le Pays du Vin qui s'Éveille.",
        "country_image_url": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=1200"
    },
    {
        "country": "China",
        "country_en": "China",
        "country_fr": "Chine",
        "country_emoji": "🇨🇳",
        "region": "Kanton / Hongkong",
        "dish": "Dim Sum (Kantonesische Teigtaschen)",
        "dish_description": "Die Kunst des Yum Cha: Gedämpfte Har Gow, Siu Mai, Char Siu Bao – kleine Kunstwerke in Bambuskörben. Brunch auf Kantonesisch.",
        "dish_description_en": "The art of Yum Cha: Steamed Har Gow, Siu Mai, Char Siu Bao – little works of art in bamboo steamers. Brunch Cantonese style.",
        "dish_description_fr": "L'art du Yum Cha : Har Gow, Siu Mai, Char Siu Bao à la vapeur – petites œuvres d'art dans des paniers en bambou. Brunch à la cantonaise.",
        
        "wine_name": "Champagner (Brut) oder Crémant",
        "wine_type": "Eleganter Schaumwein",
        "wine_description": "Die Luxus-Kombination: Champagner mit Dim Sum ist in Hongkong längst ein Klassiker. Die Bläschen reinigen den Gaumen zwischen den verschiedenen Geschmäckern.",
        "wine_description_en": "The luxury combination: Champagne with dim sum has long been a classic in Hong Kong. The bubbles cleanse the palate between different flavors.",
        "wine_description_fr": "La combinaison luxueuse : Champagne avec dim sum est depuis longtemps un classique à Hong Kong. Les bulles nettoient le palais entre les différentes saveurs.",
        
        "local_wine_name": "Sparkling Wine (Changli) oder Pu-Erh Tee",
        "local_wine_type": "Chinesischer Schaumwein / Tee",
        "local_wine_description": "🍵 Die Entdeckung: Chinesische Schaumweine aus Changli (Hebei) werden immer besser! Traditionell gehört jedoch Pu-Erh-Tee zu Dim Sum – sein erdiger Geschmack und die fettlösenden Eigenschaften sind perfekt für die reichhaltigen Teigtaschen.",
        "local_wine_description_en": "🍵 The discovery: Chinese sparkling wines from Changli (Hebei) are getting better! Traditionally, however, Pu-erh tea belongs with dim sum – its earthy taste and fat-dissolving properties are perfect for the rich dumplings.",
        "local_wine_description_fr": "🍵 La découverte : Les vins mousseux chinois de Changli (Hebei) s'améliorent ! Traditionnellement, le thé Pu-erh accompagne les dim sum – son goût terreux et ses propriétés dissolvant les graisses sont parfaits pour les raviolis riches.",
        
        "country_intro": "🐉 Zhōngguó – Das erwachende Weinland.",
        "country_intro_en": "🐉 Zhōngguó – The Awakening Wine Country.",
        "country_intro_fr": "🐉 Zhōngguó – Le Pays du Vin qui s'Éveille.",
        "country_image_url": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=1200"
    }
]

async def update_exotic_pairings():
    """Update the regional pairings with exotic countries"""
    print("=" * 60)
    print("🌍 EXOTISCHE LÄNDER IM SOMMELIER-KOMPASS AKTUALISIEREN")
    print("=" * 60)
    
    # Load existing pairings
    data_file = ROOT_DIR / "data" / "regional_pairings.json"
    with open(data_file, 'r', encoding='utf-8') as f:
        existing_pairings = json.load(f)
    
    print(f"📊 Vorhandene Pairings: {len(existing_pairings)}")
    
    # Remove old exotic pairings
    exotic_countries = ['Griechenland', 'Japan', 'Türkei', 'China']
    filtered_pairings = [p for p in existing_pairings if p.get('country') not in exotic_countries]
    removed = len(existing_pairings) - len(filtered_pairings)
    print(f"🗑️  Entfernt: {removed} alte exotische Pairings")
    
    # Add new exotic pairings with IDs
    import uuid
    for pairing in EXOTIC_PAIRINGS:
        pairing['id'] = str(uuid.uuid4())
    
    # Combine
    all_pairings = filtered_pairings + EXOTIC_PAIRINGS
    print(f"➕ Hinzugefügt: {len(EXOTIC_PAIRINGS)} neue exotische Pairings")
    
    # Save to JSON file
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(all_pairings, f, ensure_ascii=False, indent=2)
    print(f"💾 JSON gespeichert: {len(all_pairings)} Pairings")
    
    # Update MongoDB
    await db.regional_pairings.delete_many({"country": {"$in": exotic_countries}})
    if EXOTIC_PAIRINGS:
        await db.regional_pairings.insert_many(EXOTIC_PAIRINGS)
    
    final_count = await db.regional_pairings.count_documents({})
    print(f"🗄️  MongoDB aktualisiert: {final_count} Pairings")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ FERTIG! Neue Struktur:")
    print("=" * 60)
    for country in exotic_countries:
        count = len([p for p in EXOTIC_PAIRINGS if p.get('country') == country])
        print(f"   {country}: {count} Pairings")
    print("\n🍷 Jedes Pairing hat jetzt:")
    print("   1. Internationale Empfehlung (sichere Wahl)")
    print("   2. Lokale Alternative (zum Entdecken)")


if __name__ == "__main__":
    asyncio.run(update_exotic_pairings())
