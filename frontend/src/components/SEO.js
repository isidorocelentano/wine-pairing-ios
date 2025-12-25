import React from 'react';
import { Helmet } from 'react-helmet-async';
import { useLanguage } from '@/contexts/LanguageContext';

/**
 * SEO-Komponente für wine-pairing.online
 * Optimiert für Google, Social Media UND KI-Suchmaschinen (Perplexity, ChatGPT Search, Google SGE)
 * 
 * Haupt-Keywords: Wein-Pairing, Wein zu Essen, welcher Wein passt, Wein-Empfehlung KI
 * Neben-Keywords: Geschmacks-Balance, Wein-Wissen, Sommelier-Beratung online, Wein-Budget
 */

const defaultMeta = {
  de: {
    siteName: 'wine-pairing.online',
    title: 'Wein-Pairing leicht gemacht – Genuss ohne Regeln',
    description: 'Genuss steht an erster Stelle. Entdecke spannende Wein-Kombinationen zu deinem Lieblingsessen. Einfach, intuitiv und direkt online nutzbar.',
    keywords: 'Wein-Pairing, Wein zu Essen, welcher Wein passt, Wein-Empfehlung KI, KI Sommelier, digitaler Sommelier, Wein Pairing App, Online Weinberater, Geschmacks-Balance, Wein-Wissen, Sommelier-Beratung online, Food Pairing Wein',
    abstract: 'wine-pairing.online ist ein KI-gestützter virtueller Sommelier, der passende Weinempfehlungen zu jedem Gericht liefert. Die App analysiert Aromen und Geschmacksprofile für harmonische Wein-Speisen-Kombinationen.'
  },
  en: {
    siteName: 'wine-pairing.online',
    title: 'Wine Pairing Made Easy – Enjoy Without Rules',
    description: 'Enjoyment comes first. Discover exciting wine combinations for your favorite dishes. Simple, intuitive, and available online.',
    keywords: 'Wine Pairing, Wine with Food, which wine goes with, AI Wine Recommendation, AI Sommelier, Digital Sommelier, Wine Pairing App, Online Wine Advisor, Flavor Balance, Wine Knowledge, Sommelier Advice Online, Food Wine Pairing',
    abstract: 'wine-pairing.online is an AI-powered virtual sommelier that provides wine recommendations for any dish. The app analyzes flavors and taste profiles for harmonious wine-food combinations.'
  },
  fr: {
    siteName: 'wine-pairing.online',
    title: 'Accord Mets-Vin Simplifié – Le Plaisir Sans Règles',
    description: 'Le plaisir avant tout. Découvrez des combinaisons de vins passionnantes pour vos plats préférés. Simple, intuitif et disponible en ligne.',
    keywords: 'Accord Mets-Vin, Vin avec Repas, quel vin choisir, Recommandation Vin IA, Sommelier IA, Sommelier Digital, App Accord Vin, Conseiller Vin en Ligne, Équilibre des Saveurs, Connaissance du Vin',
    abstract: 'wine-pairing.online est un sommelier virtuel alimenté par l\'IA qui fournit des recommandations de vins pour chaque plat. L\'application analyse les arômes et profils gustatifs.'
  }
};

// Seitenspezifische SEO-Daten
const pageSEO = {
  pairing: {
    de: {
      title: 'Welcher Wein passt zu deinem Gericht?',
      description: 'Gib dein Gericht ein und erhalte sofort die perfekte Weinempfehlung. KI-gestützt, mit Erklärung warum der Wein harmoniert.',
      keywords: 'Wein-Empfehlung, welcher Wein passt zu, Wein zu Essen finden, KI Weinberatung'
    },
    en: {
      title: 'Which Wine Goes With Your Dish?',
      description: 'Enter your dish and get instant wine recommendations. AI-powered with explanations why the wine harmonizes.',
      keywords: 'Wine recommendation, which wine goes with, find wine for food, AI wine advice'
    }
  },
  cellar: {
    de: {
      title: 'Mein Weinkeller verwalten',
      description: 'Verwalte deinen persönlichen Weinkeller digital. Behalte den Überblick über deine Weine und erhalte Pairing-Vorschläge.',
      keywords: 'Weinkeller App, Wein verwalten, Weinsammlung organisieren, digitaler Weinkeller'
    },
    en: {
      title: 'Manage My Wine Cellar',
      description: 'Manage your personal wine cellar digitally. Keep track of your wines and get pairing suggestions.',
      keywords: 'Wine cellar app, manage wine, organize wine collection, digital wine cellar'
    }
  },
  wineDatabase: {
    de: {
      title: 'Wein-Datenbank – 7.000+ Weine entdecken',
      description: 'Durchsuche unsere umfangreiche Wein-Datenbank mit über 7.000 Weinen aus aller Welt. Filter nach Land, Region und Rebsorte.',
      keywords: 'Wein-Datenbank, Weine entdecken, Weinsuche, Weine nach Region'
    },
    en: {
      title: 'Wine Database – Discover 7,000+ Wines',
      description: 'Browse our extensive wine database with over 7,000 wines from around the world. Filter by country, region, and grape variety.',
      keywords: 'Wine database, discover wines, wine search, wines by region'
    }
  },
  sommelierKompass: {
    de: {
      title: 'Sommelier-Kompass – 1.900+ regionale Pairings',
      description: 'Entdecke traditionelle Wein-Pairings aus 16 Ländern. Von italienischer Pasta bis zu japanischem Sushi – finde den passenden Wein.',
      keywords: 'regionale Wein-Pairings, traditionelle Weinempfehlungen, Wein zu Länderküche'
    },
    en: {
      title: 'Sommelier Compass – 1,900+ Regional Pairings',
      description: 'Discover traditional wine pairings from 16 countries. From Italian pasta to Japanese sushi – find the perfect wine.',
      keywords: 'regional wine pairings, traditional wine recommendations, wine for world cuisine'
    }
  },
  weeklyTip: {
    de: {
      title: 'Wein-Tipp der Woche – Überraschende Pairings',
      description: 'Jede Woche neue, überraschende Wein-Pairings von unserem KI-Sommelier. Lass dich inspirieren!',
      keywords: 'Wein-Tipp, Wein der Woche, Pairing Inspiration, Weinempfehlung aktuell'
    },
    en: {
      title: 'Wine Tip of the Week – Surprising Pairings',
      description: 'New, surprising wine pairings from our AI sommelier every week. Get inspired!',
      keywords: 'Wine tip, wine of the week, pairing inspiration, current wine recommendation'
    }
  }
};

export const SEO = ({ 
  title, 
  description, 
  keywords,
  image = 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=1200&q=80',
  url,
  type = 'website',
  article = null,
  page = null // 'pairing', 'cellar', 'wineDatabase', 'sommelierKompass', 'weeklyTip'
}) => {
  const { language } = useLanguage();
  const meta = defaultMeta[language] || defaultMeta.de;
  
  // Seitenspezifische Meta-Daten verwenden, falls verfügbar
  const pageData = page && pageSEO[page] ? (pageSEO[page][language] || pageSEO[page].de) : null;
  
  const finalTitle = title 
    ? `${title} | ${meta.siteName}` 
    : pageData 
      ? `${pageData.title} | ${meta.siteName}`
      : meta.title;
  
  const finalDescription = description || (pageData?.description) || meta.description;
  const finalKeywords = keywords || (pageData?.keywords) || meta.keywords;
  const finalUrl = url || 'https://wine-pairing.online';

  const structuredData = {
    '@context': 'https://schema.org',
    '@type': type === 'article' ? 'Article' : 'WebSite',
    name: finalTitle,
    description: finalDescription,
    url: finalUrl,
    image: image,
    ...(type === 'article' && article ? {
      headline: article.title,
      author: {
        '@type': 'Person',
        name: article.author
      },
      datePublished: article.datePublished,
      dateModified: article.dateModified
    } : {}),
    publisher: {
      '@type': 'Organization',
      name: 'wine-pairing.online',
      logo: {
        '@type': 'ImageObject',
        url: 'https://wine-pairing.online/logo.png'
      }
    }
  };

  return (
    <Helmet>
      {/* Basic Meta Tags */}
      <html lang={language} />
      <title>{finalTitle}</title>
      <meta name="description" content={finalDescription} />
      <meta name="keywords" content={finalKeywords} />
      <link rel="canonical" href={finalUrl} />
      
      {/* AI Search Engine Optimization */}
      <meta name="abstract" content={meta.abstract} />
      <meta name="ai-content-declaration" content="human-created" />
      
      {/* Open Graph / Facebook */}
      <meta property="og:type" content={type} />
      <meta property="og:url" content={finalUrl} />
      <meta property="og:title" content={finalTitle} />
      <meta property="og:description" content={finalDescription} />
      <meta property="og:image" content={image} />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />
      <meta property="og:locale" content={language === 'de' ? 'de_DE' : language === 'fr' ? 'fr_FR' : 'en_US'} />
      <meta property="og:site_name" content={meta.siteName} />
      
      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:url" content={finalUrl} />
      <meta name="twitter:title" content={finalTitle} />
      <meta name="twitter:description" content={finalDescription} />
      <meta name="twitter:image" content={image} />
      
      {/* Structured Data */}
      <script type="application/ld+json">
        {JSON.stringify(structuredData)}
      </script>
      
      {/* Additional SEO */}
      <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
      <meta name="googlebot" content="index, follow" />
      <meta name="theme-color" content="#722F37" />
      <link rel="alternate" hrefLang="de" href="https://wine-pairing.online" />
      <link rel="alternate" hrefLang="en" href="https://wine-pairing.online" />
      <link rel="alternate" hrefLang="fr" href="https://wine-pairing.online" />
      <link rel="alternate" hrefLang="x-default" href="https://wine-pairing.online" />
    </Helmet>
  );
};

export default SEO;
