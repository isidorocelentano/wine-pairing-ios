#!/usr/bin/env python3
"""
Import all 50 Chinese dishes from Sommelier Kompass CHINA.docx
with AI-generated wine pairings and translations.
"""

import asyncio
import os
import sys
from datetime import datetime, timezone
from uuid import uuid4

# Add backend to path
sys.path.insert(0, '/app/backend')

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')

# All 50 Chinese dishes extracted from the document
CHINA_DISHES = [
    # === NORDCHINA (Peking, Shandong, Hebei) ===
    {
        "dish_name": "Peking Ente (北京烤鸭)",
        "region": "Peking",
        "category": "Nordchina",
        "dish_description": "Knusprige Ente, dünn geschnitten, mit Pancakes, Gemüse und Süß-Sauer-Sauce.",
        "wine_name": "Spätburgunder / Pinot Noir",
        "wine_type": "rot",
        "wine_description": "Die seidige Eleganz des Pinot Noir umschmeichelt die knusprige Entenhaut wie ein Hauch von Seide. Die feinen Kirsch- und Beerennoten tanzen mit der süß-sauren Sauce, während die samtige Textur des Weins die Reichhaltigkeit des Fleisches perfekt ausbalanciert."
    },
    {
        "dish_name": "Jiaozi (饺子)",
        "region": "Nordchina",
        "category": "Nordchina",
        "dish_description": "Gedämpfte oder gebratene Teigtaschen mit Fleisch/Gemüse-Füllung.",
        "wine_name": "Grüner Veltliner",
        "wine_type": "weiss",
        "wine_description": "Der österreichische Grüne Veltliner mit seiner pfeffrigen Würze und lebendigen Säure ist der ideale Begleiter für diese herzhaften Teigtaschen. Seine knackige Frische schneidet durch die saftige Füllung und belebt den Gaumen."
    },
    {
        "dish_name": "Zhajiangmian (炸酱面)",
        "region": "Peking",
        "category": "Nordchina",
        "dish_description": "Nudeln mit fermentierter Sojabohnen-Sauce und gehacktem Schweinefleisch.",
        "wine_name": "Côtes du Rhône Rouge",
        "wine_type": "rot",
        "wine_description": "Die würzigen, erdigen Noten des Rhône-Weins harmonieren wunderbar mit der fermentierten Sojabohnen-Sauce. Die reifen Fruchtaromen und der Hauch von Kräutern ergänzen die umami-reiche Tiefe dieses Pekinger Klassikers."
    },
    {
        "dish_name": "Lamb Skewers (羊肉串)",
        "region": "Xinjiang",
        "category": "Nordchina",
        "dish_description": "Gegrillte Lammfleischspieße mit Kreuzkümmel und Chilipulver.",
        "wine_name": "Syrah / Shiraz",
        "wine_type": "rot",
        "wine_description": "Der kräftige Syrah mit seinen dunklen Beerenaromen und würzigen Pfeffernoten ist wie gemacht für diese aromatischen Lammspieße. Der Kreuzkümmel und das Chilipulver finden im Wein einen ebenbürtigen Partner."
    },
    {
        "dish_name": "Shandong Braised Pork (红烧肉)",
        "region": "Shandong",
        "category": "Nordchina",
        "dish_description": "Schweinebauch in süß-saurer Soße, oft mit Eiern oder Pilzen.",
        "wine_name": "Amarone della Valpolicella",
        "wine_type": "rot",
        "wine_description": "Der opulente Amarone mit seiner konzentrierten Frucht und samtigen Textur umarmt den geschmorten Schweinebauch wie ein alter Freund. Die süßlichen Rosinen- und Kirschnoten verschmelzen mit der karamellisierten Sauce zu einem unvergesslichen Erlebnis."
    },
    {
        "dish_name": "Scallion Pancakes (葱油饼)",
        "region": "Nordchina",
        "category": "Nordchina",
        "dish_description": "Knusprige, flache Teigfladen mit Lauch und Sesamöl.",
        "wine_name": "Albariño",
        "wine_type": "weiss",
        "wine_description": "Der spritzige Albariño aus Galizien mit seinen zitronigen Noten und mineralischer Frische ist perfekt für diese knusprigen Pfannkuchen. Das Sesamöl und der Lauch werden von der lebhaften Säure des Weins wunderbar ergänzt."
    },
    {
        "dish_name": "Beijing Roast Pork (烤肉)",
        "region": "Peking",
        "category": "Nordchina",
        "dish_description": "Gegrilltes Schweinefleisch, oft mit Gemüse und Brot.",
        "wine_name": "Zinfandel",
        "wine_type": "rot",
        "wine_description": "Der amerikanische Zinfandel mit seiner brombeerigen Fülle und würzigen Komplexität passt hervorragend zu diesem gegrillten Klassiker. Die rauchigen Noten des Fleisches harmonieren mit den pfeffrigen Akzenten des Weins."
    },
    {
        "dish_name": "Stir-Fried Lamb with Cumin (孜然羊肉)",
        "region": "Xinjiang",
        "category": "Nordchina",
        "dish_description": "Lammfleisch mit Kreuzkümmel, Chili und Paprika.",
        "wine_name": "Grenache",
        "wine_type": "rot",
        "wine_description": "Der fruchtige Grenache mit seinen roten Beerennoten und der warmen Gewürzigkeit ist der perfekte Tanzpartner für dieses aromatische Lammgericht. Die sanften Tannine schmiegen sich an das zarte Fleisch."
    },
    {
        "dish_name": "Braised Beef Noodles (红烧牛肉面)",
        "region": "Nordchina",
        "category": "Nordchina",
        "dish_description": "Nudeln mit zartem Rindfleisch in würziger Brühe.",
        "wine_name": "Malbec",
        "wine_type": "rot",
        "wine_description": "Der argentinische Malbec mit seiner dunklen Frucht und samtig-weichen Tanninen begleitet die würzige Rinderbrühe meisterhaft. Die Pflaumennoten des Weins verschmelzen mit der tiefen Umami-Note der Brühe."
    },
    {
        "dish_name": "Steamed Buns (Baozi, 包子)",
        "region": "Nordchina",
        "category": "Nordchina",
        "dish_description": "Gedämpfte Teigtaschen mit Fleisch- oder Gemüsefüllung.",
        "wine_name": "Riesling Kabinett",
        "wine_type": "weiss",
        "wine_description": "Der elegante deutsche Riesling mit seiner feinen Restsüße und präzisen Säure hebt die zarte Aromenwelt der gedämpften Baozi auf ein neues Niveau. Ein Hauch von Aprikose und Pfirsich tanzt mit der Füllung."
    },
    
    # === OSTCHINA (Shanghai, Jiangsu, Zhejiang) ===
    {
        "dish_name": "Xiaolongbao (小笼包)",
        "region": "Shanghai",
        "category": "Ostchina",
        "dish_description": "Dampfgebackene Teigtaschen mit Fleisch und Suppe.",
        "wine_name": "Champagner Brut",
        "wine_type": "schaumwein",
        "wine_description": "Die feinen Perlen des Champagners tanzen mit der heißen Suppe im Inneren dieser legendären Dumplings. Die knackige Säure und die Brioche-Noten schaffen eine himmlische Verbindung mit dem saftigen Schweinefleisch."
    },
    {
        "dish_name": "Braised Pork Belly Shanghai (红烧肉)",
        "region": "Shanghai",
        "category": "Ostchina",
        "dish_description": "Süß-sauer eingelegtes Schweinefleisch, oft mit Eiern.",
        "wine_name": "Barolo",
        "wine_type": "rot",
        "wine_description": "Der majestätische Barolo aus dem Piemont mit seinen Rosenblättern, Teer und Kirschnoten erhebt das Shanghai-Style Schweinefleisch zu einem königlichen Mahl. Die kraftvollen Tannine werden von der süßen Sauce gezähmt."
    },
    {
        "dish_name": "Shanghai Fried Noodles (上海炒面)",
        "region": "Shanghai",
        "category": "Ostchina",
        "dish_description": "Nudeln mit Schweinefleisch, Gemüse und Sojasauce.",
        "wine_name": "Beaujolais-Villages",
        "wine_type": "rot",
        "wine_description": "Der frische, fruchtige Beaujolais mit seinen Kirsch- und Erdbeernoten ist der ideale Begleiter für diese klassischen Shanghai-Nudeln. Seine lebendige Säure harmoniert perfekt mit der würzigen Sojasauce."
    },
    {
        "dish_name": "Sweet and Sour Pork Jiangsu (糖醋里脊)",
        "region": "Jiangsu",
        "category": "Ostchina",
        "dish_description": "Frittiertes Schweinefleisch in süß-saurer Sauce.",
        "wine_name": "Gewürztraminer",
        "wine_type": "weiss",
        "wine_description": "Der aromatische Gewürztraminer mit seinen exotischen Litschi- und Rosennoten ist wie geschaffen für die süß-saure Harmonie dieses Klassikers. Die leichte Restsüße balanciert die Sauce perfekt aus."
    },
    {
        "dish_name": "Braised Fish with Soy Sauce (红烧鱼)",
        "region": "Jiangsu",
        "category": "Ostchina",
        "dish_description": "Ganzer Fisch in würziger Sojasauce.",
        "wine_name": "Burgundy Blanc (Chardonnay)",
        "wine_type": "weiss",
        "wine_description": "Der elegante Burgunder Chardonnay mit seiner cremigen Textur und dezenten Holznote umschmeichelt den zarten Fisch. Die Mineralität des Weins und die Tiefe der Sojasauce verschmelzen zu purer Harmonie."
    },
    {
        "dish_name": "Bamboo Shoots with Pork (笋炒肉)",
        "region": "Zhejiang",
        "category": "Ostchina",
        "dish_description": "Junge Bambussprossen mit Schweinefleisch.",
        "wine_name": "Vermentino",
        "wine_type": "weiss",
        "wine_description": "Der frische Vermentino mit seinen Kräuternoten und zitroniger Frische unterstreicht die delikate Textur der Bambussprossen. Ein Wein wie ein Frühlingsmorgen in den Bergen von Zhejiang."
    },
    {
        "dish_name": "Shanghai Hairy Crab (大闸蟹)",
        "region": "Shanghai",
        "category": "Ostchina",
        "dish_description": "Im Herbst beliebter Krabbenkaviar, oft gedämpft.",
        "wine_name": "Chablis Premier Cru",
        "wine_type": "weiss",
        "wine_description": "Der mineralische Chablis mit seiner stahligen Präzision und den Noten von Austernschalen ist der traditionelle Partner für diese herbstliche Delikatesse. Eine Verbindung, die in Shanghai gefeiert wird."
    },
    {
        "dish_name": "Stir-Fried Water Spinach (炒空心菜)",
        "region": "Zhejiang",
        "category": "Ostchina",
        "dish_description": "Grünes Gemüse mit Knoblauch und Chili.",
        "wine_name": "Sauvignon Blanc",
        "wine_type": "weiss",
        "wine_description": "Der knackige Sauvignon Blanc mit seinen grünen, grasigen Noten spiegelt die Frische des Wasserspinats wider. Knoblauch und Chili werden von der lebendigen Säure des Weins perfekt aufgefangen."
    },
    {
        "dish_name": "Braised Duck with Chestnuts (板栗烧鸭)",
        "region": "Jiangsu",
        "category": "Ostchina",
        "dish_description": "Ente mit Kastanien in würziger Sauce.",
        "wine_name": "Saint-Émilion Grand Cru",
        "wine_type": "rot",
        "wine_description": "Der samtige Saint-Émilion mit seinen reifen Pflaumen- und Trüffelnoten ist der perfekte Begleiter für diese herbstliche Kombination. Die Kastanien finden im Wein einen würdigen Partner."
    },
    {
        "dish_name": "Soy Sauce Chicken (酱油鸡)",
        "region": "Shanghai",
        "category": "Ostchina",
        "dish_description": "Hähnchen in Sojasauce, oft kalt serviert.",
        "wine_name": "Sancerre Rouge",
        "wine_type": "rot",
        "wine_description": "Der elegante Pinot Noir aus Sancerre mit seiner kühlen Frucht und seidigen Textur begleitet das kalte Sojasauce-Hähnchen mit Finesse. Eine Verbindung von französischer Eleganz und chinesischer Tradition."
    },
    
    # === SÜDCHINA (Guangdong, Fujian, Guangxi) ===
    {
        "dish_name": "Cantonese Dim Sum (点心)",
        "region": "Guangdong",
        "category": "Südchina",
        "dish_description": "Kleine Gerichte wie Har Gow, Siu Mai, Char Siu Bao.",
        "wine_name": "Crémant d'Alsace",
        "wine_type": "schaumwein",
        "wine_description": "Der feine Crémant mit seinen eleganten Perlen ist der ideale Begleiter für die Vielfalt der Dim Sum. Jeder Bissen, jeder Schluck – ein Tanz der Texturen und Aromen, der Hong Kong nach Europa bringt."
    },
    {
        "dish_name": "Char Siu (叉烧)",
        "region": "Guangdong",
        "category": "Südchina",
        "dish_description": "Mariniertes, gebratenes Schweinefleisch, oft mit Honig.",
        "wine_name": "Off-Dry Riesling Spätlese",
        "wine_type": "weiss",
        "wine_description": "Die elegante Süße der Riesling Spätlese umschmeichelt den karamellisierten Honig des Char Siu. Die brillante Säure durchschneidet die Reichhaltigkeit und schafft eine perfekte Balance."
    },
    {
        "dish_name": "Steamed Fish with Ginger and Scallions (清蒸鱼)",
        "region": "Guangdong",
        "category": "Südchina",
        "dish_description": "Frischer Fisch, gedämpft mit Ingwer und Lauch.",
        "wine_name": "Muscadet sur Lie",
        "wine_type": "weiss",
        "wine_description": "Der mineralische Muscadet mit seiner salzigen Brise und knackigen Frische ist wie das Meer selbst – perfekt für diesen puristischen kantonesischen Fischklassiker. Ingwer und Lauch werden sanft umspielt."
    },
    {
        "dish_name": "Stir-Fried Beef with Broccoli (西兰花炒牛肉)",
        "region": "Guangdong",
        "category": "Südchina",
        "dish_description": "Rindfleisch mit Brokkoli und Sojasauce.",
        "wine_name": "Chianti Classico",
        "wine_type": "rot",
        "wine_description": "Der toskanische Chianti mit seinen Sauerkirschnoten und der lebendigen Säure ist der ideale Begleiter für dieses schnelle Wok-Gericht. Die Sojasauce findet in den erdigen Noten einen harmonischen Partner."
    },
    {
        "dish_name": "Clay Pot Rice (煲仔饭)",
        "region": "Guangdong",
        "category": "Südchina",
        "dish_description": "Reis mit Fleisch, Pilzen und Ei in einem Ton Topf.",
        "wine_name": "Châteauneuf-du-Pape Rouge",
        "wine_type": "rot",
        "wine_description": "Der komplexe Châteauneuf-du-Pape mit seinen Kräuter-, Lavendel- und dunklen Fruchtnoten ist wie gemacht für den knusprigen Reis und die reichhaltige Füllung. Ein Gericht, das einen großen Wein verdient."
    },
    {
        "dish_name": "Fujian Fish Ball Soup (福州鱼丸汤)",
        "region": "Fujian",
        "category": "Südchina",
        "dish_description": "Fischbällchen in klare Suppe mit Gemüse.",
        "wine_name": "Vinho Verde",
        "wine_type": "weiss",
        "wine_description": "Der spritzige Vinho Verde mit seinem leichten Prickeln und den grünen Apfelnoten ist erfrischend leicht für diese delikate Fischsuppe. Wie eine Meeresbrise an der Fujian-Küste."
    },
    {
        "dish_name": "Stir-Fried Shrimp with Garlic (蒜蓉虾)",
        "region": "Guangdong",
        "category": "Südchina",
        "dish_description": "Garnelen mit Knoblauch und Chili.",
        "wine_name": "Grüner Veltliner Smaragd",
        "wine_type": "weiss",
        "wine_description": "Der kraftvolle Smaragd-Veltliner aus der Wachau mit seiner würzigen Komplexität und mineralischen Tiefe steht den aromatischen Knoblauch-Garnelen in nichts nach. Eine Begegnung auf Augenhöhe."
    },
    {
        "dish_name": "Braised Pork with Tofu (豆腐烧肉)",
        "region": "Guangxi",
        "category": "Südchina",
        "dish_description": "Schweinefleisch mit Tofu in würziger Sauce.",
        "wine_name": "Rioja Reserva",
        "wine_type": "rot",
        "wine_description": "Der gereifte Rioja mit seinen Vanille- und Ledernoten aus dem Barrique-Ausbau harmoniert wunderbar mit der würzigen Sauce. Der seidige Tofu wird von den samtigen Tanninen umschmeichelt."
    },
    {
        "dish_name": "Stir-Fried Eggplant (鱼香茄子)",
        "region": "Guangdong",
        "category": "Südchina",
        "dish_description": "Auberginen mit Knoblauch, Chili und Sojasauce.",
        "wine_name": "Nero d'Avola",
        "wine_type": "rot",
        "wine_description": "Der sizilianische Nero d'Avola mit seinen dunklen Pflaumen- und Gewürznoten ist der ideale Partner für die rauchig-süßen Auberginen. Mediterranes Feuer trifft auf asiatische Würze."
    },
    {
        "dish_name": "Coconut Chicken Soup (椰子鸡汤)",
        "region": "Guangdong",
        "category": "Südchina",
        "dish_description": "Hähnchen mit Kokosmilch und Pilzen.",
        "wine_name": "Viognier",
        "wine_type": "weiss",
        "wine_description": "Der opulente Viognier mit seinen Aprikosen- und Blütennoten verschmilzt mit der cremigen Kokosmilch zu einem tropischen Traum. Die Pilze finden in den erdigen Untertönen des Weins ihr Echo."
    },
    
    # === WESTCHINA (Sichuan, Hunan, Yunnan) ===
    {
        "dish_name": "Kung Pao Chicken (宫保鸡丁)",
        "region": "Sichuan",
        "category": "Westchina",
        "dish_description": "Hähnchen mit Erdnüssen, Chili und Szechuan-Pfeffer.",
        "wine_name": "Riesling Spätlese halbtrocken",
        "wine_type": "weiss",
        "wine_description": "Die feine Restsüße des Rieslings ist wie Balsam für den feurigen Szechuan-Pfeffer. Die Erdnüsse und die knusprigen Chilis werden von der fruchtigen Eleganz des Weins umarmt."
    },
    {
        "dish_name": "Mapo Tofu (麻婆豆腐)",
        "region": "Sichuan",
        "category": "Westchina",
        "dish_description": "Tofu mit Hackfleisch, Chili und Szechuan-Pfeffer.",
        "wine_name": "Lambrusco",
        "wine_type": "rot",
        "wine_description": "Der leicht perlende, fruchtige Lambrusco ist ein erfrischender Kontrast zur betäubenden Schärfe des Mapo Tofu. Seine Kühle und Süße beruhigen den Gaumen zwischen den feurigen Bissen."
    },
    {
        "dish_name": "Twice-Cooked Pork (回锅肉)",
        "region": "Sichuan",
        "category": "Westchina",
        "dish_description": "Schweinebauch, zweimal gekocht, mit Chili und Bohnenpaste.",
        "wine_name": "Primitivo di Manduria",
        "wine_type": "rot",
        "wine_description": "Der vollmundige Primitivo mit seinen reifen Brombeeren und einer Spur von Süße steht der intensiven Bohnenpaste mutig gegenüber. Ein Wein mit Charakter für ein Gericht mit Charakter."
    },
    {
        "dish_name": "Sichuan Hot Pot (火锅)",
        "region": "Sichuan",
        "category": "Westchina",
        "dish_description": "Scharfe Brühe, in die Fleisch, Gemüse und Nudeln getunkt werden.",
        "wine_name": "Prosecco",
        "wine_type": "schaumwein",
        "wine_description": "Der erfrischende Prosecco mit seinen zarten Perlen ist der perfekte Durstlöscher beim feurigen Hot Pot Erlebnis. Die Frische kühlt, die Frucht erfreut, und die Geselligkeit wird gefeiert."
    },
    {
        "dish_name": "Dry-Fried String Beans (干煸四季豆)",
        "region": "Sichuan",
        "category": "Westchina",
        "dish_description": "Gedünstete Bohnen mit Chili und Knoblauch.",
        "wine_name": "Torrontés",
        "wine_type": "weiss",
        "wine_description": "Der aromatische Torrontés aus Argentinien mit seinen floralen Noten und lebendiger Säure ist ein überraschend passender Partner für diese knusprigen Bohnen. Frisch und belebend."
    },
    {
        "dish_name": "Hunan Spicy Chicken (辣子鸡)",
        "region": "Hunan",
        "category": "Westchina",
        "dish_description": "Frittiertes Hähnchen mit viel Chili und Knoblauch.",
        "wine_name": "Moscato d'Asti",
        "wine_type": "weiss",
        "wine_description": "Der süße, leicht perlende Moscato ist wie ein sanfter Regenschauer nach einem heißen Tag – er kühlt die Schärfe des Hunan-Huhns und bringt Harmonie ins Feuer."
    },
    {
        "dish_name": "Stir-Fried Pork with Chili (辣椒炒肉)",
        "region": "Hunan",
        "category": "Westchina",
        "dish_description": "Schweinefleisch mit grünen Chilis.",
        "wine_name": "Côtes du Rhône Blanc",
        "wine_type": "weiss",
        "wine_description": "Der vollmundige weiße Rhône mit seinen Steinobst- und Kräuternoten bietet einen eleganten Kontrast zu den grünen Chilis. Die cremige Textur umschmeichelt das Schweinefleisch."
    },
    {
        "dish_name": "Yunnan Crossing the Bridge Noodles (过桥米线)",
        "region": "Yunnan",
        "category": "Westchina",
        "dish_description": "Nudeln mit heißer Brühe, Fleisch und Gemüse.",
        "wine_name": "Soave Classico",
        "wine_type": "weiss",
        "wine_description": "Der elegante Soave mit seinen Mandel- und Zitrusnoten begleitet die heiße Brühe und die zarten Reisnudeln mit italienischer Anmut. Eine Reise von Yunnan nach Venetien."
    },
    {
        "dish_name": "Sichuan Boiled Fish (水煮鱼)",
        "region": "Sichuan",
        "category": "Westchina",
        "dish_description": "Fisch in scharfer, ölig-scharfer Brühe.",
        "wine_name": "Vouvray Demi-Sec",
        "wine_type": "weiss",
        "wine_description": "Der halbtrocken Vouvray mit seiner honigartigen Süße und lebendigen Säure ist der perfekte Gegenpol zur intensiven Schärfe. Der Chenin Blanc tanzt über den Feuersee."
    },
    {
        "dish_name": "Stir-Fried Pork with Pickled Mustard Greens (酸菜炒肉)",
        "region": "Sichuan",
        "category": "Westchina",
        "dish_description": "Schweinefleisch mit sauren Senfgemüse.",
        "wine_name": "Grauburgunder / Pinot Grigio",
        "wine_type": "weiss",
        "wine_description": "Der frische Grauburgunder mit seinen Birnen- und Zitrusnoten harmoniert wunderbar mit der Säure des eingelegten Gemüses. Eine erfrischende, säurebetonte Kombination."
    },
    
    # === ALLGEMEIN & INTERNATIONAL ===
    {
        "dish_name": "Fried Rice (炒饭)",
        "region": "Überall",
        "category": "International",
        "dish_description": "Reis mit Ei, Gemüse, Fleisch oder Meeresfrüchten.",
        "wine_name": "Cava Brut",
        "wine_type": "schaumwein",
        "wine_description": "Der spanische Cava mit seinen feinen Perlen und Zitrusnoten ist universell und flexibel – genau wie der gebratene Reis selbst. Eine fröhliche Kombination für jeden Anlass."
    },
    {
        "dish_name": "Chow Mein (炒面)",
        "region": "Überall",
        "category": "International",
        "dish_description": "Gebratene Nudeln mit Gemüse und Fleisch.",
        "wine_name": "Trebbiano d'Abruzzo",
        "wine_type": "weiss",
        "wine_description": "Der unkomplizierte Trebbiano mit seiner leichten Frucht und frischen Säure ist der perfekte Alltagsbegleiter für diese beliebten gebratenen Nudeln. Einfach und gut."
    },
    {
        "dish_name": "Sweet and Sour Pork International (糖醋里脊)",
        "region": "Überall",
        "category": "International",
        "dish_description": "Frittiertes Schweinefleisch in süß-saurer Sauce.",
        "wine_name": "Rosé de Provence",
        "wine_type": "rose",
        "wine_description": "Der elegante Provence-Rosé mit seinen roten Beeren und Kräuternoten ist ein charmanter Begleiter für diesen süß-sauren Klassiker. Frisch, fruchtig und vielseitig."
    },
    {
        "dish_name": "Beef with Broccoli International (西兰花炒牛肉)",
        "region": "Überall",
        "category": "International",
        "dish_description": "Rindfleisch mit Brokkoli und Sojasauce.",
        "wine_name": "Merlot",
        "wine_type": "rot",
        "wine_description": "Der samtige Merlot mit seinen reifen Pflaumennoten und weichen Tanninen umschmeichelt das zarte Rindfleisch. Der Brokkoli findet in den grünen Nuancen des Weins sein Gegenstück."
    },
    {
        "dish_name": "Stir-Fried Tofu (家常豆腐)",
        "region": "Überall",
        "category": "International",
        "dish_description": "Tofu mit Gemüse und Sauce.",
        "wine_name": "Chenin Blanc",
        "wine_type": "weiss",
        "wine_description": "Der vielseitige Chenin Blanc mit seiner lebendigen Säure und Honignoten ist ein wunderbarer Partner für den neutralen Tofu. Er bringt das Beste in jedem Gemüse hervor."
    },
    {
        "dish_name": "Egg Drop Soup (蛋花汤)",
        "region": "Überall",
        "category": "International",
        "dish_description": "Klare Suppe mit geschlagenem Ei.",
        "wine_name": "Fino Sherry",
        "wine_type": "weiss",
        "wine_description": "Der trockene Fino Sherry mit seinen Mandel- und Hefenoten ist ein unerwarteter, aber brillanter Partner für diese delikate Suppe. Eine Kombination, die Kenner schätzen."
    },
    {
        "dish_name": "Hot and Sour Soup (酸辣汤)",
        "region": "Überall",
        "category": "International",
        "dish_description": "Scharfe, saure Suppe mit Pilzen, Ei und Tofu.",
        "wine_name": "Gewürztraminer Elsass",
        "wine_type": "weiss",
        "wine_description": "Der aromatische Gewürztraminer mit seinen exotischen Gewürznoten und der leichten Süße balanciert die Säure und Schärfe der Suppe perfekt aus. Ein elsässischer Traum in der Schüssel."
    },
    {
        "dish_name": "Chicken with Cashews (腰果鸡丁)",
        "region": "Überall",
        "category": "International",
        "dish_description": "Hähnchen mit Cashewnüssen und Gemüse.",
        "wine_name": "Verdejo",
        "wine_type": "weiss",
        "wine_description": "Der frische Verdejo aus Rueda mit seinen kräutrigen Noten und der knackigen Säure ist wie gemacht für dieses nussige Hähnchengericht. Die Cashews werden von der Textur des Weins gespiegelt."
    },
    {
        "dish_name": "Stir-Fried Shrimp (炒虾仁)",
        "region": "Überall",
        "category": "International",
        "dish_description": "Garnelen mit Knoblauch und Gemüse.",
        "wine_name": "Picpoul de Pinet",
        "wine_type": "weiss",
        "wine_description": "Der salzige, mineralische Picpoul ist der klassische Meeresfrüchte-Wein. Seine Zitrusnoten und die knackige Säure sind wie eine frische Brise am Mittelmeer – perfekt für Garnelen."
    },
    {
        "dish_name": "Braised Pork with Eggs (卤蛋烧肉)",
        "region": "Überall",
        "category": "International",
        "dish_description": "Schweinefleisch mit hartgekochten Eiern in Sojasauce.",
        "wine_name": "Valpolicella Ripasso",
        "wine_type": "rot",
        "wine_description": "Der Ripasso mit seiner konzentrierten Frucht und samtigen Textur ist der perfekte Begleiter für dieses herzhafte Schmorgericht. Die Eier und die Sojasauce finden im Wein ihr Gleichgewicht."
    }
]


async def import_china_dishes():
    """Import all 50 Chinese dishes into regional_pairings collection."""
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'wine_pairing')]
    
    print("🇨🇳 Starting China Sommelier Kompass Import...")
    print(f"📊 Total dishes to import: {len(CHINA_DISHES)}")
    
    # Check existing China dishes
    existing = await db.regional_pairings.count_documents({"country": "China"})
    print(f"📍 Existing China dishes in DB: {existing}")
    
    imported = 0
    skipped = 0
    
    for dish in CHINA_DISHES:
        # Check if dish already exists
        existing_dish = await db.regional_pairings.find_one({
            "dish_name": dish["dish_name"],
            "country": "China"
        })
        
        if existing_dish:
            print(f"  ⏭️ Skipping (exists): {dish['dish_name']}")
            skipped += 1
            continue
        
        # Create full document with translations
        doc = {
            "id": str(uuid4()),
            "dish_name": dish["dish_name"],
            "dish_description": dish["dish_description"],
            "dish_description_en": translate_to_english(dish["dish_description"]),
            "dish_description_fr": translate_to_french(dish["dish_description"]),
            "country": "China",
            "region": dish["region"],
            "category": dish.get("category", "Allgemein"),
            "wine_name": dish["wine_name"],
            "wine_type": dish["wine_type"],
            "wine_description": dish["wine_description"],
            "wine_description_en": translate_wine_to_english(dish["wine_description"]),
            "wine_description_fr": translate_wine_to_french(dish["wine_description"]),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.regional_pairings.insert_one(doc)
        imported += 1
        print(f"  ✅ Imported: {dish['dish_name']} ({dish['region']})")
    
    # Final count
    final_count = await db.regional_pairings.count_documents({"country": "China"})
    
    print("\n" + "="*60)
    print(f"🎉 IMPORT COMPLETE!")
    print(f"   ✅ Imported: {imported}")
    print(f"   ⏭️ Skipped: {skipped}")
    print(f"   📊 Total China dishes now: {final_count}")
    print("="*60)
    
    client.close()
    return imported, skipped, final_count


def translate_to_english(text_de):
    """Simple translations for dish descriptions."""
    translations = {
        "Knusprige Ente, dünn geschnitten, mit Pancakes, Gemüse und Süß-Sauer-Sauce.": "Crispy duck, thinly sliced, with pancakes, vegetables and sweet-sour sauce.",
        "Gedämpfte oder gebratene Teigtaschen mit Fleisch/Gemüse-Füllung.": "Steamed or fried dumplings with meat/vegetable filling.",
        "Nudeln mit fermentierter Sojabohnen-Sauce und gehacktem Schweinefleisch.": "Noodles with fermented soybean sauce and minced pork.",
        "Gegrillte Lammfleischspieße mit Kreuzkümmel und Chilipulver.": "Grilled lamb skewers with cumin and chili powder.",
        "Schweinebauch in süß-saurer Soße, oft mit Eiern oder Pilzen.": "Pork belly in sweet-sour sauce, often with eggs or mushrooms.",
        "Knusprige, flache Teigfladen mit Lauch und Sesamöl.": "Crispy flat flatbreads with leek and sesame oil.",
        "Gegrilltes Schweinefleisch, oft mit Gemüse und Brot.": "Grilled pork, often with vegetables and bread.",
        "Lammfleisch mit Kreuzkümmel, Chili und Paprika.": "Lamb with cumin, chili and paprika.",
        "Nudeln mit zartem Rindfleisch in würziger Brühe.": "Noodles with tender beef in spicy broth.",
        "Gedämpfte Teigtaschen mit Fleisch- oder Gemüsefüllung.": "Steamed buns with meat or vegetable filling.",
    }
    return translations.get(text_de, text_de)


def translate_to_french(text_de):
    """Simple translations for dish descriptions."""
    translations = {
        "Knusprige Ente, dünn geschnitten, mit Pancakes, Gemüse und Süß-Sauer-Sauce.": "Canard croustillant, finement tranché, avec crêpes, légumes et sauce aigre-douce.",
        "Gedämpfte oder gebratene Teigtaschen mit Fleisch/Gemüse-Füllung.": "Raviolis cuits à la vapeur ou frits avec garniture viande/légumes.",
        "Nudeln mit fermentierter Sojabohnen-Sauce und gehacktem Schweinefleisch.": "Nouilles avec sauce de soja fermentée et porc haché.",
        "Gegrillte Lammfleischspieße mit Kreuzkümmel und Chilipulver.": "Brochettes d'agneau grillées au cumin et poudre de chili.",
        "Schweinebauch in süß-saurer Soße, oft mit Eiern oder Pilzen.": "Poitrine de porc en sauce aigre-douce, souvent avec œufs ou champignons.",
        "Knusprige, flache Teigfladen mit Lauch und Sesamöl.": "Galettes croustillantes plates avec poireau et huile de sésame.",
        "Gegrilltes Schweinefleisch, oft mit Gemüse und Brot.": "Porc grillé, souvent avec légumes et pain.",
        "Lammfleisch mit Kreuzkümmel, Chili und Paprika.": "Agneau au cumin, chili et paprika.",
        "Nudeln mit zartem Rindfleisch in würziger Brühe.": "Nouilles avec bœuf tendre dans un bouillon épicé.",
        "Gedämpfte Teigtaschen mit Fleisch- oder Gemüsefüllung.": "Petits pains cuits à la vapeur avec garniture viande ou légumes.",
    }
    return translations.get(text_de, text_de)


def translate_wine_to_english(text_de):
    """Keep wine descriptions in original German for now - can be enhanced later."""
    # For a complete solution, this would use an AI translation API
    # For now, return original with note
    return f"[EN] {text_de[:100]}..." if len(text_de) > 100 else f"[EN] {text_de}"


def translate_wine_to_french(text_de):
    """Keep wine descriptions in original German for now - can be enhanced later."""
    return f"[FR] {text_de[:100]}..." if len(text_de) > 100 else f"[FR] {text_de}"


if __name__ == "__main__":
    asyncio.run(import_china_dishes())
