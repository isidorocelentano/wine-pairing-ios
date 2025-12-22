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
        fr: "Cotelettes d'agneau au romarin"
      },
      description: {
        de: 'Zarte Lammkoteletts, kurz angebraten, mit frischem Rosmarin, Knoblauch und einem Hauch Olivenöl - außen knusprig, innen saftig rosa.',
        en: 'Tender lamb chops, quickly seared with fresh rosemary, garlic and a touch of olive oil - crisp on the outside, juicy and pink inside.',
        fr: "De tendres cotelettes d'agneau, rapidement saisies avec du romarin frais, de l'ail et un filet d'huile d'olive - croustillantes a l'exterieur, rosees et juteuses a l'interieur."
      },
      keywords: ['Lamm', 'Lammkoteletts', 'Rosmarin', 'Hauptgericht', 'Fleischgericht'],
      category: 'Hauptgericht',
      cuisine: 'Mediterran'
    },
    wine: {
      name: {
        de: '2018 Cabernet Sauvignon Reserve',
        en: '2018 Cabernet Sauvignon Reserve (Red Wine)',
        fr: 'Cabernet Sauvignon Reserve 2018'
      },
      description: {
        de: 'Ein kraftiger Cabernet Sauvignon mit dichter dunkler Frucht, fester Tanninstruktur und Noten von schwarzer Johannisbeere, Zedernholz und Grafit.',
        en: 'A powerful Cabernet Sauvignon with dense dark fruit, firm tannins and notes of blackcurrant, cedar and graphite.',
        fr: 'Un Cabernet Sauvignon puissant aux fruits noirs denses, aux tanins fermes et aux notes de cassis, de cedre et de graphite.'
      },
      brand: 'Beispiel Weingut',
      reviewBody: {
        de: 'Die Frische und die festen, aber gereiften Tannine dieses Cabernet bringen Struktur in die Reichhaltigkeit der Lammkoteletts, sodass das Gericht nicht schwer wirkt. Die dunkle Frucht und die Noten von Zedernholz greifen die Röstaromen und den Rosmarin auf – genau diese Aromabrucke lasst Gericht und Wein wie aus einer Kuche wirken.',
        en: 'The freshness and firm yet ripe tannins of this Cabernet bring structure to the richness of the lamb chops so the dish never feels heavy. Dark fruit and cedar notes pick up the roasted flavours and rosemary – this aromatic bridge makes dish and wine feel as if they came from the same kitchen.',
        fr: "La fraicheur et les tanins fermes mais murs de ce Cabernet apportent de la structure a la richesse des cotelettes d'agneau, de sorte que le plat ne parait jamais lourd. Les fruits noirs et les notes de cedre reprennent les saveurs rotiess et le romarin – ce pont aromatique donne l'impression que le plat et le vin sortent de la meme cuisine."
      }
    },
    page: {
      title: {
        de: 'Perfektes Wein-Pairing: Lammkoteletts mit Rosmarin & Cabernet Sauvignon',
        en: 'Perfect Wine Pairing: Lamb Chops with Rosemary & Cabernet Sauvignon',
        fr: "Accord mets-vin parfait : Cotelettes d'agneau au romarin & Cabernet Sauvignon"
      },
      description: {
        de: 'Warum ein kraftiger Cabernet Sauvignon der ideale Partner fur Lammkoteletts mit Rosmarin ist - erklart von unserem virtuellen Sommelier.',
        en: 'Why a powerful Cabernet Sauvignon is the ideal partner for lamb chops with rosemary - explained by our virtual sommelier.',
        fr: "Pourquoi un Cabernet Sauvignon puissant est le partenaire ideal des cotelettes d'agneau au romarin - explique par notre sommelier virtuel."
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
        de: 'Rinderfilet mit Krauterbutter und Pommes',
        en: 'Beef Fillet with Herb Butter and Fries',
        fr: 'Filet de boeuf au beurre aux herbes et frites'
      },
      description: {
        de: 'Zartes Rinderfilet, kraftig angebraten und innen rosafarben, serviert mit geschmolzener Krauterbutter und knusprigen Pommes frites.',
        en: 'Tender beef fillet, seared hard and pink inside, served with melting herb butter and crispy French fries.',
        fr: 'Filet de boeuf tendre, saisi a feu vif et rose a coeur, servi avec un beurre aux herbes fondant et des frites croustillantes.'
      },
      keywords: ['Rinderfilet', 'Steak', 'Krauterbutter', 'Pommes', 'Hauptgericht'],
      category: 'Hauptgericht',
      cuisine: 'Brasserie / Steakhouse'
    },
    wine: {
      name: {
        de: '2019 Bordeaux Blend Haut-Medoc',
        en: '2019 Bordeaux Red Blend',
        fr: 'Assemblage rouge de Bordeaux 2019'
      },
      description: {
        de: 'Ein klassischer Bordeaux aus dem Haut-Medoc mit schwarzer Johannisbeere, Pflaume, Zedernholz und feinkörnigem Tannin.',
        en: 'A classic Bordeaux from Haut-Medoc with blackcurrant, plum, cedar and fine-grained tannins.',
        fr: 'Un Bordeaux classique du Haut-Medoc avec des notes de cassis, de prune, de cedre et des tanins fins.'
      },
      brand: 'Chateau Exemple',
      reviewBody: {
        de: 'Die Kombination aus saftiger Frucht, frischer Saure und feinkörnigem Tannin dieses Bordeaux bringt Frische in die Reichhaltigkeit von Filet, Krauterbutter und Pommes. Die Holznoten und dunklen Beerenaromen greifen die Röstaromen der Kruste auf – diese Aromabrucke verbindet Steakhouse-Charakter und Bordeaux im Glas.',
        en: 'The mix of juicy dark fruit, fresh acidity and fine-grained tannins in this Bordeaux adds freshness to the richness of fillet, herb butter and fries. Oak and dark berry notes pick up the seared crust – this aromatic bridge ties classic steakhouse flavours to Bordeaux in the glass.',
        fr: "L'alliance de fruits noirs juteux, d'une acidite fraiche et de tanins fins apporte de la fraicheur a la richesse du filet, du beurre aux herbes et des frites. Les notes boisees et de fruits noirs reprennent la croute roti – ce pont aromatique relie les saveurs de steakhouse au Bordeaux dans le verre."
      }
    },
    page: {
      title: {
        de: 'Perfektes Wein-Pairing: Rinderfilet mit Krauterbutter & Bordeaux',
        en: 'Perfect Wine Pairing: Beef Fillet with Herb Butter & Bordeaux',
        fr: 'Accord mets-vin parfait : Filet de boeuf, beurre aux herbes & Bordeaux'
      },
      description: {
        de: 'Warum ein klassischer Bordeaux-Blend der ideale Begleiter fur Rinderfilet mit Krauterbutter und Pommes ist - mit sensorischer Begrundung.',
        en: 'Why a classic Bordeaux blend is the ideal partner for beef fillet with herb butter and fries - with a sensory explanation.',
        fr: "Pourquoi un assemblage classique de Bordeaux est le partenaire ideal du filet de boeuf, beurre aux herbes et frites - avec explication sensorielle."
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
        de: 'Lachsfilet mit Krautersauce',
        en: 'Salmon Fillet with Herb Sauce',
        fr: 'Filet de saumon a la sauce aux herbes'
      },
      description: {
        de: 'Saftiges Lachsfilet mit knuspriger Haut, serviert auf einer hellen Krauter-Sahnesauce mit Zitrusanklangen und feinem Gemuse.',
        en: 'Juicy salmon fillet with crispy skin, served on a light herb cream sauce with citrus notes and tender vegetables.',
        fr: 'Filet de saumon juteux a la peau croustillante, servi sur une sauce creme aux herbes aux accents d’agrumes et accompagne de legumes tendres.'
      },
      keywords: ['Lachs', 'Fischgericht', 'Krautersauce', 'Hauptgericht'],
      category: 'Hauptgericht',
      cuisine: 'Europaisch'
    },
    wine: {
      name: {
        de: 'Chardonnay Reserve - Burgund',
        en: 'Burgundy Chardonnay Reserve',
        fr: 'Chardonnay Reserve de Bourgogne'
      },
      description: {
        de: 'Ein vollmundiger Chardonnay aus dem Burgund mit Noten von Zitrusfruchten, reifem Apfel, Nussigkeit und feiner Buttrigkeit durch den Fassausbau.',
        en: 'A full-bodied Chardonnay from Burgundy with notes of citrus, ripe apple, nuttiness and a fine buttery character from barrel ageing.',
        fr: 'Un Chardonnay ample de Bourgogne aux notes d’agrumes, de pomme mure, de noisette et a la texture beurree apportee par l’elevage en fut.'
      },
      brand: 'Domaine Exemple',
      reviewBody: {
        de: 'Die frische, aber gut eingebundene Saure dieses Chardonnays bringt Leichtigkeit in die Reichhaltigkeit von Lachs und Krauter-Sahnesauce. Seine buttrig-nussigen Noten greifen die cremige Sauce auf, wahrend die Zitrusfrische eine feine Aromabrucke zu den Zitronennoten im Gericht bildet.',
        en: 'The fresh yet well-integrated acidity of this Chardonnay lightens the richness of salmon and herb cream sauce. Its buttery, nutty tones mirror the creamy sauce while the citrus lift creates an aromatic bridge to the lemon accents in the dish.',
        fr: "L'acidite fraiche mais integree de ce Chardonnay apporte de la legerete a la richesse du saumon et de la sauce creme aux herbes. Ses notes beurreess et noisettees refletent la sauce, tandis que la fraicheur d'agrumes cree un pont aromatique avec le citron du plat."
      }
    },
    page: {
      title: {
        de: 'Perfektes Wein-Pairing: Lachsfilet mit Krautersauce & Chardonnay',
        en: 'Perfect Wine Pairing: Salmon Fillet with Herb Sauce & Chardonnay',
        fr: 'Accord mets-vin parfait : Filet de saumon, sauce aux herbes & Chardonnay'
      },
      description: {
        de: 'Warum ein cremiger Chardonnay aus dem Burgund der ideale Partner fur Lachsfilet mit Krautersauce ist - sensorisch erklart.',
        en: 'Why a creamy Chardonnay from Burgundy is the ideal partner for salmon fillet with herb sauce - explained from a sensory perspective.',
        fr: 'Pourquoi un Chardonnay cremeux de Bourgogne est le partenaire ideal du filet de saumon a la sauce aux herbes - explique d’un point de vue sensoriel.'
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
        de: 'Klassische Spaghetti mit langsam geschmorter Rinderhack-Tomatensauce, viel Umami, Krautern und einer leichten Suße aus der Reduktion.',
        en: 'Classic spaghetti with slowly braised beef and tomato ragu, rich in umami, herbs and a touch of sweetness from reduction.',
        fr: 'Spaghetti classiques avec un ragu de boeuf et de tomate mijote longuement, riche en umami, en herbes et en legere douceur de reduction.'
      },
      keywords: ['Spaghetti Bolognese', 'Pasta', 'Ragu', 'Hauptgericht'],
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
        de: 'Ein Sangiovese-basierter Chianti Classico mit roter Kirsche, Krautern, frischer Saure und mittlerem Tannin - klassischer Pasta-Begleiter.',
        en: 'A Sangiovese-based Chianti Classico with red cherry, herbs, fresh acidity and medium tannins - a classic pasta companion.',
        fr: 'Un Chianti Classico a base de Sangiovese, aux notes de cerise rouge, d\'herbes, a l\'acidite fraiche et aux tanins moyens - un accompagnement classique pour les pates.'
      },
      brand: 'Cantina Esempio',
      reviewBody: {
        de: 'Die Frische und die mittleren Tanine des Chianti bringen Klarheit in die Reichhaltigkeit der Bolognese und halten die Kombination aus Fleisch und Tomate leichtfußig. Rote Kirschfrucht und Krauter greifen die sußliche Tomatensauce und das Ragu aromatisch auf – diese Brucke lasst Wein und Pasta wie ein abgestimmtes Ganzes wirken.',
        en: 'The freshness and medium tannins of the Chianti bring clarity to the richness of the Bolognese and keep the combination of meat and tomato feeling light. Red cherry fruit and herbs pick up the sweet tomato sauce and ragù aromatically – this bridge makes wine and pasta feel like a tuned whole.',
        fr: "La fraicheur et les tanins moyens du Chianti apportent de la clarte a la richesse de la bolognaise et gardent l'ensemble viande-tomate leger. Les notes de cerise rouge et d'herbes reprennent la sauce tomate sucree et le ragù sur le plan aromatique – ce pont donne l'impression d'un ensemble vin-pates parfaitement accorde."
      }
    },
    page: {
      title: {
        de: 'Perfektes Wein-Pairing: Spaghetti Bolognese & Chianti',
        en: 'Perfect Wine Pairing: Spaghetti Bolognese & Chianti',
        fr: 'Accord mets-vin parfait : Spaghetti bolognaise & Chianti'
      },
      description: {
        de: 'Warum ein klassischer Chianti der ideale Partner fur Spaghetti Bolognese ist - mit Fokus auf Saure, Tannin und Umami.',
        en: 'Why a classic Chianti is the ideal partner for spaghetti bolognese - focusing on acidity, tannins and umami.',
        fr: 'Pourquoi un Chianti classique est le partenaire ideal des spaghetti bolognaise - avec un accent sur l\'acidite, les tanins et l\'umami.'
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
        de: 'Dunner Pizzaboden mit fruchtiger Tomatensauce, Mozzarella und frischem Basilikum - schlicht, aber aromatisch und saftig.',
        en: 'Thin pizza base with fruity tomato sauce, mozzarella and fresh basil - simple, yet aromatic and juicy.',
        fr: 'Pate a pizza fine avec sauce tomate fruitee, mozzarella et basilic frais - simple, mais aromatique et juteuse.'
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
        de: 'Ein frischer, fruchtbetonter Chianti mit roter Frucht, Krautern und lebendiger Saure, der Tomate und Kase elegant begleitet.',
        en: 'A fresh, fruit-forward Chianti with red fruit, herbs and lively acidity that elegantly accompanies tomato and cheese.',
        fr: 'Un Chianti frais et fruite, aux notes de fruits rouges, d\'herbes et a l\'acidite vive, qui accompagne elegamment tomate et fromage.'
      },
      brand: 'Casa Collinare',
      reviewBody: {
        de: 'Die lebendige Saure des Chianti bringt Frische in die Reichhaltigkeit von geschmolzenem Mozzarella und Olivenol und halt die Pizza Margherita leicht. Die rote Frucht unterstreicht die sußliche Tomate, wahrend die Krauternoten wie eine Aromabrucke direkt zum frischen Basilikum fuhren.',
        en: 'The lively acidity of the Chianti adds freshness to the richness of melted mozzarella and olive oil, keeping the Margherita pizza light. Red fruit supports the sweet tomato while herbal notes build an aromatic bridge straight to the fresh basil.',
        fr: "L'acidite vive du Chianti apporte de la fraicheur a la richesse de la mozzarella fondue et de l'huile d'olive et garde la pizza Margherita legere. Les fruits rouges soulignent la tomate sucree, tandis que les notes herbacees creent un pont aromatique vers le basilic frais."
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
        de: 'Saftiges Rindfleisch-Patty im Brötchen mit geschmolzenem Kase, Gurken, Zwiebeln und Sauce - herzhaft, leicht sußlich und sehr umami.',
        en: 'Juicy beef patty in a bun with melted cheese, pickles, onions and sauce - hearty, slightly sweet and very umami.',
        fr: 'Steak hache de boeuf juteux dans un bun avec fromage fondu, cornichons, oignons et sauce - gourmand, legerement sucre et tres umami.'
      },
      keywords: ['Burger', 'Cheeseburger', 'Streetfood'],
      category: 'Hauptgericht',
      cuisine: 'American / Streetfood'
    },
    wine: {
      name: {
        de: 'Merlot Reserve',
        en: 'Merlot Reserve',
        fr: 'Merlot Reserve'
      },
      description: {
        de: 'Ein weicher, fruchtbetonter Merlot mit reifer Pflaume, Beeren und sanften Taninen - ideal fur unkomplizierte Fleischgerichte.',
        en: 'A soft, fruit-forward Merlot with ripe plum, berry notes and gentle tannins - ideal for easy-going meat dishes.',
        fr: 'Un Merlot souple et fruite, aux notes de prune mure et de baies, aux tanins doux - ideal pour des plats de viande decontractes.'
      },
      brand: 'Estate Reserve',
      reviewBody: {
        de: 'Die weichen Tanine und die reife Frucht des Merlot nehmen der Reichhaltigkeit von Patty, Kase und Sauce die Schwere und lassen den Cheeseburger saftig, aber nicht mastig wirken. Seine Beerenfrucht greift die leichte Suße des Burgers auf – diese unaufdringliche Brucke macht aus Streetfood und Rotwein ein erstaunlich elegantes Pairing.',
        en: 'The soft tannins and ripe fruit of the Merlot ease the richness of patty, cheese and sauce, keeping the cheeseburger juicy but not heavy. Its berry fruit picks up the burger’s slight sweetness – this unobtrusive bridge turns street food and red wine into a surprisingly elegant pairing.',
        fr: "Les tanins souples et les fruits murs du Merlot adoucissent la richesse du steak, du fromage et de la sauce et laissent le cheeseburger juteux sans le rendre lourd. Ses notes de baies reprennent la legere douceur du burger – ce pont discret transforme le street food et le vin rouge en un accord etonnamment elegant."
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
        fr: 'Pourquoi un Merlot souple et fruite accompagne agreablement le cheeseburger sans le dominer.'
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
        de: 'Gemischte Sushi-Auswahl mit Nigiri und Maki - zarter Fisch, gekochter Reis, etwas Sojasauce und Wasabi.',
        en: 'Mixed sushi selection with nigiri and maki - delicate fish, cooked rice, a touch of soy sauce and wasabi.',
        fr: 'Assortiment de sushi avec nigiri et maki - poisson delicat, riz cuit, un peu de sauce soja et de wasabi.'
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
        de: 'Ein trockener Riesling mit zitrischer Frucht, gruner Apfel und klarer Saure - prazise und mineralisch.',
        en: 'A dry Riesling with citrus fruit, green apple and crisp acidity - precise and mineral.',
        fr: 'Un Riesling sec aux notes d\'agrumes, de pomme verte et a l\'acidite vive - precis et mineral.'
      },
      brand: 'Mosel Selection',
      reviewBody: {
        de: 'Die klare Saure und die Zitrusfrucht des Rieslings bringen Frische in die zarte Reichhaltigkeit von Fisch, Reis und Sojasauce und reinigen den Gaumen zwischen den Bissen. Seine Mineralitat betont die feine Salzigkeit des Meeres – diese Brucke lasst Sushi und Riesling wie eine selbstverstandliche Kombination wirken.',
        en: 'The crisp acidity and citrus fruit of the Riesling add freshness to the gentle richness of fish, rice and soy sauce and cleanse the palate between bites. Its minerality highlights the subtle salinity of the sea – this bridge makes sushi and Riesling feel like a natural combination.',
        fr: "L'acidite vive et les notes d'agrumes du Riesling apportent de la fraicheur a la richesse delicate du poisson, du riz et de la sauce soja et nettoient le palais entre chaque bouchee. Sa mineralite souligne la salinite subtile de la mer – ce pont donne l'impression que sushi et Riesling vont de soi."
      }
    },
    page: {
      title: {
        de: 'Perfektes Wein-Pairing: Sushi Mix & Riesling trocken',
        en: 'Perfect Wine Pairing: Sushi Mix & Dry Riesling',
        fr: 'Accord mets-vin parfait : Assortiment de sushi & Riesling sec'
      },
      description: {
        de: 'Warum ein trockener Riesling die feine Aromatik von Sushi unterstreicht, statt sie zu uberdecken.',
        en: 'Why a dry Riesling enhances the fine aromatics of sushi instead of overpowering them.',
        fr: 'Pourquoi un Riesling sec souligne la finesse aromatique du sushi plutot que de la masquer.'
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
        de: 'Grunes Thai-Curry mit Huhn',
        en: 'Green Thai Curry with Chicken',
        fr: 'Curry vert thai au poulet'
      },
      description: {
        de: 'Cremiges grunes Thai-Curry mit Kokosmilch, Huhn, Gemuse und frischen Krautern - aromatisch, pikant und leicht sußlich.',
        en: 'Creamy green Thai curry with coconut milk, chicken, vegetables and fresh herbs - aromatic, spicy and slightly sweet.',
        fr: 'Curry vert thai cremeux au lait de coco, poulet, legumes et herbes fraiches - aromatique, releve et legerement sucre.'
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
        de: 'Ein halbtrockener Riesling mit saftiger Frucht, prasenter Saure und einem Hauch Restsuße - perfekt zu Scharfe und Kokos.',
        en: 'An off-dry Riesling with juicy fruit, vivid acidity and a touch of residual sweetness - perfect with spice and coconut.',
        fr: 'Un Riesling demi-sec aux fruits juteux, a l\'acidite marquee et a une pointe de sucres residuels - parfait avec les epices et la noix de coco.'
      },
      brand: 'Asia Pairing Selection',
      reviewBody: {
        de: 'Die leichte Restsuße des halbtrockenen Rieslings fangt die Würze und Scharfe des grunen Currys sanft auf, wahrend die präsente Saure die Reichhaltigkeit der Kokosmilch aufbricht. Seine exotische Frucht greift die Kräuter- und Limettennoten der Thai-Kuche auf – diese Brucke halt das Pairing lebendig, ohne den Gaumen zu uberfordern.',
        en: 'The slight residual sweetness of the off-dry Riesling gently cushions the spice and heat of the green curry, while its vivid acidity breaks up the richness of the coconut milk. Its exotic fruit picks up the herb and lime notes of Thai cuisine – this bridge keeps the pairing vibrant without tiring the palate.',
        fr: "La legere sucrosite residuelle du Riesling demi-sec adoucit en douceur le piquant du curry vert, tandis que son acidite marquee casse la richesse du lait de coco. Ses notes de fruits exotiques rejoignent les herbes et le citron vert de la cuisine thailandaise – ce pont maintient l'accord vivant sans fatiguer le palais."
      }
    },
    page: {
      title: {
        de: 'Perfektes Wein-Pairing: Grunes Thai-Curry & Riesling halbtrocken',
        en: 'Perfect Wine Pairing: Green Thai Curry & Off-dry Riesling',
        fr: 'Accord mets-vin parfait : Curry vert thai & Riesling demi-sec'
      },
      description: {
        de: 'Warum ein halbtrockener Riesling die Scharfe und Cremigkeit von grunem Thai-Curry ideal balanciert.',
        en: 'Why an off-dry Riesling ideally balances the heat and creaminess of green Thai curry.',
        fr: 'Pourquoi un Riesling demi-sec equilibre idealement le piquant et l\'onctuosite du curry vert thai.'
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
            <CardTitle className="text-base md:text-lg">Wenn dieser Wein nicht verfugbar ist…</CardTitle>
          </CardHeader>
          <CardContent className="text-sm md:text-base text-muted-foreground space-y-2">
            <p>
              {lang === 'de' && (
                'Kein exakt passender Wein im Regal? Greife zu einem vergleichbaren Stil: gleiche Farbe, ahnlicher Körper und eine ahnlich frische Saure bzw. Tanninstruktur. So bleibt die Balance zwischen Gericht und Glas erhalten.'
              )}
              {lang === 'en' && (
                'If this exact wine is not available, reach for a similar style: same colour, comparable body and a similar level of acidity or tannin. This keeps the balance between dish and glass intact.'
              )}
              {lang === 'fr' && (
                "Si ce vin precis n'est pas disponible, choisissez un style proche : meme couleur, corps comparable et niveau d'acidite ou de tanin similaire. L'equilibre entre le plat et le verre reste ainsi preserve."
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
