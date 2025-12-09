import React, { useState, useEffect, useRef, useCallback } from 'react';
import "@/App.css";
import { BrowserRouter, Routes, Route, useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import { Toaster, toast } from 'sonner';
import { Wine, Utensils, MessageCircle, Home, Camera, Upload, X, Send, Loader2, Plus, Trash2, Star, Mic, MicOff, Globe, BookOpen, Users, Grape, Moon, Sun, Edit, Search, Heart } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogDescription } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ScrollArea } from "@/components/ui/scroll-area";
import { LanguageProvider, useLanguage } from "@/contexts/LanguageContext";
import { DarkModeProvider, useDarkMode } from "@/contexts/DarkModeContext";
import { useVoiceInput } from "@/hooks/useVoiceInput";
import { SEO } from "@/components/SEO";
import BlogPage from "@/pages/BlogPage";
import BlogPostPage from "@/pages/BlogPostPage";
import FeedPage from "@/pages/FeedPage";
import { GrapesPage, GrapeDetailPage } from "@/pages/GrapesPage";
import WineDatabasePage from "@/pages/WineDatabasePage";
import FavoritesPage from "@/pages/FavoritesPage";
import GrapeAdminPage from "@/pages/GrapeAdminPage";
import DishAdminPage from "@/pages/DishAdminPage";
import PairingSeoPage from "@/pages/PairingSeoPage";
import SeoPairingExplorerPage from "@/pages/SeoPairingExplorerPage";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// ===================== LANGUAGE & DARK MODE SELECTOR =====================
const LanguageSelector = () => {
  const { language, setLanguage, languageNames, languages } = useLanguage();
  const { isDark, toggleDarkMode } = useDarkMode();

  return (
    <div className="fixed top-4 right-4 z-50 flex items-center gap-2" data-testid="language-selector">
      {/* Dark Mode Toggle */}
      <Button
        variant="outline"
        size="icon"
        onClick={toggleDarkMode}
        className="rounded-full bg-background/80 backdrop-blur-sm border-border/50 hover:bg-accent"
        aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
      >
        {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
      </Button>

      {/* Language Selector */}
      <Select value={language} onValueChange={setLanguage}>
        <SelectTrigger className="w-auto gap-2 bg-background/80 backdrop-blur-sm border-border/50 rounded-full px-4">
          <Globe className="w-4 h-4" />
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          {languages.map((lang) => (
            <SelectItem key={lang} value={lang}>
              {languageNames[lang]}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};

// ===================== VOICE INPUT BUTTON =====================
const VoiceInputButton = ({ onResult, className = '' }) => {
  const { language, t } = useLanguage();
  const { isListening, isSupported, toggleListening } = useVoiceInput(onResult, language);

  if (!isSupported) return null;

  return (
    <button
      onClick={toggleListening}
      className={`p-3 rounded-full transition-all ${isListening 
        ? 'bg-primary text-primary-foreground animate-pulse' 
        : 'bg-secondary hover:bg-secondary/80'
      } ${className}`}
      data-testid="voice-input-btn"
      title={isListening ? t('listening') : t('chat_voice_hint')}
    >
      {isListening ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
    </button>
  );
};

// ===================== NAVIGATION =====================
const Navigation = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useLanguage();

  const navItems = [
    { path: '/', icon: Home, labelKey: 'nav_home' },
    { path: '/pairing', icon: Utensils, labelKey: 'nav_pairing' },
    { path: '/grapes', icon: Grape, labelKey: 'nav_grapes' },
    { path: '/wine-database', icon: BookOpen, labelKey: 'nav_wine_database' },
    { path: '/favorites', icon: Heart, labelKey: 'nav_favorites' },
    { path: '/cellar', icon: Wine, labelKey: 'nav_cellar' },
    { path: '/blog', icon: BookOpen, labelKey: 'nav_blog' },
    { path: '/feed', icon: Users, labelKey: 'nav_feed' },
    { path: '/chat', icon: MessageCircle, labelKey: 'nav_sommelier', isClaude: true },
  ];

  return (
    <nav className="nav-dock fixed bottom-4 md:bottom-6 left-1/2 -translate-x-1/2 rounded-full px-3 md:px-6 py-2 md:py-3 shadow-2xl z-50" data-testid="main-navigation">
      <div className="flex items-center gap-1 md:gap-2">
        {navItems.map((item) => (
          <button
            key={item.path}
            onClick={() => navigate(item.path)}
            data-testid={`nav-${item.labelKey.split('_')[1]}`}
            className={`flex items-center gap-1 md:gap-2 px-3 md:px-4 py-2 rounded-full transition-elegant ${
              location.pathname === item.path
                ? 'bg-primary text-primary-foreground'
                : 'hover:bg-secondary'
            }`}
          >
            {item.isClaude ? (
              <img
                src="https://customer-assets.emergentagent.com/job_e57eae36-225b-4e20-a944-048ef9749606/artifacts/w9w52bm4_CLAUDE%20SOMMELIER%2001%20%284%29.png"
                alt="Claude Avatar"
                className="w-6 h-6 rounded-full border border-border/60 object-cover shadow-sm"
              />
            ) : (
              <item.icon className="w-5 h-5" strokeWidth={1.5} />
            )}
            <span className="hidden md:inline text-sm font-medium">{t(item.labelKey)}</span>
          </button>
        ))}
      </div>
    </nav>
  );
};

// ===================== HOME PAGE =====================
const HomePage = () => {
  const navigate = useNavigate();
  const { t } = useLanguage();

  return (
    <div className="min-h-screen pb-20 md:pb-24" data-testid="home-page">
      {/* Hero Section */}
      <section className="relative min-h-[85vh] flex items-center">
        <div className="absolute inset-0 z-0">
          <img
            src="https://images.unsplash.com/photo-1666475877071-1cc8b7c33f3a?crop=entropy&cs=srgb&fm=jpg&q=85&w=1920"
            alt="Wine Pour"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-background via-background/90 to-background/40" />
        </div>
        
        <div className="relative z-10 container mx-auto px-4 md:px-12 lg:px-24">
          <div className="max-w-2xl space-y-6 md:space-y-8 opacity-0 animate-fade-in-up" style={{ animationDelay: '0.2s', animationFillMode: 'forwards' }}>
            <p className="text-accent font-accent text-base md:text-lg tracking-widest uppercase">{t('hero_tagline')}</p>
            <h1 className="text-3xl md:text-5xl lg:text-6xl font-semibold leading-tight tracking-tight">
              {t('hero_title')}
            </h1>
            <p className="text-base md:text-lg text-muted-foreground leading-relaxed">
              {t('hero_description')}
            </p>
            <div className="flex items-center gap-4 pt-2">
              <img
                src="https://customer-assets.emergentagent.com/job_e57eae36-225b-4e20-a944-048ef9749606/artifacts/w9w52bm4_CLAUDE%20SOMMELIER%2001%20%284%29.png"
                alt="Claude, virtueller Sommelier"
                className="w-16 h-16 rounded-full shadow-md border border-border/60 object-cover"
              />
              <p className="text-sm md:text-base text-muted-foreground leading-snug">
                {t('claude_intro_short')}
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-3 md:gap-4 pt-2 md:pt-4">
              <Button
                onClick={() => navigate('/pairing')}
                className="rounded-full px-6 md:px-8 py-5 md:py-6 text-sm font-medium tracking-wide transition-elegant hover:scale-105 active:scale-95"
                data-testid="cta-pairing"
              >
                <Utensils className="mr-2 h-4 w-4" />
                {t('cta_pairing')}
              </Button>
              <Button
                variant="outline"
                onClick={() => navigate('/cellar')}
                className="rounded-full px-6 md:px-8 py-5 md:py-6 text-sm font-medium tracking-wide border-primary/30 hover:bg-primary/5"
                data-testid="cta-cellar"
              >
                <Wine className="mr-2 h-4 w-4" />
                {t('cta_cellar')}
              </Button>
              <Button
                variant="outline"
                onClick={() => navigate('/blog')}
                className="rounded-full px-6 md:px-8 py-5 md:py-6 text-sm font-medium tracking-wide border-primary/30 hover:bg-primary/5"
                data-testid="cta-blog"
              >
                <BookOpen className="mr-2 h-4 w-4" />
                Blog
              </Button>
            </div>
          </div>
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
    </div>
  );
};

// Helper to split wine description into compact summary and detailed part
const splitDescription = (description) => {
  if (!description) {
    return { short: '', long: '' };
  }

  const text = description.trim();

  if (text.length <= 160) {
    return { short: text, long: '' };
  }

  const periodIndex = text.indexOf('.');

  if (periodIndex > 0 && periodIndex < 160) {
    const short = text.slice(0, periodIndex + 1).trim();
    const long = text.slice(periodIndex + 1).trim();
    return { short, long };
  }

  const short = `${text.slice(0, 140).trim()}…`;
  const long = text.slice(140).trim();

  return { short, long };
};

// ===================== WINE PAIRING PAGE =====================
const PairingPage = () => {
  const { t, language } = useLanguage();
  const [dish, setDish] = useState('');
  const [useCellar, setUseCellar] = useState(false);
  const [wineTypeFilter, setWineTypeFilter] = useState('all');
  const [dishCountryFilter, setDishCountryFilter] = useState('');
  const [dishTrendFilter, setDishTrendFilter] = useState('');
  const [dishBestsellerFilter, setDishBestsellerFilter] = useState('');
  const [dishes, setDishes] = useState([]);
  const [filteredDishSuggestions, setFilteredDishSuggestions] = useState([]);
  const [selectedDishId, setSelectedDishId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  // Profi-Modus 4D Werte
  const [richness, setRichness] = useState(null);
  const [freshness, setFreshness] = useState(null);
  const [sweetness, setSweetness] = useState(null);
  const [spice, setSpice] = useState(null);

  const [history, setHistory] = useState([]);
  useEffect(() => {
    const fetchDishes = async () => {
      try {
        const response = await axios.get(`${API}/dishes`);
        setDishes(response.data || []);
      } catch (error) {
        console.error('Error loading dishes for pairing:', error);
      }
    };
    fetchDishes();
  }, []);

  // Update dish suggestions based on input and filters
  useEffect(() => {
    if (!dish.trim() && !dishCountryFilter && !dishTrendFilter && !dishBestsellerFilter) {
      setFilteredDishSuggestions([]);
      setSelectedDishId(null);
      return;
    }
    const needle = dish.toLowerCase();
    const filtered = dishes.filter((d) => {
      // Text match on names
      const matchesText =
        !needle ||
        (d.name_de || '').toLowerCase().includes(needle) ||
        (d.name_en || '').toLowerCase().includes(needle) ||
        (d.name_fr || '').toLowerCase().includes(needle);

      if (!matchesText) return false;

      if (dishCountryFilter && (d.country || '').toLowerCase() !== dishCountryFilter.toLowerCase()) {
        return false;
      }
      if (
        dishTrendFilter &&
        !(d.trend_cuisines || []).some((t) => t.toLowerCase() === dishTrendFilter.toLowerCase())
      ) {
        return false;
      }
      if (
        dishBestsellerFilter &&
        (d.bestseller_category || '').toLowerCase() !== dishBestsellerFilter.toLowerCase()
      ) {
        return false;
      }

      return true;
    });

    setFilteredDishSuggestions(filtered.slice(0, 6));
    // Do not auto-select; user must click suggestion
  }, [dish, dishCountryFilter, dishTrendFilter, dishBestsellerFilter, dishes]);

  const handleSelectDishSuggestion = (suggestion) => {
    setDish(suggestion.name_de || suggestion.name_en || suggestion.name_fr || '');
    setSelectedDishId(suggestion.id);

    // Map structured dish matrix to 0-10 scale for 4D Profi-Modus
    const mapLevel = (value, mapping) => {
      if (!value) return null;
      const v = String(value).toLowerCase();
      if (mapping[v] !== undefined) return mapping[v];
      return null;
    };

    // Reichhaltigkeit aus Fettgehalt/Intensität ableiten
    const fatLevel = mapLevel(suggestion.fat_level, { niedrig: 2, mittel: 5, hoch: 8 });
    const intensityLevel = mapLevel(suggestion.intensity, { leicht: 3, mittel: 6, kräftig: 8 });
    const richnessValue = Math.round(
      [fatLevel, intensityLevel]
        .filter((v) => typeof v === 'number')
        .reduce((sum, v, _, arr) => sum + v / arr.length, 0) || 5
    );

    // Frische aus Säure ableiten
    const freshnessValue = mapLevel(suggestion.acid_level, { niedrig: 2, mittel: 5, hoch: 8 }) ?? 5;

    // Süße aus sweetness_level ableiten
    const sweetnessValue = mapLevel(suggestion.sweetness_level, {
      trocken: 2,
      leicht_süß: 6,
      süß: 9,
    }) ?? 3;

    // Würze aus spice_level ableiten
    const spiceValue = mapLevel(suggestion.spice_level, {
      keine: 1,
      leicht: 3,
      mittel: 6,
      dominant: 9,
    }) ?? 2;

    setRichness(richnessValue);
    setFreshness(freshnessValue);
    setSweetness(sweetnessValue);
    setSpice(spiceValue);
  };


  const handleVoiceResult = useCallback((transcript) => {
    setDish(prev => prev + (prev ? ' ' : '') + transcript);
  }, []);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API}/pairings`);
      setHistory(response.data.slice(0, 5));
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  const handlePairing = async () => {
    if (!dish.trim()) {
      toast.error(t('error_dish_required'));
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post(`${API}/pairing`, {
        dish: dish,
        use_cellar: useCellar,
        wine_type_filter: wineTypeFilter || null,
        language: language,
        dish_id: selectedDishId,
        richness,
        freshness,
        sweetness,
        spice,
      });
      setResult(response.data);
      fetchHistory();
      toast.success(t('success_recommendation'));
    } catch (error) {
      toast.error(t('error_general'));
      console.error('Pairing error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen pb-20 md:pb-24 pt-6 md:pt-8 px-4 md:px-12 lg:px-24" data-testid="pairing-page">
      <div className="container mx-auto max-w-4xl">
        <header className="text-center mb-8 md:mb-12">
          <p className="text-accent font-accent text-sm tracking-widest uppercase mb-2">{t('pairing_tagline')}</p>
          <h1 className="text-2xl md:text-4xl font-semibold tracking-tight mb-3 md:mb-4">{t('pairing_title')}</h1>
          <p className="text-muted-foreground max-w-xl mx-auto text-sm md:text-base">
            {t('pairing_description')}
          </p>
        </header>

        <Card className="bg-card/50 backdrop-blur-sm border-border/50 mb-6 md:mb-8">
          <CardContent className="p-4 md:p-8 space-y-4 md:space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2 md:mb-3">{t('pairing_label')}</label>
              <div className="relative">
                <Textarea
                  value={dish}
                  onChange={(e) => setDish(e.target.value)}
                  placeholder={t('pairing_placeholder')}
                  className="min-h-[80px] md:min-h-[100px] resize-none pr-24"
                  data-testid="dish-input"
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handlePairing();
                    }
                  }}
                />
                <div className="absolute right-2 bottom-2 flex gap-2">
                  <Button
                    size="icon"
                    variant="ghost"
                    onClick={handlePairing}
                    disabled={!dish.trim() || loading}
                    className="rounded-full h-9 w-9"
                    data-testid="search-button"
                  >
                    <Search className="h-5 w-5" />
                  </Button>
                  <VoiceInputButton onResult={handleVoiceResult} />
                </div>
              </div>
              
              {/* Dish Suggestions */}
              {filteredDishSuggestions.length > 0 && (
                <div className="mt-2 bg-background border border-border/60 rounded-lg shadow-lg max-h-56 overflow-y-auto text-sm" data-testid="dish-suggestions">
                  {filteredDishSuggestions.map((suggestion) => (
                    <button
                      key={suggestion.id}
                      type="button"
                      onClick={() => handleSelectDishSuggestion(suggestion)}
                      className="w-full text-left px-3 py-2 hover:bg-accent/40 flex flex-col"
                      data-testid="dish-suggestion-item"
                    >
                      <span className="font-medium">{suggestion.name_de || suggestion.name_en || suggestion.name_fr}</span>
                      <span className="text-xs text-muted-foreground flex gap-2">
                        {suggestion.country && <span>{suggestion.country}</span>}
                        {suggestion.bestseller_category && <span>· {suggestion.bestseller_category}</span>}
                      </span>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Wine Type Preference */}
            <div className="space-y-3">
              <label className="text-sm font-medium block">
                {t('pairing_wine_preference')}
              </label>
              <Select value={wineTypeFilter || 'all'} onValueChange={setWineTypeFilter}>
                <SelectTrigger className="w-full" data-testid="wine-type-filter">
                  <SelectValue placeholder={t('pairing_all_types')} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">{t('pairing_all_types')}</SelectItem>
                  <SelectItem value="weiss">{t('pairing_white')}</SelectItem>
                  <SelectItem value="rot">{t('pairing_red')}</SelectItem>
                  <SelectItem value="rose">{t('pairing_rose')}</SelectItem>
                  <SelectItem value="schaumwein">{t('pairing_sparkling')}</SelectItem>
                  <SelectItem value="suesswein">{t('pairing_sweet')}</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Profi-Modus 4D Gaumen-Übersetzer */}
            <details className="group">
              <summary className="flex items-center justify-between cursor-pointer select-none mb-2">
                <div>
                  <span className="text-xs font-semibold uppercase tracking-wide text-accent">
                    {t('pairing_pro_mode_title')}
                  </span>
                  <p className="text-[11px] md:text-xs text-muted-foreground max-w-xl mt-1">
                    {t('pairing_pro_mode_subtitle')}
                  </p>
                </div>
                <span className="text-[11px] text-muted-foreground group-open:rotate-180 transition-transform">
                  ▾
                </span>
              </summary>

              <Card className="bg-muted/40 border-dashed border-border/60">
                <CardContent className="p-4 md:p-5 space-y-4">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-accent">
                      {t('pairing_pro_mode_title')}
                    </p>
                    <p className="text-xs md:text-sm text-muted-foreground mt-1 max-w-xl">
                      {t('pairing_pro_mode_subtitle')}
                    </p>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {[{
                    key: 'richness',
                    label: t('pairing_dim_richness'),
                    value: richness,
                    setter: setRichness,
                  }, {
                    key: 'freshness',
                    label: t('pairing_dim_freshness'),
                    value: freshness,
                    setter: setFreshness,
                  }, {
                    key: 'sweetness',
                    label: t('pairing_dim_sweetness'),
                    value: sweetness,
                    setter: setSweetness,
                  }, {
                    key: 'spice',
                    label: t('pairing_dim_spice'),
                    value: spice,
                    setter: setSpice,
                  }].map((dim) => (
                    <div key={dim.key} className="space-y-1">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-medium">{dim.label}</span>
                        <span className="text-muted-foreground">
                          {typeof dim.value === 'number' ? dim.value : '–'} / 10
                        </span>
                      </div>
                      <input
                        type="range"
                        min="0"
                        max="10"
                        step="1"
                        value={typeof dim.value === 'number' ? dim.value : 5}
                        onChange={(e) => dim.setter(parseInt(e.target.value, 10))}
                        className="w-full accent-primary cursor-pointer"
                      />
                      <div className="flex justify-between text-[10px] text-muted-foreground uppercase tracking-wide">
                        <span>{t('pairing_dim_hint_low')}</span>
                        <span>{t('pairing_dim_hint_high')}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
              </Card>
            </details>

            {/* Dish Filters */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div>
                <label className="text-xs font-medium mb-1 block">{t('pairing_filter_country')}</label>
                <Input
                  value={dishCountryFilter}
                  onChange={(e) => setDishCountryFilter(e.target.value)}
                  placeholder="italien, thailand, usa..."
                />
              </div>
              <div>
                <label className="text-xs font-medium mb-1 block">{t('pairing_filter_trend')}</label>
                <Input
                  value={dishTrendFilter}
                  onChange={(e) => setDishTrendFilter(e.target.value)}
                  placeholder="thai, streetfood, fine_dining..."
                />
              </div>
              <div>
                <label className="text-xs font-medium mb-1 block">{t('pairing_filter_bestseller')}</label>
                <Input
                  value={dishBestsellerFilter}
                  onChange={(e) => setDishBestsellerFilter(e.target.value)}
                  placeholder="burger, pasta, steak, fisch..."
                />
              </div>
            </div>

            {/* Cellar Option */}
            <div>
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={useCellar}
                  onChange={(e) => setUseCellar(e.target.checked)}
                  className="w-5 h-5 rounded border-border text-primary focus:ring-primary"
                  data-testid="use-cellar-checkbox"
                />
                <span className="text-sm">{t('pairing_use_cellar')}</span>
              </label>
            </div>

            <Button
              onClick={handlePairing}
              disabled={loading || !dish.trim()}
              className="w-full rounded-full py-5 md:py-6 text-sm font-medium tracking-wide"
              data-testid="get-pairing-btn"
            >
              {loading ? (
                <><Loader2 className="mr-2 h-4 w-4 animate-spin" />{t('pairing_loading')}</>
              ) : (
                <><Wine className="mr-2 h-4 w-4" />{t('pairing_button')}</>
              )}
            </Button>
          </CardContent>
        </Card>

        {/* Result */}
        {result && (
          <Card className="pairing-card border-border/50 mb-6 md:mb-8 animate-fade-in-up" data-testid="pairing-result">
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="sommelier-avatar w-10 h-10 rounded-full flex items-center justify-center">
                  <Wine className="w-5 h-5 text-white" />
                </div>
                <div>
                  <CardTitle className="text-base md:text-lg">{t('pairing_result_title')}</CardTitle>
                  <CardDescription>{t('pairing_result_for')} &bdquo;{result.dish}&ldquo;</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              {/* Warum dieses Pairing funktioniert – 4D Erklärung */}
              {result.why_explanation && (
                <div className="mb-6 p-4 rounded-lg bg-muted/40 border border-border/40">
                  <h3 className="text-sm md:text-base font-semibold mb-2 flex items-center gap-2">
                    <span>✨</span>
                    <span>{t('pairing_why_title')}</span>
                  </h3>
                  <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-line">
                    {result.why_explanation}
                  </p>
                </div>
              )}

              {!result.why_explanation && (
                <div className="mb-6 p-4 rounded-lg bg-muted/20 border border-dashed border-border/40">
                  <h3 className="text-xs md:text-sm font-semibold mb-1 flex items-center gap-2">
                    <span>✨</span>
                    <span>{t('pairing_why_title')}</span>
                  </h3>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    {t('pairing_why_fallback')}
                  </p>
                </div>
              )}

              {(() => {
                // Parse recommendation text into structured wine cards
                const lines = result.recommendation.split('\n');
                const sections = [];
                let currentSection = null;
                let currentIntro = '';
                let wines = [];
                
                lines.forEach((line, idx) => {
                  const trimmedLine = line.trim();
                  
                  // Main heading
                  if (trimmedLine.match(/^1\.\s*\*\*.*HAUPTEMPFEHLUNG/i)) {
                    if (currentSection) {
                      currentSection.wines = wines;
                      sections.push(currentSection);
                    }
                    currentSection = { title: '🍷 Hauptempfehlung', type: 'main', intro: '', wines: [] };
                    wines = [];
                    currentIntro = '';
                  }
                  // Alternative Options heading
                  else if (trimmedLine.match(/^2\.\s*\*\*.*Alternative/i)) {
                    if (currentSection) {
                      currentSection.intro = currentIntro;
                      currentSection.wines = wines;
                      sections.push(currentSection);
                    }
                    currentSection = { title: '🔄 Alternative Optionen', type: 'alternatives', intro: '', wines: [] };
                    wines = [];
                    currentIntro = '';
                  }
                  // Sub-heading (wine categories)
                  else if (trimmedLine.match(/^\*\*.*wein/i) || trimmedLine.match(/^-\s*\*\*.*wein/i)) {
                    // Extract category name
                    const categoryMatch = trimmedLine.match(/\*\*([^*]+)\*\*/);
                    if (categoryMatch) {
                      currentIntro = categoryMatch[1];
                    }
                  }
                  // Wine recommendation (starts with - or *)
                  else if (trimmedLine.match(/^[-*]\s+\*\*(.+?)\*\*/)) {
                    const wineMatch = trimmedLine.match(/^[-*]\s+\*\*(.+?)\*\*\s*[-–—]\s*(.+)/);
                    if (wineMatch) {
                      wines.push({
                        name: wineMatch[1].trim(),
                        description: wineMatch[2].trim(),
                        category: currentIntro
                      });
                    }
                  }
                  // Introduction text (not a wine, not a heading)
                  else if (trimmedLine && !trimmedLine.match(/^[-*#]/) && !trimmedLine.match(/^---/) && currentSection && wines.length === 0) {
                    currentIntro += (currentIntro ? ' ' : '') + trimmedLine;
                  }
                });
                
                // Add last section
                if (currentSection) {
                  currentSection.intro = currentIntro;
                  currentSection.wines = wines;
                  sections.push(currentSection);
                }
                
                // Render wine cards
                return (
                  <div className="space-y-6">
                    {sections.map((section, sectionIdx) => (
                      <div key={sectionIdx}>
                        {/* Section Title */}
                        <h3 className="text-xl font-extrabold mb-3 text-primary flex items-center gap-2">
                          {section.title}
                        </h3>
                        
                        {/* Introduction */}
                        {section.intro && (
                          <p className="text-sm text-muted-foreground mb-4 leading-relaxed">
                            {section.intro}
                          </p>
                        )}
                        
                        {/* Wine Cards */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {section.wines.map((wine, wineIdx) => {
                            const { short, long } = splitDescription(wine.description);
                            const hasDetails = Boolean(long);

                            return (
                              <Card
                                key={wineIdx}
                                className="border-2 border-border hover:border-primary hover:shadow-lg transition-all cursor-pointer group"
                              >
                                <CardContent className="p-4 flex flex-col gap-2">
                                  {/* Wine Name - PROMINENT */}
                                  <h4 className="font-semibold text-base md:text-lg text-primary group-hover:text-primary/80 line-clamp-2">
                                    {wine.name}
                                  </h4>

                                  {/* Category Badge */}
                                  {wine.category && (
                                    <Badge variant="secondary" className="text-xs self-start">
                                      {wine.category}
                                    </Badge>
                                  )}

                                  {/* Compact one-line summary */}
                                  {short && (
                                    <p className="text-sm text-muted-foreground leading-snug line-clamp-2">
                                      {short}
                                    </p>
                                  )}

                                  {/* Expandable details */}
                                  {hasDetails && (
                                    <details className="mt-1 group-open:mt-2">
                                      <summary className="text-xs text-primary/80 hover:text-primary font-medium flex items-center gap-1 cursor-pointer list-none">
                                        <span>{t('pairing_more_details')}</span>
                                      </summary>
                                      <p className="mt-2 text-xs text-muted-foreground leading-relaxed whitespace-pre-line">
                                        {long}
                                      </p>
                                    </details>
                                  )}
                                </CardContent>
                              </Card>
                            );
                          })}
                        </div>
                        
                        {/* Divider between sections */}
                        {sectionIdx < sections.length - 1 && (
                          <hr className="my-6 opacity-50" />
                        )}
                      </div>
                    ))}
                  </div>
                );
              })()}
              
              {/* Cellar Matches */}
              {result.cellar_matches && result.cellar_matches.length > 0 && (
                <div className="mt-6 pt-6 border-t border-border/50">
                  <p className="text-sm font-medium mb-3">{t('pairing_cellar_matches')}</p>
                  <div className="flex flex-wrap gap-2">
                    {result.cellar_matches.map((wine) => (
                      <Badge key={wine.id} variant="outline" className="px-3 py-1">
                        {wine.name}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* History */}
        {history.length > 0 && (
          <div>
            <h3 className="text-base md:text-lg font-medium mb-3 md:mb-4">{t('pairing_history')}</h3>
            <div className="space-y-3">
              {history.map((item) => (
                <Card
                  key={item.id}
                  className="bg-secondary/30 border-border/30 hover:bg-secondary/50 transition-colors cursor-pointer"
                  data-testid="history-item"
                  onClick={() => {
                    // Beim Klick letzte Empfehlung wieder anzeigen
                    setDish(item.dish);
                    setResult({
                      dish: item.dish,
                      recommendation: item.recommendation,
                      why_explanation: item.why_explanation || null,
                      cellar_matches: item.cellar_matches || [],
                    });
                  }}
                >
                  <CardContent className="p-3 md:p-4">
                    <p className="font-medium text-sm md:text-base">{item.dish}</p>
                    <p className="text-xs md:text-sm text-muted-foreground line-clamp-2 mt-1">
                      {item.recommendation.slice(0, 150)}...
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// ===================== WINE CELLAR PAGE =====================
const CellarPage = () => {
  const { t } = useLanguage();
  const [wines, setWines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [inStockOnly, setInStockOnly] = useState(false);
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [showScanDialog, setShowScanDialog] = useState(false);
  const [showEditDialog, setShowEditDialog] = useState(false);
  const [editingWine, setEditingWine] = useState(null);
  const [newWine, setNewWine] = useState({ name: '', type: 'rot', region: '', year: '', grape: '', description: '', notes: '', image_base64: '', quantity: 1 });
  const [scanning, setScanning] = useState(false);
  const fileInputRef = useRef(null);
  const scanInputRef = useRef(null);

  const fetchWines = useCallback(async () => {
    try {
      const params = [];
      if (filter !== 'all') {
        params.push(`type_filter=${filter}`);
      }
      if (inStockOnly) {
        params.push('in_stock_only=true');
      }
      const query = params.length ? `?${params.join('&')}` : '';
      const response = await axios.get(`${API}/wines${query}`);
      setWines(response.data);
    } catch (error) {
      toast.error(t('error_general'));
    } finally {
      setLoading(false);
    }
  }, [filter, inStockOnly, t]);

  useEffect(() => {
    fetchWines();
  }, [fetchWines]);

  const handleImageUpload = (e, isScan = false) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64 = reader.result.split(',')[1];
        if (isScan) {
          handleScanLabel(base64);
        } else {
          setNewWine({ ...newWine, image_base64: base64 });
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleScanLabel = async (imageBase64) => {
    setScanning(true);
    try {
      const response = await axios.post(`${API}/scan-label`, { image_base64: imageBase64 });
      setNewWine((prev) => ({
        ...prev,
        ...response.data,
        year: response.data.year?.toString() || '',
        image_base64: imageBase64,
        quantity: typeof prev.quantity === 'number' ? prev.quantity : 1,
      }));
      setShowScanDialog(false);
      setShowAddDialog(true);
      toast.success(t('success_label_scanned'));
    } catch (error) {
      toast.error(t('error_general'));
    } finally {
      setScanning(false);
    }
  };

  const handleAddWine = async () => {
    if (!newWine.name.trim()) {
      toast.error(t('error_wine_name'));
      return;
    }

    try {
      await axios.post(`${API}/wines`, {
        ...newWine,
        year: newWine.year ? parseInt(newWine.year) : null,
        quantity: newWine.quantity ? parseInt(newWine.quantity, 10) : 1,
      });
      toast.success(t('success_wine_added'));
      setShowAddDialog(false);
      setNewWine({ name: '', type: 'rot', region: '', year: '', grape: '', description: '', notes: '', image_base64: '', quantity: 1 });
      fetchWines();
    } catch (error) {
      toast.error(t('error_general'));
    }
  };

  const handleToggleFavorite = async (wineId) => {
    try {
      await axios.post(`${API}/wines/${wineId}/favorite`);
      fetchWines();
    } catch (error) {
      toast.error(t('error_general'));
    }
  };

  const handleDeleteWine = async (wineId) => {
    try {
      await axios.delete(`${API}/wines/${wineId}`);
      toast.success(t('success_wine_deleted'));
      fetchWines();
    } catch (error) {
      toast.error(t('error_general'));
    }
  };

  const handleEditWine = (wine) => {
    setEditingWine({
      id: wine.id,
      name: wine.name,
      type: wine.type,
      region: wine.region || '',
      year: wine.year || '',
      grape: wine.grape || '',
      description: wine.description || '',  // Include description field
      notes: wine.notes || '',
      quantity: typeof wine.quantity === 'number' ? wine.quantity : 1,
    });
    setShowEditDialog(true);
  };

  const handleUpdateWine = async () => {
    try {
      await axios.put(`${API}/wines/${editingWine.id}`, {
        name: editingWine.name,
        type: editingWine.type,
        region: editingWine.region || null,
        year: editingWine.year ? parseInt(editingWine.year) : null,
        grape: editingWine.grape || null,
        notes: editingWine.notes || null,
        quantity: typeof editingWine.quantity === 'number' ? editingWine.quantity : parseInt(editingWine.quantity || '1', 10),
      });
      toast.success('Wein erfolgreich aktualisiert!');
      setShowEditDialog(false);
      setEditingWine(null);
      fetchWines();
    } catch (error) {
      toast.error(t('error_general'));
    }
  };

  const getWineTypeBadgeClass = (type) => {
    const classes = { rot: 'badge-rot', weiss: 'badge-weiss', rose: 'badge-rose', schaumwein: 'badge-schaumwein' };
    return classes[type] || 'bg-secondary';
  };

  const getWineTypeLabel = (type) => {
    const labels = { rot: t('pairing_red'), weiss: t('pairing_white'), rose: t('pairing_rose'), schaumwein: t('pairing_sparkling') };
    return labels[type] || type;
  };

  return (
    <div className="min-h-screen pb-20 md:pb-24 pt-6 md:pt-8 px-4 md:px-12 lg:px-24" data-testid="cellar-page">
      <div className="container mx-auto">
        <header className="flex flex-col gap-4 mb-6 md:mb-8">
          <div>
            <p className="text-accent font-accent text-sm tracking-widest uppercase mb-2">{t('cellar_tagline')}</p>
            <h1 className="text-2xl md:text-4xl font-semibold tracking-tight">{t('cellar_title')}</h1>
          </div>
            <label className="inline-flex items-center gap-2 text-xs md:text-sm text-muted-foreground">
              <input
                type="checkbox"
                checked={inStockOnly}
                onChange={(e) => setInStockOnly(e.target.checked)}
                className="w-4 h-4 rounded border-border text-primary focus:ring-primary"
              />
              <span>{t('cellar_filter_in_stock')}</span>
            </label>

          <div className="flex flex-wrap gap-2 md:gap-3 items-center">
            <Select value={filter} onValueChange={setFilter}>
              <SelectTrigger className="w-[140px] md:w-[160px]" data-testid="cellar-filter">
                <SelectValue placeholder="Filter" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">{t('cellar_filter_all')}</SelectItem>
                <SelectItem value="rot">{t('pairing_red')}</SelectItem>
                <SelectItem value="weiss">{t('pairing_white')}</SelectItem>
                <SelectItem value="rose">{t('pairing_rose')}</SelectItem>
                <SelectItem value="schaumwein">{t('pairing_sparkling')}</SelectItem>
              </SelectContent>
            </Select>
            
            <Dialog open={showScanDialog} onOpenChange={setShowScanDialog}>
              <DialogTrigger asChild>
                <Button variant="outline" className="rounded-full text-sm" data-testid="scan-label-btn">
                  <Camera className="mr-2 h-4 w-4" /><span className="hidden sm:inline">{t('cellar_scan')}</span><span className="sm:hidden">Scan</span>
                </Button>
              </DialogTrigger>
              <DialogContent className="mx-4 max-w-md">
                <DialogHeader>
                  <DialogTitle>{t('cellar_scan_title')}</DialogTitle>
                  <DialogDescription>{t('cellar_scan_desc')}</DialogDescription>
                </DialogHeader>
                <div 
                  className="upload-zone rounded-lg p-8 md:p-12 text-center cursor-pointer"
                  onClick={() => scanInputRef.current?.click()}
                >
                  {scanning ? (
                    <div className="flex flex-col items-center gap-3">
                      <Loader2 className="h-8 w-8 animate-spin text-primary" />
                      <p className="text-sm text-muted-foreground">{t('cellar_scanning')}</p>
                    </div>
                  ) : (
                    <>
                      <Camera className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                      <p className="text-sm text-muted-foreground">{t('cellar_scan_prompt')}</p>
                    </>
                  )}
                </div>
                <input ref={scanInputRef} type="file" accept="image/*" capture="environment" className="hidden" onChange={(e) => handleImageUpload(e, true)} />
              </DialogContent>
            </Dialog>

            <Dialog open={showAddDialog} onOpenChange={setShowAddDialog}>
              <DialogTrigger asChild>
                <Button className="rounded-full text-sm" data-testid="add-wine-btn">
                  <Plus className="mr-2 h-4 w-4" /><span className="hidden sm:inline">{t('cellar_add')}</span><span className="sm:hidden">+</span>
                </Button>
              </DialogTrigger>
              <DialogContent className="mx-4 max-w-md max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle>{t('cellar_add_title')}</DialogTitle>
                  <DialogDescription>{t('cellar_add_desc')}</DialogDescription>
                </DialogHeader>
                <p className="text-[11px] text-muted-foreground leading-snug border-l-2 border-accent pl-2 mb-3">
                  {t('cellar_scan_hint')}
                </p>
                <div className="space-y-4">
                  <Input placeholder={t('cellar_wine_name')} value={newWine.name} onChange={(e) => setNewWine({ ...newWine, name: e.target.value })} data-testid="wine-name-input" />
                  <Select value={newWine.type} onValueChange={(v) => setNewWine({ ...newWine, type: v })}>
                    <SelectTrigger data-testid="wine-type-select"><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="rot">{t('pairing_red')}</SelectItem>
                      <SelectItem value="weiss">{t('pairing_white')}</SelectItem>
                      <SelectItem value="rose">{t('pairing_rose')}</SelectItem>
                      <SelectItem value="schaumwein">{t('pairing_sparkling')}</SelectItem>
                    </SelectContent>
                  </Select>
                  <div className="grid grid-cols-3 gap-4">
                    <Input placeholder={t('cellar_region')} value={newWine.region} onChange={(e) => setNewWine({ ...newWine, region: e.target.value })} />
                    <Input placeholder={t('cellar_year')} type="number" value={newWine.year} onChange={(e) => setNewWine({ ...newWine, year: e.target.value })} />
                    <Input placeholder={t('cellar_quantity')} type="number" min={0} value={newWine.quantity} onChange={(e) => setNewWine({ ...newWine, quantity: e.target.value })} />
                  </div>
                  <Input placeholder={t('cellar_grape')} value={newWine.grape} onChange={(e) => setNewWine({ ...newWine, grape: e.target.value })} />
                  {newWine.description && (
                    <div className="bg-secondary/30 p-4 rounded-md border border-border">
                      <label className="text-sm font-medium mb-2 block">Beschreibung</label>
                      <p className="text-sm text-muted-foreground font-accent italic leading-relaxed">
                        {newWine.description}
                      </p>
                    </div>
                  )}
                  <Textarea placeholder={t('cellar_notes')} value={newWine.notes} onChange={(e) => setNewWine({ ...newWine, notes: e.target.value })} />
                  <div className="upload-zone rounded-lg p-4 md:p-6 text-center cursor-pointer" onClick={() => fileInputRef.current?.click()}>
                    {newWine.image_base64 ? (
                      <div className="relative inline-block">
                        <img src={`data:image/jpeg;base64,${newWine.image_base64}`} alt="Preview" className="max-h-24 md:max-h-32 mx-auto rounded" />
                        <button onClick={(e) => { e.stopPropagation(); setNewWine({ ...newWine, image_base64: '' }); }} className="absolute -top-2 -right-2 bg-destructive text-white rounded-full p-1">
                          <X className="h-3 w-3" />
                        </button>
                      </div>
                    ) : (
                      <><Upload className="h-8 w-8 mx-auto mb-2 text-muted-foreground" /><p className="text-sm text-muted-foreground">{t('cellar_upload_image')}</p></>
                    )}
                  </div>
                  <input ref={fileInputRef} type="file" accept="image/*" className="hidden" onChange={(e) => handleImageUpload(e, false)} />
                  <Button onClick={handleAddWine} className="w-full rounded-full" data-testid="save-wine-btn">{t('cellar_save')}</Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>
        </header>

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
        ) : wines.length === 0 ? (
          <Card className="bg-secondary/30 border-dashed border-2 border-border">
            <CardContent className="py-12 md:py-16 text-center">
              <Wine className="h-12 md:h-16 w-12 md:w-16 mx-auto mb-4 text-muted-foreground" strokeWidth={1} />
              <h3 className="text-lg md:text-xl font-medium mb-2">{t('cellar_empty_title')}</h3>
              <p className="text-muted-foreground mb-6 text-sm md:text-base">{t('cellar_empty_desc')}</p>
              <Button onClick={() => setShowAddDialog(true)} className="rounded-full">
                <Plus className="mr-2 h-4 w-4" />{t('cellar_empty_button')}
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-6" data-testid="wine-grid">
            {wines.map((wine) => (
              <Card key={wine.id} className="wine-card bg-card/50 backdrop-blur-sm border-border/50 overflow-hidden group" data-testid="wine-card">
                {wine.image_base64 ? (
                  <div className="aspect-[4/3] overflow-hidden bg-secondary/30">
                    <img src={`data:image/jpeg;base64,${wine.image_base64}`} alt={wine.name} className="w-full h-full object-cover" />
                  </div>
                ) : (
                  <div className="aspect-[4/3] bg-secondary/30 flex items-center justify-center">
                    <Wine className="h-12 md:h-16 w-12 md:w-16 text-muted-foreground/30" strokeWidth={1} />
                  </div>
                )}
                <CardContent className="p-3 md:p-4">
                  <div className="flex items-start justify-between mb-2">
                    <Badge className={`${getWineTypeBadgeClass(wine.type)} border-0 text-xs`}>{getWineTypeLabel(wine.type)}</Badge>
                    <button onClick={() => handleToggleFavorite(wine.id)} className="text-muted-foreground hover:text-primary transition-colors" data-testid="favorite-btn">
                      <Star className={`h-4 md:h-5 w-4 md:w-5 ${wine.is_favorite ? 'fill-accent text-accent' : ''}`} />
                    </button>
                  </div>
                  <h3 className="font-medium text-sm md:text-lg leading-tight mb-1 line-clamp-2">{wine.name}</h3>
                  <div className="text-xs md:text-sm text-muted-foreground space-y-0.5">
                    {wine.region && <p className="line-clamp-1">{wine.region}</p>}
                    {typeof wine.quantity === 'number' && wine.quantity > 0 && (
                      <p className="text-[11px] md:text-xs text-muted-foreground">{wine.quantity}x im Keller</p>
                    )}

                    <div className="flex gap-2">
                      {wine.year && <span>{wine.year}</span>}
                      {wine.grape && <span className="hidden md:inline">• {wine.grape}</span>}
                    </div>
                  </div>
                  <div className="flex gap-2 mt-3 md:mt-4 opacity-100 md:opacity-0 md:group-hover:opacity-100 transition-opacity">
                    <Button variant="outline" size="sm" className="flex-1 rounded-full text-xs" onClick={() => handleEditWine(wine)} data-testid="edit-wine-btn">
                      <Edit className="h-3 md:h-4 w-3 md:w-4" />
                    </Button>
                    <Button variant="destructive" size="sm" className="flex-1 rounded-full text-xs" onClick={() => handleDeleteWine(wine.id)} data-testid="delete-wine-btn">
                      <Trash2 className="h-3 md:h-4 w-3 md:w-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Edit Wine Dialog */}
        {editingWine && (
          <Dialog open={showEditDialog} onOpenChange={setShowEditDialog}>
            <DialogContent className="mx-4 max-w-md">
              <DialogHeader>
                <DialogTitle>Wein bearbeiten</DialogTitle>
                <DialogDescription>Aktualisieren Sie die Informationen zu Ihrem Wein</DialogDescription>
              </DialogHeader>
              <div className="space-y-4 pt-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">Name</label>
                  <Input
                    value={editingWine.name}
                    onChange={(e) => setEditingWine({ ...editingWine, name: e.target.value })}
                    placeholder="Weinname"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">Typ</label>
                  <Select value={editingWine.type} onValueChange={(v) => setEditingWine({ ...editingWine, type: v })}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="rot">{t('pairing_red')}</SelectItem>
                      <SelectItem value="weiss">{t('pairing_white')}</SelectItem>
                      <SelectItem value="rose">{t('pairing_rose')}</SelectItem>
                      <SelectItem value="schaumwein">{t('pairing_sparkling')}</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">Region</label>
                  <Input
                    value={editingWine.region}
                    onChange={(e) => setEditingWine({ ...editingWine, region: e.target.value })}
                    placeholder="z.B. Bordeaux"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">Jahrgang</label>
                  <Input
                    type="number"
                    value={editingWine.year}
                    onChange={(e) => setEditingWine({ ...editingWine, year: e.target.value })}
                    placeholder="z.B. 2018"
                  />
                <div>
                  <label className="text-sm font-medium mb-2 block">Anzahl Flaschen</label>
                  <Input
                    type="number"
                    min={0}
                    value={editingWine.quantity}
                    onChange={(e) => setEditingWine({ ...editingWine, quantity: e.target.value })}
                    placeholder="z.B. 3"
                  />
                </div>

                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">Rebsorte</label>
                  <Input
                    value={editingWine.grape}
                    onChange={(e) => setEditingWine({ ...editingWine, grape: e.target.value })}
                    placeholder="z.B. Cabernet Sauvignon"
                  />
                </div>
                {editingWine.description && (
                  <div className="bg-secondary/30 p-4 rounded-md border border-border">
                    <label className="text-sm font-medium mb-2 block">Beschreibung</label>
                    <p className="text-sm text-muted-foreground font-accent italic leading-relaxed">
                      {editingWine.description}
                    </p>
                  </div>
                )}
                <div>
                  <label className="text-sm font-medium mb-2 block">Notizen</label>
                  <Textarea
                    value={editingWine.notes}
                    onChange={(e) => setEditingWine({ ...editingWine, notes: e.target.value })}
                    placeholder="Ihre persönlichen Notizen..."
                    rows={3}
                  />
                </div>
                <div className="flex gap-3 pt-4">
                  <Button onClick={handleUpdateWine} className="flex-1">
                    Speichern
                  </Button>
                  <Button variant="outline" onClick={() => setShowEditDialog(false)} className="flex-1">
                    Abbrechen
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        )}
      </div>
    </div>
  );
};

// ===================== SOMMELIER CHAT PAGE =====================
const ChatPage = () => {
  const { t, language } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [imageBase64, setImageBase64] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const handleVoiceResult = useCallback((transcript) => {
    setInput(prev => prev + (prev ? ' ' : '') + transcript);
  }, []);

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  useEffect(() => { scrollToBottom(); }, [messages]);

  const handleSend = async () => {
    if (!input.trim() && !imageBase64) return;

    const userMessage = { role: 'user', content: input, image: imageBase64 };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`${API}/chat`, {
        message: input || 'Was siehst du auf diesem Bild?',
        session_id: sessionId,
        image_base64: imageBase64,
        language: language
      });

      setSessionId(response.data.session_id);
      setMessages((prev) => [...prev, { role: 'assistant', content: response.data.response }]);
      setImageBase64(null);
    } catch (error) {
      toast.error(t('error_general'));
      console.error('Chat error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setImageBase64(reader.result.split(',')[1]);
      reader.readAsDataURL(file);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const suggestions = [t('chat_suggestion1'), t('chat_suggestion2'), t('chat_suggestion3')];

  return (
    <div className="min-h-screen pb-20 md:pb-24 pt-6 md:pt-8 px-4 md:px-12 lg:px-24" data-testid="chat-page">
      <div className="container mx-auto max-w-3xl h-[calc(100vh-140px)] md:h-[calc(100vh-180px)] flex flex-col">
        <header className="mb-4 md:mb-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 md:gap-6">
            <div className="text-center md:text-left">
              <div className="sommelier-avatar w-14 md:w-20 h-14 md:h-20 rounded-full mx-auto md:mx-0 mb-3 md:mb-4 overflow-hidden border border-border/60 shadow-md">
                <img
                  src="https://customer-assets.emergentagent.com/job_e57eae36-225b-4e20-a944-048ef9749606/artifacts/w9w52bm4_CLAUDE%20SOMMELIER%2001%20%284%29.png"
                  alt="Claude, virtueller Sommelier"
                  className="w-full h-full object-cover"
                />
              </div>
              <h1 className="text-xl md:text-3xl font-semibold tracking-tight">{t('chat_title')}</h1>
              <p className="text-muted-foreground text-xs md:text-sm mt-1 md:mt-2">{t('chat_subtitle')}</p>
            </div>
            <div className="hidden md:block w-40 lg:w-56 rounded-2xl overflow-hidden shadow-xl border border-border/60">
              <img
                src="https://customer-assets.emergentagent.com/job_e57eae36-225b-4e20-a944-048ef9749606/artifacts/ulsy1h5x_CLAUDE%20SOMMELIER%2001%20%286%29.png"
                alt="Claude im Weinkeller"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
          <div className="mt-3 md:mt-4 p-3 md:p-4 rounded-xl bg-muted/40 border border-border/40 text-left">
            <h2 className="text-sm md:text-base font-semibold mb-1">{t('claude_bio_title')}</h2>
            <p className="text-[11px] md:text-sm text-muted-foreground leading-snug">
              {t('claude_bio_text1')}
            </p>
            <p className="hidden md:block text-[11px] md:text-sm text-muted-foreground leading-snug mt-1">
              {t('claude_bio_text2')}
            </p>
          </div>
        </header>

        <Card className="flex-1 bg-card/50 backdrop-blur-sm border-border/50 flex flex-col overflow-hidden">
          <ScrollArea className="flex-1 p-3 md:p-6">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center py-8 md:py-12">
                <Wine className="h-10 md:h-12 w-10 md:w-12 text-muted-foreground/30 mb-4" strokeWidth={1} />
                <p className="text-muted-foreground text-sm md:text-base">{t('chat_empty')}</p>
                <div className="flex flex-wrap gap-2 mt-4 md:mt-6 justify-center">
                  {suggestions.map((q) => (
                    <button key={q} onClick={() => setInput(q)} className="px-3 md:px-4 py-2 bg-secondary/50 rounded-full text-xs md:text-sm hover:bg-secondary transition-colors">
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="space-y-3 md:space-y-4">
                {messages.map((msg, idx) => (
                  <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[85%] md:max-w-[80%] p-3 md:p-4 ${msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-assistant'}`} data-testid={`chat-message-${msg.role}`}>
                      {msg.image && <img src={`data:image/jpeg;base64,${msg.image}`} alt="Uploaded" className="max-w-[150px] md:max-w-[200px] rounded mb-2" />}
                      <p className="text-xs md:text-sm whitespace-pre-wrap">{msg.content}</p>
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="flex justify-start">
                    <div className="chat-bubble-assistant p-3 md:p-4"><Loader2 className="h-4 md:h-5 w-4 md:w-5 animate-spin" /></div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </ScrollArea>

          <div className="p-3 md:p-4 border-t border-border/50">
            {imageBase64 && (
              <div className="mb-3 relative inline-block">
                <img src={`data:image/jpeg;base64,${imageBase64}`} alt="Preview" className="h-12 md:h-16 rounded" />
                <button onClick={() => setImageBase64(null)} className="absolute -top-2 -right-2 bg-destructive text-white rounded-full p-1">
                  <X className="h-3 w-3" />
                </button>
              </div>
            )}
            <div className="flex gap-2 md:gap-3">
              <button onClick={() => fileInputRef.current?.click()} className="p-2 md:p-3 rounded-full bg-secondary hover:bg-secondary/80 transition-colors" data-testid="chat-upload-btn">
                <Camera className="h-4 md:h-5 w-4 md:w-5" />
              </button>
              <input ref={fileInputRef} type="file" accept="image/*" className="hidden" onChange={handleImageUpload} />
              <VoiceInputButton onResult={handleVoiceResult} />
              <Input value={input} onChange={(e) => setInput(e.target.value)} onKeyPress={handleKeyPress} placeholder={t('chat_placeholder')} className="flex-1 rounded-full text-sm" data-testid="chat-input" />
              <Button onClick={handleSend} disabled={loading || (!input.trim() && !imageBase64)} className="rounded-full px-4 md:px-6" data-testid="chat-send-btn">
                <Send className="h-4 md:h-5 w-4 md:w-5" />
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

// ===================== MAIN APP =====================
function App() {
  return (
    <DarkModeProvider>
      <LanguageProvider>
        <div className="App" data-testid="wine-pairing-app">
          <Toaster position="top-center" richColors />
          <BrowserRouter>
            <LanguageSelector />
            <Routes>
              <Route path="/" element={<><SEO /><HomePage /><Navigation /></>} />
              <Route path="/pairing" element={<><PairingPage /><Navigation /></>} />
              <Route path="/pairing/:slug" element={<><PairingSeoPage /><Navigation /></>} />
              <Route path="/grapes" element={<><GrapesPage /><Navigation /></>} />
              <Route path="/grapes/:slug" element={<><GrapeDetailPage /><Navigation /></>} />
              <Route path="/wine-database" element={<><WineDatabasePage /><Navigation /></>} />
              <Route path="/favorites" element={<><FavoritesPage /><Navigation /></>} />
              <Route path="/cellar" element={<><CellarPage /><Navigation /></>} />
              <Route path="/admin/grapes" element={<><GrapeAdminPage /><Navigation /></>} />
              <Route path="/admin/dishes" element={<><DishAdminPage /><Navigation /></>} />
              <Route path="/seo/pairings" element={<><SeoPairingExplorerPage /><Navigation /></>} />
              <Route path="/feed" element={<><FeedPage /><Navigation /></>} />
              <Route path="/chat" element={<><ChatPage /><Navigation /></>} />
              <Route path="/blog" element={<><BlogPage /><Navigation /></>} />
              <Route path="/blog/:slug" element={<><BlogPostPage /><Navigation /></>} />
            </Routes>
          </BrowserRouter>
        </div>
      </LanguageProvider>
    </DarkModeProvider>
  );
}

export default App;
