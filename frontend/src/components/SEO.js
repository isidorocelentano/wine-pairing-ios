import React from 'react';
import { Helmet } from 'react-helmet-async';
import { useLanguage } from '@/contexts/LanguageContext';

const defaultMeta = {
  de: {
    siteName: 'wine-pairing.online',
    title: 'Virtueller Sommelier | Wine Pairing App',
    description: 'Entdecken Sie die perfekte Harmonie von Wein und Speise. Unser KI-Sommelier empfiehlt den idealen Wein zu Ihrem Gericht – unabhängig, ehrlich, kostenlos.',
    keywords: 'Wein Pairing, Sommelier, Weinempfehlung, Essen und Wein, Weinkeller, Wein App'
  },
  en: {
    siteName: 'wine-pairing.online',
    title: 'Virtual Sommelier | Wine Pairing App',
    description: 'Discover the perfect harmony of wine and food. Our AI sommelier recommends the ideal wine for your dish – independent, honest, free.',
    keywords: 'Wine Pairing, Sommelier, Wine Recommendation, Food and Wine, Wine Cellar, Wine App'
  },
  fr: {
    siteName: 'wine-pairing.online',
    title: 'Sommelier Virtuel | Application d\'Accord Mets-Vin',
    description: 'Découvrez l\'harmonie parfaite du vin et de la nourriture. Notre sommelier IA recommande le vin idéal pour votre plat – indépendant, honnête, gratuit.',
    keywords: 'Accord Mets-Vin, Sommelier, Recommandation de Vin, Vin et Nourriture, Cave à Vin, Application Vin'
  }
};

export const SEO = ({ 
  title, 
  description, 
  keywords,
  image = 'https://images.unsplash.com/photo-1666475877071-1cc8b7c33f3a?w=1200',
  url,
  type = 'website',
  article = null
}) => {
  const { language } = useLanguage();
  const meta = defaultMeta[language] || defaultMeta.de;
  
  const finalTitle = title ? `${title} | ${meta.siteName}` : meta.title;
  const finalDescription = description || meta.description;
  const finalKeywords = keywords || meta.keywords;
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
      
      {/* Open Graph / Facebook */}
      <meta property="og:type" content={type} />
      <meta property="og:url" content={finalUrl} />
      <meta property="og:title" content={finalTitle} />
      <meta property="og:description" content={finalDescription} />
      <meta property="og:image" content={image} />
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
      <meta name="robots" content="index, follow" />
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
