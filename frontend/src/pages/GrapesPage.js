import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import { Wine, Grape, ArrowLeft, MapPin, Droplet, Flame, Loader2, Utensils } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useLanguage } from '@/contexts/LanguageContext';
import { SEO } from '@/components/SEO';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Grape List Page
export const GrapesPage = () => {
  const { t, language } = useLanguage();
  const navigate = useNavigate();
  const [grapes, setGrapes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  const fetchGrapes = useCallback(async () => {
    try {
      const params = filter !== 'all' ? `?type_filter=${filter}` : '';
      const response = await axios.get(`${API}/grapes${params}`);
      setGrapes(response.data);
    } catch (error) {
      console.error('Error fetching grapes:', error);
    } finally {
      setLoading(false);
    }
  }, [filter]);

  useEffect(() => {
    fetchGrapes();
  }, [fetchGrapes]);

  const getLocalizedDescription = (grape) => {
    if (language === 'en' && grape.description_en) return grape.description_en;
    if (language === 'fr' && grape.description_fr) return grape.description_fr;
    return grape.description;
  };

  return (
    <>
      <SEO 
        title={t('grapes_title')}
        description={t('grapes_description')}
        url="https://wine-pairing.online/grapes"
      />
      
      <div className="min-h-screen pb-20 md:pb-24 pt-6 md:pt-8 px-4 md:px-12 lg:px-24" data-testid="grapes-page">
        <div className="container mx-auto max-w-6xl">
          <header className="text-center mb-8 md:mb-12">
            <p className="text-accent font-accent text-sm tracking-widest uppercase mb-2">{t('grapes_tagline')}</p>
            <h1 className="text-2xl md:text-4xl font-semibold tracking-tight mb-3 md:mb-4">{t('grapes_title')}</h1>
            <p className="text-muted-foreground max-w-xl mx-auto text-sm md:text-base">
              {t('grapes_description')}
            </p>
          </header>

          {/* Optional Admin Link */}
          <div className="flex justify-end mb-4">
            <button
              type="button"
              onClick={() => navigate('/admin/grapes')}
              className="text-xs text-muted-foreground hover:text-primary underline-offset-2 hover:underline"
            >
              {t('admin_grapes_title')}
            </button>
          </div>

          {/* Filter Tabs */}
          <Tabs value={filter} onValueChange={setFilter} className="mb-8">
            <TabsList className="grid w-full max-w-md mx-auto grid-cols-3">
              <TabsTrigger value="all" data-testid="filter-all">{t('grapes_all')}</TabsTrigger>
              <TabsTrigger value="weiss" data-testid="filter-white">{t('grapes_white')}</TabsTrigger>
              <TabsTrigger value="rot" data-testid="filter-red">{t('grapes_red')}</TabsTrigger>
            </TabsList>
          </Tabs>

          {loading ? (
            <div className="flex items-center justify-center py-20">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : grapes.length === 0 ? (
            <Card className="bg-secondary/30 border-dashed border-2 border-border">
              <CardContent className="py-16 text-center">
                <Grape className="h-16 w-16 mx-auto mb-4 text-muted-foreground" strokeWidth={1} />
                <h3 className="text-xl font-medium mb-2">{t('grapes_empty')}</h3>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="grapes-grid">
              {grapes.map((grape) => (
                <Card 
                  key={grape.id} 
                  className="bg-card/50 backdrop-blur-sm border-border/50 hover-lift cursor-pointer overflow-hidden group"
                  onClick={() => navigate(`/grapes/${grape.slug}`)}
                  data-testid="grape-card"
                >
                  {grape.image_url && (
                    <div className="aspect-[16/10] overflow-hidden relative">
                      <img 
                        src={grape.image_url} 
                        alt={grape.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        loading="lazy"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-background/80 to-transparent" />
                      <div className="absolute bottom-4 left-4 right-4">
                        <Badge className={`${grape.type === 'rot' ? 'badge-rot' : 'badge-weiss'} border-0`}>
                          {grape.type === 'rot' ? t('grapes_red') : t('grapes_white')}
                        </Badge>
                        <h3 className="text-xl md:text-2xl font-semibold text-white mt-2 drop-shadow-lg">
                          {grape.name}
                        </h3>
                      </div>
                    </div>
                  )}
                  <CardContent className="p-4">
                    <p className="text-sm text-muted-foreground line-clamp-3 font-accent italic">
                      {getLocalizedDescription(grape).slice(0, 150)}...
                    </p>
                    
                    {/* Quick characteristics */}
                    <div className="flex flex-wrap gap-2 mt-4">
                      <span className="text-xs bg-secondary/50 px-2 py-1 rounded-full">
                        {grape.body}
                      </span>
                      <span className="text-xs bg-secondary/50 px-2 py-1 rounded-full flex items-center gap-1">
                        <Droplet className="w-3 h-3" /> {grape.acidity}
                      </span>
                      {grape.type === 'rot' && (
                        <span className="text-xs bg-secondary/50 px-2 py-1 rounded-full flex items-center gap-1">
                          <Flame className="w-3 h-3" /> {grape.tannin}
                        </span>
                      )}
                    </div>
                    
                    {/* Main regions */}
                    <div className="flex items-center gap-1 mt-3 text-xs text-muted-foreground">
                      <MapPin className="w-3 h-3" />
                      <span className="truncate">{grape.main_regions?.slice(0, 3).join(', ')}</span>
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

// Grape Detail Page
export const GrapeDetailPage = () => {
  const { slug } = useParams();
  const { t, language } = useLanguage();
  const navigate = useNavigate();
  const [grape, setGrape] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchGrape = async () => {
      try {
        const response = await axios.get(`${API}/grapes/${slug}`);
        setGrape(response.data);
      } catch (error) {
        console.error('Error fetching grape:', error);
        navigate('/grapes');
      } finally {
        setLoading(false);
      }
    };
    fetchGrape();
  }, [slug, navigate]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!grape) return null;

  const getLocalizedDescription = () => {
    if (language === 'en' && grape.description_en) return grape.description_en;
    if (language === 'fr' && grape.description_fr) return grape.description_fr;
    return grape.description;
  };

  const getLocalizedPairings = () => {
    if (language === 'en' && grape.perfect_pairings_en?.length) return grape.perfect_pairings_en;
    if (language === 'fr' && grape.perfect_pairings_fr?.length) return grape.perfect_pairings_fr;
    return grape.perfect_pairings;
  };

  return (
    <>
      <SEO 
        title={`${grape.name} - ${t('grapes_title')}`}
        description={getLocalizedDescription().slice(0, 160)}
        image={grape.image_url}
        url={`https://wine-pairing.online/grapes/${slug}`}
      />
      
      <div className="min-h-screen pb-20 md:pb-24" data-testid="grape-detail-page">
        {/* Hero Image */}
        {grape.image_url && (
          <div className="relative h-[40vh] md:h-[50vh] w-full">
            <img 
              src={grape.image_url} 
              alt={grape.name}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-background via-background/60 to-transparent" />
          </div>
        )}
        
        <div className="container mx-auto max-w-4xl px-4 md:px-8 -mt-32 relative z-10">
          {/* Back Button */}
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate('/grapes')}
            className="mb-4 text-white/80 hover:text-white hover:bg-white/10"
            data-testid="back-to-grapes"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            {t('grapes_back')}
          </Button>

          <article className="bg-card/90 backdrop-blur-md rounded-lg border border-border/50 p-6 md:p-10">
            {/* Header */}
            <div className="mb-8">
              <Badge className={`${grape.type === 'rot' ? 'badge-rot' : 'badge-weiss'} border-0 mb-3`}>
                {grape.type === 'rot' ? t('grapes_red') : t('grapes_white')}
              </Badge>
              <h1 className="text-3xl md:text-5xl font-semibold tracking-tight mb-4">
                {grape.name}
              </h1>
              {grape.synonyms?.length > 0 && (
                <p className="text-muted-foreground text-sm">
                  <span className="font-medium">{t('grapes_synonyms')}:</span> {grape.synonyms.join(', ')}
                </p>
              )}
            </div>

            {/* Poetic Description */}
            <div className="mb-10 p-6 bg-secondary/30 rounded-lg border-l-4 border-accent">
              <p className="font-accent text-lg md:text-xl leading-relaxed italic text-foreground/90">
                {getLocalizedDescription()}
              </p>
            </div>

            {/* Characteristics Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
              <div className="bg-secondary/30 rounded-lg p-4 text-center">
                <Wine className="w-6 h-6 mx-auto mb-2 text-primary" />
                <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">{t('grapes_body')}</p>
                <p className="font-medium">{grape.body}</p>
              </div>
              <div className="bg-secondary/30 rounded-lg p-4 text-center">
                <Droplet className="w-6 h-6 mx-auto mb-2 text-primary" />
                <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">{t('grapes_acidity')}</p>
                <p className="font-medium">{grape.acidity}</p>
              </div>
              <div className="bg-secondary/30 rounded-lg p-4 text-center">
                <Flame className="w-6 h-6 mx-auto mb-2 text-primary" />
                <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">{t('grapes_tannin')}</p>
                <p className="font-medium">{grape.tannin}</p>
              </div>
              <div className="bg-secondary/30 rounded-lg p-4 text-center">
                <Wine className="w-6 h-6 mx-auto mb-2 text-primary" />
                <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">{t('grapes_aging')}</p>
                <p className="font-medium text-sm">{grape.aging}</p>
              </div>
            </div>

            {/* Aromas */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
              <div>
                <h3 className="font-semibold mb-3 flex items-center gap-2">
                  <span className="w-2 h-2 bg-accent rounded-full"></span>
                  {t('grapes_primary_aromas')}
                </h3>
                <div className="flex flex-wrap gap-2">
                  {grape.primary_aromas?.map((aroma) => (
                    <Badge key={aroma} variant="outline" className="px-3 py-1">
                      {aroma}
                    </Badge>
                  ))}
                </div>
              </div>
              <div>
                <h3 className="font-semibold mb-3 flex items-center gap-2">
                  <span className="w-2 h-2 bg-primary rounded-full"></span>
                  {t('grapes_tertiary_aromas')}
                </h3>
                <div className="flex flex-wrap gap-2">
                  {grape.tertiary_aromas?.map((aroma) => (
                    <Badge key={aroma} variant="outline" className="px-3 py-1">
                      {aroma}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>

            {/* Perfect Pairings */}
            <div className="mb-10">
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Utensils className="w-5 h-5 text-accent" />
                {t('grapes_perfect_pairings')}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {getLocalizedPairings()?.map((pairing, idx) => (
                  <Card key={idx} className="bg-secondary/30 border-border/50">
                    <CardContent className="p-4">
                      <p className="font-medium text-sm">{pairing}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>

            {/* Regions */}
            <div>
              <h3 className="font-semibold mb-3 flex items-center gap-2">
                <MapPin className="w-5 h-5 text-primary" />
                {t('grapes_main_regions')}
              </h3>
              <div className="flex flex-wrap gap-2">
                {grape.main_regions?.map((region) => (
                  <Badge key={region} className="bg-primary/10 text-primary border-0 px-3 py-1">
                    {region}
                  </Badge>
                ))}
              </div>
            </div>
          </article>
        </div>
      </div>
    </>
  );
};

export default GrapesPage;
