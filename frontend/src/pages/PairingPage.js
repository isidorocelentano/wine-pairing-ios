import React, { useState, useEffect, useCallback } from 'react';
import axios from "axios";
import { toast } from 'sonner';
import { Wine, Loader2, Search, ExternalLink, Beaker } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useLanguage } from "@/contexts/LanguageContext";
import { useNavigate, Link } from 'react-router-dom';
import VoiceInputButton from "@/components/VoiceInputButton";

import { API_URL as BACKEND_URL, API } from '@/config/api';

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

const PairingPage = () => {
  const { t, language } = useLanguage();
  const navigate = useNavigate();
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
  
  // Handle wine card click - go directly to wine database
  const handleWineClick = (wine) => {
    // Extract the main wine name (before parentheses or commas)
    const searchTerm = wine.name.split('(')[0].split(',')[0].trim();
    navigate(`/wine-database?search=${encodeURIComponent(searchTerm)}`);
  };
  
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
        !(d.trend_cuisines || []).some((tc) => tc.toLowerCase() === dishTrendFilter.toLowerCase())
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
                  
                  // Main heading - more flexible regex to catch various formats
                  // Matches: "1. **🍷 HAUPTEMPFEHLUNG**", "1. **HAUPTEMPFEHLUNG**", "**🍷 HAUPTEMPFEHLUNG**", etc.
                  if (trimmedLine.match(/HAUPTEMPFEHLUNG|TOP RECOMMENDATION|RECOMMANDATION PRINCIPALE/i)) {
                    if (currentSection) {
                      currentSection.wines = wines;
                      sections.push(currentSection);
                    }
                    currentSection = { title: '🍷 Hauptempfehlung', type: 'main', intro: '', wines: [] };
                    wines = [];
                    currentIntro = '';
                  }
                  // Alternative Options heading
                  else if (trimmedLine.match(/Alternative.*Option|Options.*Alternative/i)) {
                    if (currentSection) {
                      currentSection.intro = currentIntro;
                      currentSection.wines = wines;
                      sections.push(currentSection);
                    }
                    currentSection = { title: '🔄 Alternative Optionen', type: 'alternatives', intro: '', wines: [] };
                    wines = [];
                    currentIntro = '';
                  }
                  // Sub-heading for wine type categories (Bester Weintyp, Schaumwein, etc.)
                  else if (trimmedLine.match(/^\*\*.*(?:Weintyp|wein|Wine Type|Vin).*:/i) || trimmedLine.match(/^\*\*(?:Schaumwein|Rotwein|Weißwein|Sparkling|Red Wine|White Wine)/i)) {
                    // Extract category name
                    const categoryMatch = trimmedLine.match(/\*\*([^*]+)\*\*/);
                    if (categoryMatch) {
                      currentIntro = categoryMatch[1].replace(/:/g, '').trim();
                    }
                  }
                  // Wine recommendation (starts with - or *)
                  else if (trimmedLine.match(/^[-*]\s+\*\*(.+?)\*\*/)) {
                    const wineMatch = trimmedLine.match(/^[-*]\s+\*\*(.+?)\*\*\s*[-–—:]\s*(.+)/);
                    if (wineMatch) {
                      wines.push({
                        name: wineMatch[1].trim(),
                        description: wineMatch[2].trim(),
                        category: currentIntro
                      });
                    }
                  }
                  // Introduction text (not a wine, not a heading, not "Bester Weintyp")
                  else if (trimmedLine && !trimmedLine.match(/^[-*#\d]/) && !trimmedLine.match(/^---/) && !trimmedLine.match(/^\*\*/) && currentSection && wines.length === 0) {
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
                            const fullDescription = wine.description || '';

                            return (
                              <Card
                                key={wineIdx}
                                className="border-2 border-border hover:border-primary hover:shadow-lg transition-all cursor-pointer group"
                                onClick={() => handleWineClick({ ...wine, fullDescription })}
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

                                  {/* Tap hint */}
                                  <p className="text-xs text-primary/60 mt-1 flex items-center gap-1">
                                    <ExternalLink className="w-3 h-3" />
                                    {language === 'de' ? '→ In Wein-Datenbank suchen' : language === 'fr' ? '→ Rechercher dans la base' : '→ Search in wine database'}
                                  </p>
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
              
              {/* Pairing Science CTA - After Results */}
              <div className="mt-8 pt-6 border-t border-border/50">
                <Link 
                  to="/wie-wir-pairen"
                  state={{ 
                    pairing: {
                      dish: result.dish,
                      recommendation: result.recommendation,
                      why_explanation: result.why_explanation
                    }
                  }}
                  className="block p-4 md:p-5 rounded-xl bg-gradient-to-r from-primary/5 via-accent/5 to-primary/10 border border-primary/20 hover:border-primary/40 transition-all group"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 md:w-12 md:h-12 rounded-full bg-primary/15 flex items-center justify-center flex-shrink-0 group-hover:bg-primary/25 transition-colors">
                      <Beaker className="w-5 h-5 md:w-6 md:h-6 text-primary" />
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-sm md:text-base text-primary">
                        {language === 'de' ? `Warum passt das zu "${result.dish}"?` : language === 'en' ? `Why does this match "${result.dish}"?` : `Pourquoi ça correspond à "${result.dish}"?`}
                      </p>
                      <p className="text-xs md:text-sm text-muted-foreground mt-0.5">
                        {language === 'de' 
                          ? 'Analyse basierend auf unseren 12 Pairing-Variablen ansehen →' 
                          : language === 'en' 
                          ? 'View analysis based on our 12 pairing variables →'
                          : 'Voir l\'analyse basée sur nos 12 variables d\'accord →'}
                      </p>
                    </div>
                  </div>
                </Link>
              </div>
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

export default PairingPage;
