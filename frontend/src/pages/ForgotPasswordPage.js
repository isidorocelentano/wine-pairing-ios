import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail, ArrowLeft, CheckCircle, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useLanguage } from '@/contexts/LanguageContext';
import { API } from '@/config/api';
import { toast } from 'sonner';

const ForgotPasswordPage = () => {
  const { language } = useLanguage();
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);

  const t = {
    de: {
      title: 'Passwort vergessen',
      subtitle: 'Geben Sie Ihre E-Mail-Adresse ein und wir senden Ihnen einen Link zum Zurücksetzen.',
      email: 'E-Mail-Adresse',
      send: 'Reset-Link senden',
      sending: 'Wird gesendet...',
      back: 'Zurück zum Login',
      success_title: 'E-Mail gesendet!',
      success_text: 'Falls ein Account mit dieser E-Mail existiert, haben wir Ihnen einen Link zum Zurücksetzen gesendet. Bitte prüfen Sie auch Ihren Spam-Ordner.',
      try_again: 'Erneut senden'
    },
    en: {
      title: 'Forgot Password',
      subtitle: 'Enter your email address and we will send you a reset link.',
      email: 'Email address',
      send: 'Send reset link',
      sending: 'Sending...',
      back: 'Back to login',
      success_title: 'Email sent!',
      success_text: 'If an account with this email exists, we have sent you a reset link. Please also check your spam folder.',
      try_again: 'Send again'
    },
    fr: {
      title: 'Mot de passe oublié',
      subtitle: 'Entrez votre adresse e-mail et nous vous enverrons un lien de réinitialisation.',
      email: 'Adresse e-mail',
      send: 'Envoyer le lien',
      sending: 'Envoi en cours...',
      back: 'Retour à la connexion',
      success_title: 'E-mail envoyé!',
      success_text: 'Si un compte avec cet e-mail existe, nous vous avons envoyé un lien de réinitialisation. Veuillez également vérifier votre dossier spam.',
      try_again: 'Renvoyer'
    }
  }[language] || {};

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!email) {
      toast.error(language === 'de' ? 'Bitte E-Mail eingeben' : 'Please enter email');
      return;
    }

    setLoading(true);
    
    try {
      await api.post('/auth/forgot-password', { email });
      setSent(true);
      toast.success(language === 'de' ? 'E-Mail gesendet!' : 'Email sent!');
    } catch (error) {
      // Always show success to prevent email enumeration
      setSent(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#1a0a0a] via-[#2d1515] to-[#1a0a0a] flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-black/40 backdrop-blur-sm border border-primary/20 rounded-2xl p-8">
          {/* Logo */}
          <div className="text-center mb-8">
            <span className="text-4xl">🍷</span>
            <h1 className="text-2xl font-bold text-white mt-4">{t.title}</h1>
            {!sent && (
              <p className="text-gray-400 mt-2 text-sm">{t.subtitle}</p>
            )}
          </div>

          {sent ? (
            /* Success State */
            <div className="text-center">
              <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-8 h-8 text-green-500" />
              </div>
              <h2 className="text-xl font-semibold text-white mb-2">{t.success_title}</h2>
              <p className="text-gray-400 text-sm mb-6">{t.success_text}</p>
              
              <div className="space-y-3">
                <Button 
                  onClick={() => setSent(false)}
                  variant="outline"
                  className="w-full"
                >
                  {t.try_again}
                </Button>
                <Link to="/login">
                  <Button variant="ghost" className="w-full text-gray-400">
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    {t.back}
                  </Button>
                </Link>
              </div>
            </div>
          ) : (
            /* Form */
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  {t.email}
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" />
                  <Input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="name@example.com"
                    className="pl-10 bg-black/30 border-primary/30 text-white"
                    required
                  />
                </div>
              </div>

              <Button 
                type="submit" 
                className="w-full bg-primary hover:bg-primary/90"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    {t.sending}
                  </>
                ) : (
                  t.send
                )}
              </Button>

              <Link to="/login">
                <Button variant="ghost" className="w-full text-gray-400 mt-2">
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  {t.back}
                </Button>
              </Link>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;
