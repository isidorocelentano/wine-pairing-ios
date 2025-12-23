import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { useLanguage } from '@/contexts/LanguageContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Wine, Loader2, Eye, EyeOff, CheckCircle, AlertCircle } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import GoogleLoginButton from '@/components/GoogleLoginButton';

const LoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, register, error, clearError, isAuthenticated } = useAuth();
  const { language } = useLanguage();
  const lang = language || 'de';
  
  const [activeTab, setActiveTab] = useState('login');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [success, setSuccess] = useState('');
  const [authError, setAuthError] = useState('');
  
  // Login form
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  
  // Register form
  const [registerName, setRegisterName] = useState('');
  const [registerEmail, setRegisterEmail] = useState('');
  const [registerPassword, setRegisterPassword] = useState('');
  const [registerPassword2, setRegisterPassword2] = useState('');

  // Redirect if already logged in
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/pairing');
    }
  }, [isAuthenticated, navigate]);

  // Check for error from OAuth callback - use location.state directly in render
  const oauthError = location.state?.error;

  const handleLogin = async (e) => {
    e.preventDefault();
    clearError();
    setAuthError('');
    setLoading(true);
    
    const result = await login(loginEmail, loginPassword);
    
    if (result.success) {
      navigate('/pairing');
    }
    setLoading(false);
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    clearError();
    setAuthError('');
    setSuccess('');
    
    if (registerPassword !== registerPassword2) {
      return;
    }
    
    setLoading(true);
    const result = await register(registerEmail, registerPassword, registerName);
    
    if (result.success) {
      setSuccess(lang === 'de' ? 'Registrierung erfolgreich!' : 'Registration successful!');
      setTimeout(() => navigate('/pairing'), 1500);
    }
    setLoading(false);
  };

  const texts = {
    de: {
      title: 'Willkommen',
      subtitle: 'Melden Sie sich an oder erstellen Sie ein Konto',
      login: 'Anmelden',
      register: 'Registrieren',
      email: 'E-Mail',
      password: 'Passwort',
      password2: 'Passwort bestätigen',
      name: 'Name',
      loginBtn: 'Anmelden',
      registerBtn: 'Registrieren',
      passwordMismatch: 'Passwörter stimmen nicht überein',
      forgotPassword: 'Passwort vergessen?',
      noAccount: 'Noch kein Konto?',
      hasAccount: 'Bereits registriert?',
    },
    en: {
      title: 'Welcome',
      subtitle: 'Sign in or create an account',
      login: 'Sign In',
      register: 'Register',
      email: 'Email',
      password: 'Password',
      password2: 'Confirm Password',
      name: 'Name',
      loginBtn: 'Sign In',
      registerBtn: 'Register',
      passwordMismatch: 'Passwords do not match',
      forgotPassword: 'Forgot password?',
      noAccount: 'No account yet?',
      hasAccount: 'Already registered?',
    },
    fr: {
      title: 'Bienvenue',
      subtitle: 'Connectez-vous ou créez un compte',
      login: 'Connexion',
      register: 'Inscription',
      email: 'E-mail',
      password: 'Mot de passe',
      password2: 'Confirmer le mot de passe',
      name: 'Nom',
      loginBtn: 'Se connecter',
      registerBtn: 'S\'inscrire',
      passwordMismatch: 'Les mots de passe ne correspondent pas',
      forgotPassword: 'Mot de passe oublié?',
      noAccount: 'Pas encore de compte?',
      hasAccount: 'Déjà inscrit?',
    }
  };

  const t = texts[lang] || texts.de;

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4 py-8">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="mx-auto w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
            <Wine className="h-6 w-6 text-primary" />
          </div>
          <CardTitle className="text-2xl">{t.title}</CardTitle>
          <CardDescription>{t.subtitle}</CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-2 mb-6">
              <TabsTrigger value="login">{t.login}</TabsTrigger>
              <TabsTrigger value="register">{t.register}</TabsTrigger>
            </TabsList>

            {/* Error Alert */}
            {(error || authError || oauthError) && (
              <Alert variant="destructive" className="mb-4">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error || authError || oauthError}</AlertDescription>
              </Alert>
            )}

            {/* Success Alert */}
            {success && (
              <Alert className="mb-4 border-green-500 text-green-600">
                <CheckCircle className="h-4 w-4" />
                <AlertDescription>{success}</AlertDescription>
              </Alert>
            )}

            {/* Google Login Button */}
            <div className="mb-6">
              <GoogleLoginButton redirectPath="/pairing" />
              
              {/* Divider */}
              <div className="relative my-6">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-card px-2 text-muted-foreground">
                    {lang === 'de' ? 'oder mit E-Mail' : lang === 'fr' ? 'ou par e-mail' : 'or with email'}
                  </span>
                </div>
              </div>
            </div>

            {/* Login Tab */}
            <TabsContent value="login">
              <form onSubmit={handleLogin} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="login-email">{t.email}</Label>
                  <Input
                    id="login-email"
                    type="email"
                    value={loginEmail}
                    onChange={(e) => setLoginEmail(e.target.value)}
                    placeholder="name@example.com"
                    required
                    disabled={loading}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="login-password">{t.password}</Label>
                  <div className="relative">
                    <Input
                      id="login-password"
                      type={showPassword ? 'text' : 'password'}
                      value={loginPassword}
                      onChange={(e) => setLoginPassword(e.target.value)}
                      required
                      disabled={loading}
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      className="absolute right-0 top-0 h-full px-3"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </Button>
                  </div>
                </div>
                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                  {t.loginBtn}
                </Button>
                <div className="text-center mt-3">
                  <a href="/forgot-password" className="text-sm text-primary hover:underline">
                    {t.forgotPassword}
                  </a>
                </div>
              </form>
            </TabsContent>

            {/* Register Tab */}
            <TabsContent value="register">
              <form onSubmit={handleRegister} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="register-name">{t.name}</Label>
                  <Input
                    id="register-name"
                    type="text"
                    value={registerName}
                    onChange={(e) => setRegisterName(e.target.value)}
                    placeholder="Max Mustermann"
                    required
                    disabled={loading}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="register-email">{t.email}</Label>
                  <Input
                    id="register-email"
                    type="email"
                    value={registerEmail}
                    onChange={(e) => setRegisterEmail(e.target.value)}
                    placeholder="name@example.com"
                    required
                    disabled={loading}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="register-password">{t.password}</Label>
                  <Input
                    id="register-password"
                    type="password"
                    value={registerPassword}
                    onChange={(e) => setRegisterPassword(e.target.value)}
                    required
                    minLength={6}
                    disabled={loading}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="register-password2">{t.password2}</Label>
                  <Input
                    id="register-password2"
                    type="password"
                    value={registerPassword2}
                    onChange={(e) => setRegisterPassword2(e.target.value)}
                    required
                    disabled={loading}
                  />
                  {registerPassword2 && registerPassword !== registerPassword2 && (
                    <p className="text-xs text-red-500">{t.passwordMismatch}</p>
                  )}
                </div>
                <Button 
                  type="submit" 
                  className="w-full" 
                  disabled={loading || (registerPassword !== registerPassword2)}
                >
                  {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                  {t.registerBtn}
                </Button>
              </form>
            </TabsContent>
          </Tabs>

          {/* Back to Home */}
          <div className="mt-6 text-center">
            <Button variant="link" onClick={() => navigate('/')}>
              ← {lang === 'de' ? 'Zurück zur Startseite' : 'Back to Home'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default LoginPage;
