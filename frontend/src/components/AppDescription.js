import React from 'react';
import { Wine, Utensils, MessageCircle, Database, Grape, BookOpen, Heart, Sparkles } from 'lucide-react';
import { useLanguage } from '@/contexts/LanguageContext';

const AppDescription = () => {
  const { language } = useLanguage();

  const content = {
    de: {
      tagline: 'Ihre digitale Weinwelt',
      title: 'Entdecken Sie wine-pairing.online',
      subtitle: 'Die intelligente Plattform für perfekte Weinmomente',
      intro: 'wine-pairing.online vereint modernste KI-Technologie mit jahrhundertealtem Weinwissen. Unsere Plattform wurde entwickelt, um jeden Weinliebhaber – vom Einsteiger bis zum Kenner – bei der Entdeckung der perfekten Weine zu unterstützen.',
      features: [
        {
          icon: Utensils,
          title: 'KI-Weinpairing',
          description: 'Geben Sie Ihr Gericht ein und erhalten Sie sofort massgeschneiderte Weinempfehlungen. Unsere KI analysiert Aromen, Texturen und regionale Traditionen für das perfekte Zusammenspiel.'
        },
        {
          icon: MessageCircle,
          title: 'Virtueller Sommelier',
          description: 'Chatten Sie mit Claude, Ihrem persönlichen KI-Sommelier. Stellen Sie Fragen zu Weinen, Regionen, Jahrgängen oder lassen Sie sich individuell beraten – rund um die Uhr verfügbar.'
        },
        {
          icon: Database,
          title: 'Umfangreiche Weindatenbank',
          description: 'Entdecken Sie über 1.700 sorgfältig kuratierte Weine aus aller Welt. Filtern Sie nach Region, Rebsorte, Geschmacksprofil und finden Sie Ihren neuen Lieblingswein.'
        },
        {
          icon: Grape,
          title: 'Rebsorten-Lexikon',
          description: 'Vertiefen Sie Ihr Wissen über Rebsorten. Von Riesling bis Nebbiolo – erfahren Sie alles über Charakteristiken, Anbaugebiete und ideale Speisebegleiter.'
        },
        {
          icon: Wine,
          title: 'Mein Weinkeller',
          description: 'Verwalten Sie Ihre persönliche Weinsammlung digital. Behalten Sie den Überblick über Ihre Bestände, Trinkreife und Notizen zu jedem Wein.'
        },
        {
          icon: Heart,
          title: 'Favoriten & Community',
          description: 'Speichern Sie Ihre Lieblingsweine und teilen Sie Entdeckungen mit der Community. Lassen Sie sich von den Empfehlungen anderer Weinliebhaber inspirieren.'
        },
        {
          icon: BookOpen,
          title: 'Wein-Blog',
          description: 'Tauchen Sie ein in über 230 Fachartikel zu Weinregionen, Weingütern und Weinkultur. Dreisprachig verfügbar – Deutsch, Englisch und Französisch.'
        },
        {
          icon: Sparkles,
          title: 'Ständig wachsend',
          description: 'Unsere Datenbank wächst organisch durch KI-generierte Empfehlungen. Jede Pairing-Anfrage kann neue, einzigartige Weine in unser System bringen.'
        }
      ],
      closing: 'wine-pairing.online ist Ihr vertrauenswürdiger Begleiter auf der Reise durch die faszinierende Welt des Weins. Kostenlos, werbefrei und mit Leidenschaft für Qualität entwickelt.',
      cta: 'Ein Projekt von MYSYMP AG – Your Partner for Lifestyle'
    },
    en: {
      tagline: 'Your Digital Wine World',
      title: 'Discover wine-pairing.online',
      subtitle: 'The intelligent platform for perfect wine moments',
      intro: 'wine-pairing.online combines cutting-edge AI technology with centuries of wine expertise. Our platform was designed to help every wine enthusiast – from beginners to connoisseurs – discover the perfect wines.',
      features: [
        {
          icon: Utensils,
          title: 'AI Wine Pairing',
          description: 'Enter your dish and instantly receive tailored wine recommendations. Our AI analyzes flavors, textures, and regional traditions for the perfect match.'
        },
        {
          icon: MessageCircle,
          title: 'Virtual Sommelier',
          description: 'Chat with Claude, your personal AI sommelier. Ask questions about wines, regions, vintages, or get personalized advice – available 24/7.'
        },
        {
          icon: Database,
          title: 'Extensive Wine Database',
          description: 'Explore over 1,700 carefully curated wines from around the world. Filter by region, grape variety, flavor profile and find your new favorite wine.'
        },
        {
          icon: Grape,
          title: 'Grape Variety Encyclopedia',
          description: 'Deepen your knowledge of grape varieties. From Riesling to Nebbiolo – learn everything about characteristics, growing regions, and ideal food pairings.'
        },
        {
          icon: Wine,
          title: 'My Wine Cellar',
          description: 'Manage your personal wine collection digitally. Keep track of your inventory, drinking windows, and notes for each wine.'
        },
        {
          icon: Heart,
          title: 'Favorites & Community',
          description: 'Save your favorite wines and share discoveries with the community. Get inspired by recommendations from other wine lovers.'
        },
        {
          icon: BookOpen,
          title: 'Wine Blog',
          description: 'Dive into over 230 expert articles on wine regions, wineries, and wine culture. Available in three languages – German, English, and French.'
        },
        {
          icon: Sparkles,
          title: 'Constantly Growing',
          description: 'Our database grows organically through AI-generated recommendations. Every pairing request can bring new, unique wines into our system.'
        }
      ],
      closing: 'wine-pairing.online is your trusted companion on your journey through the fascinating world of wine. Free, ad-free, and developed with a passion for quality.',
      cta: 'A project by MYSYMP AG – Your Partner for Lifestyle'
    },
    fr: {
      tagline: 'Votre Univers Vinicole Digital',
      title: 'Découvrez wine-pairing.online',
      subtitle: 'La plateforme intelligente pour des moments de vin parfaits',
      intro: 'wine-pairing.online combine la technologie IA de pointe avec des siècles de savoir-faire vinicole. Notre plateforme a été conçue pour aider chaque amateur de vin – du débutant au connaisseur – à découvrir les vins parfaits.',
      features: [
        {
          icon: Utensils,
          title: 'Accord Mets-Vins IA',
          description: 'Entrez votre plat et recevez instantanément des recommandations de vins sur mesure. Notre IA analyse les saveurs, textures et traditions régionales pour un accord parfait.'
        },
        {
          icon: MessageCircle,
          title: 'Sommelier Virtuel',
          description: 'Discutez avec Claude, votre sommelier IA personnel. Posez des questions sur les vins, régions, millésimes ou obtenez des conseils personnalisés – disponible 24h/24.'
        },
        {
          icon: Database,
          title: 'Base de Données Extensive',
          description: 'Explorez plus de 1 700 vins soigneusement sélectionnés du monde entier. Filtrez par région, cépage, profil gustatif et trouvez votre nouveau vin préféré.'
        },
        {
          icon: Grape,
          title: 'Encyclopédie des Cépages',
          description: 'Approfondissez vos connaissances sur les cépages. Du Riesling au Nebbiolo – découvrez tout sur les caractéristiques, régions de culture et accords mets idéaux.'
        },
        {
          icon: Wine,
          title: 'Ma Cave',
          description: 'Gérez votre collection de vins personnelle numériquement. Gardez une trace de vos stocks, fenêtres de dégustation et notes pour chaque vin.'
        },
        {
          icon: Heart,
          title: 'Favoris & Communauté',
          description: 'Sauvegardez vos vins préférés et partagez vos découvertes avec la communauté. Inspirez-vous des recommandations d\'autres amateurs de vin.'
        },
        {
          icon: BookOpen,
          title: 'Blog Vin',
          description: 'Plongez dans plus de 230 articles experts sur les régions viticoles, domaines et culture du vin. Disponible en trois langues – allemand, anglais et français.'
        },
        {
          icon: Sparkles,
          title: 'En Croissance Constante',
          description: 'Notre base de données s\'enrichit organiquement grâce aux recommandations générées par IA. Chaque demande d\'accord peut apporter de nouveaux vins uniques.'
        }
      ],
      closing: 'wine-pairing.online est votre compagnon de confiance dans votre voyage à travers le monde fascinant du vin. Gratuit, sans publicité et développé avec passion pour la qualité.',
      cta: 'Un projet de MYSYMP AG – Your Partner for Lifestyle'
    }
  };

  const c = content[language] || content.de;

  return (
    <section className="py-16 md:py-24 px-4 md:px-12 lg:px-24 bg-gradient-to-b from-background to-secondary/20" data-testid="app-description">
      <div className="container mx-auto">
        <div className="max-w-4xl mx-auto text-center mb-12 md:mb-16">
          <p className="text-accent font-accent text-sm tracking-widest uppercase mb-4">{c.tagline}</p>
          <h2 className="text-2xl md:text-4xl font-semibold tracking-tight mb-4">{c.title}</h2>
          <p className="text-lg md:text-xl text-muted-foreground">{c.subtitle}</p>
        </div>

        <div className="max-w-3xl mx-auto mb-12">
          <p className="text-muted-foreground text-center leading-relaxed">{c.intro}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {c.features.map((feature, idx) => (
            <div 
              key={idx} 
              className="bg-card/50 backdrop-blur-sm border border-border/50 rounded-xl p-6 hover:border-primary/30 transition-all duration-300"
            >
              <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                <feature.icon className="w-6 h-6 text-primary" strokeWidth={1.5} />
              </div>
              <h3 className="font-semibold mb-2">{feature.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>

        <div className="max-w-2xl mx-auto text-center">
          <p className="text-muted-foreground leading-relaxed mb-4">{c.closing}</p>
          <p className="text-sm text-accent font-accent tracking-wide">{c.cta}</p>
        </div>
      </div>
    </section>
  );
};

export default AppDescription;
