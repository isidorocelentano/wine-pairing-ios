import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ChevronRight, Home } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';
import { BreadcrumbSchema } from './SEOSchemas';

/**
 * Breadcrumb Navigation für bessere UX und SEO
 */
const Breadcrumb = ({ items, className = '' }) => {
  const location = useLocation();
  const { t } = useLanguage();

  // Automatische Breadcrumb-Generierung basierend auf URL
  const generateBreadcrumbs = () => {
    if (items) return items;

    const pathnames = location.pathname.split('/').filter(x => x);
    
    const pathLabels = {
      'pairing': t('nav_pairing') || 'Wine Pairing',
      'wine-database': t('nav_wine_database') || 'Weindatenbank',
      'grapes': t('nav_grapes') || 'Rebsorten',
      'blog': 'Blog',
      'sommelier-kompass': t('regional_nav') || 'Sommelier Kompass',
      'favorites': t('nav_favorites') || 'Favoriten',
      'cellar': t('nav_cellar') || 'Weinkeller',
      'feed': t('nav_feed') || 'Community',
      'chat': t('nav_sommelier') || 'Sommelier',
      'kontakt': 'Kontakt',
      'impressum': 'Impressum',
      'datenschutz': 'Datenschutz'
    };

    const breadcrumbs = [
      { name: 'Home', url: 'https://wine-pairing.online/' }
    ];

    let currentPath = '';
    pathnames.forEach((pathname, index) => {
      currentPath += `/${pathname}`;
      const isLast = index === pathnames.length - 1;
      
      breadcrumbs.push({
        name: pathLabels[pathname] || pathname.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        url: `https://wine-pairing.online${currentPath}`,
        isLast
      });
    });

    return breadcrumbs;
  };

  const breadcrumbs = generateBreadcrumbs();

  if (breadcrumbs.length <= 1) return null;

  return (
    <>
      <BreadcrumbSchema items={breadcrumbs} />
      <nav 
        aria-label="Breadcrumb" 
        className={`flex items-center text-sm text-muted-foreground mb-4 ${className}`}
      >
        <ol className="flex items-center flex-wrap gap-1" itemScope itemType="https://schema.org/BreadcrumbList">
          {breadcrumbs.map((crumb, index) => (
            <li 
              key={index} 
              className="flex items-center"
              itemScope 
              itemType="https://schema.org/ListItem" 
              itemProp="itemListElement"
            >
              {index > 0 && (
                <ChevronRight className="h-4 w-4 mx-1 text-muted-foreground/50" />
              )}
              {index === 0 ? (
                <Link 
                  to="/" 
                  className="hover:text-foreground transition-colors flex items-center"
                  itemProp="item"
                >
                  <Home className="h-4 w-4" />
                  <span className="sr-only" itemProp="name">{crumb.name}</span>
                </Link>
              ) : crumb.isLast ? (
                <span 
                  className="text-foreground font-medium"
                  itemProp="name"
                >
                  {crumb.name}
                </span>
              ) : (
                <Link 
                  to={crumb.url.replace('https://wine-pairing.online', '')} 
                  className="hover:text-foreground transition-colors"
                  itemProp="item"
                >
                  <span itemProp="name">{crumb.name}</span>
                </Link>
              )}
              <meta itemProp="position" content={String(index + 1)} />
            </li>
          ))}
        </ol>
      </nav>
    </>
  );
};

export default Breadcrumb;
