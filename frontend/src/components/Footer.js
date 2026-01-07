import React from 'react';
import { Link } from 'react-router-dom';
import { Wine, Facebook, Linkedin, Twitter } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';

// TikTok Icon (custom SVG)
const TikTokIcon = ({ size = 18, className = '' }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" className={className}>
    <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64 2.93 2.93 0 01.88.13V9.4a6.84 6.84 0 00-1-.05A6.33 6.33 0 005 20.1a6.34 6.34 0 0010.86-4.43v-7a8.16 8.16 0 004.77 1.52v-3.4a4.85 4.85 0 01-1-.1z"/>
  </svg>
);

// Instagram Icon
const InstagramIcon = ({ size = 18, className = '' }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
    <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
    <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
  </svg>
);

const Footer = () => {
  const { t, language } = useLanguage();
  const currentYear = new Date().getFullYear();

  // Social Media Links - UPDATE THESE WITH YOUR ACTUAL PROFILES
  const socialLinks = [
    { name: 'Instagram', icon: InstagramIcon, url: 'https://www.instagram.com/wine_pairing_online', color: 'hover:text-pink-500' },
    { name: 'Facebook', icon: Facebook, url: 'https://www.facebook.com/winepairing.online', color: 'hover:text-blue-600' },
    { name: 'LinkedIn', icon: Linkedin, url: 'https://www.linkedin.com/company/wine-pairing', color: 'hover:text-blue-700' },
    { name: 'TikTok', icon: TikTokIcon, url: 'https://www.tiktok.com/@wine_pairing_online', color: 'hover:text-foreground' },
    { name: 'X', icon: Twitter, url: 'https://twitter.com/winepairing_app', color: 'hover:text-sky-500' },
  ];

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
          
          {/* Social Media Icons */}
          <div className="mt-6 flex items-center justify-center gap-4">
            <span className="text-xs text-muted-foreground mr-2">
              {language === 'de' ? 'Folge uns:' : language === 'en' ? 'Follow us:' : 'Suivez-nous:'}
            </span>
            {socialLinks.map((social) => (
              <a
                key={social.name}
                href={social.url}
                target="_blank"
                rel="noopener noreferrer"
                className={`text-muted-foreground ${social.color} transition-colors`}
                title={social.name}
              >
                <social.icon size={20} />
              </a>
            ))}
          </div>
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
