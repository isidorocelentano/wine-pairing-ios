import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { MapPin, Wine, Search, X, Globe } from 'lucide-react';
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
      const response = await axios.get(`${API}/regional-pairings/countries`);
      setCountries(response.data);
    } catch (error) {
      console.error('Error fetching countries:', error);
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

  const fetchPairings = async () => {
    setLoading(true);
    try {
      const params = {};
      if (selectedCountry) params.country = selectedCountry;
      if (selectedRegion) params.region = selectedRegion;
      if (searchQuery.trim()) params.search = searchQuery.trim();

      const response = await axios.get(`${API}/regional-pairings`, { params });
      setPairings(response.data);
    } catch (error) {
      console.error('Error fetching pairings:', error);
    } finally {
      setLoading(false);
    }
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

  return (
    <>
      <SEO
        title={t('regional_title')}
        description={t('regional_intro')}
        url="https://wine-pairing.online/sommelier-kompass"
      />

      <div className="min-h-screen pb-20 md:pb-24 pt-6 md:pt-8 px-4 md:px-12 lg:px-24" data-testid="sommelier-kompass-page">
        <div className="container mx-auto max-w-6xl">
          {/* Hero Section */}
          <header className="text-center mb-8 md:mb-12">
            <p className="text-accent font-accent text-sm tracking-widest uppercase mb-2">{t('regional_tagline')}</p>
            <h1 className="text-2xl md:text-4xl font-semibold tracking-tight mb-3">{t('regional_title')}</h1>
            <p className="text-lg md:text-xl text-muted-foreground font-light mb-4">{t('regional_subtitle')}</p>
            <p className="text-muted-foreground max-w-3xl mx-auto text-sm md:text-base leading-relaxed">
              {t('regional_intro')}
            </p>
          </header>

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
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {pairings.map((pairing) => (
                <Card
                  key={pairing.id}
                  className="bg-card/50 backdrop-blur-sm border-border/50 overflow-hidden hover:shadow-lg transition-shadow"
                >
                  {pairing.image_url && (
                    <div className="h-40 overflow-hidden">
                      <img
                        src={pairing.image_url}
                        alt={pairing.dish}
                        className="w-full h-full object-cover"
                      />
                    </div>
                  )}
                  <CardHeader className="pb-3">
                    <div className="flex items-start justify-between mb-2">
                      <Badge variant="outline" className="text-xs">
                        {pairing.country_emoji} {pairing.region}
                      </Badge>
                    </div>
                    <CardTitle className="text-lg">{pairing.dish}</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="bg-secondary/30 rounded-lg p-3">
                      <div className="flex items-center gap-2 mb-1">
                        <Wine className="w-4 h-4 text-accent" />
                        <span className="text-xs font-medium text-accent">{t('regional_wine_pairing')}</span>
                      </div>
                      <p className="font-medium text-sm">{pairing.wine_name}</p>
                      <p className="text-xs text-muted-foreground mt-1">{pairing.wine_type}</p>
                    </div>
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
