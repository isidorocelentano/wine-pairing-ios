import React from 'react';
import { useNavigate } from "react-router-dom";
import { Wine, Utensils, Camera, MessageCircle, BookOpen, Users, Database, Heart, Map, Beaker, Crown, Sparkles, ArrowRight, Check, Infinity } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";
import { useAuth } from "@/contexts/AuthContext";
import AppDescription from "@/components/AppDescription";
import Footer from "@/components/Footer";

const HomePage = () => {
  const navigate = useNavigate();
  const { t, language } = useLanguage();
  const { user } = useAuth();

  // Pricing translations
  const pricingT = {
    de: {
      tagline: 'DEIN SOMMELIER. IMMER DABEI.',
      title: 'Entdecke die volle Welt des Weins',
      subtitle: 'Starte kostenlos – upgrade für unbegrenzte Möglichkeiten',
      free: 'Basic',
      free_desc: 'Kostenlos für immer',
      pro: 'Pro',
      pro_price: '€4.99/Monat',
      features_free: ['5 Pairings/Tag', '5 Chat-Nachrichten/Tag', 'Max. 10 Weine im Keller'],
      features_pro: ['Unbegrenzte Pairings', 'Unbegrenzter Chat', 'Unbegrenzter Weinkeller'],
      cta_free: 'Jetzt starten',
      cta_pro: 'Pro werden',
      see_all: 'Alle Vorteile ansehen'
    },
    en: {
      tagline: 'YOUR SOMMELIER. ALWAYS WITH YOU.',
      title: 'Discover the full world of wine',
      subtitle: 'Start for free – upgrade for unlimited possibilities',
      free: 'Basic',
      free_desc: 'Free forever',
      pro: 'Pro',
      pro_price: '€4.99/month',
      features_free: ['5 pairings/day', '5 chat messages/day', 'Max. 10 wines in cellar'],
      features_pro: ['Unlimited pairings', 'Unlimited chat', 'Unlimited wine cellar'],
      cta_free: 'Get Started',
      cta_pro: 'Go Pro',
      see_all: 'See all benefits'
    },
    fr: {
      tagline: 'VOTRE SOMMELIER. TOUJOURS AVEC VOUS.',
      title: 'Découvrez le monde complet du vin',
      subtitle: 'Commencez gratuitement – passez Pro pour des possibilités illimitées',
      free: 'Basic',
      free_desc: 'Gratuit pour toujours',
      pro: 'Pro',
      pro_price: '€4.99/mois',
      features_free: ['5 accords/jour', '5 messages chat/jour', 'Max. 10 vins en cave'],
      features_pro: ['Accords illimités', 'Chat illimité', 'Cave à vin illimitée'],
      cta_free: 'Commencer',
      cta_pro: 'Passer Pro',
      see_all: 'Voir tous les avantages'
    }
  }[language] || {};

  const isPro = user?.plan === 'pro' || user?.plan === 'pro_monthly' || user?.plan === 'pro_yearly';

  return (
    <div className="min-h-screen pb-20 md:pb-24" data-testid="home-page">
      {/* NEW: Genuss-First Hero Section */}
      <section className="relative min-h-[90vh] flex items-center overflow-hidden">
        {/* Background Image */}
        <div className="absolute inset-0 z-0">
          <img
            src="https://images.unsplash.com/photo-1666475877071-1cc8b7c33f3a?crop=entropy&cs=srgb&fm=jpg&q=85&w=1920"
            alt="Wine Pour"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-background via-background/95 to-background/60" />
        </div>
        
        <div className="relative z-10 container mx-auto px-4 md:px-12 lg:px-24 py-12">
          <div className="max-w-3xl space-y-8 md:space-y-10">
            
            {/* 1. Headline - Die emotionale Botschaft */}
            <div className="space-y-4 opacity-0 animate-fade-in-up" style={{ animationDelay: '0.1s', animationFillMode: 'forwards' }}>
              <p className="text-accent font-accent text-sm md:text-base tracking-widest uppercase">
                {language === 'de' ? 'WEIN-PAIRING NEU GEDACHT' : 
                 language === 'en' ? 'WINE PAIRING REIMAGINED' : 
                 'L\'ACCORD METS-VINS RÉINVENTÉ'}
              </p>
              <h1 className="text-3xl md:text-5xl lg:text-6xl font-semibold leading-tight tracking-tight">
                {language === 'de' ? (
                  <>Dein Wein. Dein Essen.<br /><span className="text-primary">Dein Moment.</span></>
                ) : language === 'en' ? (
                  <>Your Wine. Your Food.<br /><span className="text-primary">Your Moment.</span></>
                ) : (
                  <>Votre Vin. Votre Repas.<br /><span className="text-primary">Votre Moment.</span></>
                )}
              </h1>
              <p className="text-lg md:text-xl text-muted-foreground leading-relaxed max-w-2xl">
                {language === 'de' ? 'Wissenschaftlich fundierte Empfehlungen – ganz ohne Dogmen.' : 
                 language === 'en' ? 'Scientifically founded recommendations – without dogma.' : 
                 'Des recommandations scientifiques – sans dogmes.'}
              </p>
            </div>

            {/* 2. Die Philosophie - 4 Punkte mit Icons */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 opacity-0 animate-fade-in-up" style={{ animationDelay: '0.3s', animationFillMode: 'forwards' }}>
              {/* Kein Richtig oder Falsch */}
              <div className="flex items-start gap-3 p-4 rounded-xl bg-card/40 backdrop-blur-sm border border-border/30 hover:bg-card/60 transition-colors">
                <span className="text-2xl">✨</span>
                <div>
                  <h3 className="font-semibold text-sm mb-1">
                    {language === 'de' ? 'Kein Richtig oder Falsch' : 
                     language === 'en' ? 'No Right or Wrong' : 
                     'Pas de bon ou mauvais'}
                  </h3>
                  <p className="text-xs text-muted-foreground">
                    {language === 'de' ? 'Beim Wein-Pairing geht es nur um eines: Deinen Genuss.' : 
                     language === 'en' ? 'Wine pairing is about one thing only: Your enjoyment.' : 
                     'L\'accord mets-vins ne vise qu\'une chose : votre plaisir.'}
                  </p>
                </div>
              </div>
              
              {/* Dein Geschmack weist den Weg */}
              <div className="flex items-start gap-3 p-4 rounded-xl bg-card/40 backdrop-blur-sm border border-border/30 hover:bg-card/60 transition-colors">
                <span className="text-2xl">👅</span>
                <div>
                  <h3 className="font-semibold text-sm mb-1">
                    {language === 'de' ? 'Dein Geschmack weist den Weg' : 
                     language === 'en' ? 'Your Taste Leads the Way' : 
                     'Votre goût vous guide'}
                  </h3>
                  <p className="text-xs text-muted-foreground">
                    {language === 'de' ? 'Unsere Vorschläge sind Inspirationen, dein Gaumen ist der Chef.' : 
                     language === 'en' ? 'Our suggestions are inspiration, your palate is the boss.' : 
                     'Nos suggestions sont des inspirations, votre palais décide.'}
                  </p>
                </div>
              </div>
              
              {/* Einfach ausprobieren */}
              <div className="flex items-start gap-3 p-4 rounded-xl bg-card/40 backdrop-blur-sm border border-border/30 hover:bg-card/60 transition-colors">
                <span className="text-2xl">🍞</span>
                <div>
                  <h3 className="font-semibold text-sm mb-1">
                    {language === 'de' ? 'Einfach ausprobieren' : 
                     language === 'en' ? 'Just Try It' : 
                     'Essayez simplement'}
                  </h3>
                  <p className="text-xs text-muted-foreground">
                    {language === 'de' ? 'Neutralisiere kurz mit Wasser oder Brot und weiter geht\'s.' : 
                     language === 'en' ? 'Neutralize briefly with water or bread and continue.' : 
                     'Neutralisez avec de l\'eau ou du pain et continuez.'}
                  </p>
                </div>
              </div>
              
              {/* Hab einfach Spaß */}
              <div className="flex items-start gap-3 p-4 rounded-xl bg-card/40 backdrop-blur-sm border border-border/30 hover:bg-card/60 transition-colors">
                <span className="text-2xl">🎉</span>
                <div>
                  <h3 className="font-semibold text-sm mb-1">
                    {language === 'de' ? 'Hab einfach Spaß' : 
                     language === 'en' ? 'Just Have Fun' : 
                     'Amusez-vous'}
                  </h3>
                  <p className="text-xs text-muted-foreground">
                    {language === 'de' ? 'Entdecke neue Welten, ganz ohne Stress.' : 
                     language === 'en' ? 'Discover new worlds, completely stress-free.' : 
                     'Découvrez de nouveaux mondes, sans stress.'}
                  </p>
                </div>
              </div>
            </div>

            {/* 3. Call-to-Action */}
            <div className="space-y-4 opacity-0 animate-fade-in-up" style={{ animationDelay: '0.5s', animationFillMode: 'forwards' }}>
              <Button
                onClick={() => navigate('/pairing')}
                size="lg"
                className="rounded-full px-8 py-6 text-base font-semibold tracking-wide bg-primary hover:bg-primary/90 transition-all hover:scale-105 active:scale-95 shadow-lg shadow-primary/25"
                data-testid="cta-pairing-hero"
              >
                <Wine className="mr-2 h-5 w-5" />
                {language === 'de' ? '🍷 Jetzt mein perfektes Pairing finden' : 
                 language === 'en' ? '🍷 Find My Perfect Pairing Now' : 
                 '🍷 Trouver mon accord parfait'}
              </Button>
              <p className="text-sm text-muted-foreground">
                {language === 'de' ? 'Kostenlos testen – ohne Registrierung' : 
                 language === 'en' ? 'Try for free – no registration required' : 
                 'Essai gratuit – sans inscription'}
              </p>
            </div>

            {/* 4. Vertrauens-Element */}
            <div className="flex items-center gap-3 pt-4 opacity-0 animate-fade-in-up" style={{ animationDelay: '0.7s', animationFillMode: 'forwards' }}>
              <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-card/60 backdrop-blur-sm border border-border/30">
                <Sparkles className="h-4 w-4 text-amber-500" />
                <span className="text-xs text-muted-foreground">
                  {language === 'de' ? 'Powered by KI & Sommelier-Expertise' : 
                   language === 'en' ? 'Powered by AI & Sommelier Expertise' : 
                   'Propulsé par IA & Expertise Sommelier'}
                </span>
              </div>
            </div>
            <p className="text-xs text-muted-foreground/70 max-w-lg opacity-0 animate-fade-in-up" style={{ animationDelay: '0.8s', animationFillMode: 'forwards' }}>
              {language === 'de' ? 'Wissenschaftliche Analyse trifft auf puren Genuss.' : 
               language === 'en' ? 'Scientific analysis meets pure enjoyment.' : 
               'L\'analyse scientifique rencontre le pur plaisir.'}
            </p>
          </div>
        </div>
      </section>

      {/* Quick Navigation Buttons */}
      <section className="py-8 px-4 md:px-12 lg:px-24 bg-muted/30">
        <div className="container mx-auto">
          <div className="flex flex-wrap justify-center gap-3">
            <Button
              variant="outline"
              onClick={() => navigate('/sommelier-kompass')}
              className="rounded-full px-5 py-5 text-sm font-medium border-primary/30 hover:bg-primary/5"
            >
              <Map className="mr-2 h-4 w-4" />
              {t('regional_nav') || 'Sommelier Kompass'}
            </Button>
            <Button
              variant="outline"
              onClick={() => navigate('/wine-database')}
              className="rounded-full px-5 py-5 text-sm font-medium border-primary/30 hover:bg-primary/5"
            >
              <Database className="mr-2 h-4 w-4" />
              {t('nav_wine_database') || 'Weindatenbank'}
            </Button>
            <Button
              variant="outline"
              onClick={() => navigate('/cellar')}
              className="rounded-full px-5 py-5 text-sm font-medium border-primary/30 hover:bg-primary/5"
            >
              <Wine className="mr-2 h-4 w-4" />
              {t('cta_cellar')}
            </Button>
            <Button
              variant="outline"
              onClick={() => navigate('/wie-wir-pairen')}
              className="rounded-full px-5 py-5 text-sm font-medium border-primary/30 hover:bg-primary/5"
            >
              <Beaker className="mr-2 h-4 w-4" />
              {language === 'de' ? 'Wie wir pairen' : language === 'en' ? 'How We Pair' : 'Notre Méthode'}
            </Button>
          </div>
        </div>
      </section>

      {/* Mission Section - "Über uns" */}
      <section className="py-12 md:py-20 px-4 md:px-12 lg:px-24 bg-gradient-to-b from-background to-muted/30">
        <div className="container mx-auto max-w-5xl">
          {/* Header */}
          <div className="text-center mb-12">
            <p className="text-accent font-accent text-sm tracking-widest uppercase mb-3">
              {language === 'de' ? 'ÜBER UNS' : language === 'en' ? 'ABOUT US' : 'À PROPOS'}
            </p>
            <h2 className="text-2xl md:text-4xl font-semibold tracking-tight mb-4">
              {language === 'de' ? 'Unsere Mission: Genuss für alle' : 
               language === 'en' ? 'Our Mission: Enjoyment for Everyone' : 
               'Notre Mission: Le plaisir pour tous'}
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              {language === 'de' ? 'Ohne Komplexität. Ohne Dogmen.' : 
               language === 'en' ? 'Without complexity. Without dogma.' : 
               'Sans complexité. Sans dogmes.'}
            </p>
          </div>

          {/* Who we are */}
          <Card className="bg-card/50 backdrop-blur-sm border-border/50 mb-8">
            <CardContent className="p-6 md:p-8">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                  <Heart className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-3">
                    {language === 'de' ? 'Wer wir sind' : language === 'en' ? 'Who We Are' : 'Qui nous sommes'}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    {language === 'de' 
                      ? 'Hinter wine-pairing.online steht die Überzeugung, dass man kein Sommelier-Studium braucht, um das perfekte Weinerlebnis zu genießen. Wir haben diese Plattform geschaffen, um die Brücke zwischen wissenschaftlicher Aromen-Analyse und dem echten Leben zu schlagen.'
                      : language === 'en'
                      ? 'Behind wine-pairing.online is the conviction that you don\'t need a sommelier degree to enjoy the perfect wine experience. We created this platform to bridge the gap between scientific aroma analysis and real life.'
                      : 'Derrière wine-pairing.online, il y a la conviction qu\'il n\'est pas nécessaire d\'être sommelier pour profiter de l\'expérience vinicole parfaite. Nous avons créé cette plateforme pour faire le pont entre l\'analyse scientifique des arômes et la vie réelle.'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Science meets Joy */}
          <Card className="bg-gradient-to-r from-primary/5 via-accent/5 to-primary/10 border-primary/20 mb-8">
            <CardContent className="p-6 md:p-8">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-full bg-amber-500/10 flex items-center justify-center flex-shrink-0">
                  <Beaker className="w-6 h-6 text-amber-500" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-3">
                    {language === 'de' ? 'Wissenschaft trifft Lebensfreude' : 
                     language === 'en' ? 'Science Meets Joy' : 
                     'La science rencontre la joie de vivre'}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed mb-4">
                    {language === 'de' 
                      ? 'Warum passt ein Wein zu einem Gericht? Die Antwort liegt oft in der Chemie – in der Balance von Säuren, Fetten und Aromen. Unsere App nutzt modernste KI-Technologie, um diese komplexen Verbindungen in Sekunden zu entschlüsseln.'
                      : language === 'en'
                      ? 'Why does a wine pair well with a dish? The answer often lies in chemistry – in the balance of acids, fats, and aromas. Our app uses cutting-edge AI technology to decode these complex connections in seconds.'
                      : 'Pourquoi un vin s\'accorde-t-il bien avec un plat ? La réponse réside souvent dans la chimie – dans l\'équilibre des acides, des graisses et des arômes. Notre application utilise la technologie IA de pointe pour décoder ces connexions complexes en quelques secondes.'}
                  </p>
                  <p className="text-primary font-medium italic">
                    {language === 'de' ? 'Aber: Die Wissenschaft ist nur der Wegweiser, nicht das Ziel.' : 
                     language === 'en' ? 'But: Science is only the guide, not the destination.' : 
                     'Mais : La science n\'est que le guide, pas la destination.'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Philosophy in 3 Points */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold mb-6 text-center">
              {language === 'de' ? 'Unsere Philosophie in drei Sätzen:' : 
               language === 'en' ? 'Our Philosophy in Three Sentences:' : 
               'Notre philosophie en trois phrases :'}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* 1. Technik für den Menschen */}
              <Card className="bg-card/50 border-border/50 hover:border-primary/30 transition-colors">
                <CardContent className="p-5">
                  <div className="flex items-center gap-3 mb-3">
                    <span className="w-8 h-8 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-500 font-bold text-sm">1</span>
                    <h4 className="font-semibold text-sm">
                      {language === 'de' ? 'Technik für den Menschen' : 
                       language === 'en' ? 'Technology for People' : 
                       'La technologie au service de l\'homme'}
                    </h4>
                  </div>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    {language === 'de' 
                      ? 'Wir nutzen Daten, um dir Vorschläge zu machen, die wirklich funktionieren – egal welcher Wein du kaufst oder trinkst.'
                      : language === 'en'
                      ? 'We use data to give you suggestions that really work – no matter which wine you buy or drink.'
                      : 'Nous utilisons les données pour vous faire des suggestions qui fonctionnent vraiment – quel que soit le vin que vous achetez ou buvez.'}
                  </p>
                </CardContent>
              </Card>

              {/* 2. Dein Geschmack ist das Gesetz */}
              <Card className="bg-card/50 border-border/50 hover:border-primary/30 transition-colors">
                <CardContent className="p-5">
                  <div className="flex items-center gap-3 mb-3">
                    <span className="w-8 h-8 rounded-full bg-rose-500/10 flex items-center justify-center text-rose-500 font-bold text-sm">2</span>
                    <h4 className="font-semibold text-sm">
                      {language === 'de' ? 'Dein Geschmack ist das Gesetz' : 
                       language === 'en' ? 'Your Taste is the Law' : 
                       'Votre goût fait loi'}
                    </h4>
                  </div>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    {language === 'de' 
                      ? 'Wenn dir ein Pairing schmeckt, das in keinem Lehrbuch steht, dann hast du alles richtig gemacht.'
                      : language === 'en'
                      ? 'If you like a pairing that\'s not in any textbook, then you\'ve done everything right.'
                      : 'Si vous aimez un accord qui ne figure dans aucun manuel, alors vous avez tout fait correctement.'}
                  </p>
                </CardContent>
              </Card>

              {/* 3. Barrierefreier Genuss */}
              <Card className="bg-card/50 border-border/50 hover:border-primary/30 transition-colors">
                <CardContent className="p-5">
                  <div className="flex items-center gap-3 mb-3">
                    <span className="w-8 h-8 rounded-full bg-green-500/10 flex items-center justify-center text-green-500 font-bold text-sm">3</span>
                    <h4 className="font-semibold text-sm">
                      {language === 'de' ? 'Barrierefreier Genuss' : 
                       language === 'en' ? 'Accessible Enjoyment' : 
                       'Plaisir accessible'}
                    </h4>
                  </div>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    {language === 'de' 
                      ? 'Wir machen Schluss mit elitärer Weinsprache. Wir reden über Geschmack, Freude und den perfekten Moment am Esstisch.'
                      : language === 'en'
                      ? 'We\'re done with elitist wine language. We talk about taste, joy, and the perfect moment at the dinner table.'
                      : 'Nous en avons fini avec le langage élitiste du vin. Nous parlons de goût, de joie et du moment parfait à table.'}
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Quote */}
          <Card className="bg-primary/5 border-primary/20">
            <CardContent className="p-6 md:p-8 text-center">
              <blockquote className="text-lg md:text-xl italic text-foreground/90 leading-relaxed">
                {language === 'de' 
                  ? '"Wir liefern die Daten, du lieferst den Gaumen. Gemeinsam machen wir aus einem einfachen Abendessen ein unvergessliches Erlebnis."'
                  : language === 'en'
                  ? '"We provide the data, you provide the palate. Together, we turn a simple dinner into an unforgettable experience."'
                  : '"Nous fournissons les données, vous fournissez le palais. Ensemble, nous transformons un simple dîner en une expérience inoubliable."'}
              </blockquote>
              <div className="mt-4 flex items-center justify-center gap-2">
                <Wine className="w-5 h-5 text-primary" />
                <span className="text-sm text-muted-foreground">wine-pairing.online</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Pairing Science Highlight Card */}
      <section className="py-8 md:py-12 px-4 md:px-12 lg:px-24">
        <div className="container mx-auto max-w-4xl">
          <Card 
            className="bg-gradient-to-r from-primary/10 via-accent/10 to-primary/5 border-primary/20 hover:border-primary/40 transition-all cursor-pointer group"
            onClick={() => navigate('/wie-wir-pairen')}
            data-testid="pairing-science-card"
          >
            <CardContent className="p-6 md:p-8">
              <div className="flex flex-col md:flex-row items-start md:items-center gap-4 md:gap-6">
                <div className="w-14 h-14 md:w-16 md:h-16 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 group-hover:bg-primary/30 transition-colors">
                  <Beaker className="w-7 h-7 md:w-8 md:h-8 text-primary" strokeWidth={1.5} />
                </div>
                <div className="flex-1 space-y-2">
                  <h3 className="text-lg md:text-xl font-semibold text-primary">
                    {language === 'de' ? 'Wissenschaftlich fundiertes Pairing' : language === 'en' ? 'Science-Based Pairing' : 'Accords scientifiques'}
                  </h3>
                  <p className="text-sm md:text-base text-muted-foreground leading-relaxed">
                    {language === 'de' 
                      ? 'Entdecken Sie unsere 12 Schlüsselvariablen – 6 für den Wein, 6 für das Gericht – die das Geheimnis des perfekten Pairings enthüllen.' 
                      : language === 'en' 
                      ? 'Discover our 12 key variables – 6 for wine, 6 for food – that reveal the secret of perfect pairing.'
                      : 'Découvrez nos 12 variables clés – 6 pour le vin, 6 pour le plat – qui révèlent le secret de l\'accord parfait.'}
                  </p>
                </div>
                <div className="flex-shrink-0">
                  <Button 
                    variant="outline" 
                    className="rounded-full border-primary/30 hover:bg-primary hover:text-primary-foreground group-hover:border-primary transition-all"
                  >
                    {language === 'de' ? 'Methodik entdecken' : language === 'en' ? 'Discover Method' : 'Découvrir'}
                    <span className="ml-2">→</span>
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Philosophy Section */}
      <section className="py-16 md:py-24 px-4 md:px-12 lg:px-24">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-8 md:gap-12">
            <div className="md:col-span-5 space-y-4 md:space-y-6 opacity-0 animate-fade-in-up animate-delay-100" style={{ animationFillMode: 'forwards' }}>
              <p className="text-accent font-accent text-sm tracking-widest uppercase">{t('philosophy_tagline')}</p>
              <h2 className="text-2xl md:text-4xl font-semibold tracking-tight">
                {t('philosophy_title')}
              </h2>
            </div>
            <div className="md:col-span-7 space-y-4 md:space-y-6 opacity-0 animate-fade-in-up animate-delay-200" style={{ animationFillMode: 'forwards' }}>
              <p className="text-muted-foreground leading-relaxed text-base md:text-lg">
                {t('philosophy_text1')}
              </p>
              <p className="text-muted-foreground leading-relaxed text-base md:text-lg">
                {t('philosophy_text2')}
              </p>
              <blockquote className="border-l-4 border-accent pl-4 md:pl-6 py-2 font-accent text-lg md:text-xl italic text-foreground/80">
                {t('philosophy_quote')}
              </blockquote>
            </div>
          </div>
        </div>
      </section>
      
      {/* Manifest Section */}
      <section className="py-12 md:py-16 px-4 md:px-12 lg:px-24">
        <div className="container mx-auto max-w-4xl">
          <div className="opacity-0 animate-fade-in-up animate-delay-200" style={{ animationFillMode: 'forwards' }}>
            <p className="text-accent font-accent text-sm tracking-widest uppercase mb-2">{t('manifesto_title')}</p>
            <ul className="space-y-2 text-sm md:text-base text-muted-foreground list-disc pl-5">
              <li>{t('manifesto_point1')}</li>
              <li>{t('manifesto_point2')}</li>
              <li>{t('manifesto_point3')}</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-12 md:py-16 px-4 md:px-12 lg:px-24 bg-secondary/30">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8">
            {[
              { icon: Utensils, titleKey: 'feature_pairing_title', descKey: 'feature_pairing_desc' },
              { icon: Camera, titleKey: 'feature_scanner_title', descKey: 'feature_scanner_desc' },
              { icon: MessageCircle, titleKey: 'feature_sommelier_title', descKey: 'feature_sommelier_desc' }
            ].map((feature, idx) => (
              <Card key={idx} className="bg-card/50 backdrop-blur-sm border-border/50 hover-lift" data-testid={`feature-card-${idx}`}>
                <CardHeader>
                  <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                    <feature.icon className="w-6 h-6 text-primary" strokeWidth={1.5} />
                  </div>
                  <CardTitle className="text-lg md:text-xl">{t(feature.titleKey)}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-sm md:text-base">{t(feature.descKey)}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Freemium Pricing Teaser */}
      {!isPro && (
        <section className="py-16 md:py-24 px-4 md:px-12 lg:px-24 relative overflow-hidden">
          {/* Background Image */}
          <div className="absolute inset-0 z-0">
            <img
              src="https://images.unsplash.com/photo-1694147183672-57ccff109059?auto=format&fit=crop&w=1920&q=80"
              alt="Wine Experience"
              className="w-full h-full object-cover opacity-10"
            />
            <div className="absolute inset-0 bg-gradient-to-b from-background via-background/95 to-background" />
          </div>
          
          <div className="container mx-auto relative z-10">
            {/* Header */}
            <div className="text-center mb-12 space-y-4">
              <div className="inline-flex items-center gap-2 bg-primary/10 px-4 py-2 rounded-full border border-primary/20">
                <Crown className="w-4 h-4 text-primary" />
                <span className="text-sm font-medium text-primary">{pricingT.tagline}</span>
              </div>
              <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold">
                {pricingT.title}
              </h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                {pricingT.subtitle}
              </p>
            </div>
            
            {/* Pricing Cards */}
            <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
              {/* Free Plan */}
              <Card className="border-border/50 hover:border-border/80 transition-all p-6">
                <div className="text-center mb-6">
                  <h3 className="text-xl font-semibold mb-1">{pricingT.free}</h3>
                  <p className="text-muted-foreground text-sm">{pricingT.free_desc}</p>
                </div>
                <ul className="space-y-3 mb-6">
                  {pricingT.features_free?.map((feature, idx) => (
                    <li key={idx} className="flex items-center gap-3">
                      <Check className="w-5 h-5 text-green-500 flex-shrink-0" />
                      <span className="text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>
                <Button 
                  onClick={() => navigate('/pairing')}
                  variant="outline" 
                  className="w-full rounded-full"
                >
                  {pricingT.cta_free}
                </Button>
              </Card>

              {/* Pro Plan */}
              <Card className="border-primary/50 bg-gradient-to-b from-primary/5 to-transparent p-6 relative">
                <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                  <span className="bg-primary text-primary-foreground text-xs font-bold px-3 py-1 rounded-full">
                    BELIEBT
                  </span>
                </div>
                <div className="text-center mb-6">
                  <h3 className="text-xl font-semibold mb-1 flex items-center justify-center gap-2">
                    <Crown className="w-5 h-5 text-primary" />
                    {pricingT.pro}
                  </h3>
                  <p className="text-primary font-bold">{pricingT.pro_price}</p>
                </div>
                <ul className="space-y-3 mb-6">
                  {pricingT.features_pro?.map((feature, idx) => (
                    <li key={idx} className="flex items-center gap-3">
                      <Infinity className="w-5 h-5 text-primary flex-shrink-0" />
                      <span className="text-sm font-medium">{feature}</span>
                    </li>
                  ))}
                </ul>
                <Button 
                  onClick={() => user ? navigate('/subscription') : navigate('/login')}
                  className="w-full rounded-full bg-primary hover:bg-primary/90 group"
                >
                  <Sparkles className="mr-2 h-4 w-4 group-hover:animate-pulse" />
                  {pricingT.cta_pro}
                </Button>
              </Card>
            </div>

            {/* See All Link */}
            <div className="text-center mt-8">
              <Button 
                variant="ghost" 
                onClick={() => navigate('/pricing')}
                className="group text-muted-foreground hover:text-primary"
              >
                {pricingT.see_all}
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Button>
            </div>
          </div>
        </section>
      )}

      {/* App Description Section */}
      <AppDescription />

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default HomePage;
