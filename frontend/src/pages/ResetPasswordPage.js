import React, { useState, useEffect } from 'react';
import { Link, useSearchParams, useNavigate } from 'react-router-dom';
import { Lock, Eye, EyeOff, ArrowLeft, CheckCircle, Loader2, AlertCircle } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { useLanguage } from '../contexts/LanguageContext';
import api from '../services/api';
import toast from 'react-hot-toast';

const ResetPasswordPage = () => {
  const { language } = useLanguage();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');

  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [verifying, setVerifying] = useState(true);
  const [tokenValid, setTokenValid] = useState(false);
  const [success, setSuccess] = useState(false);
  const [maskedEmail, setMaskedEmail] = useState('');

  const t = {
    de: {
      title: 'Neues Passwort setzen',
      subtitle: 'Geben Sie Ihr neues Passwort ein.',
      password: 'Neues Passwort',
      confirm: 'Passwort bestätigen',
      min_chars: 'Mindestens 6 Zeichen',
      reset: 'Passwort ändern',
      resetting: 'Wird geändert...',
      success_title: 'Passwort geändert!',
      success_text: 'Ihr Passwort wurde erfolgreich geändert. Sie können sich jetzt einloggen.',
      to_login: 'Zum Login',
      invalid_title: 'Ungültiger Link',
      invalid_text: 'Dieser Reset-Link ist ungültig oder abgelaufen. Bitte fordern Sie einen neuen an.',
      request_new: 'Neuen Link anfordern',
      passwords_dont_match: 'Passwörter stimmen nicht überein',
      password_too_short: 'Passwort muss mindestens 6 Zeichen haben'
    },
    en: {
      title: 'Set new password',
      subtitle: 'Enter your new password.',
      password: 'New password',
      confirm: 'Confirm password',
      min_chars: 'At least 6 characters',
      reset: 'Change password',
      resetting: 'Changing...',
      success_title: 'Password changed!',
      success_text: 'Your password has been changed successfully. You can now log in.',
      to_login: 'Go to login',
      invalid_title: 'Invalid link',
      invalid_text: 'This reset link is invalid or expired. Please request a new one.',
      request_new: 'Request new link',
      passwords_dont_match: 'Passwords do not match',
      password_too_short: 'Password must be at least 6 characters'
    },
    fr: {
      title: 'Définir un nouveau mot de passe',
      subtitle: 'Entrez votre nouveau mot de passe.',
      password: 'Nouveau mot de passe',
      confirm: 'Confirmer le mot de passe',
      min_chars: 'Au moins 6 caractères',
      reset: 'Changer le mot de passe',
      resetting: 'Modification...',
      success_title: 'Mot de passe changé!',
      success_text: 'Votre mot de passe a été changé avec succès. Vous pouvez maintenant vous connecter.',
      to_login: 'Aller à la connexion',
      invalid_title: 'Lien invalide',
      invalid_text: 'Ce lien de réinitialisation est invalide ou expiré. Veuillez en demander un nouveau.',
      request_new: 'Demander un nouveau lien',
      passwords_dont_match: 'Les mots de passe ne correspondent pas',
      password_too_short: 'Le mot de passe doit comporter au moins 6 caractères'
    }
  }[language] || {};

  // Verify token on mount
  useEffect(() => {
    const verifyToken = async () => {
      if (!token) {
        setVerifying(false);
        setTokenValid(false);
        return;
      }

      try {
        const response = await api.get(`/auth/verify-reset-token/${token}`);
        setTokenValid(true);
        setMaskedEmail(response.data.email || '');
      } catch (error) {
        setTokenValid(false);
      } finally {
        setVerifying(false);
      }
    };

    verifyToken();
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (password.length < 6) {
      toast.error(t.password_too_short);
      return;
    }

    if (password !== confirmPassword) {
      toast.error(t.passwords_dont_match);
      return;
    }

    setLoading(true);

    try {
      await api.post('/auth/reset-password', {
        token,
        new_password: password
      });
      setSuccess(true);
      toast.success(t.success_title);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Error resetting password');
    } finally {
      setLoading(false);
    }
  };

  // Loading state
  if (verifying) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#1a0a0a] via-[#2d1515] to-[#1a0a0a] flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-primary animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#1a0a0a] via-[#2d1515] to-[#1a0a0a] flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-black/40 backdrop-blur-sm border border-primary/20 rounded-2xl p-8">
          {/* Logo */}
          <div className="text-center mb-8">
            <span className="text-4xl">🍷</span>
          </div>

          {!tokenValid ? (
            /* Invalid Token */
            <div className="text-center">
              <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <AlertCircle className="w-8 h-8 text-red-500" />
              </div>
              <h2 className="text-xl font-semibold text-white mb-2">{t.invalid_title}</h2>
              <p className="text-gray-400 text-sm mb-6">{t.invalid_text}</p>
              
              <Link to="/forgot-password">
                <Button className="w-full bg-primary hover:bg-primary/90">
                  {t.request_new}
                </Button>
              </Link>
            </div>
          ) : success ? (
            /* Success State */
            <div className="text-center">
              <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-8 h-8 text-green-500" />
              </div>
              <h2 className="text-xl font-semibold text-white mb-2">{t.success_title}</h2>
              <p className="text-gray-400 text-sm mb-6">{t.success_text}</p>
              
              <Link to="/login">
                <Button className="w-full bg-primary hover:bg-primary/90">
                  {t.to_login}
                </Button>
              </Link>
            </div>
          ) : (
            /* Reset Form */
            <>
              <h1 className="text-2xl font-bold text-white text-center">{t.title}</h1>
              <p className="text-gray-400 text-center mt-2 text-sm mb-6">
                {t.subtitle}
                {maskedEmail && <span className="text-primary"> ({maskedEmail})</span>}
              </p>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    {t.password}
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" />
                    <Input
                      type={showPassword ? 'text' : 'password'}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••"
                      className="pl-10 pr-10 bg-black/30 border-primary/30 text-white"
                      required
                      minLength={6}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-300"
                    >
                      {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">{t.min_chars}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    {t.confirm}
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" />
                    <Input
                      type={showPassword ? 'text' : 'password'}
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      placeholder="••••••••"
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
                      {t.resetting}
                    </>
                  ) : (
                    t.reset
                  )}
                </Button>

                <Link to="/login">
                  <Button variant="ghost" className="w-full text-gray-400">
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    {language === 'de' ? 'Zurück zum Login' : 'Back to login'}
                  </Button>
                </Link>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResetPasswordPage;
