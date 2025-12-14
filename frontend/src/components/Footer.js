import React from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '@/contexts/LanguageContext';

const Footer = () => {
  const { t } = useLanguage();
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-secondary/50 border-t border-border/50 py-8 pb-24 md:pb-8" data-testid="footer">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-sm text-muted-foreground">
            © {currentYear} MYSYMP AG. {t('footer_rights') || 'Alle Rechte vorbehalten.'}
          </div>
          <nav className="flex items-center gap-6">
            <Link 
              to="/kontakt" 
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              data-testid="footer-kontakt"
            >
              {t('footer_kontakt') || 'Kontakt'}
            </Link>
            <Link 
              to="/datenschutz" 
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              data-testid="footer-datenschutz"
            >
              {t('footer_datenschutz') || 'Datenschutz'}
            </Link>
            <Link 
              to="/impressum" 
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              data-testid="footer-impressum"
            >
              {t('footer_impressum') || 'Impressum'}
            </Link>
          </nav>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
