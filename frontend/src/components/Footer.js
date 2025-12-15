import React from 'react';
import { Link } from 'react-router-dom';
import { Wine } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';

const Footer = () => {
  const { t, language } = useLanguage();
  const currentYear = new Date().getFullYear();

  const marketingText = {
    de: {
      headline: 'Die smarte Art, Wein zu entdecken',
      description: 'KI-gestützte Weinempfehlungen, virtueller Sommelier-Chat und über 1.700 kuratierte Weine – wine-pairing.online revolutioniert Ihr Weinerlebnis. Perfekte Pairings für jeden Anlass.',
      cta: 'Jetzt Pairing starten'
    },
    en: {
      headline: 'The smart way to discover wine',
      description: 'AI-powered wine recommendations, virtual sommelier chat, and over 1,700 curated wines – wine-pairing.online revolutionizes your wine experience. Perfect pairings for every occasion.',
      cta: 'Start Pairing Now'
    },
    fr: {
      headline: 'La façon intelligente de découvrir le vin',
      description: 'Recommandations de vins par IA, chat sommelier virtuel et plus de 1 700 vins sélectionnés – wine-pairing.online révolutionne votre expérience du vin. Accords parfaits pour chaque occasion.',
      cta: 'Commencer maintenant'
    }
  };

  const text = marketingText[language] || marketingText.de;

  return (
    <footer className="bg-secondary/50 border-t border-border/50" data-testid="footer">
      {/* Marketing Section */}
      <div className="container mx-auto px-4 py-10 md:py-12">
        <div className="max-w-3xl mx-auto text-center">
          <div className="flex justify-center mb-4">
            <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
              <Wine className="w-6 h-6 text-primary" />
            </div>
          </div>
          <h3 className="text-lg md:text-xl font-semibold mb-3">{text.headline}</h3>
          <p className="text-sm md:text-base text-muted-foreground mb-5 leading-relaxed">
            {text.description}
          </p>
          <Link 
            to="/pairing"
            className="inline-flex items-center gap-2 bg-primary text-primary-foreground px-6 py-2.5 rounded-full text-sm font-medium hover:bg-primary/90 transition-colors"
          >
            {text.cta}
          </Link>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-border/30 py-6 pb-24 md:pb-6">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="text-sm text-muted-foreground">
              © {currentYear} MYSYMP AG. {t('footer_rights') || 'Alle Rechte vorbehalten.'}
            </div>
            <nav className="flex items-center gap-4 md:gap-6 flex-wrap justify-center">
              <Link 
                to="/wie-wir-pairen" 
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                {language === 'de' ? 'Wie wir pairen' : language === 'en' ? 'How We Pair' : 'Notre Méthode'}
              </Link>
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
      </div>
    </footer>
  );
};

export default Footer;
