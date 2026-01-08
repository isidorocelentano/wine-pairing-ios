import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Wine, Lightbulb, Calendar, ChevronRight, Sparkles, Archive, ArrowLeft, Search, Filter, X } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { useLanguage } from "@/contexts/LanguageContext";
import { API } from "@/config/api";

const TippDerWochePage = () => {
  const { language } = useLanguage();
  const navigate = useNavigate();
  const [tips, setTips] = useState([]);
  const [archiveTips, setArchiveTips] = useState([]);
  const [showArchive, setShowArchive] = useState(false);
  const [loading, setLoading] = useState(true);
  const [archiveLoading, setArchiveLoading] = useState(false);
  const [archivePage, setArchivePage] = useState(1);
  const [archiveTotal, setArchiveTotal] = useState(0);
  
  // Filter & Search State
  const [searchQuery, setSearchQuery] = useState('');
  const [wineTypeFilter, setWineTypeFilter] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  // Wine type options
  const wineTypes = [
    { value: '', label: language === 'de' ? 'Alle Weintypen' : 'All Wine Types' },
    { value: 'rot', label: language === 'de' ? 'Rotwein' : 'Red Wine', color: 'bg-red-500' },
    { value: 'weiss', label: language === 'de' ? 'Weißwein' : 'White Wine', color: 'bg-amber-400' },
    { value: 'rose', label: 'Rosé', color: 'bg-pink-400' },
    { value: 'schaumwein', label: language === 'de' ? 'Schaumwein' : 'Sparkling', color: 'bg-sky-400' },
  ];

  // Lade die neuesten 4 Tipps
  useEffect(() => {
    const fetchTips = async () => {
      try {
        const response = await fetch(`${API}/weekly-tips?limit=4`);
        if (response.ok) {
          const data = await response.json();
          setTips(data);
        }
      } catch (error) {
        console.error('Fehler beim Laden der Tipps:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchTips();
  }, []);

  // Lade Archiv
  const loadArchive = async (page = 1) => {
    setArchiveLoading(true);
    try {
      const response = await fetch(`${API}/weekly-tips/archive?page=${page}&per_page=12`);
      if (response.ok) {
        const data = await response.json();
        setArchiveTips(data.tips);
        setArchiveTotal(data.total);
        setArchivePage(page);
      }
    } catch (error) {
      console.error('Fehler beim Laden des Archivs:', error);
    } finally {
      setArchiveLoading(false);
    }
  };

  // Weintyp Badge Farbe
  const getWineTypeBadge = (type) => {
    const colors = {
      'rot': 'bg-red-500/10 text-red-600 dark:text-red-400',
      'weiss': 'bg-amber-500/10 text-amber-600 dark:text-amber-400',
      'rose': 'bg-pink-500/10 text-pink-600 dark:text-pink-400',
      'schaumwein': 'bg-sky-500/10 text-sky-600 dark:text-sky-400'
    };
    const labels = {
      'rot': language === 'de' ? 'Rotwein' : 'Red Wine',
      'weiss': language === 'de' ? 'Weißwein' : 'White Wine',
      'rose': language === 'de' ? 'Rosé' : 'Rosé',
      'schaumwein': language === 'de' ? 'Schaumwein' : 'Sparkling'
    };
    return { color: colors[type] || colors['weiss'], label: labels[type] || type };
  };

  // Tipp Karte Komponente
  const TipCard = ({ tip, isLatest = false }) => {
    const wineType = getWineTypeBadge(tip.wine_type);
    
    return (
      <Card className={`overflow-hidden transition-all hover:shadow-lg ${isLatest ? 'border-primary/50 bg-gradient-to-br from-primary/5 to-accent/5' : 'border-border/50'}`}>
        <CardContent className="p-5">
          {/* Header mit Emoji und Badges */}
          <div className="flex items-start justify-between mb-4">
            <span className="text-4xl">{tip.dish_emoji || '🍽️'}</span>
            <div className="flex flex-col items-end gap-1">
              {isLatest && (
                <Badge className="bg-primary/10 text-primary border-0 text-xs">
                  <Sparkles className="w-3 h-3 mr-1" />
                  {language === 'de' ? 'Neu' : 'New'}
                </Badge>
              )}
              <Badge className={`${wineType.color} border-0 text-xs`}>
                {wineType.label}
              </Badge>
            </div>
          </div>

          {/* Gericht */}
          <h3 className="font-semibold text-lg mb-1">{tip.dish}</h3>
          
          {/* Wein */}
          <div className="flex items-center gap-2 mb-3">
            <Wine className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">{tip.wine}</span>
          </div>
          
          {/* Region */}
          {tip.region && (
            <p className="text-xs text-muted-foreground mb-3">📍 {tip.region}</p>
          )}
          
          {/* Warum */}
          <p className="text-sm text-muted-foreground leading-relaxed mb-3 italic">
            "{tip.why}"
          </p>
          
          {/* Fun Fact */}
          {tip.fun_fact && (
            <div className="p-3 rounded-lg bg-muted/50 border border-border/30">
              <div className="flex items-start gap-2">
                <Lightbulb className="w-4 h-4 text-amber-500 flex-shrink-0 mt-0.5" />
                <p className="text-xs text-muted-foreground">{tip.fun_fact}</p>
              </div>
            </div>
          )}
          
          {/* Datum */}
          <div className="flex items-center justify-between mt-4 pt-3 border-t border-border/30">
            <div className="flex items-center gap-1 text-xs text-muted-foreground">
              <Calendar className="w-3 h-3" />
              <span>KW {tip.week_number}/{tip.year}</span>
            </div>
            <Button 
              variant="ghost" 
              size="sm" 
              className="text-xs h-7 px-2"
              onClick={() => navigate(`/pairing?dish=${encodeURIComponent(tip.dish)}`)}
            >
              {language === 'de' ? 'Selbst testen' : 'Try it'}
              <ChevronRight className="w-3 h-3 ml-1" />
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="min-h-screen pb-24 pt-4">
      <div className="container mx-auto px-4 md:px-8 lg:px-16 max-w-6xl">
        
        {/* Header */}
        <header className="text-center mb-10">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate('/')}
            className="mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            {language === 'de' ? 'Zurück zur Startseite' : 'Back to Home'}
          </Button>
          
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
              <Lightbulb className="w-6 h-6 text-primary" />
            </div>
          </div>
          
          <p className="text-accent font-accent text-sm tracking-widest uppercase mb-2">
            {language === 'de' ? 'INSPIRATION DER WOCHE' : 'WEEKLY INSPIRATION'}
          </p>
          <h1 className="text-2xl md:text-4xl font-semibold tracking-tight mb-3">
            {language === 'de' ? 'Tipp der Woche' : 'Tip of the Week'}
          </h1>
          <p className="text-muted-foreground max-w-xl mx-auto text-sm md:text-base">
            {language === 'de' 
              ? 'Entdecke jede Woche neue, überraschende Wein-Pairings – von unserer KI kuratiert, von Sommeliers inspiriert.'
              : 'Discover new, surprising wine pairings every week – curated by our AI, inspired by sommeliers.'}
          </p>
        </header>

        {/* Aktuelle Tipps */}
        {!showArchive && (
          <>
            {loading ? (
              <div className="flex justify-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : tips.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
                {tips.map((tip, index) => (
                  <TipCard key={tip.id} tip={tip} isLatest={index === 0} />
                ))}
              </div>
            ) : (
              <Card className="text-center py-12 mb-10">
                <CardContent>
                  <Wine className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground">
                    {language === 'de' ? 'Noch keine Tipps vorhanden.' : 'No tips available yet.'}
                  </p>
                </CardContent>
              </Card>
            )}

            {/* Archiv Button */}
            <div className="text-center">
              <Button
                variant="outline"
                onClick={() => {
                  setShowArchive(true);
                  loadArchive(1);
                }}
                className="rounded-full px-6"
              >
                <Archive className="w-4 h-4 mr-2" />
                {language === 'de' ? 'Alle Tipps im Archiv ansehen' : 'View all tips in archive'}
              </Button>
            </div>
          </>
        )}

        {/* Archiv Ansicht */}
        {showArchive && (
          <>
            <div className="flex items-center justify-between mb-6">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowArchive(false)}
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                {language === 'de' ? 'Zurück zu aktuellen Tipps' : 'Back to current tips'}
              </Button>
              <h2 className="text-lg font-semibold flex items-center gap-2">
                <Archive className="w-5 h-5" />
                {language === 'de' ? 'Tipp-Archiv' : 'Tip Archive'}
                <Badge variant="secondary" className="ml-2">{archiveTotal}</Badge>
              </h2>
            </div>

            {archiveLoading ? (
              <div className="flex justify-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
                  {archiveTips.map((tip) => (
                    <TipCard key={tip.id} tip={tip} />
                  ))}
                </div>

                {/* Pagination */}
                {archiveTotal > 12 && (
                  <div className="flex justify-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => loadArchive(archivePage - 1)}
                      disabled={archivePage <= 1}
                    >
                      {language === 'de' ? 'Vorherige' : 'Previous'}
                    </Button>
                    <span className="flex items-center px-4 text-sm text-muted-foreground">
                      {language === 'de' ? 'Seite' : 'Page'} {archivePage} / {Math.ceil(archiveTotal / 12)}
                    </span>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => loadArchive(archivePage + 1)}
                      disabled={archivePage >= Math.ceil(archiveTotal / 12)}
                    >
                      {language === 'de' ? 'Nächste' : 'Next'}
                    </Button>
                  </div>
                )}
              </>
            )}
          </>
        )}

        {/* CTA Section */}
        <Card className="mt-12 bg-gradient-to-r from-primary/5 via-accent/5 to-primary/10 border-primary/20">
          <CardContent className="p-6 md:p-8 text-center">
            <h3 className="text-lg font-semibold mb-2">
              {language === 'de' ? 'Lust auf mehr?' : 'Want more?'}
            </h3>
            <p className="text-muted-foreground mb-4 text-sm">
              {language === 'de' 
                ? 'Erstelle dein eigenes Pairing mit unserer KI – für jedes Gericht, das du dir vorstellen kannst.'
                : 'Create your own pairing with our AI – for any dish you can imagine.'}
            </p>
            <Button
              onClick={() => navigate('/pairing')}
              className="rounded-full px-6"
            >
              <Wine className="w-4 h-4 mr-2" />
              {language === 'de' ? 'Eigenes Pairing erstellen' : 'Create Your Own Pairing'}
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default TippDerWochePage;
