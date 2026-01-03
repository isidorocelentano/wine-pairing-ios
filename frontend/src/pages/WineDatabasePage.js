import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import axios from 'axios';
import { Wine, Search, Filter, ChevronDown, Heart, Plus, Loader2, X, Bookmark, ArrowLeft, Sparkles, Grape, Thermometer, Calendar, UtensilsCrossed } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useLanguage } from '@/contexts/LanguageContext';
import { SEO } from '@/components/SEO';
import { toast } from 'sonner';

import { API_URL as BACKEND_URL, API } from '@/config/api';

const WineDatabasePage = () => {
  const { t, language } = useLanguage();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  
  // Get initial values from URL
  const initialSearch = searchParams.get('search') || '';
  const initialCountry = searchParams.get('country') || 'all';
  const initialRegion = searchParams.get('region') || 'all';
  
  // Helper function to get description in current language
  const getDescription = (wine) => {
    if (language === 'en') return wine.description_en || wine.description_de || wine.description;
    if (language === 'fr') return wine.description_fr || wine.description_de || wine.description;
    return wine.description_de || wine.description;
  };
  
  // Helper function to get food pairings in current language
  const getFoodPairings = (wine) => {
    if (language === 'en') return wine.food_pairings_en || wine.food_pairings_de || wine.food_pairings || [];
    if (language === 'fr') return wine.food_pairings_fr || wine.food_pairings_de || wine.food_pairings || [];
    return wine.food_pairings_de || wine.food_pairings || [];
  };
  
  const [wines, setWines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState(initialSearch);
  const [filters, setFilters] = useState({
    country: initialCountry,
    region: initialRegion,
    appellation: 'all',
    grape_variety: 'all',
    wine_color: 'all',
    price_category: 'all'
  });
  const [availableFilters, setAvailableFilters] = useState({});
  const [showFilters, setShowFilters] = useState(false);
  const [selectedWine, setSelectedWine] = useState(null);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [favorites, setFavorites] = useState(new Set());
  const [wishlist, setWishlist] = useState(new Set());
  
  // AI-enriched wines state
  const [activeTab, setActiveTab] = useState('database');
  const [enrichedWines, setEnrichedWines] = useState([]);
  const [enrichedLoading, setEnrichedLoading] = useState(false);
  const [enrichedSearchQuery, setEnrichedSearchQuery] = useState('');
  const [enrichedTotal, setEnrichedTotal] = useState(0);
  const [selectedEnrichedWine, setSelectedEnrichedWine] = useState(null);

  // Update filters when URL parameters change
  useEffect(() => {
    const urlSearch = searchParams.get('search');
    const urlCountry = searchParams.get('country');
    const urlRegion = searchParams.get('region');
    
    if (urlSearch && urlSearch !== searchQuery) {
      setSearchQuery(urlSearch);
    }
    if (urlCountry && urlCountry !== filters.country) {
      setFilters(prev => ({ ...prev, country: urlCountry }));
    }
    if (urlRegion && urlRegion !== filters.region) {
      setFilters(prev => ({ ...prev, region: urlRegion }));
    }
  }, [searchParams]);

  // Fetch available filter options
  const fetchFilterOptions = useCallback(async () => {
    try {
      const params = new URLSearchParams();
      if (filters.country !== 'all') params.append('country', filters.country);
      if (filters.region !== 'all') params.append('region', filters.region);
      
      const response = await axios.get(`${API}/public-wines-filters?${params}`);
      setAvailableFilters(response.data);
    } catch (error) {
      console.error('Error fetching filters:', error);
    }
  }, [filters.country, filters.region]);

  // Fetch wines
  const fetchWines = useCallback(async (reset = false) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      
      if (searchQuery) params.append('search', searchQuery);
      if (filters.country && filters.country !== 'all') params.append('country', filters.country);
      if (filters.region && filters.region !== 'all') params.append('region', filters.region);
      if (filters.appellation && filters.appellation !== 'all') params.append('appellation', filters.appellation);
      if (filters.grape_variety && filters.grape_variety !== 'all') params.append('grape_variety', filters.grape_variety);
      if (filters.wine_color && filters.wine_color !== 'all') params.append('wine_color', filters.wine_color);
      if (filters.price_category && filters.price_category !== 'all') params.append('price_category', filters.price_category);
      
      const currentPage = reset ? 0 : page;
      params.append('skip', currentPage * 50);
      params.append('limit', 50);
      
      const response = await axios.get(`${API}/public-wines?${params}`);
      
      if (reset) {
        setWines(response.data);
        setPage(0);
      } else {
        setWines(prev => [...prev, ...response.data]);
      }
      
      setHasMore(response.data.length === 50);
    } catch (error) {
      console.error('Error fetching wines:', error);
      toast.error('Fehler beim Laden der Weine');
    } finally {
      setLoading(false);
    }
  }, [searchQuery, filters, page]);

  useEffect(() => {
    fetchFilterOptions();
  }, [fetchFilterOptions]);

  useEffect(() => {
    fetchWines(true);
  }, [searchQuery, filters]);

  // Fetch AI-enriched wines
  const fetchEnrichedWines = useCallback(async () => {
    try {
      setEnrichedLoading(true);
      const params = new URLSearchParams();
      if (enrichedSearchQuery) params.append('search', enrichedSearchQuery);
      params.append('limit', '50');
      params.append('skip', '0');
      
      const response = await axios.get(`${API}/wine-knowledge?${params}`);
      setEnrichedWines(response.data.wines || []);
      setEnrichedTotal(response.data.total || 0);
    } catch (error) {
      console.error('Error fetching enriched wines:', error);
      toast.error('Fehler beim Laden der angereicherten Weine');
    } finally {
      setEnrichedLoading(false);
    }
  }, [enrichedSearchQuery]);

  // Fetch enriched wines count on initial load, full data when tab changes
  useEffect(() => {
    // Always fetch count on mount
    const fetchCount = async () => {
      try {
        const response = await axios.get(`${API}/wine-knowledge?limit=1&skip=0`);
        setEnrichedTotal(response.data.total || 0);
      } catch (error) {
        console.error('Error fetching enriched count:', error);
      }
    };
    fetchCount();
  }, []);

  useEffect(() => {
    if (activeTab === 'enriched') {
      fetchEnrichedWines();
    }
  }, [activeTab, enrichedSearchQuery, fetchEnrichedWines]);

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => {
      const newFilters = { ...prev, [key]: value };
      
      // Cascade: if country changes, reset region and appellation
      if (key === 'country') {
        newFilters.region = 'all';
        newFilters.appellation = 'all';
      }
      
      // Cascade: if region changes, reset appellation
      if (key === 'region') {
        newFilters.appellation = 'all';
      }
      
      return newFilters;
    });
  };

  const clearFilters = () => {
    setFilters({
      country: 'all',
      region: 'all',
      appellation: 'all',
      grape_variety: 'all',
      wine_color: 'all',
      price_category: 'all'
    });
    setSearchQuery('');
  };

  const loadMore = () => {
    setPage(prev => prev + 1);
    fetchWines(false);
  };

  const addToCellar = async (wine) => {
    try {
      const token = localStorage.getItem('wine_auth_token');
      if (!token) {
        toast.error('Bitte melden Sie sich an, um Weine zu speichern');
        return;
      }
      
      await axios.post(`${API}/wines`, {
        name: wine.name,
        type: wine.wine_color || wine.color || 'rot',
        region: wine.region || '',
        year: wine.year || wine.vintage || null,
        grape: wine.grape_variety || wine.grape || '',
        description: getDescription(wine),
        notes: ''
      }, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      toast.success('Wein wurde zum Keller hinzugefügt!');
    } catch (error) {
      console.error('Error adding to cellar:', error);
      if (error.response?.status === 401) {
        toast.error('Bitte melden Sie sich an, um Weine zu speichern');
      } else {
        toast.error('Fehler beim Hinzufügen');
      }
    }
  };

  const toggleFavorite = async (wine) => {
    try {
      if (favorites.has(wine.id)) {
        await axios.delete(`${API}/favorites/${wine.id}`);
        setFavorites(prev => {
          const newSet = new Set(prev);
          newSet.delete(wine.id);
          return newSet;
        });
        toast.success('Aus Favoriten entfernt');
      } else {
        await axios.post(`${API}/favorites/${wine.id}?is_wishlist=false`);
        setFavorites(prev => new Set(prev).add(wine.id));
        toast.success('Zu Favoriten hinzugefügt!');
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
      toast.error('Fehler');
    }
  };

  const toggleWishlist = async (wine) => {
    try {
      if (wishlist.has(wine.id)) {
        await axios.delete(`${API}/favorites/${wine.id}`);
        setWishlist(prev => {
          const newSet = new Set(prev);
          newSet.delete(wine.id);
          return newSet;
        });
        toast.success('Aus Merkliste entfernt');
      } else {
        await axios.post(`${API}/favorites/${wine.id}?is_wishlist=true`);
        setWishlist(prev => new Set(prev).add(wine.id));
        toast.success('Zur Merkliste hinzugefügt!');
      }
    } catch (error) {
      console.error('Error toggling wishlist:', error);
      toast.error('Fehler');
    }
  };

  const getWineColorBadge = (color) => {
    const colorMap = {
      'rot': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
      'weiss': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
      'rose': 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200',
      'suesswein': 'bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200',
      'schaumwein': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
    };
    return colorMap[color] || 'bg-gray-100 text-gray-800';
  };

  const activeFilterCount = Object.values(filters).filter(v => v && v !== 'all').length;

  return (
    <>
      <SEO 
        title="Wein-Datenbank"
        description="Durchsuchen Sie unsere umfangreiche Wein-Datenbank mit Tausenden von Weinen aus aller Welt"
        url="https://wine-pairing.online/wine-database"
      />
      
      <div className="min-h-screen pb-20 md:pb-24 pt-6 md:pt-8 px-4 md:px-12 lg:px-24" data-testid="wine-database-page">
        <div className="container mx-auto max-w-7xl">
          {/* Header */}
          <header className="text-center mb-8 md:mb-12">
            <p className="text-accent font-accent text-sm tracking-widest uppercase mb-2">Wein-Entdeckung</p>
            <h1 className="text-2xl md:text-4xl font-semibold tracking-tight mb-3 md:mb-4">Wein-Datenbank</h1>
            <p className="text-muted-foreground max-w-xl mx-auto text-sm md:text-base">
              Entdecken Sie Tausende von Weinen aus aller Welt mit emotionalen Beschreibungen und perfekten Pairings
            </p>
          </header>

          {/* Tabs for Database vs AI-Enriched */}
          <Tabs value={activeTab} onValueChange={setActiveTab} className="mb-8">
            <TabsList className="grid w-full grid-cols-2 max-w-md mx-auto">
              <TabsTrigger value="database" className="gap-2">
                <Wine className="h-4 w-4" />
                Wein-Datenbank
              </TabsTrigger>
              <TabsTrigger value="enriched" className="gap-2">
                <Sparkles className="h-4 w-4" />
                AI-Weine ({enrichedTotal})
              </TabsTrigger>
            </TabsList>

            {/* AI-Enriched Wines Tab */}
            <TabsContent value="enriched" className="mt-6">
              {/* Search for enriched wines */}
              <div className="mb-6">
                <div className="relative max-w-xl mx-auto">
                  <Sparkles className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-amber-500" />
                  <Input
                    type="text"
                    placeholder="Suchen in AI-angereicherten Weinen (Name, Region, Rebsorte)..."
                    value={enrichedSearchQuery}
                    onChange={(e) => setEnrichedSearchQuery(e.target.value)}
                    className="pl-10 pr-4 h-12"
                  />
                </div>
                <p className="text-center text-sm text-muted-foreground mt-2">
                  {enrichedTotal} Weine mit detaillierten AI-Profilen verfügbar
                </p>
              </div>

              {/* Enriched Wines Grid */}
              {enrichedLoading ? (
                <div className="flex items-center justify-center py-20">
                  <Loader2 className="h-8 w-8 animate-spin text-amber-500" />
                </div>
              ) : enrichedWines.length === 0 ? (
                <Card className="bg-secondary/30 border-dashed border-2 border-border">
                  <CardContent className="py-16 text-center">
                    <Sparkles className="h-16 w-16 mx-auto mb-4 text-amber-500" strokeWidth={1} />
                    <h3 className="text-xl font-medium mb-2">Keine AI-angereicherten Weine gefunden</h3>
                    <p className="text-muted-foreground mb-4">
                      {enrichedSearchQuery 
                        ? 'Versuchen Sie eine andere Suche' 
                        : 'Weine werden automatisch angereichert, wenn Pro-User sie in ihrem Keller anreichern'}
                    </p>
                  </CardContent>
                </Card>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {enrichedWines.map((wine) => (
                    <Card 
                      key={wine.search_key || wine.id}
                      className="bg-gradient-to-br from-amber-50/50 to-orange-50/30 dark:from-amber-950/20 dark:to-orange-950/10 border-amber-200/50 dark:border-amber-800/30 hover-lift cursor-pointer overflow-hidden group"
                      onClick={() => setSelectedEnrichedWine(wine)}
                    >
                      <CardContent className="p-5">
                        {/* AI Badge & Vintage */}
                        <div className="flex items-start justify-between mb-3">
                          <Badge className="bg-amber-100 text-amber-800 dark:bg-amber-900/50 dark:text-amber-200">
                            <Sparkles className="h-3 w-3 mr-1" />
                            AI-Profil
                          </Badge>
                          {wine.vintage && (
                            <span className="text-xs font-medium text-muted-foreground">{wine.vintage}</span>
                          )}
                        </div>

                        {/* Wine Name */}
                        <h3 className="font-bold text-lg mb-1 line-clamp-2 leading-tight">{wine.name}</h3>
                        
                        {/* Region */}
                        <p className="text-sm text-muted-foreground mb-3">
                          📍 {wine.region || 'Unbekannte Region'}
                        </p>
                        
                        {/* Grape Varieties */}
                        {wine.grape_varieties && wine.grape_varieties.length > 0 && (
                          <div className="flex items-center gap-2 mb-3 text-xs text-muted-foreground">
                            <Grape className="h-3 w-3" />
                            <span className="line-clamp-1">{wine.grape_varieties.join(', ')}</span>
                          </div>
                        )}
                        
                        {/* Emotional Description Preview */}
                        {wine.emotional_description && (
                          <p className="text-sm text-muted-foreground line-clamp-3 mb-4 font-accent italic leading-relaxed">
                            {wine.emotional_description}
                          </p>
                        )}

                        {/* Quick Info Pills */}
                        <div className="flex flex-wrap gap-2">
                          {wine.serving_temp && (
                            <span className="text-xs px-2 py-1 rounded-full bg-blue-50 text-blue-700 dark:bg-blue-950/50 dark:text-blue-300 flex items-center gap-1">
                              <Thermometer className="h-3 w-3" />
                              {wine.serving_temp}
                            </span>
                          )}
                          {wine.drinking_window && (
                            <span className="text-xs px-2 py-1 rounded-full bg-green-50 text-green-700 dark:bg-green-950/50 dark:text-green-300 flex items-center gap-1">
                              <Calendar className="h-3 w-3" />
                              {wine.drinking_window}
                            </span>
                          )}
                          {wine.price_category && (
                            <span className="text-xs px-2 py-1 rounded-full bg-purple-50 text-purple-700 dark:bg-purple-950/50 dark:text-purple-300">
                              {wine.price_category}
                            </span>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </TabsContent>

            {/* Regular Wine Database Tab */}
            <TabsContent value="database" className="mt-6">

          {/* Search & Filter Bar */}
          <div className="mb-8 space-y-4">
            {/* Search Input */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Suchen Sie nach Wein, Weingut, Rebsorte..."
                value={searchQuery}
                onChange={handleSearch}
                className="pl-10 pr-4 h-12"
              />
            </div>

            {/* Filter Toggle */}
            <div className="flex items-center justify-between">
              <Button
                variant="outline"
                onClick={() => setShowFilters(!showFilters)}
                className="gap-2"
              >
                <Filter className="h-4 w-4" />
                Filter
                {activeFilterCount > 0 && (
                  <Badge variant="secondary" className="ml-2">{activeFilterCount}</Badge>
                )}
                <ChevronDown className={`h-4 w-4 transition-transform ${showFilters ? 'rotate-180' : ''}`} />
              </Button>

              {activeFilterCount > 0 && (
                <Button variant="ghost" size="sm" onClick={clearFilters}>
                  <X className="h-4 w-4 mr-2" />
                  Filter löschen
                </Button>
              )}
            </div>

            {/* Filter Panel */}
            {showFilters && (
              <Card className="p-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {/* Country Filter */}
                  <div>
                    <label className="text-sm font-medium mb-2 block">Land</label>
                    <Select value={filters.country} onValueChange={(v) => handleFilterChange('country', v)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Alle Länder" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">Alle Länder</SelectItem>
                        {availableFilters.countries?.map(country => (
                          <SelectItem key={country} value={country}>{country}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Region Filter */}
                  <div>
                    <label className="text-sm font-medium mb-2 block">Region</label>
                    <Select value={filters.region} onValueChange={(v) => handleFilterChange('region', v)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Alle Regionen" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">Alle Regionen</SelectItem>
                        {availableFilters.regions?.map(region => (
                          <SelectItem key={region} value={region}>{region}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Appellation Filter */}
                  <div>
                    <label className="text-sm font-medium mb-2 block">Appellation</label>
                    <Select value={filters.appellation} onValueChange={(v) => handleFilterChange('appellation', v)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Alle Appellationen" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">Alle Appellationen</SelectItem>
                        {availableFilters.appellations?.map(appellation => (
                          <SelectItem key={appellation} value={appellation}>{appellation}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Grape Variety Filter */}
                  <div>
                    <label className="text-sm font-medium mb-2 block">Rebsorte</label>
                    <Select value={filters.grape_variety} onValueChange={(v) => handleFilterChange('grape_variety', v)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Alle Rebsorten" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">Alle Rebsorten</SelectItem>
                        {availableFilters.grape_varieties?.map(grape => (
                          <SelectItem key={grape} value={grape}>{grape}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Wine Color Filter */}
                  <div>
                    <label className="text-sm font-medium mb-2 block">Weinfarbe</label>
                    <Select value={filters.wine_color} onValueChange={(v) => handleFilterChange('wine_color', v)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Alle Farben" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">Alle Farben</SelectItem>
                        <SelectItem value="rot">Rotwein</SelectItem>
                        <SelectItem value="weiss">Weißwein</SelectItem>
                        <SelectItem value="rose">Roséwein</SelectItem>
                        <SelectItem value="suesswein">Süßwein</SelectItem>
                        <SelectItem value="schaumwein">Schaumwein</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Price Category Filter */}
                  <div>
                    <label className="text-sm font-medium mb-2 block">Preiskategorie</label>
                    <Select value={filters.price_category} onValueChange={(v) => handleFilterChange('price_category', v)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Alle Preise" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">Alle Preise</SelectItem>
                        <SelectItem value="1">🍷 bis €20</SelectItem>
                        <SelectItem value="2">🍷🍷 €20-50</SelectItem>
                        <SelectItem value="3">🍷🍷🍷 ab €50</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </Card>
            )}
          </div>

          {/* Wine Grid */}
          {loading && wines.length === 0 ? (
            <div className="flex items-center justify-center py-20">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : wines.length === 0 ? (
            <Card className="bg-secondary/30 border-dashed border-2 border-border">
              <CardContent className="py-16 text-center">
                <Wine className="h-16 w-16 mx-auto mb-4 text-muted-foreground" strokeWidth={1} />
                <h3 className="text-xl font-medium mb-2">Keine Weine gefunden</h3>
                <p className="text-muted-foreground mb-4">Versuchen Sie eine andere Suche oder Filter</p>
                <Button variant="outline" onClick={clearFilters}>Filter zurücksetzen</Button>
              </CardContent>
            </Card>
          ) : (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                {wines.map((wine) => {
                  // Check if wine has a real image (not placeholder)
                  const hasRealImage = wine.image_url && wine.image_url !== '/placeholder-wine.png';
                  
                  return (
                    <Card 
                      key={wine.id} 
                      className="bg-card/50 backdrop-blur-sm border-border/50 hover-lift cursor-pointer overflow-hidden group"
                      onClick={() => setSelectedWine(wine)}
                    >
                      <CardContent className="p-5">
                        {/* Wine Color Badge & Region */}
                        <div className="flex items-start justify-between mb-3">
                          <Badge className={getWineColorBadge(wine.wine_color)}>
                            {wine.wine_color}
                          </Badge>
                          {wine.year && (
                            <span className="text-xs font-medium text-muted-foreground">{wine.year}</span>
                          )}
                        </div>

                        {/* Wine Name & Winery */}
                        <h3 className="font-bold text-lg mb-1 line-clamp-2 leading-tight">{wine.name}</h3>
                        <p className="text-sm text-muted-foreground mb-3">{wine.winery}</p>
                        
                        {/* Location Info */}
                        <div className="flex items-center gap-2 mb-3 text-xs text-muted-foreground">
                          <Wine className="h-3 w-3" />
                          <span className="line-clamp-1">
                            {wine.grape_variety}
                          </span>
                        </div>
                        
                        <div className="text-xs text-muted-foreground mb-3">
                          📍 {wine.appellation || wine.region}, {wine.country}
                        </div>
                        
                        {/* Description */}
                        <p className="text-sm text-muted-foreground line-clamp-3 mb-4 font-accent italic leading-relaxed">
                          {getDescription(wine)}
                        </p>
                        
                        {/* Price Category Badge */}
                        {wine.price_category && (
                          <div className="mb-4">
                            <span className={`text-xs px-2.5 py-1 rounded-full inline-flex items-center gap-1 ${
                              wine.price_category === '1' ? 'bg-green-100 text-green-700 dark:bg-green-950/50 dark:text-green-400' :
                              wine.price_category === '2' ? 'bg-amber-100 text-amber-700 dark:bg-amber-950/50 dark:text-amber-400' :
                              wine.price_category === '3' ? 'bg-orange-100 text-orange-700 dark:bg-orange-950/50 dark:text-orange-400' :
                              'bg-secondary text-secondary-foreground'
                            }`}>
                              {wine.price_category === '1' && '🍷 bis €20'}
                              {wine.price_category === '2' && '🍷🍷 €20-50'}
                              {wine.price_category === '3' && '🍷🍷🍷 ab €50'}
                              {/* Legacy support for old categories */}
                              {wine.price_category === 'budget' && '🍷 Budget'}
                              {wine.price_category === 'mid-range' && '🍷🍷 Mittelklasse'}
                              {wine.price_category === 'premium' && '🍷🍷🍷 Premium'}
                              {wine.price_category === 'luxury' && '🍷🍷🍷 Luxus'}
                            </span>
                          </div>
                        )}
                      
                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant={favorites.has(wine.id) ? "default" : "outline"}
                          className="flex-1"
                          onClick={(e) => {
                            e.stopPropagation();
                            toggleFavorite(wine);
                          }}
                        >
                          <Heart className={`h-4 w-4 ${favorites.has(wine.id) ? 'fill-current' : ''}`} />
                        </Button>
                        <Button
                          size="sm"
                          variant={wishlist.has(wine.id) ? "default" : "outline"}
                          className="flex-1"
                          onClick={(e) => {
                            e.stopPropagation();
                            toggleWishlist(wine);
                          }}
                        >
                          <Bookmark className={`h-4 w-4 ${wishlist.has(wine.id) ? 'fill-current' : ''}`} />
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          className="flex-1"
                          onClick={(e) => {
                            e.stopPropagation();
                            addToCellar(wine);
                          }}
                        >
                          <Plus className="h-4 w-4" />
                        </Button>
                        </div>
                      </CardContent>
                    </Card>
                  );
                })}
              </div>

              {/* Load More Button */}
              {hasMore && (
                <div className="flex justify-center">
                  <Button onClick={loadMore} disabled={loading} variant="outline" size="lg">
                    {loading ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Lädt...
                      </>
                    ) : (
                      'Mehr laden'
                    )}
                  </Button>
                </div>
              )}
            </>
          )}
            </TabsContent>
          </Tabs>
        </div>
      </div>

      {/* AI-Enriched Wine Detail Modal */}
      {selectedEnrichedWine && (
        <Dialog open={!!selectedEnrichedWine} onOpenChange={() => setSelectedEnrichedWine(null)}>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            {/* Zurück Button */}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSelectedEnrichedWine(null)}
              className="absolute left-4 top-4 rounded-full"
            >
              <ArrowLeft className="h-4 w-4 mr-1" />
              Zurück
            </Button>
            
            <DialogHeader className="pt-8">
              <div className="flex items-center gap-2 mb-2">
                <Badge className="bg-amber-100 text-amber-800 dark:bg-amber-900/50 dark:text-amber-200">
                  <Sparkles className="h-3 w-3 mr-1" />
                  AI-angereichert
                </Badge>
                {selectedEnrichedWine.vintage && (
                  <Badge variant="outline">{selectedEnrichedWine.vintage}</Badge>
                )}
              </div>
              <DialogTitle className="text-2xl">{selectedEnrichedWine.name}</DialogTitle>
              <DialogDescription className="text-base">
                📍 {selectedEnrichedWine.region || 'Unbekannte Region'}
              </DialogDescription>
            </DialogHeader>

            <div className="space-y-6">
              {/* Emotional Description */}
              {selectedEnrichedWine.emotional_description && (
                <div className="bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-950/30 dark:to-orange-950/20 rounded-lg p-4">
                  <p className="text-foreground font-accent italic leading-relaxed">
                    &ldquo;{selectedEnrichedWine.emotional_description}&rdquo;
                  </p>
                </div>
              )}

              {/* Wine Details Grid */}
              <div className="grid grid-cols-2 gap-4 text-sm">
                {/* Grape Varieties */}
                {selectedEnrichedWine.grape_varieties && selectedEnrichedWine.grape_varieties.length > 0 && (
                  <div className="col-span-2">
                    <p className="text-muted-foreground flex items-center gap-1 mb-1">
                      <Grape className="h-4 w-4" /> Rebsorten
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {selectedEnrichedWine.grape_varieties.map((grape, idx) => (
                        <Badge key={idx} variant="secondary">{grape}</Badge>
                      ))}
                    </div>
                  </div>
                )}

                {/* Appellation */}
                {selectedEnrichedWine.appellation && (
                  <div>
                    <p className="text-muted-foreground">Appellation</p>
                    <p className="font-medium">{selectedEnrichedWine.appellation}</p>
                  </div>
                )}

                {/* Serving Temperature */}
                {selectedEnrichedWine.serving_temp && (
                  <div>
                    <p className="text-muted-foreground flex items-center gap-1">
                      <Thermometer className="h-3 w-3" /> Serviertemperatur
                    </p>
                    <p className="font-medium">{selectedEnrichedWine.serving_temp}</p>
                  </div>
                )}

                {/* Drinking Window */}
                {selectedEnrichedWine.drinking_window && (
                  <div>
                    <p className="text-muted-foreground flex items-center gap-1">
                      <Calendar className="h-3 w-3" /> Trinkreife
                    </p>
                    <p className="font-medium">{selectedEnrichedWine.drinking_window}</p>
                  </div>
                )}

                {/* Price Category */}
                {selectedEnrichedWine.price_category && (
                  <div>
                    <p className="text-muted-foreground">Preiskategorie</p>
                    <p className="font-medium">{selectedEnrichedWine.price_category}</p>
                  </div>
                )}
              </div>

              {/* Taste Profile */}
              {selectedEnrichedWine.taste_profile && (
                <div>
                  <h4 className="font-semibold mb-3">Geschmacksprofil</h4>
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    {selectedEnrichedWine.taste_profile.body && (
                      <div className="flex justify-between items-center p-2 bg-secondary/30 rounded">
                        <span className="text-muted-foreground">Körper</span>
                        <span className="font-medium">{selectedEnrichedWine.taste_profile.body}</span>
                      </div>
                    )}
                    {selectedEnrichedWine.taste_profile.tannins && (
                      <div className="flex justify-between items-center p-2 bg-secondary/30 rounded">
                        <span className="text-muted-foreground">Tannine</span>
                        <span className="font-medium">{selectedEnrichedWine.taste_profile.tannins}</span>
                      </div>
                    )}
                    {selectedEnrichedWine.taste_profile.acidity && (
                      <div className="flex justify-between items-center p-2 bg-secondary/30 rounded">
                        <span className="text-muted-foreground">Säure</span>
                        <span className="font-medium">{selectedEnrichedWine.taste_profile.acidity}</span>
                      </div>
                    )}
                    {selectedEnrichedWine.taste_profile.finish && (
                      <div className="flex justify-between items-center p-2 bg-secondary/30 rounded">
                        <span className="text-muted-foreground">Abgang</span>
                        <span className="font-medium">{selectedEnrichedWine.taste_profile.finish}</span>
                      </div>
                    )}
                  </div>
                  {selectedEnrichedWine.taste_profile.aromas && selectedEnrichedWine.taste_profile.aromas.length > 0 && (
                    <div className="mt-3">
                      <p className="text-muted-foreground text-sm mb-2">Aromen</p>
                      <div className="flex flex-wrap gap-2">
                        {selectedEnrichedWine.taste_profile.aromas.map((aroma, idx) => (
                          <span key={idx} className="px-2 py-1 text-xs bg-rose-50 text-rose-700 dark:bg-rose-950/50 dark:text-rose-300 rounded-full">
                            {aroma}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Food Pairings */}
              {selectedEnrichedWine.food_pairings && selectedEnrichedWine.food_pairings.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-3 flex items-center gap-2">
                    <UtensilsCrossed className="h-4 w-4" /> Passende Speisen
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {selectedEnrichedWine.food_pairings.map((pairing, idx) => (
                      <span key={idx} className="inline-block px-3 py-1.5 text-sm border border-border rounded-md bg-secondary/30">
                        {pairing}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Winery Info */}
              {selectedEnrichedWine.winery_info && (
                <div>
                  <h4 className="font-semibold mb-2">Über das Weingut</h4>
                  <p className="text-sm text-muted-foreground">{selectedEnrichedWine.winery_info}</p>
                </div>
              )}

              {/* Close Button */}
              <div className="pt-4">
                <Button variant="outline" className="w-full" onClick={() => setSelectedEnrichedWine(null)}>
                  Schließen
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      )}

      {/* Wine Detail Modal */}
      {selectedWine && (
        <Dialog open={!!selectedWine} onOpenChange={() => setSelectedWine(null)}>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            {/* Zurück Button */}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSelectedWine(null)}
              className="absolute left-4 top-4 rounded-full"
            >
              <ArrowLeft className="h-4 w-4 mr-1" />
              {language === 'de' ? 'Zurück' : language === 'fr' ? 'Retour' : 'Back'}
            </Button>
            
            <DialogHeader className="pt-8">
              <DialogTitle className="text-2xl">{selectedWine.name}</DialogTitle>
              <DialogDescription className="text-base">{selectedWine.winery}</DialogDescription>
            </DialogHeader>

            <div className="space-y-6">
              {/* Wine Details */}
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-muted-foreground">{t('wine_country')}</p>
                  <p className="font-medium">{selectedWine.country || t('wine_unknown')}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">{t('wine_region')}</p>
                  <p className="font-medium">{selectedWine.region || t('wine_unknown')}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">{t('wine_grape')}</p>
                  <p className="font-medium">{selectedWine.grape_variety || t('wine_unknown')}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">{t('wine_type')}</p>
                  <Badge className={getWineColorBadge(selectedWine.wine_color)}>
                    {selectedWine.wine_color}
                  </Badge>
                </div>
                {selectedWine.year && (
                  <div>
                    <p className="text-muted-foreground">{t('wine_vintage')}</p>
                    <p className="font-medium">{selectedWine.year}</p>
                  </div>
                )}
                {selectedWine.appellation && (
                  <div>
                    <p className="text-muted-foreground">{t('wine_appellation')}</p>
                    <p className="font-medium">{selectedWine.appellation}</p>
                  </div>
                )}
                {selectedWine.price_category && (
                  <div>
                    <p className="text-muted-foreground">{language === 'de' ? 'Preiskategorie' : 'Price Category'}</p>
                    <span className={`text-xs px-2.5 py-1 rounded-full inline-flex items-center gap-1 ${
                      selectedWine.price_category === '1' ? 'bg-green-100 text-green-700 dark:bg-green-950/50 dark:text-green-400' :
                      selectedWine.price_category === '2' ? 'bg-amber-100 text-amber-700 dark:bg-amber-950/50 dark:text-amber-400' :
                      selectedWine.price_category === '3' ? 'bg-orange-100 text-orange-700 dark:bg-orange-950/50 dark:text-orange-400' :
                      'bg-secondary text-secondary-foreground'
                    }`}>
                      {selectedWine.price_category === '1' && '🍷 bis €20'}
                      {selectedWine.price_category === '2' && '🍷🍷 €20-50'}
                      {selectedWine.price_category === '3' && '🍷🍷🍷 ab €50'}
                      {selectedWine.price_category === 'budget' && '🍷 Budget'}
                      {selectedWine.price_category === 'mid-range' && '🍷🍷 Mittelklasse'}
                      {selectedWine.price_category === 'premium' && '🍷🍷🍷 Premium'}
                      {selectedWine.price_category === 'luxury' && '🍷🍷🍷 Luxus'}
                    </span>
                  </div>
                )}
              </div>

              {/* Description */}
              <div>
                <h4 className="font-semibold mb-2">{t('wine_description')}</h4>
                <p className="text-muted-foreground font-accent italic">
                  {getDescription(selectedWine)}
                </p>
              </div>

              {/* Food Pairings */}
              {getFoodPairings(selectedWine).length > 0 && (
                <div>
                  <h4 className="font-semibold mb-3">{t('wine_pairings')}</h4>
                  <div className="flex flex-wrap gap-2">
                    {getFoodPairings(selectedWine).map((pairing, idx) => (
                      <span 
                        key={idx} 
                        className="inline-block px-3 py-1.5 text-sm border border-border rounded-md bg-secondary/30 break-words max-w-full"
                      >
                        {pairing}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="space-y-3 pt-4">
                <div className="flex gap-2">
                  <Button 
                    variant={favorites.has(selectedWine.id) ? "default" : "outline"}
                    className="flex-1"
                    onClick={() => toggleFavorite(selectedWine)}
                  >
                    <Heart className={`h-4 w-4 mr-2 ${favorites.has(selectedWine.id) ? 'fill-current' : ''}`} />
                    {t('wine_add_favorites')}
                  </Button>
                  <Button 
                    variant={wishlist.has(selectedWine.id) ? "default" : "outline"}
                    className="flex-1"
                    onClick={() => toggleWishlist(selectedWine)}
                  >
                    <Bookmark className={`h-4 w-4 mr-2 ${wishlist.has(selectedWine.id) ? 'fill-current' : ''}`} />
                    {t('wine_add_wishlist')}
                  </Button>
                </div>
                <Button className="w-full" onClick={() => {
                  addToCellar(selectedWine);
                  setSelectedWine(null);
                }}>
                  <Plus className="h-4 w-4 mr-2" />
                  {t('wine_add_cellar')}
                </Button>
                <Button variant="outline" className="w-full" onClick={() => setSelectedWine(null)}>
                  {t('wine_close')}
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      )}
    </>
  );
};

export default WineDatabasePage;
