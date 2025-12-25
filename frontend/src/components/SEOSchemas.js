import React from 'react';
import { Helmet } from 'react-helmet-async';

/**
 * SEO Schema.org Komponenten für wine-pairing.online
 * Optimiert für Google Rich Results und KI-Auffindbarkeit
 */

// Organization Schema für MYSYMP AG
export const OrganizationSchema = () => {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "MYSYMP AG",
    "url": "https://mysymp.ch",
    "logo": "https://wine-pairing.online/logo.png",
    "contactPoint": {
      "@type": "ContactPoint",
      "telephone": "+41-79-471-06-25",
      "contactType": "customer service",
      "email": "info@mysymp.ch",
      "areaServed": ["CH", "DE", "AT"],
      "availableLanguage": ["German", "English", "French"]
    },
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Studenstrasse 14B",
      "addressLocality": "Nottwil",
      "postalCode": "6207",
      "addressCountry": "CH"
    },
    "sameAs": [
      "https://mysymp.ch"
    ]
  };

  return (
    <Helmet>
      <script type="application/ld+json">
        {JSON.stringify(schema)}
      </script>
    </Helmet>
  );
};

// WebSite Schema für Suchfunktion
export const WebSiteSchema = () => {
  const schema = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "wine-pairing.online",
    "alternateName": ["Wein-Pairing App", "KI Sommelier", "Digitaler Weinberater", "Online Sommelier-Beratung"],
    "url": "https://wine-pairing.online",
    "description": "Genuss steht an erster Stelle. Entdecke spannende Wein-Kombinationen zu deinem Lieblingsessen. KI-gestützte Weinempfehlungen – einfach, intuitiv und kostenlos. Über 7.000 Weine, 1.900+ regionale Pairings.",
    "inLanguage": ["de", "en", "fr"],
    "potentialAction": {
      "@type": "SearchAction",
      "target": {
        "@type": "EntryPoint",
        "urlTemplate": "https://wine-pairing.online/blog?search={search_term_string}"
      },
      "query-input": "required name=search_term_string"
    },
    "publisher": {
      "@type": "Organization",
      "name": "MYSYMP AG"
    }
  };

  return (
    <Helmet>
      <script type="application/ld+json">
        {JSON.stringify(schema)}
      </script>
    </Helmet>
  );
};

// Article Schema für Blog-Posts
export const ArticleSchema = ({ article, language = 'de' }) => {
  if (!article) return null;

  const title = language === 'en' ? article.title_en : 
                language === 'fr' ? article.title_fr : article.title;
  
  const content = language === 'en' ? article.content_en : 
                  language === 'fr' ? article.content_fr : article.content;

  const schema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": title,
    "description": article.excerpt || content?.substring(0, 160),
    "image": article.image_url || "https://wine-pairing.online/wine-default.jpg",
    "author": {
      "@type": "Organization",
      "name": "MYSYMP AG",
      "url": "https://mysymp.ch"
    },
    "publisher": {
      "@type": "Organization",
      "name": "MYSYMP AG",
      "logo": {
        "@type": "ImageObject",
        "url": "https://wine-pairing.online/logo.png"
      }
    },
    "datePublished": article.created_at,
    "dateModified": article.updated_at || article.created_at,
    "mainEntityOfPage": {
      "@type": "WebPage",
      "@id": `https://wine-pairing.online/blog/${article.slug}`
    },
    "articleSection": article.category,
    "keywords": article.tags?.join(", ") || "Wein, Wine, Vin"
  };

  return (
    <Helmet>
      <script type="application/ld+json">
        {JSON.stringify(schema)}
      </script>
    </Helmet>
  );
};

// FAQ Schema für Blog-Artikel mit FAQs
export const FAQSchema = ({ faqs }) => {
  if (!faqs || faqs.length === 0) return null;

  const schema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": faqs.map(faq => ({
      "@type": "Question",
      "name": faq.question,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": faq.answer
      }
    }))
  };

  return (
    <Helmet>
      <script type="application/ld+json">
        {JSON.stringify(schema)}
      </script>
    </Helmet>
  );
};

// Product Schema für Weine
export const WineProductSchema = ({ wine }) => {
  if (!wine) return null;

  const schema = {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": wine.name || wine.wine_name,
    "description": wine.description || wine.description_de,
    "image": wine.image_url,
    "brand": {
      "@type": "Brand",
      "name": wine.winery || wine.producer
    },
    "category": wine.wine_type || wine.wine_color,
    "countryOfOrigin": {
      "@type": "Country",
      "name": wine.country
    },
    "additionalProperty": [
      {
        "@type": "PropertyValue",
        "name": "Region",
        "value": wine.region
      },
      {
        "@type": "PropertyValue",
        "name": "Rebsorte",
        "value": wine.grape_variety || wine.grape
      }
    ]
  };

  return (
    <Helmet>
      <script type="application/ld+json">
        {JSON.stringify(schema)}
      </script>
    </Helmet>
  );
};

// BreadcrumbList Schema
export const BreadcrumbSchema = ({ items }) => {
  if (!items || items.length === 0) return null;

  const schema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": items.map((item, index) => ({
      "@type": "ListItem",
      "position": index + 1,
      "name": item.name,
      "item": item.url
    }))
  };

  return (
    <Helmet>
      <script type="application/ld+json">
        {JSON.stringify(schema)}
      </script>
    </Helmet>
  );
};

// Recipe Schema für Food Pairings
export const FoodPairingSchema = ({ dish, wines, region }) => {
  if (!dish) return null;

  const schema = {
    "@context": "https://schema.org",
    "@type": "Recipe",
    "name": dish,
    "description": `Perfekte Weinempfehlungen für ${dish}`,
    "recipeCategory": "Food & Wine Pairing",
    "recipeCuisine": region || "International",
    "keywords": `${dish}, Weinpairing, Wine Pairing, Sommelier`,
    "author": {
      "@type": "Organization",
      "name": "wine-pairing.online"
    },
    "nutrition": {
      "@type": "NutritionInformation",
      "description": "Weinempfehlung"
    }
  };

  return (
    <Helmet>
      <script type="application/ld+json">
        {JSON.stringify(schema)}
      </script>
    </Helmet>
  );
};

// LocalBusiness Schema für Sommelier-Service
export const SommelierServiceSchema = () => {
  const schema = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "name": "wine-pairing.online - Virtueller Sommelier",
    "description": "KI-gestützter Sommelier-Service für perfekte Weinempfehlungen. Über 1.700 kuratierte Weine, 84 Weinregionen und personalisierte Pairings.",
    "url": "https://wine-pairing.online",
    "serviceType": "Wine Consulting",
    "areaServed": {
      "@type": "GeoCircle",
      "geoMidpoint": {
        "@type": "GeoCoordinates",
        "latitude": 47.0502,
        "longitude": 8.3093
      },
      "geoRadius": "5000"
    },
    "hasOfferCatalog": {
      "@type": "OfferCatalog",
      "name": "Sommelier Services",
      "itemListElement": [
        {
          "@type": "Offer",
          "itemOffered": {
            "@type": "Service",
            "name": "KI Wine Pairing",
            "description": "Automatische Weinempfehlungen basierend auf Ihrem Gericht"
          }
        },
        {
          "@type": "Offer",
          "itemOffered": {
            "@type": "Service",
            "name": "Sommelier Chat",
            "description": "Persönliche Beratung durch unseren KI-Sommelier"
          }
        },
        {
          "@type": "Offer",
          "itemOffered": {
            "@type": "Service",
            "name": "Weindatenbank",
            "description": "Zugang zu über 1.700 kuratierten Weinen"
          }
        }
      ]
    },
    "provider": {
      "@type": "Organization",
      "name": "MYSYMP AG"
    }
  };

  return (
    <Helmet>
      <script type="application/ld+json">
        {JSON.stringify(schema)}
      </script>
    </Helmet>
  );
};

export default {
  OrganizationSchema,
  WebSiteSchema,
  ArticleSchema,
  FAQSchema,
  WineProductSchema,
  BreadcrumbSchema,
  FoodPairingSchema,
  SommelierServiceSchema
};
