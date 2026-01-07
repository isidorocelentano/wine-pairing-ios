#!/usr/bin/env python3
"""
Import all Greek dishes from Sommelier Kompass griechenland.docx
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

# All Greek dishes extracted from the document with wine pairings
GREECE_DISHES = [
    # === ÜBERALL (Klassiker) ===
    {
        "dish_name": "Moussaka (Μουσακάς)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Schichtgericht aus Auberginen, Hackfleisch, Tomatensoße und Béchamel-Sauce.",
        "wine_name": "Xinomavro (Naoussa)",
        "wine_type": "rot",
        "wine_description": "Der edle Xinomavro aus Naoussa mit seinen Kirsch- und Tomatenblätternoten ist der klassische Partner für Moussaka. Seine Säure schneidet durch die cremige Béchamel, während die Tannine das Hackfleisch umschmeicheln."
    },
    {
        "dish_name": "Pastitsio (Παστίτσιο)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Nudelauflauf mit Hackfleisch und Béchamel, ähnlich Lasagne.",
        "wine_name": "Agiorgitiko",
        "wine_type": "rot",
        "wine_description": "Der samtige Agiorgitiko aus Nemea mit seinen reifen Pflaumennoten und weichen Tanninen begleitet diesen griechischen Nudelauflauf perfekt. Ein Wein wie ein warmer Abend am Mittelmeer."
    },
    {
        "dish_name": "Gemista (Γεμιστά)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Gefüllte Tomaten und Paprika mit Reis, Kräutern und manchmal Hackfleisch.",
        "wine_name": "Assyrtiko",
        "wine_type": "weiss",
        "wine_description": "Der mineralische Assyrtiko aus Santorin mit seiner vulkanischen Seele und zitronigen Frische ist wie gemacht für dieses sommerliche Gemüsegericht. Die Säure hebt die süße der Tomaten hervor."
    },
    {
        "dish_name": "Arni me Patates (Αρνί με πατάτες)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Ofenkartoffeln mit Lammfleisch, oft mit Rosmarin und Olivenöl.",
        "wine_name": "Mavrodaphne",
        "wine_type": "rot",
        "wine_description": "Der aromatische Mavrodaphne mit seinen dunklen Beeren und einer Spur von süßen Gewürzen ist der traditionelle Begleiter für griechisches Ofenlamm. Die mediterrane Seele Griechenlands im Glas."
    },
    {
        "dish_name": "Keftedakia (Κεφτεδάκια)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Fleischbällchen aus Rind oder Schwein, oft mit Reis oder Gemüse.",
        "wine_name": "Xinomavro Rosé",
        "wine_type": "rose",
        "wine_description": "Ein frischer Xinomavro Rosé mit seinen Erdbeernoten und lebendiger Säure ist der perfekte Sommerpartner für diese würzigen Fleischbällchen. Leicht gekühlt serviert – ein Genuss!"
    },
    {
        "dish_name": "Yiahni (Γιαχνί)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Eintopf aus Fleisch (meist Lamm oder Rind) mit Gemüse und Tomaten.",
        "wine_name": "Limnio",
        "wine_type": "rot",
        "wine_description": "Der uralte Limnio – eine der ältesten Rebsorten der Welt – mit seinen Kräuternoten und samtiger Textur ist wie aus der Zeit gefallen. Perfekt für diesen rustikalen Eintopf."
    },
    {
        "dish_name": "Psari Plaki (Ψάρι Πλακί)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Ofenfisch mit Tomaten, Zwiebeln, Olivenöl und Kräutern.",
        "wine_name": "Malagousia",
        "wine_type": "weiss",
        "wine_description": "Die wiederentdeckte Malagousia mit ihren exotischen Pfirsich- und Jasminblütennoten ist ein Traum mit gebackenem Fisch. Das Olivenöl und die Kräuter werden von der aromatischen Fülle des Weins umspielt."
    },
    {
        "dish_name": "Dolmades (Δολμάδες)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Reis gefüllte Weinblätter, oft mit Kräutern und Zitrone.",
        "wine_name": "Roditis",
        "wine_type": "weiss",
        "wine_description": "Der frische Roditis mit seiner knackigen Säure und den Noten von grünem Apfel ist wie geschaffen für diese zarten Weinblattröllchen. Die Zitrone im Gericht findet im Wein ihr Echo."
    },
    {
        "dish_name": "Spanakopita (Σπανακόπιτα)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Blätterteig mit Spinat und Feta-Käse.",
        "wine_name": "Savatiano",
        "wine_type": "weiss",
        "wine_description": "Der unkomplizierte Savatiano mit seiner leichten Frucht und erfrischenden Art ist der perfekte Alltagswein für diesen beliebten Spinatkuchen. Ein Stück Griechenland auf dem Teller."
    },
    {
        "dish_name": "Tiropita (Τυρόπιτα)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Blätterteig mit Feta-Käse.",
        "wine_name": "Moschofilero",
        "wine_type": "weiss",
        "wine_description": "Der aromatische Moschofilero mit seinen Rosenblüten- und Zitrusnoten ist ein eleganter Partner für die salzige Fülle des Feta. Ein Wein, der überrascht und begeistert."
    },
    {
        "dish_name": "Fasoulia (Φασούλια)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Bohnen in Tomatensoße mit Karotten und Zwiebeln.",
        "wine_name": "Mavrotragano",
        "wine_type": "rot",
        "wine_description": "Der kraftvolle Mavrotragano aus Santorin mit seinen dunklen Frucht- und Gewürznoten ist ein würdiger Partner für diesen herzhaften Bohneneintopf. Vulkanische Energie im Glas."
    },
    {
        "dish_name": "Briam (Μπριάμ)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Ofengemüse mit Auberginen, Zucchini, Tomaten und Olivenöl.",
        "wine_name": "Vidiano",
        "wine_type": "weiss",
        "wine_description": "Der kretische Vidiano mit seiner üppigen Textur und den Noten von tropischen Früchten ist ideal für dieses mediterrane Ofengemüse. Das Olivenöl und die Kräuter werden wunderbar ergänzt."
    },
    {
        "dish_name": "Tzatziki (Τζατζίκι)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Joghurt mit Gurke, Knoblauch und Minze (oft als Beilage).",
        "wine_name": "Assyrtiko",
        "wine_type": "weiss",
        "wine_description": "Der mineralische Assyrtiko mit seiner salzigen Brise und zitronigen Frische ist der perfekte Partner für das kühle Tzatziki. Die Gurke und Minze finden im Wein ihr Spiegelbild."
    },
    {
        "dish_name": "Melitzanosalata (Μελιτζανοσαλάτα)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Auberginenpüree mit Knoblauch, Zitrone und Olivenöl.",
        "wine_name": "Athiri",
        "wine_type": "weiss",
        "wine_description": "Der elegante Athiri mit seinen zarten Blüten- und Zitrusnoten umspielt das rauchige Auberginenpüree mit Finesse. Der Knoblauch wird von der Frische des Weins gezähmt."
    },
    {
        "dish_name": "Souvlaki (Σουβλάκι)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Gegrillte Fleischspieße (meist Schwein oder Huhn).",
        "wine_name": "Agiorgitiko",
        "wine_type": "rot",
        "wine_description": "Der fruchtige Agiorgitiko mit seinen Kirsch- und Gewürznoten ist der klassische Partner für gegrillte Souvlaki. Ein Wein, der nach Sommernächten in Athen schmeckt."
    },
    {
        "dish_name": "Gyros (Γύρος)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Gedrehtes Fleisch (Schwein oder Huhn) in Fladenbrot mit Salat und Tzatziki.",
        "wine_name": "Xinomavro Rosé",
        "wine_type": "rose",
        "wine_description": "Ein kühler Xinomavro Rosé mit seiner lebendigen Frucht und erfrischenden Säure ist der ideale Begleiter für Gyros. Das Tzatziki und das gegrillte Fleisch werden perfekt ergänzt."
    },
    {
        "dish_name": "Kotopoulo me Lemoni (Κοτόπουλο με λεμόνι)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Hähnchen mit Zitrone und Knoblauch.",
        "wine_name": "Robola",
        "wine_type": "weiss",
        "wine_description": "Die elegante Robola von Kefalonia mit ihrer mineralischen Eleganz und zitronigen Säure ist wie für Zitronenhähnchen gemacht. Ein Wein von der Insel für ein Gericht mit Sonne."
    },
    {
        "dish_name": "Kokoretsi (Κοκορέτσι)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Gegrillte Innereien (Därme) mit Kräutern, oft zu Festen.",
        "wine_name": "Xinomavro Reserve",
        "wine_type": "rot",
        "wine_description": "Ein gereifter Xinomavro Reserve mit seiner Komplexität von Leder, Tabak und roten Früchten ist mutig genug für dieses traditionelle Festtagsgericht. Ein Wein für Kenner."
    },
    {
        "dish_name": "Loukanika (Λουκάνικα)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Griechische Würstchen, oft mit Kräutern und Paprika.",
        "wine_name": "Mavroudi",
        "wine_type": "rot",
        "wine_description": "Der würzige Mavroudi mit seinen pfeffrigen Noten und mittlerem Körper ist der perfekte Begleiter für diese aromatischen Würstchen. Griechisches Terroir pur."
    },
    {
        "dish_name": "Hirino me Prasa (Χοιρινό με πράσα)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Schweinefleisch mit Lauch und Kräutern.",
        "wine_name": "Limniona",
        "wine_type": "rot",
        "wine_description": "Die seltene Limniona aus Thessalien mit ihren floralen Noten und eleganten Tanninen ist ein wunderbarer Partner für das zarte Schweinefleisch mit Lauch."
    },
    {
        "dish_name": "Fakes (Φακές)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Linsensuppe mit Tomaten, Karotten und Kräutern.",
        "wine_name": "Kotsifali",
        "wine_type": "rot",
        "wine_description": "Der fruchtige Kotsifali aus Kreta mit seinen roten Beerennoten und weichen Tanninen wärmt zusammen mit dieser traditionellen Linsensuppe Körper und Seele."
    },
    {
        "dish_name": "Revithia (Ρεβιθιά)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Kichererbsensuppe mit Tomaten und Kräutern.",
        "wine_name": "Vidiano",
        "wine_type": "weiss",
        "wine_description": "Der vollmundige Vidiano mit seinen cremigen Noten ist ein überraschend guter Partner für diese erdige Kichererbsensuppe. Kretische Wärme im Glas."
    },
    {
        "dish_name": "Avgolemono (Αυγολέμονο)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Hühnersuppe mit Ei und Zitrone.",
        "wine_name": "Debina",
        "wine_type": "weiss",
        "wine_description": "Die spritzige Debina aus Epirus mit ihrer prickelnden Frische und Zitrusnoten ist der ideale Partner für diese säurebetonte, cremige Suppe. Erfrischend und belebend."
    },
    
    # === PELOPONNES, ATTIKA ===
    {
        "dish_name": "Stifado (Στιφάδο)",
        "region": "Peloponnes",
        "category": "Peloponnes",
        "dish_description": "Rindfleisch in Zwiebel-Wein-Soße mit Zimt und Nelken.",
        "wine_name": "Agiorgitiko Reserve",
        "wine_type": "rot",
        "wine_description": "Der gereifte Agiorgitiko aus Nemea mit seiner samtigen Fülle und Noten von Gewürzen ist wie für Stifado gemacht. Die Zimt- und Nelkennoten des Gerichts finden im Wein ihr Echo."
    },
    {
        "dish_name": "Soutzoukakia (Σουτζουκάκια)",
        "region": "Attika",
        "category": "Peloponnes",
        "dish_description": "Gewürzte Fleischwürstchen in Tomatensoße, oft mit Reis.",
        "wine_name": "Mandilaria",
        "wine_type": "rot",
        "wine_description": "Der kräftige Mandilaria mit seiner tiefen Farbe und würzigen Noten ist ein kraftvoller Partner für diese aromatischen Fleischwürstchen. Griechische Lebensfreude auf dem Teller."
    },
    {
        "dish_name": "Bakaliaros Skordalia (Μπακαλιάρος σκορδαλιά)",
        "region": "Attika",
        "category": "Peloponnes",
        "dish_description": "Stockfisch mit Knoblauch-Kartoffelpüree.",
        "wine_name": "Retsina Modern",
        "wine_type": "weiss",
        "wine_description": "Eine moderne Retsina mit dezenter Harznote ist der traditionelle und überraschend passende Partner für diesen salzigen Stockfisch. Eine Kombination, die seit Jahrhunderten besteht."
    },
    {
        "dish_name": "Arni me Kremmydia (Αρνί με κρεμμύδια)",
        "region": "Peloponnes",
        "category": "Peloponnes",
        "dish_description": "Lammfleisch mit Zwiebeln in Tomatensoße.",
        "wine_name": "Agiorgitiko",
        "wine_type": "rot",
        "wine_description": "Der elegante Agiorgitiko mit seinen geschmeidigen Tanninen und roten Fruchtnoten umschmeichelt das zarte Lamm. Die Zwiebeln und Tomaten werden von der Frucht des Weins aufgefangen."
    },
    
    # === ZENTRALGRIECHENLAND, KRETA ===
    {
        "dish_name": "Kleftiko (Κλέφτικο)",
        "region": "Kreta",
        "category": "Kreta",
        "dish_description": "Langsam gegartes Lammfleisch mit Knoblauch, Zitrone und Kräutern.",
        "wine_name": "Liatiko",
        "wine_type": "rot",
        "wine_description": "Der elegante Liatiko aus Kreta mit seinen Aromen von getrockneten Kräutern und roten Beeren ist der authentische Partner für dieses legendäre Schmorgericht. Kretische Tradition im Glas."
    },
    {
        "dish_name": "Kleftiko me Patates (Κλέφτικο με πατάτες)",
        "region": "Kreta",
        "category": "Kreta",
        "dish_description": "Langsam gegartes Lammfleisch mit Kartoffeln.",
        "wine_name": "Kotsifali-Mandilaria Blend",
        "wine_type": "rot",
        "wine_description": "Die klassische kretische Cuvée aus Kotsifali und Mandilaria vereint Frucht und Struktur – perfekt für das butterzarte Kleftiko mit knusprigen Kartoffeln."
    },
    
    # === NORDGRIECHENLAND ===
    {
        "dish_name": "Giouvetsi (Γιουβέτσι)",
        "region": "Nordgriechenland",
        "category": "Nordgriechenland",
        "dish_description": "Lammfleisch mit Nudeln in Tomatensoße, im Ofen gebacken.",
        "wine_name": "Xinomavro",
        "wine_type": "rot",
        "wine_description": "Der majestätische Xinomavro aus Naoussa mit seinen komplexen Aromen von Oliven, Tomaten und Gewürzen ist der König der nordgriechischen Weine – und perfekt für Giouvetsi."
    },
    {
        "dish_name": "Garides Saganaki (Γαρίδες Σαγανάκι)",
        "region": "Nordgriechenland",
        "category": "Nordgriechenland",
        "dish_description": "Garnelen in Tomaten- und Feta-Käse-Soße.",
        "wine_name": "Malagouzia",
        "wine_type": "weiss",
        "wine_description": "Die aromatische Malagouzia mit ihren exotischen Fruchtnoten und cremiger Textur ist ein Traum mit den Garnelen in der reichhaltigen Tomaten-Feta-Sauce."
    },
    {
        "dish_name": "Kebab (Κεμπάπ)",
        "region": "Nordgriechenland",
        "category": "Nordgriechenland",
        "dish_description": "Gegrilltes Fleisch mit Gemüse, oft mit Reis.",
        "wine_name": "Negoska",
        "wine_type": "rot",
        "wine_description": "Die seltene Negoska aus Mazedonien mit ihren würzigen Noten und mittlerem Körper ist der lokale Partner für gegrilltes Kebab. Ein authentisches Erlebnis."
    },
    
    # === KÜSTENREGIONEN ===
    {
        "dish_name": "Kalamari (Καλαμάρι)",
        "region": "Küstenregionen",
        "category": "Küste",
        "dish_description": "Gebratene oder gegrillte Tintenfische, oft mit Zitrone.",
        "wine_name": "Assyrtiko",
        "wine_type": "weiss",
        "wine_description": "Der salzige, mineralische Assyrtiko aus Santorin ist wie das Meer selbst – perfekt für frische Kalamari. Die Zitrone und das Meersalz werden von der vulkanischen Mineralität umspielt."
    },
    {
        "dish_name": "Kakavia (Κακαβιά)",
        "region": "Küstenregionen",
        "category": "Küste",
        "dish_description": "Fischsuppe mit Tomaten, Kartoffeln und Kräutern.",
        "wine_name": "Robola",
        "wine_type": "weiss",
        "wine_description": "Die elegante Robola von Kefalonia mit ihrer kristallinen Reinheit und mineralischen Tiefe ist der ideale Begleiter für diese traditionelle Fischersuppe."
    },
    {
        "dish_name": "Psari me Patates (Ψάρι με πατάτες)",
        "region": "Küstenregionen",
        "category": "Küste",
        "dish_description": "Fisch mit Ofenkartoffeln, oft mit Rosmarin.",
        "wine_name": "Vilana",
        "wine_type": "weiss",
        "wine_description": "Die kretische Vilana mit ihrer leichten Frucht und erfrischenden Säure ist ein unkomplizierter, aber perfekter Partner für gebackenen Fisch mit Kartoffeln."
    },
    
    # === KRETA, ÄGÄIS ===
    {
        "dish_name": "Oktapodi Stifado (Οκτάποδι Στιφάδο)",
        "region": "Kreta",
        "category": "Kreta",
        "dish_description": "Tintenfisch in Zwiebel-Wein-Soße mit Kräutern.",
        "wine_name": "Vidiano",
        "wine_type": "weiss",
        "wine_description": "Der kretische Vidiano mit seiner üppigen Textur und den Noten von reifen Steinfrüchten ist ein überraschend guter Partner für dieses würzige Oktopus-Gericht."
    },
    
    # === SANTORIN, KYKLADEN ===
    {
        "dish_name": "Fava (Φάβα)",
        "region": "Santorin",
        "category": "Inseln",
        "dish_description": "Püree aus gelben Linsen, oft mit Zwiebeln und Olivenöl.",
        "wine_name": "Assyrtiko Santorini",
        "wine_type": "weiss",
        "wine_description": "Der legendäre Assyrtiko aus Santorin mit seiner vulkanischen Mineralität und salzigen Brise ist das perfekte lokale Pairing für dieses traditionelle Inselgericht."
    },
    {
        "dish_name": "Tomatokeftedes (Ντοματοκεφτέδες)",
        "region": "Santorin",
        "category": "Inseln",
        "dish_description": "Gebratene Tomatenbällchen mit Minze und Kräutern, typisch für Santorin.",
        "wine_name": "Nykteri (Santorin)",
        "wine_type": "weiss",
        "wine_description": "Der kraftvolle Nykteri – bei Nacht geerntet – mit seiner konzentrierten Frucht und mineralischen Tiefe ist der prestigeträchtige Partner für diese ikonischen Santorin-Tomatenbällchen."
    },
    
    # === WEITERE KLASSIKER ===
    {
        "dish_name": "Psari me Lahanika (Ψάρι με λαχανικά)",
        "region": "Überall",
        "category": "Küste",
        "dish_description": "Fisch mit Gemüse in Tomatensoße.",
        "wine_name": "Moschofilero",
        "wine_type": "weiss",
        "wine_description": "Der duftende Moschofilero mit seinen floralen Noten und knackiger Säure begleitet den Fisch mit Gemüse elegant. Die Tomatensoße wird von der Frucht des Weins aufgehellt."
    },
    {
        "dish_name": "Lahanosalata (Λαχανοσαλάτα)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Kohl-Salat mit Zitrone und Olivenöl.",
        "wine_name": "Debina",
        "wine_type": "weiss",
        "wine_description": "Die prickelnde Debina aus Epirus mit ihrer erfrischenden Säure ist der ideale Partner für diesen simplen, aber köstlichen Kohlsalat. Leicht und belebend."
    },
    {
        "dish_name": "Dakos (Ντάκος)",
        "region": "Kreta",
        "category": "Kreta",
        "dish_description": "Kretischer Zwieback-Salat mit Tomaten, Feta und Olivenöl.",
        "wine_name": "Vidiano",
        "wine_type": "weiss",
        "wine_description": "Der üppige kretische Vidiano mit seinen tropischen Noten ist perfekt für diesen rustikalen Zwieback-Salat. Das Olivenöl und der Feta werden wunderbar ergänzt."
    },
    {
        "dish_name": "Saganaki (Σαγανάκι)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Gebratener Käse (oft Kasseri oder Kefalotiri) mit Zitrone.",
        "wine_name": "Xinomavro Rosé",
        "wine_type": "rose",
        "wine_description": "Ein kühler Xinomavro Rosé mit seiner lebendigen Säure durchschneidet die Reichhaltigkeit des gebratenen Käses perfekt. Die Zitrone im Gericht findet im Wein ihr Gegenstück."
    },
    {
        "dish_name": "Horiatiki Salata (Χωριάτικη)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Griechischer Bauernsalat mit Tomaten, Gurken, Oliven, Feta und Olivenöl.",
        "wine_name": "Assyrtiko",
        "wine_type": "weiss",
        "wine_description": "Der mineralische Assyrtiko mit seiner salzigen Note ist der perfekte Partner für den klassischen Horiatiki. Die Oliven und der Feta finden im Wein ihren idealen Begleiter."
    },
    {
        "dish_name": "Htapodi Krasato (Χταπόδι κρασάτο)",
        "region": "Inseln",
        "category": "Inseln",
        "dish_description": "Oktopus in Rotwein geschmort mit Zwiebeln und Kräutern.",
        "wine_name": "Mavrotragano",
        "wine_type": "rot",
        "wine_description": "Der intensive Mavrotragano aus Santorin mit seiner dunklen Frucht und würzigen Komplexität ist der mutige Partner für in Rotwein geschmorten Oktopus. Vulkanische Kraft trifft auf Meeresfrüchte."
    },
    {
        "dish_name": "Papoutsakia (Παπουτσάκια)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Gefüllte Auberginen mit Hackfleisch und Béchamel – kleine Schuhe.",
        "wine_name": "Agiorgitiko",
        "wine_type": "rot",
        "wine_description": "Der samtige Agiorgitiko mit seinen Pflaumennoten umschmeichelt die cremige Béchamel und das würzige Hackfleisch. Ein klassisches griechisches Pairing."
    },
    {
        "dish_name": "Imam Baildi (Ιμάμ Μπαϊλντί)",
        "region": "Überall",
        "category": "Klassiker",
        "dish_description": "Geschmorte Auberginen gefüllt mit Zwiebeln, Tomaten und Knoblauch.",
        "wine_name": "Roditis",
        "wine_type": "weiss",
        "wine_description": "Der frische Roditis mit seinen grünen Apfelnoten und lebendiger Säure ist ein erfrischender Kontrast zu den reichhaltigen, geschmorten Auberginen. Der Knoblauch wird sanft gezähmt."
    }
]


async def import_greece_dishes():
    """Import all Greek dishes into regional_pairings collection."""
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'wine_pairing')]
    
    print("🇬🇷 Starting Greece Sommelier Kompass Import...")
    print(f"📊 Total dishes to import: {len(GREECE_DISHES)}")
    
    # Check existing Greece dishes
    existing = await db.regional_pairings.count_documents({"country": "Griechenland"})
    print(f"📍 Existing Greece dishes in DB: {existing}")
    
    imported = 0
    skipped = 0
    
    for dish in GREECE_DISHES:
        # Check if dish already exists (by name)
        existing_dish = await db.regional_pairings.find_one({
            "dish_name": dish["dish_name"],
            "country": "Griechenland"
        })
        
        if existing_dish:
            print(f"  ⏭️ Skipping (exists): {dish['dish_name']}")
            skipped += 1
            continue
        
        # Create full document
        doc = {
            "id": str(uuid4()),
            "dish_name": dish["dish_name"],
            "dish_description": dish["dish_description"],
            "dish_description_en": translate_dish_en(dish["dish_description"]),
            "dish_description_fr": translate_dish_fr(dish["dish_description"]),
            "country": "Griechenland",
            "region": dish["region"],
            "category": dish.get("category", "Klassiker"),
            "wine_name": dish["wine_name"],
            "wine_type": dish["wine_type"],
            "wine_description": dish["wine_description"],
            "wine_description_en": f"[EN] {dish['wine_description'][:100]}...",
            "wine_description_fr": f"[FR] {dish['wine_description'][:100]}...",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.regional_pairings.insert_one(doc)
        imported += 1
        print(f"  ✅ Imported: {dish['dish_name']} ({dish['region']})")
    
    # Final count
    final_count = await db.regional_pairings.count_documents({"country": "Griechenland"})
    
    print("\n" + "="*60)
    print(f"🎉 IMPORT COMPLETE!")
    print(f"   ✅ Imported: {imported}")
    print(f"   ⏭️ Skipped: {skipped}")
    print(f"   📊 Total Greece dishes now: {final_count}")
    print("="*60)
    
    client.close()
    return imported, skipped, final_count


def translate_dish_en(text_de):
    """Basic translations for common dish descriptions."""
    # Simple mapping for common phrases
    translations = {
        "Schichtgericht aus Auberginen, Hackfleisch, Tomatensoße und Béchamel-Sauce.": "Layered dish of eggplant, minced meat, tomato sauce and Béchamel sauce.",
        "Nudelauflauf mit Hackfleisch und Béchamel, ähnlich Lasagne.": "Pasta bake with minced meat and Béchamel, similar to lasagna.",
        "Gefüllte Tomaten und Paprika mit Reis, Kräutern und manchmal Hackfleisch.": "Stuffed tomatoes and peppers with rice, herbs and sometimes minced meat.",
        "Reis gefüllte Weinblätter, oft mit Kräutern und Zitrone.": "Rice-stuffed vine leaves, often with herbs and lemon.",
        "Blätterteig mit Spinat und Feta-Käse.": "Phyllo pastry with spinach and feta cheese.",
        "Gegrillte Fleischspieße (meist Schwein oder Huhn).": "Grilled meat skewers (mostly pork or chicken).",
    }
    return translations.get(text_de, text_de)


def translate_dish_fr(text_de):
    """Basic translations for common dish descriptions."""
    translations = {
        "Schichtgericht aus Auberginen, Hackfleisch, Tomatensoße und Béchamel-Sauce.": "Plat en couches d'aubergines, viande hachée, sauce tomate et Béchamel.",
        "Nudelauflauf mit Hackfleisch und Béchamel, ähnlich Lasagne.": "Gratin de pâtes avec viande hachée et Béchamel, similaire aux lasagnes.",
        "Gefüllte Tomaten und Paprika mit Reis, Kräutern und manchmal Hackfleisch.": "Tomates et poivrons farcis au riz, herbes et parfois viande hachée.",
        "Reis gefüllte Weinblätter, oft mit Kräutern und Zitrone.": "Feuilles de vigne farcies au riz, souvent avec herbes et citron.",
        "Blätterteig mit Spinat und Feta-Käse.": "Pâte feuilletée aux épinards et feta.",
        "Gegrillte Fleischspieße (meist Schwein oder Huhn).": "Brochettes de viande grillée (porc ou poulet).",
    }
    return translations.get(text_de, text_de)


if __name__ == "__main__":
    asyncio.run(import_greece_dishes())
