import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Wine, Search, Filter, ChevronDown, Heart, Plus, Loader2, X } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useLanguage } from '@/contexts/LanguageContext';
import { SEO } from '@/components/SEO';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const WineDatabasePage = () => {
  const { t, language } = useLanguage();
  const navigate = useNavigate();
  
  const [wines, setWines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({
    country: 'all',
    region: 'all',
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

  // Fetch available filter options
  const fetchFilterOptions = useCallback(async () => {
    try {
      const response = await axios.get(`${API}/wine-database-filters`);
      setAvailableFilters(response.data);
    } catch (error) {
      console.error('Error fetching filters:', error);
    }
  }, []);

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
      
      const response = await axios.get(`${API}/wine-database?${params}`);
      
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

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
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
      await axios.post(`${API}/wines`, {
        name: wine.name,
        type: wine.wine_color,
        region: wine.region,
        year: wine.year,
        grape: wine.grape_variety,
        notes: wine.description
      });
      toast.success('Wein wurde zum Keller hinzugefügt!');
    } catch (error) {
      console.error('Error adding to cellar:', error);
      toast.error('Fehler beim Hinzufügen');
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
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
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
                        <SelectItem value="budget">Budget</SelectItem>
                        <SelectItem value="mid-range">Mittelklasse</SelectItem>
                        <SelectItem value="premium">Premium</SelectItem>
                        <SelectItem value="luxury">Luxus</SelectItem>
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
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
                {wines.map((wine) => (
                  <Card 
                    key={wine.id} 
                    className="bg-card/50 backdrop-blur-sm border-border/50 hover-lift cursor-pointer overflow-hidden group"
                    onClick={() => setSelectedWine(wine)}
                  >
                    {/* Wine Image Placeholder */}
                    <div className="aspect-[3/4] bg-gradient-to-br from-primary/10 to-accent/10 flex items-center justify-center relative overflow-hidden">
                      <Wine className="h-20 w-20 text-primary/20" strokeWidth={1} />
                      <div className="absolute inset-0 bg-gradient-to-t from-background/80 to-transparent" />
                      <div className="absolute bottom-4 left-4 right-4">
                        <Badge className={getWineColorBadge(wine.wine_color)}>
                          {wine.wine_color}
                        </Badge>
                      </div>
                    </div>

                    <CardContent className="p-4">
                      <h3 className="font-semibold mb-1 line-clamp-1">{wine.name}</h3>
                      <p className="text-sm text-muted-foreground mb-2">{wine.winery}</p>
                      <p className="text-xs text-muted-foreground mb-3">
                        {wine.grape_variety} • {wine.country}
                      </p>
                      <p className="text-sm text-muted-foreground line-clamp-2 mb-3 font-accent italic">
                        {wine.description}
                      </p>
                      
                      <Button
                        size="sm"
                        variant="outline"
                        className="w-full"
                        onClick={(e) => {
                          e.stopPropagation();
                          addToCellar(wine);
                        }}
                      >
                        <Plus className="h-4 w-4 mr-2" />
                        Zum Keller
                      </Button>
                    </CardContent>
                  </Card>
                ))}
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
        </div>
      </div>

      {/* Wine Detail Modal */}
      {selectedWine && (
        <Dialog open={!!selectedWine} onOpenChange={() => setSelectedWine(null)}>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle className="text-2xl">{selectedWine.name}</DialogTitle>
              <DialogDescription className="text-base">{selectedWine.winery}</DialogDescription>
            </DialogHeader>

            <div className="space-y-6">
              {/* Wine Details */}
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-muted-foreground">Land</p>
                  <p className="font-medium">{selectedWine.country}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Region</p>
                  <p className="font-medium">{selectedWine.region}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Rebsorte</p>
                  <p className="font-medium">{selectedWine.grape_variety}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Typ</p>
                  <Badge className={getWineColorBadge(selectedWine.wine_color)}>
                    {selectedWine.wine_color}
                  </Badge>
                </div>
                {selectedWine.year && (
                  <div>
                    <p className="text-muted-foreground">Jahrgang</p>
                    <p className="font-medium">{selectedWine.year}</p>
                  </div>
                )}
                {selectedWine.appellation && (
                  <div>
                    <p className="text-muted-foreground">Appellation</p>
                    <p className="font-medium">{selectedWine.appellation}</p>
                  </div>
                )}
              </div>

              {/* Description */}
              <div>
                <h4 className="font-semibold mb-2">Beschreibung</h4>
                <p className="text-muted-foreground font-accent italic">{selectedWine.description}</p>
              </div>

              {/* Food Pairings */}
              {selectedWine.food_pairings?.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-3">Perfekt zu</h4>
                  <div className="flex flex-wrap gap-2">
                    {selectedWine.food_pairings.map((pairing, idx) => (
                      <Badge key={idx} variant="outline">{pairing}</Badge>
                    ))}
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex gap-3 pt-4">
                <Button className="flex-1" onClick={() => {
                  addToCellar(selectedWine);
                  setSelectedWine(null);
                }}>
                  <Plus className="h-4 w-4 mr-2" />
                  Zum Keller hinzufügen
                </Button>
                <Button variant="outline" onClick={() => setSelectedWine(null)}>
                  Schließen
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
