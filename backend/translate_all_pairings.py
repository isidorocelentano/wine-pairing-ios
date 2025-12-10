"""
Complete translations for ALL dishes and wines (EN/FR)
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

# Complete dish translations
DISHES = {
    # Italien
    "Tartufo d'Alba (Weißer Trüffel)": {
        "de": "Der weiße Trüffel aus Alba ist eine der teuersten und begehrtesten Zutaten der Welt. Sein intensives, erdiges Aroma mit nussigen und knoblauchartigen Noten macht jedes Gericht zu einem außergewöhnlichen Erlebnis.",
        "en": "The white truffle from Alba is one of the most expensive and coveted ingredients in the world. Its intense, earthy aroma with nutty and garlicky notes makes every dish an exceptional experience.",
        "fr": "La truffe blanche d'Alba est l'un des ingrédients les plus chers et les plus convoités au monde. Son arôme intense et terreux aux notes de noisette et d'ail fait de chaque plat une expérience exceptionnelle."
    },
    "Bistecca alla Fiorentina": {
        "de": "Ein mindestens 3cm dickes T-Bone-Steak vom Chianina-Rind, gegrillt über Holzkohle. Außen knusprig, innen saftig und rosa – ein Klassiker der toskanischen Küche.",
        "en": "A T-bone steak at least 3cm thick from Chianina beef, grilled over charcoal. Crispy outside, juicy and pink inside – a classic of Tuscan cuisine.",
        "fr": "Un T-bone d'au moins 3 cm d'épaisseur de bœuf Chianina, grillé au charbon de bois. Croustillant à l'extérieur, juteux et rosé à l'intérieur – un classique de la cuisine toscane."
    },
    "Pizza Napoletana": {
        "de": "Die neapolitanische Pizza mit ihrem luftigen, leicht verkohlten Rand und dem einfachen Belag aus Tomatensauce, Mozzarella und Basilikum ist UNESCO-Weltkulturerbe.",
        "en": "The Neapolitan pizza with its airy, slightly charred edge and simple topping of tomato sauce, mozzarella and basil is a UNESCO World Heritage Site.",
        "fr": "La pizza napolitaine avec sa croûte aérée et légèrement carbonisée et sa garniture simple de sauce tomate, mozzarella et basilic est un patrimoine mondial de l'UNESCO."
    },
    "Cannoli": {
        "de": "Knusprige, frittierte Teigrollen gefüllt mit süßer Ricotta-Creme, oft verfeinert mit Pistazien oder kandierten Früchten – ein sizilianischer Dessertklassiker.",
        "en": "Crispy, fried pastry rolls filled with sweet ricotta cream, often refined with pistachios or candied fruits – a Sicilian dessert classic.",
        "fr": "Rouleaux de pâte croustillants et frits fourrés de crème de ricotta sucrée, souvent agrémentés de pistaches ou de fruits confits – un classique des desserts siciliens."
    },
    "Polenta": {
        "de": "Cremiger Maisgriess, der als Beilage zu Schmorgerichten oder als eigenständiges Gericht serviert wird. In Venetien eine Institution.",
        "en": "Creamy cornmeal served as a side dish to braised dishes or as a standalone dish. An institution in Veneto.",
        "fr": "Semoule de maïs crémeuse servie en accompagnement de plats braisés ou en plat principal. Une institution en Vénétie."
    },
    "Carbonara": {
        "de": "Pasta mit einer Sauce aus Ei, Pecorino Romano, Guanciale (Schweinebacke) und schwarzem Pfeffer – römische Einfachheit in Perfektion.",
        "en": "Pasta with a sauce made from egg, Pecorino Romano, guanciale (pork jowl) and black pepper – Roman simplicity at its finest.",
        "fr": "Pâtes avec une sauce à base d'œuf, de Pecorino Romano, de guanciale (joue de porc) et de poivre noir – la simplicité romaine à la perfection."
    },
    "Parmigiano Reggiano": {
        "de": "Der 'König der Käse' reift mindestens 12 Monate und entwickelt kristalline Strukturen und komplexe nussige Aromen.",
        "en": "The 'King of Cheeses' ages for at least 12 months and develops crystalline structures and complex nutty flavors.",
        "fr": "Le 'Roi des Fromages' vieillit pendant au moins 12 mois et développe des structures cristallines et des arômes de noisette complexes."
    },
    "Pesto alla Genovese": {
        "de": "Basilikum, Piniennüsse, Knoblauch, Parmigiano und Olivenöl – die grüne Seele Liguriens.",
        "en": "Basil, pine nuts, garlic, Parmigiano and olive oil – the green soul of Liguria.",
        "fr": "Basilic, pignons de pin, ail, Parmigiano et huile d'olive – l'âme verte de la Ligurie."
    },
    
    # Frankreich
    "Boeuf Bourguignon": {
        "de": "Rindfleisch geschmort in Burgunder-Rotwein mit Zwiebeln, Karotten, Speck und Champignons. Ein Gericht, das die Seele Burgunds einfängt.",
        "en": "Beef braised in Burgundy red wine with onions, carrots, bacon and mushrooms. A dish that captures the soul of Burgundy.",
        "fr": "Bœuf braisé au vin rouge de Bourgogne avec oignons, carottes, lard et champignons. Un plat qui capture l'âme de la Bourgogne."
    },
    "Bouillabaisse": {
        "de": "Die berühmte provenzalische Fischsuppe mit Safran, Fenchel und verschiedenen Mittelmeerfischen. Serviert mit Rouille und Baguette.",
        "en": "The famous Provençal fish soup with saffron, fennel and various Mediterranean fish. Served with rouille and baguette.",
        "fr": "La célèbre soupe de poisson provençale au safran, fenouil et divers poissons méditerranéens. Servie avec de la rouille et de la baguette."
    },
    "Choucroute Garnie": {
        "de": "Elsässer Sauerkraut mit verschiedenen Fleischsorten und Würsten – ein herzhaftes Wintergericht.",
        "en": "Alsatian sauerkraut with various meats and sausages – a hearty winter dish.",
        "fr": "Choucroute alsacienne avec diverses viandes et saucisses – un plat d'hiver copieux."
    },
    "Confit de Canard": {
        "de": "Langsam in eigenem Fett gegarte Entenkeule – zart, saftig und voller Geschmack.",
        "en": "Duck leg slowly cooked in its own fat – tender, juicy and full of flavor.",
        "fr": "Cuisse de canard cuite lentement dans sa propre graisse – tendre, juteuse et pleine de saveur."
    },
    "Tarte Tatin": {
        "de": "Karamellisierter umgestürzter Apfelkuchen, warm serviert – eine süße Verführung aus der Loire.",
        "en": "Caramelized upside-down apple tart, served warm – a sweet temptation from the Loire.",
        "fr": "Tarte aux pommes caramélisée et renversée, servie chaude – une douce tentation de la Loire."
    },
    
    # Spanien
    "Gazpacho": {
        "de": "Kalte andalusische Gemüsesuppe aus Tomaten, Paprika, Gurke und Knoblauch – erfrischend an heißen Sommertagen.",
        "en": "Cold Andalusian vegetable soup made from tomatoes, peppers, cucumber and garlic – refreshing on hot summer days.",
        "fr": "Soupe froide andalouse aux légumes à base de tomates, poivrons, concombre et ail – rafraîchissante lors des chaudes journées d'été."
    },
    "Bacalao a la Vizcaína": {
        "de": "Baskischer Kabeljau in einer samtigen Paprikasauce – ein Meisterwerk der Meeresküche.",
        "en": "Basque cod in a velvety pepper sauce – a masterpiece of seafood cuisine.",
        "fr": "Morue basque dans une sauce veloutée aux poivrons – un chef-d'œuvre de la cuisine marine."
    },
    "Pulpo a la Gallega": {
        "de": "Galizischer Oktopus auf Kartoffeln mit Paprikapulver und Olivenöl – einfach und brillant.",
        "en": "Galician octopus on potatoes with paprika and olive oil – simple and brilliant.",
        "fr": "Poulpe galicien sur pommes de terre avec paprika et huile d'olive – simple et brillant."
    },
    "Suquet de Peix": {
        "de": "Katalanischer Fischeintopf mit Kartoffeln, Tomaten und Safran.",
        "en": "Catalan fish stew with potatoes, tomatoes and saffron.",
        "fr": "Ragoût de poisson catalan aux pommes de terre, tomates et safran."
    },
    "Patatas a la Riojana": {
        "de": "Rioja-Kartoffel-Eintopf mit Chorizo und Paprika.",
        "en": "Rioja potato stew with chorizo and paprika.",
        "fr": "Ragoût de pommes de terre de la Rioja avec chorizo et paprika."
    },
    
    # Österreich
    "Wiener Schnitzel": {
        "de": "Hauchdünn geklopftes Kalbfleisch in goldbrauner Panade – knusprig, zart und eine Wiener Institution.",
        "en": "Paper-thin veal in golden-brown breading – crispy, tender and a Viennese institution.",
        "fr": "Veau finement battu dans une panure dorée – croustillant, tendre et une institution viennoise."
    },
    "Salzburger Nockerl": {
        "de": "Luftige Süßspeise aus Eischnee, die an die Salzburger Berge erinnert – eine süße Wolke.",
        "en": "Airy sweet dish made from egg whites, reminiscent of Salzburg's mountains – a sweet cloud.",
        "fr": "Dessert aérien à base de blancs d'œufs, rappelant les montagnes de Salzbourg – un nuage sucré."
    },
    "Steirisches Backhendl": {
        "de": "Knusprig gebratenes Huhn nach steirischer Art.",
        "en": "Crispy fried chicken, Styrian style.",
        "fr": "Poulet frit croustillant à la styrienne."
    },
    "Ganslbraten": {
        "de": "Festlicher Gänsebraten, traditionell zu Martini serviert.",
        "en": "Festive roast goose, traditionally served at Martinmas.",
        "fr": "Oie rôtie festive, traditionnellement servie à la Saint-Martin."
    },
    
    # Schweiz
    "Walliser Raclette": {
        "de": "Geschmolzener Käse über Pellkartoffeln – alpiner Genuss pur.",
        "en": "Melted cheese over boiled potatoes – pure alpine pleasure.",
        "fr": "Fromage fondu sur pommes de terre en robe des champs – pur plaisir alpin."
    },
    "Bündner Gerstensuppe": {
        "de": "Kräftige Suppe mit Gerste und Gemüse aus Graubünden.",
        "en": "Hearty soup with barley and vegetables from Graubünden.",
        "fr": "Soupe copieuse à l'orge et aux légumes des Grisons."
    },
    "Zürcher Geschnetzeltes": {
        "de": "Zartes Kalbfleisch in cremiger Rahmsauce mit Pilzen.",
        "en": "Tender veal in creamy cream sauce with mushrooms.",
        "fr": "Veau tendre dans une sauce crémeuse aux champignons."
    },
    "Polenta Ticinese": {
        "de": "Tessin-Polenta, oft mit Schmorfleisch serviert.",
        "en": "Ticino polenta, often served with braised meat.",
        "fr": "Polenta tessinoise, souvent servie avec de la viande braisée."
    },
    
    # Griechenland
    "Tomatokeftedes": {
        "de": "Knusprige Tomatenpuffer aus Santorini mit Kräutern.",
        "en": "Crispy tomato fritters from Santorini with herbs.",
        "fr": "Beignets de tomates croustillants de Santorin aux herbes."
    },
    "Dakos": {
        "de": "Kretischer Gerstenzwieback mit Tomaten, Feta und Olivenöl.",
        "en": "Cretan barley rusk with tomatoes, feta and olive oil.",
        "fr": "Biscotte d'orge crétoise aux tomates, feta et huile d'olive."
    },
    "Moussaka": {
        "de": "Geschichteter Auflauf aus Auberginen, Hackfleisch und Béchamelsauce.",
        "en": "Layered casserole of eggplant, minced meat and béchamel sauce.",
        "fr": "Gratin en couches d'aubergines, viande hachée et sauce béchamel."
    },
    "Souvlaki": {
        "de": "Gegrillte Fleischspieße – griechisches Street Food.",
        "en": "Grilled meat skewers – Greek street food.",
        "fr": "Brochettes de viande grillées – street food grec."
    },
    
    # Japan
    "Edo-mae Sushi": {
        "de": "Traditionelles Tokio-Sushi mit frischem Fisch und perfekt gewürztem Reis.",
        "en": "Traditional Tokyo sushi with fresh fish and perfectly seasoned rice.",
        "fr": "Sushi traditionnel de Tokyo avec poisson frais et riz parfaitement assaisonné."
    },
    "Okonomiyaki": {
        "de": "Herzhafter japanischer Pfannkuchen mit Kohl und verschiedenen Toppings.",
        "en": "Savory Japanese pancake with cabbage and various toppings.",
        "fr": "Crêpe japonaise salée au chou et diverses garnitures."
    },
    "Miso Ramen": {
        "de": "Reichhaltige Nudelsuppe mit Miso-Brühe und verschiedenen Toppings.",
        "en": "Rich noodle soup with miso broth and various toppings.",
        "fr": "Soupe de nouilles riche au bouillon miso et diverses garnitures."
    },
    
    # Deutschland
    "Pfälzer Saumagen": {
        "de": "Pfälzer Spezialität aus Schweinmagen gefüllt mit Kartoffeln und Fleisch.",
        "en": "Palatinate specialty of pork stomach filled with potatoes and meat.",
        "fr": "Spécialité du Palatinat d'estomac de porc farci de pommes de terre et de viande."
    },
    "Fränkische Bratwurst": {
        "de": "Grobkörnige Bratwurst aus Franken, oft über Buchenholz gegrillt.",
        "en": "Coarse-grained sausage from Franconia, often grilled over beech wood.",
        "fr": "Saucisse à gros grains de Franconie, souvent grillée sur bois de hêtre."
    },
    "Schweinshaxe": {
        "de": "Knusprige bayerische Schweinshaxe mit krosse Kruste.",
        "en": "Crispy Bavarian pork knuckle with crispy crust.",
        "fr": "Jarret de porc bavarois croustillant avec croûte croustillante."
    },
    "Himmel un Ääd": {
        "de": "Rheinische Spezialität aus Kartoffelpüree, Apfelmus und Blutwurst.",
        "en": "Rhenish specialty of mashed potatoes, applesauce and blood sausage.",
        "fr": "Spécialité rhénane de purée de pommes de terre, compote de pommes et boudin noir."
    },
    
    # Türkei
    "İskender Kebap": {
        "de": "Döner auf Fladenbrot mit Tomatensoße, Joghurt und zerlassener Butter.",
        "en": "Döner on flatbread with tomato sauce, yogurt and melted butter.",
        "fr": "Döner sur pain plat avec sauce tomate, yaourt et beurre fondu."
    },
    "Zeytinyağlı Enginar": {
        "de": "In Olivenöl geschmorte Artischocken – ein Klassiker der türkischen Meze-Küche.",
        "en": "Artichokes braised in olive oil – a classic of Turkish meze cuisine.",
        "fr": "Artichauts braisés à l'huile d'olive – un classique de la cuisine meze turque."
    },
    "Adana Kebap": {
        "de": "Scharfer Hackfleischspieß aus Adana, über Holzkohle gegrillt.",
        "en": "Spicy minced meat skewer from Adana, grilled over charcoal.",
        "fr": "Brochette de viande hachée épicée d'Adana, grillée au charbon de bois."
    }
}

# Complete wine translations
WINES = {
    "Barolo oder Barbaresco": {
        "de": "Die beiden großen Nebbiolo-Weine des Piemonts. Kraftvoll, tanninreich und langlebig mit Aromen von Rosen, Teer und roten Früchten.",
        "en": "The two great Nebbiolo wines of Piedmont. Powerful, tannic and long-lived with aromas of roses, tar and red fruits.",
        "fr": "Les deux grands vins de Nebbiolo du Piémont. Puissants, tanniques et de longue garde avec des arômes de roses, de goudron et de fruits rouges."
    },
    "Chianti Classico": {
        "de": "Sangiovese-Rotwein aus der Toskana mit Kirsch-Aromen, lebendiger Säure und eleganten Tanninen.",
        "en": "Sangiovese red wine from Tuscany with cherry aromas, vibrant acidity and elegant tannins.",
        "fr": "Vin rouge Sangiovese de Toscane aux arômes de cerise, acidité vive et tanins élégants."
    },
    "Fiano di Avellino": {
        "de": "Mineralischer Weißwein aus Kampanien mit Noten von Haselnuss und Honig.",
        "en": "Mineral white wine from Campania with notes of hazelnut and honey.",
        "fr": "Vin blanc minéral de Campanie avec des notes de noisette et de miel."
    },
    "Marsala Dolce": {
        "de": "Süßer Likörwein aus Sizilien, perfekt zu Desserts.",
        "en": "Sweet fortified wine from Sicily, perfect with desserts.",
        "fr": "Vin liquoreux de Sicile, parfait avec les desserts."
    },
    "Prosecco oder Amarone": {
        "de": "Prosecco: perlender Weißwein. Amarone: kraftvoller, getrockneter Rotwein aus Valpolicella.",
        "en": "Prosecco: sparkling white wine. Amarone: powerful dried red wine from Valpolicella.",
        "fr": "Prosecco: vin blanc pétillant. Amarone: vin rouge puissant de raisins séchés de Valpolicella."
    },
    "Frascati": {
        "de": "Frischer, unkomplizierter Weißwein aus Latium.",
        "en": "Fresh, uncomplicated white wine from Lazio.",
        "fr": "Vin blanc frais et simple du Latium."
    },
    "Lambrusco": {
        "de": "Leicht schäumender, halbtrockener Rotwein aus der Emilia-Romagna.",
        "en": "Lightly sparkling, semi-dry red wine from Emilia-Romagna.",
        "fr": "Vin rouge légèrement pétillant et demi-sec d'Émilie-Romagne."
    },
    "Pigato": {
        "de": "Aromatischer ligurischer Weißwein mit salziger Meeresnote.",
        "en": "Aromatic Ligurian white wine with salty sea notes.",
        "fr": "Vin blanc aromatique de Ligurie aux notes salines marines."
    },
    "Pinot Noir aus Burgund": {
        "de": "Eleganter, komplexer Rotwein mit Aromen von roten Beeren, Erde und Gewürzen.",
        "en": "Elegant, complex red wine with aromas of red berries, earth and spices.",
        "fr": "Vin rouge élégant et complexe aux arômes de baies rouges, terre et épices."
    },
    "Bandol Rosé": {
        "de": "Kraftvoller provenzalischer Rosé mit Struktur und Tiefe.",
        "en": "Powerful Provençal rosé with structure and depth.",
        "fr": "Rosé provençal puissant avec structure et profondeur."
    },
    "Riesling": {
        "de": "Trockener Elsässer Riesling mit präziser Säure und mineralischen Noten.",
        "en": "Dry Alsatian Riesling with precise acidity and mineral notes.",
        "fr": "Riesling alsacien sec avec une acidité précise et des notes minérales."
    },
    "Saint-Émilion": {
        "de": "Bordeaux-Rotwein von der rechten Ufer, Merlot-dominiert, samtig und fruchtbetont.",
        "en": "Bordeaux red wine from the right bank, Merlot-dominated, velvety and fruit-forward.",
        "fr": "Vin rouge de Bordeaux rive droite, dominé par le Merlot, velouté et fruité."
    },
    "Vouvray Moelleux": {
        "de": "Süßer Chenin Blanc aus der Loire mit Honig- und Aprikosen-Aromen.",
        "en": "Sweet Chenin Blanc from the Loire with honey and apricot aromas.",
        "fr": "Chenin Blanc doux de la Loire aux arômes de miel et d'abricot."
    },
    "Fino Sherry": {
        "de": "Trockener, oxidativer Weißwein aus Jerez mit Mandel- und Hefenoten.",
        "en": "Dry, oxidative white wine from Jerez with almond and yeast notes.",
        "fr": "Vin blanc sec et oxydatif de Jerez aux notes d'amande et de levure."
    },
    "Txakoli": {
        "de": "Leichter, leicht perlender baskischer Weißwein mit frischer Säure.",
        "en": "Light, slightly sparkling Basque white wine with fresh acidity.",
        "fr": "Vin blanc basque léger et légèrement pétillant à l'acidité fraîche."
    },
    "Albariño": {
        "de": "Aromatischer galizischer Weißwein mit Pfirsich und Zitrus-Noten.",
        "en": "Aromatic Galician white wine with peach and citrus notes.",
        "fr": "Vin blanc galicien aromatique aux notes de pêche et d'agrumes."
    },
    "Cava": {
        "de": "Spanischer Schaumwein nach traditioneller Methode.",
        "en": "Spanish sparkling wine made using the traditional method.",
        "fr": "Vin mousseux espagnol élaboré selon la méthode traditionnelle."
    },
    "Rioja Crianza": {
        "de": "Tempranillo-Rotwein mit Eichenfass-Reifung, ausgewogen und zugänglich.",
        "en": "Tempranillo red wine with oak barrel aging, balanced and accessible.",
        "fr": "Vin rouge Tempranillo avec vieillissement en fût de chêne, équilibré et accessible."
    },
    "Grüner Veltliner": {
        "de": "Österreichs Klassiker – frisch, pfeffrig, mit guter Säure.",
        "en": "Austria's classic – fresh, peppery, with good acidity.",
        "fr": "Le classique autrichien – frais, poivré, avec une bonne acidité."
    },
    "Muskateller": {
        "de": "Aromatischer Weißwein mit Rosenduft.",
        "en": "Aromatic white wine with rose fragrance.",
        "fr": "Vin blanc aromatique au parfum de rose."
    },
    "Sauvignon Blanc": {
        "de": "Steirischer Sauvignon mit Stachelbeere und Gras-Aromen.",
        "en": "Styrian Sauvignon with gooseberry and grass aromas.",
        "fr": "Sauvignon styrien aux arômes de groseille à maquereau et d'herbe."
    },
    "Blaufränkisch": {
        "de": "Kräftiger österreichischer Rotwein mit Kirsch und Gewürznoten.",
        "en": "Powerful Austrian red wine with cherry and spice notes.",
        "fr": "Vin rouge autrichien puissant aux notes de cerise et d'épices."
    },
    "Fendant oder Petite Arvine": {
        "de": "Walliser Chasselas bzw. seltene alpine Weißwein-Rarität.",
        "en": "Valais Chasselas or rare alpine white wine rarity.",
        "fr": "Chasselas valaisan ou rareté de vin blanc alpin."
    },
    "Pinot Noir": {
        "de": "Schweizer Pinot Noir aus der Bündner Herrschaft.",
        "en": "Swiss Pinot Noir from Graubünden Herrschaft.",
        "fr": "Pinot Noir suisse de la Seigneurie des Grisons."
    },
    "Chardonnay": {
        "de": "Eleganter Schweizer Chardonnay.",
        "en": "Elegant Swiss Chardonnay.",
        "fr": "Chardonnay suisse élégant."
    },
    "Merlot del Ticino": {
        "de": "Tessiner Merlot mit südlicher Frucht.",
        "en": "Ticino Merlot with southern fruit.",
        "fr": "Merlot tessinois aux fruits méridionaux."
    },
    "Assyrtiko": {
        "de": "Mineralischer Weißwein von Santorini mit salziger Note.",
        "en": "Mineral white wine from Santorini with salty notes.",
        "fr": "Vin blanc minéral de Santorin aux notes salines."
    },
    "Vidiano": {
        "de": "Aromatischer kretischer Weißwein.",
        "en": "Aromatic Cretan white wine.",
        "fr": "Vin blanc crétois aromatique."
    },
    "Xinomavro": {
        "de": "Tanninreicher griechischer Rotwein mit Alterungspotential.",
        "en": "Tannic Greek red wine with aging potential.",
        "fr": "Vin rouge grec tannique avec potentiel de vieillissement."
    },
    "Agiorgitiko": {
        "de": "Samtiger Rotwein aus dem Peloponnes.",
        "en": "Velvety red wine from the Peloponnese.",
        "fr": "Vin rouge velouté du Péloponnèse."
    },
    "Koshu": {
        "de": "Japanischer Weißwein, mineralisch und delikat.",
        "en": "Japanese white wine, mineral and delicate.",
        "fr": "Vin blanc japonais, minéral et délicat."
    },
    "Prosecco oder Cava": {
        "de": "Perlweine, die zu herzhaften Pfannkuchen passen.",
        "en": "Sparkling wines that pair well with savory pancakes.",
        "fr": "Vins mousseux qui s'accordent bien avec les crêpes salées."
    },
    "Junmai Sake": {
        "de": "Vollmundiger Sake aus nur Reis, Wasser und Koji.",
        "en": "Full-bodied sake made only from rice, water and koji.",
        "fr": "Saké corsé fait uniquement de riz, eau et koji."
    },
    "Silvaner": {
        "de": "Erdiger, zurückhaltender fränkischer Weißwein.",
        "en": "Earthy, restrained Franconian white wine.",
        "fr": "Vin blanc franconien terreux et retenu."
    },
    "Spätburgunder": {
        "de": "Deutscher Pinot Noir mit Eleganz und Finesse.",
        "en": "German Pinot Noir with elegance and finesse.",
        "fr": "Pinot Noir allemand avec élégance et finesse."
    },
    "Öküzgözü": {
        "de": "Mittelschwerer türkischer Rotwein mit Säure und Frucht.",
        "en": "Medium-bodied Turkish red wine with acidity and fruit.",
        "fr": "Vin rouge turc de corps moyen avec acidité et fruit."
    },
    "Emir": {
        "de": "Klarer, mineralischer türkischer Weißwein.",
        "en": "Clear, mineral Turkish white wine.",
        "fr": "Vin blanc turc clair et minéral."
    },
    "Bornova Misketi": {
        "de": "Aromatischer türkischer Weißwein oder Rosé.",
        "en": "Aromatic Turkish white wine or rosé.",
        "fr": "Vin blanc ou rosé turc aromatique."
    }
}


async def translate_all():
    """Update ALL dishes and wines with complete translations"""
    
    print("🌍 Complete Translation Update\n")
    print("=" * 60)
    
    total_dishes = 0
    total_wines = 0
    
    # Update all dishes
    print("\n🍽️ Translating ALL Dishes...")
    for dish_name, translations in DISHES.items():
        # Match by the beginning of the dish name (before any parentheses)
        dish_key = dish_name.split('(')[0].strip()
        
        result = await db.regional_pairings.update_many(
            {"dish": {"$regex": f"^{dish_key}", "$options": "i"}},
            {
                "$set": {
                    "dish_description": translations["de"],
                    "dish_description_en": translations["en"],
                    "dish_description_fr": translations["fr"]
                }
            }
        )
        
        if result.modified_count > 0:
            total_dishes += result.modified_count
            print(f"  ✓ {dish_key}: {result.modified_count} doc(s)")
    
    # Update all wines
    print("\n🍷 Translating ALL Wines...")
    for wine_name, translations in WINES.items():
        # Match by the beginning of the wine name (before "oder")
        wine_key = wine_name.split(' oder')[0].split(' aus')[0].strip()
        
        result = await db.regional_pairings.update_many(
            {"wine_name": {"$regex": wine_key, "$options": "i"}},
            {
                "$set": {
                    "wine_description": translations["de"],
                    "wine_description_en": translations["en"],
                    "wine_description_fr": translations["fr"]
                }
            }
        )
        
        if result.modified_count > 0:
            total_wines += result.modified_count
            print(f"  ✓ {wine_key}: {result.modified_count} doc(s)")
    
    print(f"\n{'='*60}")
    print(f"✅ Translation Complete!")
    print(f"   Total Dishes Translated: {total_dishes}")
    print(f"   Total Wines Translated: {total_wines}")
    
    # Verification
    print(f"\n📊 Verification:")
    total = await db.regional_pairings.count_documents({})
    with_dish_en = await db.regional_pairings.count_documents({"dish_description_en": {"$exists": True, "$ne": None}})
    with_wine_en = await db.regional_pairings.count_documents({"wine_description_en": {"$exists": True, "$ne": None}})
    
    print(f"   Total Pairings: {total}")
    print(f"   With Dish EN: {with_dish_en}/{total} ({100*with_dish_en//total}%)")
    print(f"   With Wine EN: {with_wine_en}/{total} ({100*with_wine_en//total}%)")


async def main():
    await translate_all()
    print("\n" + "=" * 60)


if __name__ == '__main__':
    asyncio.run(main())
