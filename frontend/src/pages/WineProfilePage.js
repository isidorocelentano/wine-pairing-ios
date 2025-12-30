import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { 
  Wine, Save, RotateCcw, Crown, Lock, Grape, MapPin, 
  Euro, Ban, Utensils, Compass, Loader2, ChevronDown, X,
  Droplets, Mountain, Sparkles
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Slider } from '@/components/ui/slider';
import { useLanguage } from '@/contexts/LanguageContext';
import { useAuth } from '@/contexts/AuthContext';
import { API } from '@/config/api';

const WineProfilePage = () => {
  const navigate = useNavigate();
  const { language } = useLanguage();
  const { user } = useAuth();
  
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [profile, setProfile] = useState({
    red_wine_style: null,
    white_wine_style: null,
    acidity_tolerance: null,
    tannin_preference: null,
    sweetness_preference: null,
    favorite_regions: [],
    budget_everyday: null,
    budget_restaurant: null,
    no_gos: [],
    dietary_preferences: [],
    adventure_level: null
  });

  // Translations
  const t = {
    de: {
      title: 'Mein Weinprofil',
      subtitle: 'Personalisiere deine Weinempfehlungen',
      pro_required: 'Pro-Mitgliedschaft erforderlich',
      pro_description: 'Das Weinprofil ist eine exklusive Pro-Funktion. Werde Pro-Mitglied, um personalisierte Empfehlungen basierend auf deinem Geschmack zu erhalten.',
      upgrade_button: 'Jetzt Pro werden',
      save: 'Profil speichern',
      reset: 'Zurücksetzen',
      saving: 'Speichern...',
      saved: 'Profil gespeichert!',
      
      // Categories
      red_wine_title: '🍷 Rotwein-Stilistik',
      red_wine_desc: 'Welcher Rotwein-Stil spricht dich an?',
      white_wine_title: '🥂 Weißwein-Charakter',
      white_wine_desc: 'Welcher Weißwein-Typ gefällt dir?',
      structure_title: '⚖️ Struktur-Präferenzen',
      structure_desc: 'Säure und Tannin',
      sweetness_title: '🍯 Süßegrad',
      sweetness_desc: 'Von knochentrocken bis edelsüß',
      regions_title: '🗺️ Lieblings-Regionen',
      regions_desc: 'Wähle deine bevorzugten Weinregionen',
      budget_title: '💰 Budget-Rahmen',
      budget_desc: 'Für verschiedene Anlässe',
      no_gos_title: '🚫 No-Gos',
      no_gos_desc: 'Was soll die KI vermeiden?',
      dietary_title: '🍽️ Kulinarischer Kontext',
      dietary_desc: 'Was isst du am liebsten?',
      adventure_title: '🧭 Abenteuer-Faktor',
      adventure_desc: 'Klassiker oder mutige Entdeckungen?',
      
      // Options
      red_kraftig: 'Kräftig & Würzig',
      red_kraftig_desc: 'Bordeaux, Rhône, Barolo',
      red_elegant: 'Fruchtig & Elegant',
      red_elegant_desc: 'Burgunder, Pinot Noir',
      red_both: 'Beides',
      
      white_mineral: 'Mineralisch & Frisch',
      white_mineral_desc: 'Chablis, Sancerre',
      white_creamy: 'Cremig & Textur',
      white_creamy_desc: 'Meursault, Weißburgunder',
      white_aromatic: 'Aromatisch & Verspielt',
      white_aromatic_desc: 'Riesling, Gewürztraminer',
      white_all: 'Alle Stile',
      
      acidity_label: 'Säure-Toleranz',
      acidity_low: 'Niedrig',
      acidity_medium: 'Mittel',
      acidity_high: 'Hoch',
      
      tannin_label: 'Tannin-Vorliebe',
      tannin_soft: 'Weich & Seidig',
      tannin_medium: 'Mittel',
      tannin_bold: 'Markant & Griffig',
      
      sweet_bone_dry: 'Knochentrocken',
      sweet_dry: 'Trocken',
      sweet_off_dry: 'Halbtrocken',
      sweet_sweet: 'Lieblich',
      sweet_noble: 'Edelsüß',
      
      budget_everyday: 'Alltag',
      budget_restaurant: 'Restaurant',
      
      adventure_classic: 'Klassiker bevorzugt',
      adventure_classic_desc: 'Bekannte Weine aus etablierten Regionen',
      adventure_balanced: 'Ausgewogen',
      adventure_balanced_desc: 'Mix aus Klassikern und Neuem',
      adventure_wild: 'Abenteuerlich',
      adventure_wild_desc: 'Überrasche mich mit Wildcards!',
      
      not_logged_in: 'Bitte melde dich an',
      login_button: 'Anmelden'
    },
    en: {
      title: 'My Wine Profile',
      subtitle: 'Personalize your wine recommendations',
      pro_required: 'Pro membership required',
      pro_description: 'The wine profile is an exclusive Pro feature. Become a Pro member to receive personalized recommendations based on your taste.',
      upgrade_button: 'Go Pro Now',
      save: 'Save Profile',
      reset: 'Reset',
      saving: 'Saving...',
      saved: 'Profile saved!',
      
      red_wine_title: '🍷 Red Wine Style',
      red_wine_desc: 'Which red wine style appeals to you?',
      white_wine_title: '🥂 White Wine Character',
      white_wine_desc: 'Which white wine type do you prefer?',
      structure_title: '⚖️ Structure Preferences',
      structure_desc: 'Acidity and tannin',
      sweetness_title: '🍯 Sweetness Level',
      sweetness_desc: 'From bone-dry to noble sweet',
      regions_title: '🗺️ Favorite Regions',
      regions_desc: 'Choose your preferred wine regions',
      budget_title: '💰 Budget Range',
      budget_desc: 'For different occasions',
      no_gos_title: '🚫 No-Gos',
      no_gos_desc: 'What should the AI avoid?',
      dietary_title: '🍽️ Culinary Context',
      dietary_desc: 'What do you like to eat?',
      adventure_title: '🧭 Adventure Factor',
      adventure_desc: 'Classics or bold discoveries?',
      
      red_kraftig: 'Bold & Spicy',
      red_kraftig_desc: 'Bordeaux, Rhône, Barolo',
      red_elegant: 'Fruity & Elegant',
      red_elegant_desc: 'Burgundy, Pinot Noir',
      red_both: 'Both',
      
      white_mineral: 'Mineral & Fresh',
      white_mineral_desc: 'Chablis, Sancerre',
      white_creamy: 'Creamy & Textured',
      white_creamy_desc: 'Meursault, White Burgundy',
      white_aromatic: 'Aromatic & Playful',
      white_aromatic_desc: 'Riesling, Gewürztraminer',
      white_all: 'All Styles',
      
      acidity_label: 'Acidity Tolerance',
      acidity_low: 'Low',
      acidity_medium: 'Medium',
      acidity_high: 'High',
      
      tannin_label: 'Tannin Preference',
      tannin_soft: 'Soft & Silky',
      tannin_medium: 'Medium',
      tannin_bold: 'Bold & Grippy',
      
      sweet_bone_dry: 'Bone Dry',
      sweet_dry: 'Dry',
      sweet_off_dry: 'Off-Dry',
      sweet_sweet: 'Sweet',
      sweet_noble: 'Noble Sweet',
      
      budget_everyday: 'Everyday',
      budget_restaurant: 'Restaurant',
      
      adventure_classic: 'Prefer Classics',
      adventure_classic_desc: 'Known wines from established regions',
      adventure_balanced: 'Balanced',
      adventure_balanced_desc: 'Mix of classics and new discoveries',
      adventure_wild: 'Adventurous',
      adventure_wild_desc: 'Surprise me with wildcards!',
      
      not_logged_in: 'Please log in',
      login_button: 'Log In'
    }
  }[language] || {};

  // Wine regions
  const wineRegions = [
    'Burgund', 'Bordeaux', 'Champagne', 'Rhône', 'Loire', 'Elsass',
    'Toskana', 'Piemont', 'Venetien', 'Sizilien',
    'Rioja', 'Ribera del Duero', 'Priorat',
    'Mosel', 'Rheingau', 'Pfalz', 'Baden',
    'Österreich', 'Schweiz',
    'Napa Valley', 'Sonoma', 'Oregon',
    'Südafrika', 'Australien', 'Neuseeland', 'Chile', 'Argentinien'
  ];

  // No-Go options
  const noGoOptions = [
    { id: 'barrique', label: 'Barrique/Holzausbau' },
    { id: 'schwefel', label: 'Hoher Schwefelgehalt' },
    { id: 'chardonnay', label: 'Chardonnay' },
    { id: 'sauvignon_blanc', label: 'Sauvignon Blanc' },
    { id: 'merlot', label: 'Merlot' },
    { id: 'cabernet', label: 'Cabernet Sauvignon' },
    { id: 'pinot_grigio', label: 'Pinot Grigio' },
    { id: 'prosecco', label: 'Prosecco' },
    { id: 'natural_wine', label: 'Naturwein' },
    { id: 'high_alcohol', label: 'Hoher Alkohol (>14%)' }
  ];

  // Dietary options
  const dietaryOptions = [
    { id: 'vegetarisch', label: '🥗 Vegetarisch' },
    { id: 'vegan', label: '🌱 Vegan' },
    { id: 'fleisch', label: '🥩 Fleisch-Liebhaber' },
    { id: 'fisch', label: '🐟 Fisch & Meeresfrüchte' },
    { id: 'asiatisch', label: '🍜 Asiatische Küche' },
    { id: 'mediterran', label: '🫒 Mediterran' },
    { id: 'scharf', label: '🌶️ Scharfes Essen' },
    { id: 'kaese', label: '🧀 Käse-Liebhaber' }
  ];

  // Budget options
  const budgetEveryday = [
    { id: 'unter_10', label: 'Unter 10€' },
    { id: '10_20', label: '10-20€' },
    { id: '20_35', label: '20-35€' },
    { id: '35_50', label: '35-50€' },
    { id: 'ueber_50', label: 'Über 50€' }
  ];

  const budgetRestaurant = [
    { id: 'unter_30', label: 'Unter 30€' },
    { id: '30_50', label: '30-50€' },
    { id: '50_80', label: '50-80€' },
    { id: '80_120', label: '80-120€' },
    { id: 'ueber_120', label: 'Über 120€' }
  ];

  // Load profile
  useEffect(() => {
    const loadProfile = async () => {
      if (!user || user.plan !== 'pro') {
        setLoading(false);
        return;
      }

      try {
        const token = localStorage.getItem('wine_auth_token');
        const response = await fetch(`${API}/profile/wine`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          const data = await response.json();
          setProfile(prev => ({ ...prev, ...data }));
        }
      } catch (error) {
        console.error('Error loading profile:', error);
      } finally {
        setLoading(false);
      }
    };

    loadProfile();
  }, [user]);

  // Save profile
  const handleSave = async () => {
    setSaving(true);
    try {
      const token = localStorage.getItem('wine_auth_token');
      const response = await fetch(`${API}/profile/wine`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(profile)
      });

      if (response.ok) {
        toast.success(t.saved || 'Profil gespeichert!');
      } else {
        const error = await response.json();
        toast.error(error.detail || 'Fehler beim Speichern');
      }
    } catch (error) {
      toast.error('Verbindungsfehler');
    } finally {
      setSaving(false);
    }
  };

  // Reset profile
  const handleReset = async () => {
    try {
      const token = localStorage.getItem('wine_auth_token');
      await fetch(`${API}/profile/wine`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      setProfile({
        red_wine_style: null,
        white_wine_style: null,
        acidity_tolerance: null,
        tannin_preference: null,
        sweetness_preference: null,
        favorite_regions: [],
        budget_everyday: null,
        budget_restaurant: null,
        no_gos: [],
        dietary_preferences: [],
        adventure_level: null
      });

      toast.success('Profil zurückgesetzt');
    } catch (error) {
      toast.error('Fehler beim Zurücksetzen');
    }
  };

  // Toggle array item
  const toggleArrayItem = (field, item) => {
    setProfile(prev => {
      const arr = prev[field] || [];
      if (arr.includes(item)) {
        return { ...prev, [field]: arr.filter(i => i !== item) };
      } else {
        return { ...prev, [field]: [...arr, item] };
      }
    });
  };

  // Not logged in
  if (!user) {
    return (
      <div className="min-h-screen bg-background py-12 px-4">
        <div className="container mx-auto max-w-2xl text-center">
          <Lock className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
          <h1 className="text-2xl font-bold mb-2">{t.not_logged_in}</h1>
          <Button onClick={() => navigate('/login')} className="mt-4">
            {t.login_button}
          </Button>
        </div>
      </div>
    );
  }

  // Not Pro
  if (user.plan !== 'pro') {
    return (
      <div className="min-h-screen bg-background py-12 px-4">
        <div className="container mx-auto max-w-2xl">
          <Card className="border-2 border-amber-400/50 bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-950/20 dark:to-orange-950/20">
            <CardContent className="p-8 text-center">
              <Crown className="w-16 h-16 mx-auto text-amber-500 mb-4" />
              <h1 className="text-2xl font-bold mb-2">{t.pro_required}</h1>
              <p className="text-muted-foreground mb-6">{t.pro_description}</p>
              <Button 
                onClick={() => navigate('/pricing')} 
                className="bg-amber-500 hover:bg-amber-600 text-white"
              >
                <Crown className="mr-2 h-4 w-4" />
                {t.upgrade_button}
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  // Style option component
  const StyleOption = ({ value, currentValue, onChange, icon: Icon, title, desc }) => (
    <button
      onClick={() => onChange(value)}
      className={`p-4 rounded-lg border-2 text-left transition-all ${
        currentValue === value 
          ? 'border-primary bg-primary/5' 
          : 'border-border hover:border-primary/50'
      }`}
    >
      <div className="flex items-start gap-3">
        {Icon && <Icon className={`w-5 h-5 mt-0.5 ${currentValue === value ? 'text-primary' : 'text-muted-foreground'}`} />}
        <div>
          <div className={`font-medium ${currentValue === value ? 'text-primary' : ''}`}>{title}</div>
          {desc && <div className="text-sm text-muted-foreground">{desc}</div>}
        </div>
      </div>
    </button>
  );

  return (
    <div className="min-h-screen bg-background py-8 px-4 pb-24">
      <div className="container mx-auto max-w-3xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-2 rounded-full mb-4">
            <Crown className="w-4 h-4" />
            <span className="text-sm font-medium">Pro Feature</span>
          </div>
          <h1 className="text-3xl font-bold mb-2">{t.title}</h1>
          <p className="text-muted-foreground">{t.subtitle}</p>
        </div>

        <div className="space-y-6">
          {/* Red Wine Style */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">{t.red_wine_title}</CardTitle>
              <CardDescription>{t.red_wine_desc}</CardDescription>
            </CardHeader>
            <CardContent className="grid gap-3 sm:grid-cols-3">
              <StyleOption
                value="kraftig_wurzig"
                currentValue={profile.red_wine_style}
                onChange={(v) => setProfile(p => ({ ...p, red_wine_style: v }))}
                icon={Wine}
                title={t.red_kraftig}
                desc={t.red_kraftig_desc}
              />
              <StyleOption
                value="fruchtig_elegant"
                currentValue={profile.red_wine_style}
                onChange={(v) => setProfile(p => ({ ...p, red_wine_style: v }))}
                icon={Grape}
                title={t.red_elegant}
                desc={t.red_elegant_desc}
              />
              <StyleOption
                value="beides"
                currentValue={profile.red_wine_style}
                onChange={(v) => setProfile(p => ({ ...p, red_wine_style: v }))}
                icon={Sparkles}
                title={t.red_both}
              />
            </CardContent>
          </Card>

          {/* White Wine Style */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">{t.white_wine_title}</CardTitle>
              <CardDescription>{t.white_wine_desc}</CardDescription>
            </CardHeader>
            <CardContent className="grid gap-3 sm:grid-cols-2">
              <StyleOption
                value="mineralisch_frisch"
                currentValue={profile.white_wine_style}
                onChange={(v) => setProfile(p => ({ ...p, white_wine_style: v }))}
                icon={Mountain}
                title={t.white_mineral}
                desc={t.white_mineral_desc}
              />
              <StyleOption
                value="cremig_textur"
                currentValue={profile.white_wine_style}
                onChange={(v) => setProfile(p => ({ ...p, white_wine_style: v }))}
                icon={Droplets}
                title={t.white_creamy}
                desc={t.white_creamy_desc}
              />
              <StyleOption
                value="aromatisch_verspielt"
                currentValue={profile.white_wine_style}
                onChange={(v) => setProfile(p => ({ ...p, white_wine_style: v }))}
                icon={Sparkles}
                title={t.white_aromatic}
                desc={t.white_aromatic_desc}
              />
              <StyleOption
                value="beides"
                currentValue={profile.white_wine_style}
                onChange={(v) => setProfile(p => ({ ...p, white_wine_style: v }))}
                title={t.white_all}
              />
            </CardContent>
          </Card>

          {/* Structure Preferences */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">{t.structure_title}</CardTitle>
              <CardDescription>{t.structure_desc}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Acidity */}
              <div>
                <label className="text-sm font-medium mb-3 block">{t.acidity_label}</label>
                <div className="grid grid-cols-3 gap-2">
                  {['niedrig', 'mittel', 'hoch'].map((level) => (
                    <button
                      key={level}
                      onClick={() => setProfile(p => ({ ...p, acidity_tolerance: level }))}
                      className={`py-2 px-4 rounded-lg border transition-all ${
                        profile.acidity_tolerance === level
                          ? 'border-primary bg-primary text-primary-foreground'
                          : 'border-border hover:border-primary/50'
                      }`}
                    >
                      {t[`acidity_${level}`] || level}
                    </button>
                  ))}
                </div>
              </div>

              {/* Tannin */}
              <div>
                <label className="text-sm font-medium mb-3 block">{t.tannin_label}</label>
                <div className="grid grid-cols-3 gap-2">
                  {['weich_seidig', 'mittel', 'markant_griffig'].map((level) => (
                    <button
                      key={level}
                      onClick={() => setProfile(p => ({ ...p, tannin_preference: level }))}
                      className={`py-2 px-4 rounded-lg border transition-all text-sm ${
                        profile.tannin_preference === level
                          ? 'border-primary bg-primary text-primary-foreground'
                          : 'border-border hover:border-primary/50'
                      }`}
                    >
                      {level === 'weich_seidig' ? t.tannin_soft : level === 'mittel' ? t.tannin_medium : t.tannin_bold}
                    </button>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Sweetness */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">{t.sweetness_title}</CardTitle>
              <CardDescription>{t.sweetness_desc}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {[
                  { id: 'knochentrocken', label: t.sweet_bone_dry },
                  { id: 'trocken', label: t.sweet_dry },
                  { id: 'halbtrocken', label: t.sweet_off_dry },
                  { id: 'lieblich', label: t.sweet_sweet },
                  { id: 'edelsuss', label: t.sweet_noble }
                ].map((option) => (
                  <button
                    key={option.id}
                    onClick={() => setProfile(p => ({ ...p, sweetness_preference: option.id }))}
                    className={`py-2 px-4 rounded-full border transition-all ${
                      profile.sweetness_preference === option.id
                        ? 'border-primary bg-primary text-primary-foreground'
                        : 'border-border hover:border-primary/50'
                    }`}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Favorite Regions */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">{t.regions_title}</CardTitle>
              <CardDescription>{t.regions_desc}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {wineRegions.map((region) => (
                  <button
                    key={region}
                    onClick={() => toggleArrayItem('favorite_regions', region)}
                    className={`py-1.5 px-3 rounded-full border text-sm transition-all ${
                      profile.favorite_regions?.includes(region)
                        ? 'border-primary bg-primary text-primary-foreground'
                        : 'border-border hover:border-primary/50'
                    }`}
                  >
                    {region}
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Budget */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">{t.budget_title}</CardTitle>
              <CardDescription>{t.budget_desc}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block flex items-center gap-2">
                  <Euro className="w-4 h-4" />
                  {t.budget_everyday}
                </label>
                <div className="flex flex-wrap gap-2">
                  {budgetEveryday.map((option) => (
                    <button
                      key={option.id}
                      onClick={() => setProfile(p => ({ ...p, budget_everyday: option.id }))}
                      className={`py-1.5 px-3 rounded-full border text-sm transition-all ${
                        profile.budget_everyday === option.id
                          ? 'border-green-500 bg-green-500 text-white'
                          : 'border-border hover:border-green-500/50'
                      }`}
                    >
                      {option.label}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block flex items-center gap-2">
                  <Utensils className="w-4 h-4" />
                  {t.budget_restaurant}
                </label>
                <div className="flex flex-wrap gap-2">
                  {budgetRestaurant.map((option) => (
                    <button
                      key={option.id}
                      onClick={() => setProfile(p => ({ ...p, budget_restaurant: option.id }))}
                      className={`py-1.5 px-3 rounded-full border text-sm transition-all ${
                        profile.budget_restaurant === option.id
                          ? 'border-amber-500 bg-amber-500 text-white'
                          : 'border-border hover:border-amber-500/50'
                      }`}
                    >
                      {option.label}
                    </button>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* No-Gos */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">{t.no_gos_title}</CardTitle>
              <CardDescription>{t.no_gos_desc}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {noGoOptions.map((option) => (
                  <button
                    key={option.id}
                    onClick={() => toggleArrayItem('no_gos', option.id)}
                    className={`py-1.5 px-3 rounded-full border text-sm transition-all ${
                      profile.no_gos?.includes(option.id)
                        ? 'border-red-500 bg-red-500 text-white'
                        : 'border-border hover:border-red-500/50'
                    }`}
                  >
                    {profile.no_gos?.includes(option.id) && <X className="w-3 h-3 inline mr-1" />}
                    {option.label}
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Dietary Preferences */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">{t.dietary_title}</CardTitle>
              <CardDescription>{t.dietary_desc}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {dietaryOptions.map((option) => (
                  <button
                    key={option.id}
                    onClick={() => toggleArrayItem('dietary_preferences', option.id)}
                    className={`py-2 px-4 rounded-full border transition-all ${
                      profile.dietary_preferences?.includes(option.id)
                        ? 'border-primary bg-primary text-primary-foreground'
                        : 'border-border hover:border-primary/50'
                    }`}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Adventure Level */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">{t.adventure_title}</CardTitle>
              <CardDescription>{t.adventure_desc}</CardDescription>
            </CardHeader>
            <CardContent className="grid gap-3 sm:grid-cols-3">
              <StyleOption
                value="klassiker"
                currentValue={profile.adventure_level}
                onChange={(v) => setProfile(p => ({ ...p, adventure_level: v }))}
                icon={Wine}
                title={t.adventure_classic}
                desc={t.adventure_classic_desc}
              />
              <StyleOption
                value="ausgewogen"
                currentValue={profile.adventure_level}
                onChange={(v) => setProfile(p => ({ ...p, adventure_level: v }))}
                icon={Compass}
                title={t.adventure_balanced}
                desc={t.adventure_balanced_desc}
              />
              <StyleOption
                value="abenteuerlich"
                currentValue={profile.adventure_level}
                onChange={(v) => setProfile(p => ({ ...p, adventure_level: v }))}
                icon={Sparkles}
                title={t.adventure_wild}
                desc={t.adventure_wild_desc}
              />
            </CardContent>
          </Card>
        </div>

        {/* Fixed Save Button - positioned above navigation */}
        <div className="fixed bottom-20 md:bottom-24 left-0 right-0 bg-background/95 backdrop-blur border-t p-4 z-40">
          <div className="container mx-auto max-w-3xl flex gap-3">
            <Button
              variant="outline"
              onClick={handleReset}
              className="flex-shrink-0"
            >
              <RotateCcw className="w-4 h-4 mr-2" />
              {t.reset}
            </Button>
            <Button
              onClick={handleSave}
              disabled={saving}
              className="flex-1 bg-primary"
            >
              {saving ? (
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              ) : (
                <Save className="w-4 h-4 mr-2" />
              )}
              {saving ? t.saving : t.save}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WineProfilePage;
