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
  },
  // TODO: Add more pairings (Spaghetti Bolognese, Pizza, Burger, Sushi, Thai Curry) here
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
      <div className="container mx-auto max-w-3xl space-y-6">
        <header className="space-y-3">
          <p className="text-accent font-accent text-xs tracking-widest uppercase">Wine Pairing Insight</p>
          <h1 className="text-2xl md:text-3xl font-semibold tracking-tight">
            {tpl.page.title[lang] || tpl.page.title.de}
          </h1>
          <p className="text-sm md:text-base text-muted-foreground">
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
            <CardTitle className="text-base md:text-lg">Warum dieses Pairing funktioniert</CardTitle>
          </CardHeader>
          <CardContent className="text-sm md:text-base text-muted-foreground whitespace-pre-line">
            {tpl.wine.reviewBody[lang] || tpl.wine.reviewBody.de}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default PairingSeoPage;
