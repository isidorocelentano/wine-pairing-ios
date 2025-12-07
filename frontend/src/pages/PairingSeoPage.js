import React from 'react';
import { useParams } from 'react-router-dom';
import { useLanguage } from '@/contexts/LanguageContext';
import { SEO } from '@/components/SEO';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export const PAIRING_TEMPLATES = {
  'lammkoteletts-mit-rosmarin-cabernet-sauvignon': {
    recipeId: 'https://wine-pairing.online/recipe/lammkoteletts-mit-rosmarin',
    wineId: 'https://wine-pairing.online/wine/2018-cabernet-sauvignon-reserve',
    url: 'https://wine-pairing.online/pairing/lammkoteletts-mit-rosmarin-cabernet-sauvignon',
    imageRecipe: 'https://wine-pairing.online/images/recipes/lammkoteletts-mit-rosmarin.jpg',
    imageWine: 'https://wine-pairing.online/images/wines/2018-cabernet-sauvignon-reserve.jpg',
    price: '24.90',
    offerUrl: 'https://wine-pairing.online/kaufen/2018-cabernet-sauvignon-reserve',
    recipe: {
      name: {
        de: 'Lammkoteletts mit Rosmarin',
        en: 'Lamb Chops with Rosemary',
        fr: "Côtelettes d'agneau au romarin"
      },
      description: {
        de: 'Zarte Lammkoteletts, kurz angebraten, mit frischem Rosmarin, Knoblauch und einem Hauch Olivenöl – außen knusprig, innen saftig rosa.',
        en: 'Tender lamb chops, quickly seared with fresh rosemary, garlic and a touch of olive oil – crisp on the outside, juicy and pink inside.',
        fr: "De tendres côtelettes d'agneau, rapidement saisies avec du romarin frais, de l'ail et un filet d'huile d'olive – croustillantes à l'extérieur, rosées et juteuses à l'intérieur."
      },
      keywords: ['Lamm', 'Lammkoteletts', 'Rosmarin', 'Hauptgericht', 'Fleischgericht'],
      category: 'Hauptgericht',
      cuisine: 'Mediterran'
    },
    wine: {
      name: {
        de: '2018 Cabernet Sauvignon Reserve',
        en: '2018 Cabernet Sauvignon Reserve (Red Wine)',
        fr: 'Cabernet Sauvignon Réserve 2018'
      },
      description: {
        de: 'Ein kräftiger Cabernet Sauvignon mit dichter dunkler Frucht, fester Tanninstruktur und Noten von schwarzer Johannisbeere, Zedernholz und Grafit.',
        en: 'A powerful Cabernet Sauvignon with dense dark fruit, firm tannins and notes of blackcurrant, cedar and graphite.',
        fr: 'Un Cabernet Sauvignon puissant aux fruits noirs denses, aux tanins fermes et aux notes de cassis, de cèdre et de graphite.'
      },
      brand: 'Beispiel Weingut',
      reviewBody: {
        de: 'Die festen, aber fein gereiften Tannine dieses Cabernet binden das Fett der Lammkoteletts und sorgen dafür, dass das Gericht nicht schwer wirkt. Die dunkle Frucht und die Noten von Zedernholz spiegeln die Röstaromen und den würzigen Rosmarin ideal wider.',
        en: 'The firm yet ripe tannins of this Cabernet bind the fat of the lamb chops, keeping the dish from feeling heavy. Dark fruit and cedar notes echo the roasted flavors and savoury rosemary on the plate.',
        fr: "Les tanins fermes mais mûrs de ce Cabernet structurent le gras des côtelettes d'agneau et évitent que le plat ne paraisse lourd. Les arômes de fruits noirs et de cèdre répondent parfaitement aux saveurs rôties et au romarin."
      }
    },
    page: {
      title: {
        de: 'Perfektes Wein-Pairing: Lammkoteletts mit Rosmarin & Cabernet Sauvignon',
        en: 'Perfect Wine Pairing: Lamb Chops with Rosemary & Cabernet Sauvignon',
        fr: "Accord mets-vin parfait : Côtelettes d'agneau au romarin & Cabernet Sauvignon"
      },
      description: {
        de: 'Warum ein kräftiger Cabernet Sauvignon der ideale Partner für Lammkoteletts mit Rosmarin ist – erklärt von unserem virtuellen Sommelier.',
        en: 'Why a powerful Cabernet Sauvignon is the ideal partner for lamb chops with rosemary – explained by our virtual sommelier.',
        fr: "Pourquoi un Cabernet Sauvignon puissant est le partenaire idéal des côtelettes d'agneau au romarin – expliqué par notre sommelier virtuel."
      }
    }
  },
  'rinderfilet-mit-kraeuterbutter-und-pommes-bordeaux': {
    recipeId: 'https://wine-pairing.online/recipe/rinderfilet-mit-kraeuterbutter-und-pommes',
    wineId: 'https://wine-pairing.online/wine/2019-bordeaux-blend',
    url: 'https://wine-pairing.online/pairing/rinderfilet-mit-kraeuterbutter-und-pommes-bordeaux',
    imageRecipe: 'https://wine-pairing.online/images/recipes/rinderfilet-mit-kraeuterbutter-und-pommes.jpg',
    imageWine: 'https://wine-pairing.online/images/wines/2019-bordeaux-blend-haut-medoc.jpg',
    price: '29.90',
    offerUrl: 'https://wine-pairing.online/kaufen/2019-bordeaux-blend',
    recipe: {
      name: {
        de: 'Rinderfilet mit Kräuterbutter und Pommes',
        en: 'Beef Fillet with Herb Butter and Fries',
        fr: 'Filet de boeuf au beurre aux herbes et frites'
      },
      description: {
        de: 'Zartes Rinderfilet, kräftig angebraten und innen rosafarben, serviert mit geschmolzener Kräuterbutter und knusprigen Pommes frites.',
        en: 'Tender beef fillet, seared hard and pink inside, served with melting herb butter and crispy French fries.',
        fr: 'Filet de boeuf tendre, saisi à feu vif et rosé à coeur, servi avec un beurre aux herbes fondant et des frites croustillantes.'
      },
      keywords: ['Rinderfilet', 'Steak', 'Kräuterbutter', 'Pommes', 'Hauptgericht'],
      category: 'Hauptgericht',
      cuisine: 'Brasserie / Steakhouse'
    },
    wine: {
      name: {
        de: '2019 Bordeaux Blend Haut-Médoc',
        en: '2019 Bordeaux Red Blend',
        fr: 'Assemblage rouge de Bordeaux 2019'
      },
      description: {
        de: 'Ein klassischer Bordeaux aus dem Haut-Médoc mit schwarzer Johannisbeere, Pflaume, Zedernholz und feinkörnigem Tannin.',
        en: 'A classic Bordeaux from Haut-Médoc with blackcurrant, plum, cedar and fine-grained tannins.',
        fr: 'Un Bordeaux classique du Haut-Médoc avec des notes de cassis, de prune, de cèdre et des tanins fins.'
      },
      brand: 'Château Exemple',
      reviewBody: {
        de: 'Die Kombination aus saftiger Frucht, frischer Säure und feinkörnigem Tannin dieses Bordeaux schneidet durch die reichhaltige Kräuterbutter und das Fett der Pommes, ohne die Zartheit des Filets zu überdecken. Die Holznoten greifen die Röstaromen des angebratenen Fleisches auf.',
        en: 'The mix of juicy dark fruit, fresh acidity and fine-grained tannins in this Bordeaux cuts through the rich herb butter and fries while respecting the tenderness of the beef fillet. Subtle oak notes mirror the seared crust of the meat.',
        fr: "L'alliance de fruits noirs juteux, d'une acidité fraîche et de tanins fins permet à ce Bordeaux de dompter le beurre aux herbes et les frites, tout en préservant la tendreté du filet. Les notes boisées rappellent la croûte rôtie de la viande."
      }
    },
    page: {
      title: {
        de: 'Perfektes Wein-Pairing: Rinderfilet mit Kräuterbutter & Bordeaux',
        en: 'Perfect Wine Pairing: Beef Fillet with Herb Butter & Bordeaux',
        fr: 'Accord mets-vin parfait : Filet de boeuf, beurre aux herbes & Bordeaux'
      },
      description: {
        de: 'Warum ein klassischer Bordeaux-Blend der ideale Begleiter für Rinderfilet mit Kräuterbutter und Pommes ist – mit sensorischer Begründung.',
        en: 'Why a classic Bordeaux blend is the ideal partner for beef fillet with herb butter and fries – with a sensory explanation.',
        fr: "Pourquoi un assemblage classique de Bordeaux est le partenaire idéal du filet de boeuf, beurre aux herbes et frites – avec explication sensorielle."
      }
    }
  },
  'lachsfilet-mit-kraeutersauce-chardonnay': {
    recipeId: 'https://wine-pairing.online/recipe/lachsfilet-mit-kraeutersauce',
    wineId: 'https://wine-pairing.online/wine/chardonnay-reserve-burgund',
    url: 'https://wine-pairing.online/pairing/lachsfilet-mit-kraeutersauce-chardonnay',
    imageRecipe: 'https://wine-pairing.online/images/recipes/lachsfilet-mit-kraeutersauce.jpg',
    imageWine: 'https://wine-pairing.online/images/wines/chardonnay-reserve-burgund.jpg',
    price: '19.90',
    offerUrl: 'https://wine-pairing.online/kaufen/chardonnay-reserve-burgund',
    recipe: {
      name: {
        de: 'Lachsfilet mit Kräutersauce',
        en: 'Salmon Fillet with Herb Sauce',
        fr: 'Filet de saumon à la sauce aux herbes'
      },
      description: {
        de: 'Saftiges Lachsfilet mit knuspriger Haut, serviert auf einer hellen Kräuter-Sahnesauce mit Zitrusanklängen und feinem Gemüse.',
        en: 'Juicy salmon fillet with crispy skin, served on a light herb cream sauce with citrus notes and tender vegetables.',
        fr: 'Filet de saumon juteux à la peau croustillante, servi sur une sauce crème aux herbes aux accents d’agrumes et accompagné de légumes tendres.'
      },
      keywords: ['Lachs', 'Fischgericht', 'Kräutersauce', 'Hauptgericht'],
      category: 'Hauptgericht',
      cuisine: 'Europäisch'
    },
    wine: {
      name: {
        de: 'Chardonnay Réserve – Burgund',
        en: 'Burgundy Chardonnay Reserve',
        fr: 'Chardonnay Réserve de Bourgogne'
      },
      description: {
        de: 'Ein vollmundiger Chardonnay aus dem Burgund mit Noten von Zitrusfrüchten, reifem Apfel, Nussigkeit und feiner Buttrigkeit durch den Fassausbau.',
        en: 'A full-bodied Chardonnay from Burgundy with notes of citrus, ripe apple, nuttiness and a fine buttery character from barrel ageing.',
        fr: 'Un Chardonnay ample de Bourgogne aux notes d’agrumes, de pomme mûre, de noisette et à la texture beurrée apportée par l’élevage en fût.'
      },
      brand: 'Domaine Exemple',
      reviewBody: {
        de: 'Die frische, aber gut eingebundene Säure dieses Chardonnays hebt den fettreichen Lachs an, während die cremige Textur und die buttrig-nussigen Noten die Kräuter-Sahnesauce spiegeln. Zitrusanklänge verbinden sich mit den Zitronennoten der Sauce und halten das Gericht in Balance.',
        en: 'The fresh yet well-integrated acidity of this Chardonnay lifts the rich salmon, while its creamy texture and buttery, nutty notes mirror the herb cream sauce. Citrus aromas pick up the lemon accents in the dish and keep everything in balance.',
        fr: 'L’acidité fraîche mais intégrée de ce Chardonnay soutient le gras du saumon, tandis que sa texture crémeuse et ses notes beurrées et noisettées reflètent la sauce aux herbes. Les arômes d’agrumes prolongent le citron du plat et assurent une belle harmonie.'
      }
    },
    page: {
      title: {
        de: 'Perfektes Wein-Pairing: Lachsfilet mit Kräutersauce & Chardonnay',
        en: 'Perfect Wine Pairing: Salmon Fillet with Herb Sauce & Chardonnay',
        fr: 'Accord mets-vin parfait : Filet de saumon, sauce aux herbes & Chardonnay'
      },
      description: {
        de: 'Warum ein cremiger Chardonnay aus dem Burgund der ideale Partner für Lachsfilet mit Kräutersauce ist – sensorisch erklärt.',
        en: 'Why a creamy Chardonnay from Burgundy is the ideal partner for salmon fillet with herb sauce – explained from a sensory perspective.',
        fr: 'Pourquoi un Chardonnay crémeux de Bourgogne est le partenaire idéal du filet de saumon à la sauce aux herbes – expliqué d’un point de vue sensoriel.'
      }
    }
  },
  'spaghetti-bolognese-chianti': {
    recipeId: 'https://wine-pairing.online/recipe/spaghetti-bolognese',
    wineId: 'https://wine-pairing.online/wine/chianti-classico',
    url: 'https://wine-pairing.online/pairing/spaghetti-bolognese-chianti',
    imageRecipe: 'https://wine-pairing.online/images/recipes/spaghetti-bolognese.jpg',
    imageWine: 'https://wine-pairing.online/images/wines/chianti-classico.jpg',
    price: '17.90',
    offerUrl: 'https://wine-pairing.online/kaufen/chianti-classico',
    recipe: {
      name: {
        de: 'Spaghetti Bolognese',
        en: 'Spaghetti Bolognese',
        fr: 'Spaghetti bolognaise'
      },
      description: {
        de: 'Klassische Spaghetti mit langsam geschmorter Rinderhack-Tomatensauce, viel Umami, Kräutern und einer leichten Süße aus der Reduktion.',
        en: 'Classic spaghetti with slowly braised beef and tomato ragù, rich in umami, herbs and a touch of sweetness from reduction.',
        fr: 'Spaghetti classiques avec un ragù de boeuf et de tomate mijoté longuement, riche en umami, en herbes et en légère douceur de réduction.'
      },
      keywords: ['Spaghetti Bolognese', 'Pasta', 'Ragù', 'Hauptgericht'],
      category: 'Hauptgericht',
      cuisine: 'Italienisch'
    },
    wine: {
      name: {
        de: 'Chianti Classico',
        en: 'Chianti Classico',
        fr: 'Chianti Classico'
      },
      description: {
        de: 'Ein Sangiovese-basierter Chianti Classico mit roter Kirsche, Kräutern, frischer Säure und mittlerem Tannin – klassischer Pasta-Begleiter.',
        en: 'A Sangiovese-based Chianti Classico with red cherry, herbs, fresh acidity and medium tannins – a classic pasta companion.',
        fr: 'Un Chianti Classico a base de Sangiovese, aux notes de cerise rouge, d\'herbes, a l\'acidite fraiche et aux tanins moyens - un accompagnement classique pour les pates.'
      },
      brand: 'Cantina Esempio',
      reviewBody: {
        de: 'Die frische Säure und die mittleren Tanine des Chianti schneiden durch das Fett der Bolognese und balancieren die Süße der Tomatensauce. Die Noten von roter Kirsche und Kräutern verbinden sich harmonisch mit dem Ragù und lassen das Gericht klarer und lebendiger wirken.',
        en: 'The fresh acidity and medium tannins of the Chianti cut through the richness of the Bolognese and balance the sweetness of the tomato sauce. Red cherry and herbal notes echo the ragù and make the dish feel brighter and more defined.',
        fr: 'L\'acidite fraiche et les tanins moyens du Chianti tranchent dans la richesse de la bolognaise et equilibrent la douceur de la sauce tomate. Les notes de cerise rouge et d\'herbes se marient au ragu et rendent le plat plus vif et plus net.'
      }
    },
    page: {
      title: {
        de: 'Perfektes Wein-Pairing: Spaghetti Bolognese & Chianti',
        en: 'Perfect Wine Pairing: Spaghetti Bolognese & Chianti',
        fr: 'Accord mets-vin parfait : Spaghetti bolognaise & Chianti'
      },
      description: {
        de: 'Warum ein klassischer Chianti der ideale Partner für Spaghetti Bolognese ist – mit Fokus auf Säure, Tannin und Umami.',
        en: 'Why a classic Chianti is the ideal partner for spaghetti bolognese – focusing on acidity, tannins and umami.',
        fr: 'Pourquoi un Chianti classique est le partenaire idéal des spaghetti bolognaise – avec un accent sur l'acidité, les tanins et l'umami.'
      }
    }
  },
  'pizza-margherita-chianti': {
    recipeId: 'https://wine-pairing.online/recipe/pizza-margherita',
    wineId: 'https://wine-pairing.online/wine/chianti-collinare',
    url: 'https://wine-pairing.online/pairing/pizza-margherita-chianti',
    imageRecipe: 'https://wine-pairing.online/images/recipes/pizza-margherita.jpg',
    imageWine: 'https://wine-pairing.online/images/wines/chianti-collinare.jpg',
    price: '14.90',
    offerUrl: 'https://wine-pairing.online/kaufen/chianti-collinare',
    recipe: {
      name: {
        de: 'Pizza Margherita',
        en: 'Pizza Margherita',
        fr: 'Pizza Margherita'
      },
      description: {
        de: 'Dünner Pizzaboden mit fruchtiger Tomatensauce, Mozzarella und frischem Basilikum – schlicht, aber aromatisch und saftig.',
        en: 'Thin pizza base with fruity tomato sauce, mozzarella and fresh basil – simple, yet aromatic and juicy.',
        fr: 'Pâte à pizza fine avec sauce tomate fruitée, mozzarella et basilic frais – simple, mais aromatique et juteuse.'
      },
      keywords: ['Pizza', 'Margherita', 'Tomate', 'Mozzarella'],
      category: 'Hauptgericht',
      cuisine: 'Italienisch'
    },
    wine: {
      name: {
        de: 'Chianti Collinare',
        en: 'Chianti Collinare',
        fr: 'Chianti Collinare'
      },
      description: {
        de: 'Ein frischer, fruchtbetonter Chianti mit roter Frucht, Kräutern und lebendiger Säure, der Tomate und Käse elegant begleitet.',
        en: 'A fresh, fruit-forward Chianti with red fruit, herbs and lively acidity that elegantly accompanies tomato and cheese.',
        fr: 'Un Chianti frais et fruité, aux notes de fruits rouges, d'herbes et à l'acidité vive, qui accompagne élégamment tomate et fromage.'
      },
      brand: 'Casa Collinare',
      reviewBody: {
        de: 'Die lebendige Säure des Chianti harmoniert mit der Tomatensauce und verhindert, dass die Pizza schwer wirkt. Die rote Frucht ergänzt die Süße der Tomate, während die Kräuternoten an frisches Basilikum erinnern und so eine aromatische Brücke schlagen.',
        en: 'The lively acidity of the Chianti matches the tomato sauce and keeps the pizza from feeling heavy. Red fruit complements the sweetness of the tomato while herbal notes recall fresh basil, building an aromatic bridge.',
        fr: 'L'acidité vive du Chianti s'accorde avec la sauce tomate et empêche la pizza de paraître lourde. Les fruits rouges complètent la douceur de la tomate, tandis que les notes herbacées évoquent le basilic frais et créent un pont aromatique.'
      }
    },
    page: {
      title: {
        de: 'Perfektes Wein-Pairing: Pizza Margherita & Chianti',
        en: 'Perfect Wine Pairing: Pizza Margherita & Chianti',
        fr: 'Accord mets-vin parfait : Pizza Margherita & Chianti'
      },
      description: {
        de: 'Warum ein frischer Chianti die Tomate-Mozzarella-Kombination der Pizza Margherita perfekt aufnimmt.',
        en: 'Why a fresh Chianti perfectly supports the tomato and mozzarella combination of pizza Margherita.',
        fr: 'Pourquoi un Chianti frais accompagne parfaitement la combinaison tomate-mozzarella de la pizza Margherita.'
      }
    }
  },
  'cheeseburger-merlot': {
    recipeId: 'https://wine-pairing.online/recipe/cheeseburger',
    wineId: 'https://wine-pairing.online/wine/merlot-reserve',
    url: 'https://wine-pairing.online/pairing/cheeseburger-merlot',
    imageRecipe: 'https://wine-pairing.online/images/recipes/cheeseburger.jpg',
    imageWine: 'https://wine-pairing.online/images/wines/merlot-reserve.jpg',
    price: '18.50',
    offerUrl: 'https://wine-pairing.online/kaufen/merlot-reserve',
    recipe: {
      name: {
        de: 'Cheeseburger',
        en: 'Cheeseburger',
        fr: 'Cheeseburger'
      },
      description: {
        de: 'Saftiges Rindfleisch-Patty im Brötchen mit geschmolzenem Käse, Gurken, Zwiebeln und Sauce – herzhaft, leicht süßlich und sehr umami.',
        en: 'Juicy beef patty in a bun with melted cheese, pickles, onions and sauce – hearty, slightly sweet and very umami.',
        fr: 'Steak haché de boeuf juteux dans un bun avec fromage fondu, cornichons, oignons et sauce – gourmand, légèrement sucré et très umami.'
      },
      keywords: ['Burger', 'Cheeseburger', 'Streetfood'],
      category: 'Hauptgericht',
      cuisine: 'American / Streetfood'
    },
    wine: {
      name: {
        de: 'Merlot Réserve',
        en: 'Merlot Reserve',
        fr: 'Merlot Réserve'
      },
      description: {
        de: 'Ein weicher, fruchtbetonter Merlot mit reifer Pflaume, Beeren und sanften Taninen – ideal für unkomplizierte Fleischgerichte.',
        en: 'A soft, fruit-forward Merlot with ripe plum, berry notes and gentle tannins – ideal for easy-going meat dishes.',
        fr: 'Un Merlot souple et fruité, aux notes de prune mûre et de baies, aux tanins doux – idéal pour des plats de viande décontractés.'
      },
      brand: 'Estate Reserve',
      reviewBody: {
        de: 'Die weichen Tanine und die reife Frucht des Merlot passen perfekt zum saftigen Rindfleisch und dem geschmolzenen Käse. Die leichte Süße des Burgers wird aufgefangen, ohne dass der Wein bitter wirkt, und die Frucht bringt Frische in das reichhaltige Streetfood-Profil.',
        en: 'The soft tannins and ripe fruit of the Merlot match the juicy beef and melted cheese perfectly. The slight sweetness of the burger is balanced without making the wine taste bitter, while the fruit adds freshness to the rich street food profile.',
        fr: 'Les tanins souples et les fruits mûrs du Merlot s'accordent parfaitement avec le boeuf juteux et le fromage fondu. La légère douceur du burger est équilibrée sans que le vin ne paraisse amer, et le fruit apporte de la fraîcheur au profil riche de ce street food.'
      }
    },
    page: {
      title: {
        de: 'Perfektes Wein-Pairing: Cheeseburger & Merlot',
        en: 'Perfect Wine Pairing: Cheeseburger & Merlot',
        fr: 'Accord mets-vin parfait : Cheeseburger & Merlot'
      },
      description: {
        de: 'Warum ein weicher, fruchtiger Merlot den Cheeseburger angenehm abrundet, ohne ihn zu erschlagen.',
        en: 'Why a soft, fruity Merlot rounds off a cheeseburger pleasantly without overpowering it.',
        fr: 'Pourquoi un Merlot souple et fruité accompagne agréablement le cheeseburger sans le dominer.'
      }
    }
  },
  'sushi-mix-riesling': {
    recipeId: 'https://wine-pairing.online/recipe/sushi-mix',
    wineId: 'https://wine-pairing.online/wine/riesling-trocken',
    url: 'https://wine-pairing.online/pairing/sushi-mix-riesling',
    imageRecipe: 'https://wine-pairing.online/images/recipes/sushi-mix.jpg',
    imageWine: 'https://wine-pairing.online/images/wines/riesling-trocken.jpg',
    price: '16.50',
    offerUrl: 'https://wine-pairing.online/kaufen/riesling-trocken',
    recipe: {
      name: {
        de: 'Sushi Mix',
        en: 'Sushi Mix',
        fr: 'Assortiment de sushi'
      },
      description: {
        de: 'Gemischte Sushi-Auswahl mit Nigiri und Maki – zarter Fisch, gekochter Reis, etwas Sojasauce und Wasabi.',
        en: 'Mixed sushi selection with nigiri and maki – delicate fish, cooked rice, a touch of soy sauce and wasabi.',
        fr: 'Assortiment de sushi avec nigiri et maki – poisson délicat, riz cuit, un peu de sauce soja et de wasabi.'
      },
      keywords: ['Sushi', 'Fisch', 'japanisch'],
      category: 'Hauptgericht',
      cuisine: 'Japanisch'
    },
    wine: {
      name: {
        de: 'Riesling trocken',
        en: 'Riesling dry',
        fr: 'Riesling sec'
      },
      description: {
        de: 'Ein trockener Riesling mit zitrischer Frucht, grüner Apfel und klarer Säure – präzise und mineralisch.',
        en: 'A dry Riesling with citrus fruit, green apple and crisp acidity – precise and mineral.',
        fr: 'Un Riesling sec aux notes d'agrumes, de pomme verte et à l'acidité vive – précis et minéral.'
      },
      brand: 'Mosel Selection',
      reviewBody: {
        de: 'Die klare Säure und die Zitrusnoten des Rieslings reinigen den Gaumen zwischen Reis, Fisch und Sojasauce, ohne die feinen Aromen des Sushi zu überdecken. Die Mineralität unterstreicht die Frische des Fisches und hält das Pairing leicht und präzise.',
        en: 'The crisp acidity and citrus notes of the Riesling cleanse the palate between rice, fish and soy sauce without overwhelming the delicate sushi aromas. Its minerality underscores the freshness of the fish and keeps the pairing light and precise.',
        fr: 'L'acidité vive et les notes d'agrumes du Riesling nettoient le palais entre le riz, le poisson et la sauce soja sans écraser les arômes délicats du sushi. Sa minéralité souligne la fraîcheur du poisson et maintient l'accord léger et précis.'
      }
    },
    page: {
      title: {
        de: 'Perfektes Wein-Pairing: Sushi Mix & Riesling trocken',
        en: 'Perfect Wine Pairing: Sushi Mix & Dry Riesling',
        fr: 'Accord mets-vin parfait : Assortiment de sushi & Riesling sec'
      },
      description: {
        de: 'Warum ein trockener Riesling die feine Aromatik von Sushi unterstreicht, statt sie zu überdecken.',
        en: 'Why a dry Riesling enhances the fine aromatics of sushi instead of overpowering them.',
        fr: 'Pourquoi un Riesling sec souligne la finesse aromatique du sushi plutôt que de la masquer.'
      }
    }
  },
  'gruenes-thai-curry-riesling-halbtrocken': {
    recipeId: 'https://wine-pairing.online/recipe/gruenes-thai-curry-mit-huhn',
    wineId: 'https://wine-pairing.online/wine/riesling-halbtrocken',
    url: 'https://wine-pairing.online/pairing/gruenes-thai-curry-riesling-halbtrocken',
    imageRecipe: 'https://wine-pairing.online/images/recipes/gruenes-thai-curry.jpg',
    imageWine: 'https://wine-pairing.online/images/wines/riesling-halbtrocken.jpg',
    price: '15.90',
    offerUrl: 'https://wine-pairing.online/kaufen/riesling-halbtrocken',
    recipe: {
      name: {
        de: 'Grünes Thai-Curry mit Huhn',
        en: 'Green Thai Curry with Chicken',
        fr: 'Curry vert thaï au poulet'
      },
      description: {
        de: 'Cremiges grünes Thai-Curry mit Kokosmilch, Huhn, Gemüse und frischen Kräutern – aromatisch, pikant und leicht süßlich.',
        en: 'Creamy green Thai curry with coconut milk, chicken, vegetables and fresh herbs – aromatic, spicy and slightly sweet.',
        fr: 'Curry vert thaï crémeux au lait de coco, poulet, légumes et herbes fraîches – aromatique, relevé et légèrement sucré.'
      },
      keywords: ['Thai Curry', 'Huhn', 'asiatisch', 'scharf'],
      category: 'Hauptgericht',
      cuisine: 'Thai'
    },
    wine: {
      name: {
        de: 'Riesling halbtrocken',
        en: 'Riesling off-dry',
        fr: 'Riesling demi-sec'
      },
      description: {
        de: 'Ein halbtrockener Riesling mit saftiger Frucht, präsenter Säure und einem Hauch Restsüße – perfekt zu Schärfe und Kokos.',
        en: 'An off-dry Riesling with juicy fruit, vivid acidity and a touch of residual sweetness – perfect with spice and coconut.',
        fr: 'Un Riesling demi-sec aux fruits juteux, à l'acidité marquée et à une pointe de sucres résiduels – parfait avec les épices et la noix de coco.'
      },
      brand: 'Asia Pairing Selection',
      reviewBody: {
        de: 'Die leichte Restsüße des halbtrockenen Rieslings mildert die Schärfe des grünen Currys, während die Säure die Cremigkeit der Kokosmilch auflockert. Die Fruchtigkeit greift die Kräuter- und Limettennoten der Thai-Küche auf und sorgt für ein spannungsreiches, aber harmonisches Pairing.',
        en: 'The slight residual sweetness of the off-dry Riesling softens the heat of the green curry while its acidity lifts the creaminess of the coconut milk. The fruit character picks up the herbal and lime notes of Thai cuisine, creating a vibrant yet harmonious pairing.',
        fr: 'La légère sucrosité résiduelle du Riesling demi-sec adoucit le piquant du curry vert tandis que son acidité allège l'onctuosité du lait de coco. Le fruit rejoint les notes d'herbes et de citron vert de la cuisine thaïe et crée un accord à la fois vif et harmonieux.'
      }
    },
    page: {
      title: {
        de: 'Perfektes Wein-Pairing: Grünes Thai-Curry & Riesling halbtrocken',
        en: 'Perfect Wine Pairing: Green Thai Curry & Off-dry Riesling',
        fr: 'Accord mets-vin parfait : Curry vert thaï & Riesling demi-sec'
      },
      description: {
        de: 'Warum ein halbtrockener Riesling die Schärfe und Cremigkeit von grünem Thai-Curry ideal balanciert.',
        en: 'Why an off-dry Riesling ideally balances the heat and creaminess of green Thai curry.',
        fr: 'Pourquoi un Riesling demi-sec équilibre idéalement le piquant et l'onctuosité du curry vert thaï.'
      }
    }
  }
};

const buildJsonLd = (slug, language) => {
  const tpl = PAIRING_TEMPLATES[slug];
  if (!tpl) return null;

  const lang = language || 'de';

  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Recipe",
        "@id": tpl.recipeId,
        "name": tpl.recipe.name.de,
        "alternateName": [tpl.recipe.name.en, tpl.recipe.name.fr],
        "image": tpl.imageRecipe,
        "description": tpl.recipe.description[lang] || tpl.recipe.description.de,
        "keywords": tpl.recipe.keywords.join(', '),
        "recipeCategory": tpl.recipe.category,
        "recipeCuisine": tpl.recipe.cuisine,
        "author": {
          "@type": "Organization",
          "name": "Wine-Pairing.online Cooking & Sommelier Team"
        }
      },
      {
        "@type": "Product",
        "@id": tpl.wineId,
        "name": tpl.wine.name.de,
        "alternateName": [tpl.wine.name.en, tpl.wine.name.fr],
        "image": tpl.imageWine,
        "description": tpl.wine.description[lang] || tpl.wine.description.de,
        "brand": {
          "@type": "Brand",
          "name": tpl.wine.brand
        },
        "review": {
          "@type": "Review",
          "reviewRating": {
            "@type": "Rating",
            "ratingValue": "5",
            "bestRating": "5"
          },
          "author": {
            "@type": "Person",
            "name": "Dein App Sommelier"
          },
          "reviewBody": `${tpl.wine.reviewBody.de}\n\n${tpl.wine.reviewBody.en}\n\n${tpl.wine.reviewBody.fr}`
        },
        "offers": {
          "@type": "Offer",
          "priceCurrency": "EUR",
          "price": tpl.price,
          "availability": "https://schema.org/InStock",
          "url": tpl.offerUrl
        }
      },
      {
        "@type": "WebPage",
        "@id": tpl.url,
        "name": tpl.page.title.de,
        "alternateName": [tpl.page.title.en, tpl.page.title.fr],
        "url": tpl.url,
        "inLanguage": ["de", "en", "fr"],
        "description": tpl.page.description[lang] || tpl.page.description.de,
        "mainEntity": [
          { "@id": tpl.recipeId },
          { "@id": tpl.wineId }
        ]
      }
    ]
  };
};

const PairingSeoPage = () => {
  const { slug } = useParams();
  const { language } = useLanguage();
  const tpl = PAIRING_TEMPLATES[slug];

  if (!tpl) {
    return (
      <div className="min-h-screen pb-20 md:pb-24 pt-10 px-4 md:px-12 lg:px-24">
        <div className="container mx-auto max-w-3xl">
          <p className="text-sm text-muted-foreground">Pairing-Seite nicht gefunden.</p>
        </div>
      </div>
    );
  }

  const lang = language || 'de';
  const jsonLd = buildJsonLd(slug, lang);

  return (
    <div className="min-h-screen pb-20 md:pb-24 pt-10 px-4 md:px-12 lg:px-24">
      <SEO
        title={tpl.page.title[lang] || tpl.page.title.de}
        description={tpl.page.description[lang] || tpl.page.description.de}
        url={tpl.url}
      />
      {jsonLd && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      )}
      <div className="container mx-auto max-w-3xl space-y-8">
        {/* Hero */}
        <header className="space-y-3 text-center md:text-left">
          <p className="text-accent font-accent text-xs tracking-widest uppercase">Wine Pairing Insight</p>
          <h1 className="text-2xl md:text-3xl font-semibold tracking-tight">
            {tpl.page.title[lang] || tpl.page.title.de}
          </h1>
          <p className="text-sm md:text-base text-muted-foreground max-w-2xl mx-auto md:mx-0">
            {tpl.page.description[lang] || tpl.page.description.de}
          </p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card className="bg-card/50 border-border/60">
            <CardHeader>
              <CardTitle className="text-base md:text-lg">Gericht</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm md:text-base">
              <p className="font-semibold">
                {tpl.recipe.name[lang] || tpl.recipe.name.de}
              </p>
              <p className="text-muted-foreground">
                {tpl.recipe.description[lang] || tpl.recipe.description.de}
              </p>
            </CardContent>
          </Card>
          <Card className="bg-card/50 border-border/60">
            <CardHeader>
              <CardTitle className="text-base md:text-lg">Wein</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm md:text-base">
              <p className="font-semibold">
                {tpl.wine.name[lang] || tpl.wine.name.de}
              </p>
              <p className="text-muted-foreground">
                {tpl.wine.description[lang] || tpl.wine.description.de}
              </p>
              <p className="text-xs text-muted-foreground">
                Preis (Platzhalter): ca. {tpl.price} EUR
              </p>
            </CardContent>
          </Card>
        </div>

        <Card className="bg-card/50 border-border/60">
          <CardHeader>
            <CardTitle className="text-base md:text-lg">Wenn dieser Wein nicht verfügbar ist…</CardTitle>
          </CardHeader>
          <CardContent className="text-sm md:text-base text-muted-foreground space-y-2">
            <p>
              {lang === 'de' && (
                'Kein exakt passender Wein im Regal? Greife zu einem vergleichbaren Stil: gleiche Farbe, ähnlicher Körper und eine ähnlich frische Säure bzw. Tanninstruktur. So bleibt die Balance zwischen Gericht und Glas erhalten.'
              )}
              {lang === 'en' && (
                'If this exact wine is not available, reach for a similar style: same colour, comparable body and a similar level of acidity or tannin. This keeps the balance between dish and glass intact.'
              )}
              {lang === 'fr' && (
                "Si ce vin précis n'est pas disponible, choisissez un style proche : même couleur, corps comparable et niveau d'acidité ou de tanin similaire. L'équilibre entre le plat et le verre reste ainsi préservé."
              )}
            </p>
          </CardContent>
        </Card>

        <Card className="bg-card/50 border-border/60">
          <CardHeader>
            <CardTitle className="text-base md:text-lg">Warum dieses Pairing funktioniert</CardTitle>
          </CardHeader>
          <CardContent className="text-sm md:text-base text-muted-foreground whitespace-pre-line">
            {tpl.wine.reviewBody[lang] || tpl.wine.reviewBody.de}
          </CardContent>
        </Card>

        <div className="flex justify-center md:justify-start pt-2">
          <a
            href="/pairing"
            className="inline-flex items-center px-4 py-2 rounded-full text-xs md:text-sm font-medium bg-primary text-primary-foreground hover:bg-primary/90 transition-colors"
          >
            Zur interaktiven Pairing-Seite
          </a>
        </div>
      </div>
    </div>
  );
};

export default PairingSeoPage;
