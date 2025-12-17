import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { MapPin, Wine, Search, X, Globe, Sparkles, GraduationCap } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useLanguage } from '@/contexts/LanguageContext';
import { SEO } from '@/components/SEO';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const SommelierKompassPage = () => {
  const { t, language } = useLanguage();
  const [countries, setCountries] = useState([]);
  const [regions, setRegions] = useState([]);
  const [pairings, setPairings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  
  // Pagination
  const [totalPairings, setTotalPairings] = useState(0);
  const [hasMore, setHasMore] = useState(false);
  const ITEMS_PER_PAGE = 50;
  
  // Filters
  const [selectedCountry, setSelectedCountry] = useState('');
  const [selectedRegion, setSelectedRegion] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  
  // Country data (intro & image)
  const [countryData, setCountryData] = useState(null);

  // Fetch countries on mount
  useEffect(() => {
    fetchCountries();
  }, []);

  // Fetch regions when country changes
  useEffect(() => {
    if (selectedCountry) {
      fetchRegions(selectedCountry);
    } else {
      setRegions([]);
      setSelectedRegion('');
    }
  }, [selectedCountry]);

  // Fetch pairings when filters change
  useEffect(() => {
    fetchPairings();
  }, [selectedCountry, selectedRegion, searchQuery]);

  const fetchCountries = async () => {
    try {
      console.log('Fetching countries from:', `${API}/regional-pairings/countries`);
      const response = await axios.get(`${API}/regional-pairings/countries`);
      console.log('Received countries:', response.data.length);
      setCountries(response.data || []);
    } catch (error) {
      console.error('Error fetching countries:', error);
      console.error('Error details:', error.response?.data || error.message);
      setCountries([]);
    }
  };

  const fetchRegions = async (country) => {
    try {
      const response = await axios.get(`${API}/regional-pairings/regions`, {
        params: { country }
      });
      setRegions(response.data);
    } catch (error) {
      console.error('Error fetching regions:', error);
    }
  };

  const fetchPairings = async (loadMore = false) => {
    if (loadMore) {
      setLoadingMore(true);
    } else {
      setLoading(true);
    }
    
    try {
      const params = {
        limit: ITEMS_PER_PAGE,
        skip: loadMore ? pairings.length : 0
      };
      if (selectedCountry) params.country = selectedCountry;
      if (selectedRegion) params.region = selectedRegion;
      if (searchQuery.trim()) params.search = searchQuery.trim();

      console.log('Fetching pairings with params:', params);
      const response = await axios.get(`${API}/regional-pairings`, { params });
      
      const { pairings: newPairings, total, has_more } = response.data;
      console.log(`Received ${newPairings.length} pairings, total: ${total}, has_more: ${has_more}`);
      
      if (loadMore) {
        // Append to existing pairings
        setPairings(prev => [...prev, ...newPairings]);
      } else {
        // Replace pairings
        setPairings(newPairings || []);
      }
      
      setTotalPairings(total);
      setHasMore(has_more);
      
      // Extract country data from first pairing if country is selected
      if (newPairings && newPairings.length > 0 && selectedCountry && !loadMore) {
        const firstPairing = newPairings[0];
        setCountryData({
          intro: firstPairing.country_intro,
          intro_en: firstPairing.country_intro_en,
          intro_fr: firstPairing.country_intro_fr,
          image_url: firstPairing.country_image_url
        });
      } else if (!loadMore) {
        setCountryData(null);
      }
    } catch (error) {
      console.error('Error fetching pairings:', error);
      console.error('Error details:', error.response?.data || error.message);
      if (!loadMore) {
        setPairings([]);
        setTotalPairings(0);
        setHasMore(false);
      }
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  };
  
  const loadMorePairings = () => {
    fetchPairings(true);
  };

  const clearFilters = () => {
    setSelectedCountry('');
    setSelectedRegion('');
    setSearchQuery('');
  };

  const hasActiveFilters = selectedCountry || selectedRegion || searchQuery;

  // Get localized country name
  const getLocalizedCountry = (country) => {
    if (language === 'en') return country.country_en;
    if (language === 'fr') return country.country_fr;
    return country.country;
  };
  
  // Get localized text
  const getLocalizedText = (item, field) => {
    if (language === 'en' && item[`${field}_en`]) return item[`${field}_en`];
    if (language === 'fr' && item[`${field}_fr`]) return item[`${field}_fr`];
    return item[field] || '';
  };

  return (
    <>
      <SEO
        title={t('regional_title')}
        description={t('regional_intro')}
        url="https://wine-pairing.online/sommelier-kompass"
      />

      <div className="min-h-screen pb-20 md:pb-24 pt-6 md:pt-8 px-4 md:px-12 lg:px-24" data-testid="sommelier-kompass-page">
        <div className="container mx-auto max-w-6xl">
          {/* Hero Section with International Image */}
          <div className="mb-8 md:mb-12">
            {/* International Hero Image - shown when no country selected */}
            {!selectedCountry && (
              <div className="mb-8 rounded-xl overflow-hidden">
                <img
                  src="https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/my8kl803_WINE-PAIRING.ONLINE%20SOMMELIER%20CLAUDE%20%20INTERNATIONAL.png"
                  alt="Sommelier Kompass International"
                  className="w-full h-48 md:h-72 object-cover"
                />
              </div>
            )}
            
            <header className="text-center">
              <p className="text-accent font-accent text-sm tracking-widest uppercase mb-2">{t('regional_tagline')}</p>
              <h1 className="text-2xl md:text-4xl font-semibold tracking-tight mb-3">{t('regional_title')}</h1>
              <p className="text-lg md:text-xl text-muted-foreground font-light mb-4">{t('regional_subtitle')}</p>
              <p className="text-muted-foreground max-w-3xl mx-auto text-sm md:text-base leading-relaxed">
                {t('regional_intro')}
              </p>
            </header>
          </div>

          {/* Country Grid - Visual Selection */}
          <div className="mb-8">
            <h2 className="text-xl font-medium mb-4 flex items-center gap-2">
              <Globe className="w-5 h-5 text-accent" />
              {t('regional_filter_all_countries')}
            </h2>
            <div className="grid grid-cols-3 md:grid-cols-5 lg:grid-cols-9 gap-3">
              {countries.map((country) => (
                <button
                  key={country.country}
                  onClick={() => setSelectedCountry(country.country === selectedCountry ? '' : country.country)}
                  className={`p-4 rounded-lg border-2 transition-all hover:scale-105 ${
                    selectedCountry === country.country
                      ? 'border-accent bg-accent/10'
                      : 'border-border hover:border-accent/50'
                  }`}
                >
                  <div className="text-3xl md:text-4xl mb-1">{country.country_emoji}</div>
                  <div className="text-xs text-center font-medium">{country.count}</div>
                </button>
              ))}
            </div>
          </div>
          
          {/* Country Hero - Only shown when country is selected */}
          {selectedCountry && countryData && (
            <Card className="mb-6 overflow-hidden border-accent/20">
              {countryData.image_url && (
                <div className="h-48 md:h-64 overflow-hidden">
                  <img
                    src={countryData.image_url}
                    alt={selectedCountry}
                    className="w-full h-full object-cover"
                  />
                </div>
              )}
              <CardContent className="p-6">
                <p className="text-muted-foreground leading-relaxed">
                  {language === 'en' && countryData.intro_en ? countryData.intro_en :
                   language === 'fr' && countryData.intro_fr ? countryData.intro_fr :
                   countryData.intro}
                </p>
              </CardContent>
            </Card>
          )}

          {/* Filters */}
          <Card className="mb-6 bg-card/50 backdrop-blur-sm border-border/50">
            <CardContent className="p-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Country Dropdown (redundant but useful) */}
                <div>
                  <Select value={selectedCountry || "all"} onValueChange={(v) => setSelectedCountry(v === "all" ? "" : v)}>
                    <SelectTrigger>
                      <SelectValue placeholder={t('regional_filter_country')} />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">{t('regional_filter_all_countries')}</SelectItem>
                      {countries.map((country) => (
                        <SelectItem key={country.country} value={country.country}>
                          {country.country_emoji} {getLocalizedCountry(country)}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Region Dropdown */}
                <div>
                  <Select
                    value={selectedRegion || "all"}
                    onValueChange={(v) => setSelectedRegion(v === "all" ? "" : v)}
                    disabled={!selectedCountry}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder={t('regional_filter_region')} />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">{t('regional_filter_all_regions')}</SelectItem>
                      {regions.map((region) => (
                        <SelectItem key={region.region} value={region.region}>
                          {region.region} ({region.count})
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Search Input */}
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder={t('regional_filter_search')}
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                  {searchQuery && (
                    <button
                      onClick={() => setSearchQuery('')}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </div>

              {/* Clear Filters Button */}
              {hasActiveFilters && (
                <div className="mt-4 flex items-center justify-between">
                  <p className="text-sm text-muted-foreground">
                    {pairings.length} {t('regional_results')}
                  </p>
                  <Button variant="outline" size="sm" onClick={clearFilters}>
                    <X className="w-4 h-4 mr-2" />
                    {t('regional_clear_filters')}
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Results */}
          {loading ? (
            <div className="text-center py-12">
              <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-accent border-r-transparent"></div>
              <p className="mt-4 text-muted-foreground">{t('loading')}</p>
            </div>
          ) : pairings.length === 0 ? (
            <Card className="bg-secondary/30 border-dashed border-2 border-border">
              <CardContent className="py-16 text-center">
                <MapPin className="h-16 w-16 mx-auto mb-4 text-muted-foreground" strokeWidth={1} />
                <h3 className="text-xl font-medium mb-2">{t('regional_no_results')}</h3>
                <p className="text-muted-foreground mb-6">{t('regional_no_results_desc')}</p>
                {hasActiveFilters && (
                  <Button onClick={clearFilters} className="rounded-full">
                    {t('regional_clear_filters')}
                  </Button>
                )}
              </CardContent>
            </Card>
          ) : (
            <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {pairings.map((pairing) => (
                <Card
                  key={pairing.id}
                  className="bg-card/50 backdrop-blur-sm border-border/50 overflow-hidden hover:shadow-lg transition-shadow flex flex-col"
                >
                  <CardHeader className="pb-3">
                    <div className="flex items-start justify-between mb-2">
                      <Badge variant="outline" className="text-xs">
                        {pairing.country_emoji} {pairing.region}
                      </Badge>
                    </div>
                    <CardTitle className="text-lg mb-2">{pairing.dish}</CardTitle>
                    {getLocalizedText(pairing, 'dish_description') && (
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        {getLocalizedText(pairing, 'dish_description')}
                      </p>
                    )}
                  </CardHeader>
                  <CardContent className="space-y-3 mt-auto">
                    {/* International Wine Recommendation (Safe Choice) */}
                    <div className="bg-secondary/30 rounded-lg p-3 space-y-2">
                      <div className="flex items-center gap-2">
                        <Wine className="w-4 h-4 text-accent" />
                        <span className="text-xs font-medium text-accent">
                          {pairing.local_wine_name ? (language === 'en' ? '🌍 International Classic' : language === 'fr' ? '🌍 Classique International' : '🌍 Internationaler Klassiker') : t('regional_wine_pairing')}
                        </span>
                      </div>
                      <p className="font-medium text-sm">{pairing.wine_name}</p>
                      <p className="text-xs text-muted-foreground">{pairing.wine_type}</p>
                      {getLocalizedText(pairing, 'wine_description') && (
                        <p className="text-xs text-muted-foreground leading-relaxed pt-2 border-t border-border/50">
                          {getLocalizedText(pairing, 'wine_description')}
                        </p>
                      )}
                    </div>
                    
                    {/* Local Wine Alternative (Discovery) - Only show if available */}
                    {pairing.local_wine_name && (
                      <div className="bg-accent/10 border border-accent/30 rounded-lg p-3 space-y-2">
                        <div className="flex items-center gap-2">
                          <Sparkles className="w-4 h-4 text-amber-500" />
                          <span className="text-xs font-medium text-amber-600 dark:text-amber-400">
                            {language === 'en' ? '✨ Local Discovery' : language === 'fr' ? '✨ Découverte Locale' : '✨ Lokale Entdeckung'}
                          </span>
                        </div>
                        <p className="font-medium text-sm">{pairing.local_wine_name}</p>
                        <p className="text-xs text-muted-foreground">{pairing.local_wine_type}</p>
                        {getLocalizedText(pairing, 'local_wine_description') && (
                          <p className="text-xs text-muted-foreground leading-relaxed pt-2 border-t border-amber-500/20">
                            {getLocalizedText(pairing, 'local_wine_description')}
                          </p>
                        )}
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default SommelierKompassPage;
