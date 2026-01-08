import React from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useLanguage } from '@/contexts/LanguageContext';
import { Link } from 'react-router-dom';
import { ArrowLeft, Gift } from 'lucide-react';
import { Button } from '@/components/ui/button';
import ReferralSection from '@/components/ReferralSection';
import Navigation from '@/components/Navigation';

const ReferralPage = () => {
  const { user } = useAuth();
  const { language } = useLanguage();

  const texts = {
    de: {
      title: 'Freunde einladen',
      subtitle: 'Teile Wine Pairing und erhalte Belohnungen',
      loginRequired: 'Bitte melde dich an, um das Empfehlungsprogramm zu nutzen.',
      login: 'Anmelden',
      back: 'Zurück'
    },
    en: {
      title: 'Invite Friends',
      subtitle: 'Share Wine Pairing and earn rewards',
      loginRequired: 'Please log in to use the referral program.',
      login: 'Log in',
      back: 'Back'
    },
    fr: {
      title: 'Inviter des amis',
      subtitle: 'Partagez Wine Pairing et gagnez des récompenses',
      loginRequired: 'Veuillez vous connecter pour utiliser le programme de parrainage.',
      login: 'Se connecter',
      back: 'Retour'
    }
  };

  const t = texts[language] || texts.de;

  if (!user) {
    return (
      <>
        <Navigation />
        <div className="min-h-screen bg-gray-50 py-12 px-4">
          <div className="max-w-md mx-auto text-center">
            <div className="bg-white rounded-lg shadow-sm p-8">
              <Gift className="w-16 h-16 text-wine-500 mx-auto mb-4" />
              <h1 className="text-2xl font-bold mb-2">{t.title}</h1>
              <p className="text-gray-600 mb-6">{t.loginRequired}</p>
              <Link to="/login">
                <Button className="w-full">{t.login}</Button>
              </Link>
            </div>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Navigation />
      <div className="min-h-screen bg-gray-50 py-8 px-4">
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="mb-6">
            <Link to="/" className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900 mb-4">
              <ArrowLeft className="w-4 h-4 mr-1" />
              {t.back}
            </Link>
            <div className="flex items-center gap-3">
              <div className="p-3 bg-wine-100 rounded-full">
                <Gift className="w-8 h-8 text-wine-600" />
              </div>
              <div>
                <h1 className="text-2xl md:text-3xl font-bold text-gray-900">{t.title}</h1>
                <p className="text-gray-600">{t.subtitle}</p>
              </div>
            </div>
          </div>

          {/* Referral Section */}
          <ReferralSection />
        </div>
      </div>
    </>
  );
};

export default ReferralPage;
