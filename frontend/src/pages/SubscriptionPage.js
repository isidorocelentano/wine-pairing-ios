import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { useLanguage } from '@/contexts/LanguageContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Crown, Check, Wine, MessageSquare, Heart, Database, Loader2, Gift, AlertCircle, CheckCircle } from 'lucide-react';

const API_URL = process.env.REACT_APP_BACKEND_URL;

const SubscriptionPage = () => {
  const { user, isAuthenticated, refreshUser } = useAuth();
  const { language } = useLanguage();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(null);
  const [couponCode, setCouponCode] = useState('');
  const [couponLoading, setCouponLoading] = useState(false);
  const [couponResult, setCouponResult] = useState(null);

  const plans = {
    basic: {
      name: { de: 'Basic', en: 'Basic', fr: 'Basic' },
      price: { de: 'Kostenlos', en: 'Free', fr: 'Gratuit' },
      features: [
        { icon: Wine, text: { de: '5 Pairing-Anfragen/Tag', en: '5 pairing requests/day', fr: '5 accords/jour' } },
        { icon: MessageSquare, text: { de: '5 Chat-Nachrichten/Tag', en: '5 chat messages/day', fr: '5 messages/jour' } },
        { icon: Database, text: { de: 'Max. 10 Weine im Keller', en: 'Max. 10 wines in cellar', fr: 'Max. 10 vins en cave' } },
        { icon: Heart, text: { de: 'Max. 10 Favoriten', en: 'Max. 10 favorites', fr: 'Max. 10 favoris' } },
      ]
    },
    pro_monthly: {
      name: { de: 'Pro Monatlich', en: 'Pro Monthly', fr: 'Pro Mensuel' },
      price: '4,99€/Monat',
      popular: true,
      features: [
        { icon: Wine, text: { de: 'Unbegrenzte Pairings', en: 'Unlimited pairings', fr: 'Accords illimités' } },
        { icon: MessageSquare, text: { de: 'Unbegrenzter Chat', en: 'Unlimited chat', fr: 'Chat illimité' } },
        { icon: Database, text: { de: 'Unbegrenzter Weinkeller', en: 'Unlimited cellar', fr: 'Cave illimitée' } },
        { icon: Heart, text: { de: 'Unbegrenzte Favoriten', en: 'Unlimited favorites', fr: 'Favoris illimités' } },
        { icon: Crown, text: { de: 'Priority Support', en: 'Priority support', fr: 'Support prioritaire' } },
      ]
    },
    pro_yearly: {
      name: { de: 'Pro Jährlich', en: 'Pro Yearly', fr: 'Pro Annuel' },
      price: '39,99€/Jahr',
      savings: { de: '2 Monate gratis!', en: '2 months free!', fr: '2 mois gratuits!' },
      features: [
        { icon: Wine, text: { de: 'Unbegrenzte Pairings', en: 'Unlimited pairings', fr: 'Accords illimités' } },
        { icon: MessageSquare, text: { de: 'Unbegrenzter Chat', en: 'Unlimited chat', fr: 'Chat illimité' } },
        { icon: Database, text: { de: 'Unbegrenzter Weinkeller', en: 'Unlimited cellar', fr: 'Cave illimitée' } },
        { icon: Heart, text: { de: 'Unbegrenzte Favoriten', en: 'Unlimited favorites', fr: 'Favoris illimités' } },
        { icon: Crown, text: { de: 'Priority Support', en: 'Priority support', fr: 'Support prioritaire' } },
      ]
    }
  };

  const handleSubscribe = async (planId) => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    setLoading(planId);
    try {
      const response = await fetch(`${API_URL}/api/subscription/checkout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          plan: planId,
          origin_url: window.location.origin
        })
      });

      if (!response.ok) {
        throw new Error('Checkout failed');
      }

      const { url } = await response.json();
      window.location.href = url;
    } catch (err) {
      console.error('Subscription error:', err);
      alert('Fehler beim Erstellen der Zahlung. Bitte versuchen Sie es erneut.');
    } finally {
      setLoading(null);
    }
  };

  const handleCouponRedeem = async (e) => {
    e.preventDefault();
    
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    setCouponLoading(true);
    setCouponResult(null);

    try {
      const response = await fetch(`${API_URL}/api/coupon/redeem`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ code: couponCode.trim() }),
      });

      const data = await response.json();
      setCouponResult(data);

      if (data.success) {
        // Refresh user data to show new plan
        await refreshUser();
        setCouponCode('');
      }
    } catch (error) {
      setCouponResult({
        success: false,
        message: 'Fehler beim Einlösen des Gutscheins'
      });
    } finally {
      setCouponLoading(false);
    }
  };

  const lang = language || 'de';
  const isPro = user?.plan === 'pro';

  return (
    <div className="min-h-screen pb-20 pt-8 px-4 md:px-12 lg:px-24">
      <div className="container mx-auto max-w-6xl">
        {/* Header */}
        <div className="text-center mb-12">
          <Badge className="mb-4 bg-primary/10 text-primary">
            <Crown className="w-3 h-3 mr-1" />
            {lang === 'de' ? 'Upgrade' : lang === 'en' ? 'Upgrade' : 'Mise à niveau'}
          </Badge>
          <h1 className="text-3xl md:text-4xl font-bold mb-4">
            {lang === 'de' ? 'Wählen Sie Ihren Plan' : lang === 'en' ? 'Choose Your Plan' : 'Choisissez votre plan'}
          </h1>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            {lang === 'de' 
              ? 'Entdecken Sie unbegrenzte Möglichkeiten mit unserem Pro-Plan'
              : lang === 'en'
              ? 'Discover unlimited possibilities with our Pro plan'
              : 'Découvrez des possibilités illimitées avec notre plan Pro'}
          </p>
        </div>

        {/* Current Status */}
        {isAuthenticated && (
          <div className="mb-8 text-center">
            <Badge variant={isPro ? "default" : "secondary"} className="text-sm py-1 px-4">
              {isPro ? (
                <>
                  <Crown className="w-4 h-4 mr-2" />
                  {lang === 'de' ? 'Sie sind Pro-Mitglied' : 'You are a Pro member'}
                </>
              ) : (
                <>{lang === 'de' ? 'Aktueller Plan: Basic' : 'Current plan: Basic'}</>
              )}
            </Badge>
          </div>
        )}

        {/* Coupon Redemption Section */}
        {isAuthenticated && !isPro && (
          <div className="mb-8 max-w-lg mx-auto">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Gift className="h-5 w-5" />
                  {lang === 'de' ? 'Gutschein einlösen' : lang === 'en' ? 'Redeem Coupon' : 'Utiliser un coupon'}
                </CardTitle>
                <CardDescription>
                  {lang === 'de' 
                    ? 'Haben Sie einen Early Adopter Gutschein? Lösen Sie ihn hier ein für 1 Jahr kostenlosen Pro-Zugang.'
                    : lang === 'en'
                    ? 'Have an Early Adopter coupon? Redeem it here for 1 year of free Pro access.'
                    : 'Avez-vous un coupon Early Adopter? Utilisez-le ici pour 1 an d\'accès Pro gratuit.'}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleCouponRedeem} className="space-y-4">
                  <div>
                    <Input
                      type="text"
                      placeholder="z.B. WINE-XXXX-XXXX-XXXX"
                      value={couponCode}
                      onChange={(e) => setCouponCode(e.target.value.toUpperCase())}
                      className="text-center text-lg font-mono"
                      disabled={couponLoading}
                    />
                  </div>
                  
                  <Button 
                    type="submit" 
                    className="w-full" 
                    disabled={couponLoading || !couponCode.trim()}
                  >
                    {couponLoading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        {lang === 'de' ? 'Wird eingelöst...' : 'Redeeming...'}
                      </>
                    ) : (
                      lang === 'de' ? 'Gutschein einlösen' : 'Redeem Coupon'
                    )}
                  </Button>
                </form>

                {couponResult && (
                  <div className={`mt-4 p-4 rounded-lg ${
                    couponResult.success 
                      ? 'bg-green-50 border border-green-200' 
                      : 'bg-red-50 border border-red-200'
                  }`}>
                    <div className={`flex items-start gap-2 ${
                      couponResult.success ? 'text-green-700' : 'text-red-700'
                    }`}>
                      {couponResult.success ? (
                        <CheckCircle className="h-5 w-5 mt-0.5 flex-shrink-0" />
                      ) : (
                        <AlertCircle className="h-5 w-5 mt-0.5 flex-shrink-0" />
                      )}
                      <div>
                        <p className="font-medium">
                          {couponResult.success ? 'Erfolg!' : 'Fehler'}
                        </p>
                        <p className="text-sm mt-1">
                          {couponResult.message}
                        </p>
                        {couponResult.success && couponResult.expires_at && (
                          <p className="text-sm mt-2">
                            {lang === 'de' ? 'Gültig bis:' : 'Valid until:'} {new Date(couponResult.expires_at).toLocaleDateString('de-DE')}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        )}

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-6">
          {/* Basic Plan */}
          <Card className="relative">
            <CardHeader>
              <CardTitle>{plans.basic.name[lang]}</CardTitle>
              <CardDescription>
                <span className="text-2xl font-bold text-foreground">{plans.basic.price[lang]}</span>
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {plans.basic.features.map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <feature.icon className="h-4 w-4 text-muted-foreground" />
                    <span>{feature.text[lang]}</span>
                  </li>
                ))}
              </ul>
              <Button 
                variant="outline" 
                className="w-full mt-6"
                disabled={!isPro}
              >
                {isPro 
                  ? (lang === 'de' ? 'Downgrade' : 'Downgrade')
                  : (lang === 'de' ? 'Aktueller Plan' : 'Current Plan')}
              </Button>
            </CardContent>
          </Card>

          {/* Pro Monthly */}
          <Card className="relative border-primary shadow-lg">
            {plans.pro_monthly.popular && (
              <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                <Badge className="bg-primary text-primary-foreground">
                  {lang === 'de' ? 'Beliebt' : 'Popular'}
                </Badge>
              </div>
            )}
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Crown className="h-5 w-5 text-primary" />
                {plans.pro_monthly.name[lang]}
              </CardTitle>
              <CardDescription>
                <span className="text-2xl font-bold text-foreground">{plans.pro_monthly.price}</span>
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {plans.pro_monthly.features.map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <Check className="h-4 w-4 text-green-500" />
                    <span>{feature.text[lang]}</span>
                  </li>
                ))}
              </ul>
              <Button 
                className="w-full mt-6"
                onClick={() => handleSubscribe('pro_monthly')}
                disabled={loading === 'pro_monthly' || isPro}
              >
                {loading === 'pro_monthly' ? (
                  <Loader2 className="h-4 w-4 animate-spin mr-2" />
                ) : null}
                {isPro 
                  ? (lang === 'de' ? 'Aktiv' : 'Active')
                  : (lang === 'de' ? 'Jetzt upgraden' : 'Upgrade now')}
              </Button>
            </CardContent>
          </Card>

          {/* Pro Yearly */}
          <Card className="relative">
            {plans.pro_yearly.savings && (
              <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                <Badge variant="secondary" className="bg-green-500/10 text-green-600">
                  {plans.pro_yearly.savings[lang]}
                </Badge>
              </div>
            )}
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Crown className="h-5 w-5 text-primary" />
                {plans.pro_yearly.name[lang]}
              </CardTitle>
              <CardDescription>
                <span className="text-2xl font-bold text-foreground">{plans.pro_yearly.price}</span>
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {plans.pro_yearly.features.map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <Check className="h-4 w-4 text-green-500" />
                    <span>{feature.text[lang]}</span>
                  </li>
                ))}
              </ul>
              <Button 
                variant="outline"
                className="w-full mt-6 border-primary text-primary hover:bg-primary hover:text-primary-foreground"
                onClick={() => handleSubscribe('pro_yearly')}
                disabled={loading === 'pro_yearly' || isPro}
              >
                {loading === 'pro_yearly' ? (
                  <Loader2 className="h-4 w-4 animate-spin mr-2" />
                ) : null}
                {isPro 
                  ? (lang === 'de' ? 'Aktiv' : 'Active')
                  : (lang === 'de' ? 'Jetzt sparen' : 'Save now')}
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Login Prompt */}
        {!isAuthenticated && (
          <div className="mt-12 text-center p-6 bg-muted/50 rounded-lg">
            <p className="text-muted-foreground mb-4">
              {lang === 'de' 
                ? 'Melden Sie sich an, um zu upgraden'
                : 'Sign in to upgrade'}
            </p>
            <Button onClick={() => navigate('/login')}>
              {lang === 'de' ? 'Anmelden / Registrieren' : 'Sign in / Register'}
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default SubscriptionPage;
