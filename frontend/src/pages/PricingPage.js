import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Check, X, Wine, Sparkles, Crown, Zap, Star, ArrowRight, Shield, Clock, Infinity, Gift, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { useLanguage } from '@/contexts/LanguageContext';
import { useAuth } from '@/contexts/AuthContext';
import { API_URL } from '@/config/api';
import { toast } from 'sonner';
import Footer from '@/components/Footer';

const PricingPage = () => {
  const navigate = useNavigate();
  const { language } = useLanguage();
  const { user, refreshUser } = useAuth();
  
  // Coupon state
  const [couponCode, setCouponCode] = useState('');
  const [couponLoading, setCouponLoading] = useState(false);
  const [couponResult, setCouponResult] = useState(null);
  const [showCouponInput, setShowCouponInput] = useState(false);

  // Handle coupon redemption
  const handleRedeemCoupon = async (e) => {
    e.preventDefault();
    
    if (!user) {
      toast.error(language === 'de' ? 'Bitte melden Sie sich zuerst an' : 'Please log in first');
      navigate('/login');
      return;
    }

    setCouponLoading(true);
    setCouponResult(null);

    try {
      const token = localStorage.getItem('wine_auth_token');
      const response = await fetch(`${API_URL}/api/coupon/redeem`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        credentials: 'include',
        body: JSON.stringify({ code: couponCode.trim() }),
      });

      const data = await response.json();
      setCouponResult(data);

      if (data.success) {
        await refreshUser();
        setCouponCode('');
        toast.success(language === 'de' ? '🎉 Gutschein erfolgreich eingelöst!' : '🎉 Coupon redeemed successfully!');
      }
    } catch (error) {
      setCouponResult({
        success: false,
        message: language === 'de' ? 'Fehler beim Einlösen des Gutscheins' : 'Error redeeming coupon'
      });
    } finally {
      setCouponLoading(false);
    }
  };

  const t = {
    de: {
      hero_tagline: 'DEIN SOMMELIER. IMMER DABEI.',
      hero_title: 'Entdecke perfekte Weine',
      hero_subtitle: 'ohne Limit.',
      hero_description: 'Von Bordeaux bis Barolo – erlebe die volle Welt des Weins mit deinem persönlichen KI-Sommelier.',
      
      plans_title: 'Wähle deinen Plan',
      plans_subtitle: 'Starte kostenlos. Upgrade, wenn du mehr willst.',
      
      free_title: 'Basic',
      free_price: 'Kostenlos',
      free_period: 'Für immer',
      free_cta: 'Jetzt starten',
      
      pro_title: 'Pro',
      pro_price: '€4.99',
      pro_period: '/Monat',
      pro_yearly: 'oder €39.99/Jahr (spare 33%)',
      pro_cta: 'Pro werden',
      pro_badge: 'BELIEBT',
      
      features: {
        pairings: 'Pairing-Empfehlungen',
        chat: 'Chat mit Sommelier',
        cellar: 'Weinkeller',
        favorites: 'Favoriten',
        scanner: 'Etiketten-Scanner',
        database: 'Wein-Datenbank Zugang',
        support: 'Prioritäts-Support',
      },
      
      free_limits: {
        pairings: '5 pro Tag',
        chat: '5 Nachrichten/Tag',
        cellar: 'Max. 10 Weine',
        favorites: 'Max. 10 Weine',
      },
      
      pro_limits: {
        pairings: 'Unbegrenzt',
        chat: 'Unbegrenzt',
        cellar: 'Unbegrenzt',
        favorites: 'Unbegrenzt',
      },
      
      why_title: 'Warum Pro?',
      why_subtitle: 'Mehr als nur Empfehlungen',
      
      benefits: [
        {
          icon: Infinity,
          title: 'Keine Limits',
          description: 'Unbegrenzte Pairing-Anfragen, Chat-Nachrichten und Weinkeller-Einträge.'
        },
        {
          icon: Zap,
          title: 'Sofortige Antworten',
          description: 'Prioritäts-Zugang zu unserem KI-Sommelier für schnellere Empfehlungen.'
        },
        {
          icon: Shield,
          title: 'Premium Features',
          description: 'Exklusive Funktionen wie erweiterte Filter und personalisierte Empfehlungen.'
        }
      ],
      
      testimonial_title: 'Was unsere Nutzer sagen',
      testimonials: [
        {
          text: '"Endlich verstehe ich, welcher Wein zu welchem Essen passt. Die App hat meine Dinner-Partys revolutioniert!"',
          author: 'Marco S., Zürich'
        },
        {
          text: '"Als Weinliebhaber nutze ich die Pro-Version täglich. Unbegrenzte Empfehlungen sind Gold wert."',
          author: 'Lisa M., Wien'
        }
      ],
      
      faq_title: 'Häufige Fragen',
      faqs: [
        {
          q: 'Kann ich jederzeit kündigen?',
          a: 'Ja, du kannst dein Pro-Abo jederzeit kündigen. Es läuft dann bis zum Ende der bezahlten Periode weiter.'
        },
        {
          q: 'Gibt es eine Geld-zurück-Garantie?',
          a: 'Ja, wir bieten eine 14-tägige Geld-zurück-Garantie, wenn du nicht zufrieden bist.'
        },
        {
          q: 'Welche Zahlungsmethoden werden akzeptiert?',
          a: 'Wir akzeptieren alle gängigen Kreditkarten über unseren sicheren Zahlungsanbieter Stripe.'
        }
      ],
      
      final_cta_title: 'Bereit für das volle Wein-Erlebnis?',
      final_cta_subtitle: 'Starte jetzt kostenlos oder werde direkt Pro.',
      final_cta_button: 'Jetzt Pro werden',
      
      // Coupon translations
      coupon_banner_title: '🎁 Gutschein-Code?',
      coupon_banner_subtitle: 'Löse deinen Early Adopter Code ein und erhalte 1 Jahr Pro kostenlos!',
      coupon_banner_button: 'Gutschein einlösen',
      coupon_placeholder: 'z.B. WINE-XXXX-XXXX-XXXX',
      coupon_redeem: 'Einlösen',
      coupon_success: 'Gutschein erfolgreich eingelöst!',
      coupon_pro_until: 'Dein Pro-Plan ist gültig bis:',
      coupon_already_pro: 'Du hast bereits Pro-Zugang!',
    },
    en: {
      hero_tagline: 'YOUR SOMMELIER. ALWAYS WITH YOU.',
      hero_title: 'Discover perfect wines',
      hero_subtitle: 'without limits.',
      hero_description: 'From Bordeaux to Barolo – experience the full world of wine with your personal AI sommelier.',
      
      plans_title: 'Choose your plan',
      plans_subtitle: 'Start for free. Upgrade when you want more.',
      
      free_title: 'Basic',
      free_price: 'Free',
      free_period: 'Forever',
      free_cta: 'Get Started',
      
      pro_title: 'Pro',
      pro_price: '€4.99',
      pro_period: '/month',
      pro_yearly: 'or €39.99/year (save 33%)',
      pro_cta: 'Go Pro',
      pro_badge: 'POPULAR',
      
      features: {
        pairings: 'Pairing recommendations',
        chat: 'Chat with sommelier',
        cellar: 'Wine cellar',
        favorites: 'Favorites',
        scanner: 'Label scanner',
        database: 'Wine database access',
        support: 'Priority support',
      },
      
      free_limits: {
        pairings: '5 per day',
        chat: '5 messages/day',
        cellar: 'Max. 10 wines',
        favorites: 'Max. 10 wines',
      },
      
      pro_limits: {
        pairings: 'Unlimited',
        chat: 'Unlimited',
        cellar: 'Unlimited',
        favorites: 'Unlimited',
      },
      
      why_title: 'Why Pro?',
      why_subtitle: 'More than just recommendations',
      
      benefits: [
        {
          icon: Infinity,
          title: 'No Limits',
          description: 'Unlimited pairing requests, chat messages, and wine cellar entries.'
        },
        {
          icon: Zap,
          title: 'Instant Answers',
          description: 'Priority access to our AI sommelier for faster recommendations.'
        },
        {
          icon: Shield,
          title: 'Premium Features',
          description: 'Exclusive features like advanced filters and personalized recommendations.'
        }
      ],
      
      testimonial_title: 'What our users say',
      testimonials: [
        {
          text: '"Finally I understand which wine goes with which food. This app revolutionized my dinner parties!"',
          author: 'Marco S., Zurich'
        },
        {
          text: '"As a wine lover, I use the Pro version daily. Unlimited recommendations are priceless."',
          author: 'Lisa M., Vienna'
        }
      ],
      
      faq_title: 'Frequently Asked Questions',
      faqs: [
        {
          q: 'Can I cancel anytime?',
          a: 'Yes, you can cancel your Pro subscription anytime. It will continue until the end of the paid period.'
        },
        {
          q: 'Is there a money-back guarantee?',
          a: "Yes, we offer a 14-day money-back guarantee if you're not satisfied."
        },
        {
          q: 'What payment methods are accepted?',
          a: 'We accept all major credit cards through our secure payment provider Stripe.'
        }
      ],
      
      final_cta_title: 'Ready for the full wine experience?',
      final_cta_subtitle: 'Start for free or go Pro directly.',
      final_cta_button: 'Go Pro Now'
    },
    fr: {
      hero_tagline: 'VOTRE SOMMELIER. TOUJOURS AVEC VOUS.',
      hero_title: 'Découvrez les vins parfaits',
      hero_subtitle: 'sans limites.',
      hero_description: 'De Bordeaux à Barolo – vivez le monde du vin avec votre sommelier IA personnel.',
      
      plans_title: 'Choisissez votre plan',
      plans_subtitle: 'Commencez gratuitement. Passez à Pro quand vous voulez plus.',
      
      free_title: 'Basic',
      free_price: 'Gratuit',
      free_period: 'Pour toujours',
      free_cta: 'Commencer',
      
      pro_title: 'Pro',
      pro_price: '€4.99',
      pro_period: '/mois',
      pro_yearly: 'ou €39.99/an (économisez 33%)',
      pro_cta: 'Passer Pro',
      pro_badge: 'POPULAIRE',
      
      features: {
        pairings: 'Recommandations d\'accords',
        chat: 'Chat avec le sommelier',
        cellar: 'Cave à vin',
        favorites: 'Favoris',
        scanner: 'Scanner d\'étiquettes',
        database: 'Accès base de données',
        support: 'Support prioritaire',
      },
      
      free_limits: {
        pairings: '5 par jour',
        chat: '5 messages/jour',
        cellar: 'Max. 10 vins',
        favorites: 'Max. 10 vins',
      },
      
      pro_limits: {
        pairings: 'Illimité',
        chat: 'Illimité',
        cellar: 'Illimité',
        favorites: 'Illimité',
      },
      
      why_title: 'Pourquoi Pro?',
      why_subtitle: 'Plus que des recommandations',
      
      benefits: [
        {
          icon: Infinity,
          title: 'Sans Limites',
          description: 'Demandes d\'accords, messages et entrées de cave illimités.'
        },
        {
          icon: Zap,
          title: 'Réponses Instantanées',
          description: 'Accès prioritaire à notre sommelier IA pour des recommandations plus rapides.'
        },
        {
          icon: Shield,
          title: 'Fonctionnalités Premium',
          description: 'Fonctionnalités exclusives comme les filtres avancés et recommandations personnalisées.'
        }
      ],
      
      testimonial_title: 'Ce que disent nos utilisateurs',
      testimonials: [
        {
          text: '"Enfin je comprends quel vin va avec quel plat. Cette app a révolutionné mes dîners!"',
          author: 'Marco S., Zurich'
        },
        {
          text: '"En tant qu\'amateur de vin, j\'utilise la version Pro quotidiennement. Les recommandations illimitées sont inestimables."',
          author: 'Lisa M., Vienne'
        }
      ],
      
      faq_title: 'Questions Fréquentes',
      faqs: [
        {
          q: 'Puis-je annuler à tout moment?',
          a: 'Oui, vous pouvez annuler votre abonnement Pro à tout moment. Il continuera jusqu\'à la fin de la période payée.'
        },
        {
          q: 'Y a-t-il une garantie de remboursement?',
          a: 'Oui, nous offrons une garantie de remboursement de 14 jours si vous n\'êtes pas satisfait.'
        },
        {
          q: 'Quels modes de paiement sont acceptés?',
          a: 'Nous acceptons toutes les cartes de crédit principales via notre fournisseur de paiement sécurisé Stripe.'
        }
      ],
      
      final_cta_title: 'Prêt pour l\'expérience vin complète?',
      final_cta_subtitle: 'Commencez gratuitement ou passez Pro directement.',
      final_cta_button: 'Passer Pro Maintenant'
    }
  }[language] || {};

  const handleProClick = () => {
    if (user) {
      navigate('/subscription');
    } else {
      navigate('/login');
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="relative min-h-[70vh] flex items-center overflow-hidden">
        <div className="absolute inset-0 z-0">
          <img
            src="https://images.unsplash.com/photo-1555830142-739f08a61dfb?auto=format&fit=crop&w=1920&q=80"
            alt="Wine Lifestyle"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-black/90 via-black/70 to-black/50" />
        </div>
        
        <div className="relative z-10 container mx-auto px-4 md:px-12 lg:px-24 py-20">
          <div className="max-w-3xl space-y-6">
            <div className="inline-flex items-center gap-2 bg-primary/20 backdrop-blur-sm px-4 py-2 rounded-full border border-primary/30">
              <Crown className="w-4 h-4 text-primary" />
              <span className="text-sm font-medium text-primary">{t.hero_tagline}</span>
            </div>
            
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-white leading-tight">
              {t.hero_title}<br />
              <span className="text-primary">{t.hero_subtitle}</span>
            </h1>
            
            <p className="text-lg md:text-xl text-gray-300 max-w-2xl">
              {t.hero_description}
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <Button 
                onClick={handleProClick}
                size="lg"
                className="bg-primary hover:bg-primary/90 text-white px-8 py-6 text-lg rounded-full group"
              >
                <Sparkles className="mr-2 h-5 w-5 group-hover:animate-pulse" />
                {t.pro_cta}
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button 
                onClick={() => navigate('/pairing')}
                variant="outline"
                size="lg"
                className="border-white/30 text-white hover:bg-white/10 px-8 py-6 text-lg rounded-full"
              >
                {t.free_cta}
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="py-20 px-4 md:px-12 lg:px-24 bg-gradient-to-b from-background to-secondary/20">
        <div className="container mx-auto max-w-5xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">{t.plans_title}</h2>
            <p className="text-muted-foreground text-lg">{t.plans_subtitle}</p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            {/* Free Plan */}
            <Card className="border-border/50 hover:border-border transition-colors">
              <CardHeader className="text-center pb-8 pt-8">
                <CardTitle className="text-2xl mb-2">{t.free_title}</CardTitle>
                <div className="space-y-1">
                  <span className="text-4xl font-bold">{t.free_price}</span>
                  <p className="text-muted-foreground">{t.free_period}</p>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <ul className="space-y-3">
                  <FeatureRow feature={t.features?.pairings} limit={t.free_limits?.pairings} included />
                  <FeatureRow feature={t.features?.chat} limit={t.free_limits?.chat} included />
                  <FeatureRow feature={t.features?.cellar} limit={t.free_limits?.cellar} included />
                  <FeatureRow feature={t.features?.favorites} limit={t.free_limits?.favorites} included />
                  <FeatureRow feature={t.features?.scanner} included />
                  <FeatureRow feature={t.features?.database} included />
                  <FeatureRow feature={t.features?.support} included={false} />
                </ul>
                <Button 
                  onClick={() => navigate('/pairing')}
                  variant="outline" 
                  className="w-full py-6 mt-6 rounded-full"
                >
                  {t.free_cta}
                </Button>
              </CardContent>
            </Card>

            {/* Pro Plan */}
            <Card className="border-primary/50 bg-gradient-to-b from-primary/5 to-transparent relative overflow-hidden">
              <div className="absolute top-4 right-4">
                <span className="bg-primary text-primary-foreground text-xs font-bold px-3 py-1 rounded-full">
                  {t.pro_badge}
                </span>
              </div>
              <CardHeader className="text-center pb-8 pt-8">
                <CardTitle className="text-2xl mb-2 flex items-center justify-center gap-2">
                  <Crown className="w-6 h-6 text-primary" />
                  {t.pro_title}
                </CardTitle>
                <div className="space-y-1">
                  <span className="text-4xl font-bold text-primary">{t.pro_price}</span>
                  <span className="text-muted-foreground">{t.pro_period}</span>
                  <p className="text-sm text-muted-foreground">{t.pro_yearly}</p>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <ul className="space-y-3">
                  <FeatureRow feature={t.features?.pairings} limit={t.pro_limits?.pairings} included pro />
                  <FeatureRow feature={t.features?.chat} limit={t.pro_limits?.chat} included pro />
                  <FeatureRow feature={t.features?.cellar} limit={t.pro_limits?.cellar} included pro />
                  <FeatureRow feature={t.features?.favorites} limit={t.pro_limits?.favorites} included pro />
                  <FeatureRow feature={t.features?.scanner} included pro />
                  <FeatureRow feature={t.features?.database} included pro />
                  <FeatureRow feature={t.features?.support} included pro />
                </ul>
                <Button 
                  onClick={handleProClick}
                  className="w-full py-6 mt-6 rounded-full bg-primary hover:bg-primary/90"
                >
                  <Sparkles className="mr-2 h-4 w-4" />
                  {t.pro_cta}
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Why Pro Section */}
      <section className="py-20 px-4 md:px-12 lg:px-24">
        <div className="container mx-auto max-w-5xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">{t.why_title}</h2>
            <p className="text-muted-foreground text-lg">{t.why_subtitle}</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {t.benefits?.map((benefit, idx) => (
              <Card key={idx} className="text-center p-6 hover:shadow-lg transition-shadow border-border/50">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-primary/10 flex items-center justify-center">
                  <benefit.icon className="w-8 h-8 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-2">{benefit.title}</h3>
                <p className="text-muted-foreground">{benefit.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 px-4 md:px-12 lg:px-24 bg-secondary/30">
        <div className="container mx-auto max-w-4xl">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">{t.testimonial_title}</h2>
          
          <div className="grid md:grid-cols-2 gap-8">
            {t.testimonials?.map((testimonial, idx) => (
              <Card key={idx} className="p-6 bg-card/50">
                <div className="flex gap-1 mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 fill-primary text-primary" />
                  ))}
                </div>
                <p className="text-lg italic mb-4">{testimonial.text}</p>
                <p className="text-sm text-muted-foreground font-medium">— {testimonial.author}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 px-4 md:px-12 lg:px-24">
        <div className="container mx-auto max-w-3xl">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">{t.faq_title}</h2>
          
          <div className="space-y-4">
            {t.faqs?.map((faq, idx) => (
              <Card key={idx} className="p-6">
                <h3 className="font-semibold text-lg mb-2">{faq.q}</h3>
                <p className="text-muted-foreground">{faq.a}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="relative py-24 px-4 md:px-12 lg:px-24 overflow-hidden">
        <div className="absolute inset-0 z-0">
          <img
            src="https://images.unsplash.com/photo-1622196103817-1e7794345385?auto=format&fit=crop&w=1920&q=80"
            alt="Wine Pour"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-black/70" />
        </div>
        
        <div className="relative z-10 container mx-auto max-w-3xl text-center">
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-4">{t.final_cta_title}</h2>
          <p className="text-xl text-gray-300 mb-8">{t.final_cta_subtitle}</p>
          <Button 
            onClick={handleProClick}
            size="lg"
            className="bg-primary hover:bg-primary/90 text-white px-10 py-7 text-lg rounded-full group"
          >
            <Crown className="mr-2 h-5 w-5" />
            {t.final_cta_button}
            <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
          </Button>
        </div>
      </section>

      <Footer />
    </div>
  );
};

// Feature Row Component
const FeatureRow = ({ feature, limit, included, pro }) => {
  return (
    <li className="flex items-center justify-between py-2 border-b border-border/30 last:border-0">
      <div className="flex items-center gap-3">
        {included ? (
          <Check className={`w-5 h-5 ${pro ? 'text-primary' : 'text-green-500'}`} />
        ) : (
          <X className="w-5 h-5 text-muted-foreground/50" />
        )}
        <span className={included ? '' : 'text-muted-foreground/50'}>{feature}</span>
      </div>
      {limit && (
        <span className={`text-sm font-medium ${pro ? 'text-primary' : 'text-muted-foreground'}`}>
          {limit}
        </span>
      )}
    </li>
  );
};

export default PricingPage;
