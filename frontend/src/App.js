import React, { useState, useEffect, useRef } from 'react';
import "@/App.css";
import { BrowserRouter, Routes, Route, useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import { Toaster, toast } from 'sonner';
import { Wine, Utensils, MessageCircle, Heart, Home, Camera, Upload, X, Send, Loader2, Search, Plus, Trash2, Star } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogDescription } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// ===================== NAVIGATION =====================
const Navigation = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { path: '/', icon: Home, label: 'Home' },
    { path: '/pairing', icon: Utensils, label: 'Pairing' },
    { path: '/cellar', icon: Wine, label: 'Keller' },
    { path: '/chat', icon: MessageCircle, label: 'Sommelier' },
  ];

  return (
    <nav className="nav-dock fixed bottom-6 left-1/2 -translate-x-1/2 rounded-full px-6 py-3 shadow-2xl z-50" data-testid="main-navigation">
      <div className="flex items-center gap-2">
        {navItems.map((item) => (
          <button
            key={item.path}
            onClick={() => navigate(item.path)}
            data-testid={`nav-${item.label.toLowerCase()}`}
            className={`flex items-center gap-2 px-4 py-2 rounded-full transition-elegant ${
              location.pathname === item.path
                ? 'bg-primary text-primary-foreground'
                : 'hover:bg-secondary'
            }`}
          >
            <item.icon className="w-5 h-5" strokeWidth={1.5} />
            <span className="hidden md:inline text-sm font-medium">{item.label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
};

// ===================== HOME PAGE =====================
const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen pb-24" data-testid="home-page">
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
        
        <div className="relative z-10 container mx-auto px-6 md:px-12 lg:px-24">
          <div className="max-w-2xl space-y-8 opacity-0 animate-fade-in-up" style={{ animationDelay: '0.2s', animationFillMode: 'forwards' }}>
            <p className="text-accent font-accent text-lg tracking-widest uppercase">Die Entdeckung des reinen Genusses</p>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-semibold leading-tight tracking-tight">
              Ihr virtueller Sommelier
            </h1>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Die einzige Empfehlung, die nichts verkauft, außer Ihrem perfekten Moment. 
              Entdecken Sie die Harmonie von Wein und Speise – unabhängig, ehrlich, genussvoll.
            </p>
            <div className="flex flex-wrap gap-4 pt-4">
              <Button
                onClick={() => navigate('/pairing')}
                className="rounded-full px-8 py-6 text-sm font-medium tracking-wide transition-elegant hover:scale-105 active:scale-95"
                data-testid="cta-pairing"
              >
                <Utensils className="mr-2 h-4 w-4" />
                Wein-Pairing starten
              </Button>
              <Button
                variant="outline"
                onClick={() => navigate('/cellar')}
                className="rounded-full px-8 py-6 text-sm font-medium tracking-wide border-primary/30 hover:bg-primary/5"
                data-testid="cta-cellar"
              >
                <Wine className="mr-2 h-4 w-4" />
                Mein Weinkeller
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Philosophy Section */}
      <section className="py-24 px-6 md:px-12 lg:px-24">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-12">
            <div className="md:col-span-5 space-y-6 opacity-0 animate-fade-in-up animate-delay-100" style={{ animationFillMode: 'forwards' }}>
              <p className="text-accent font-accent text-sm tracking-widest uppercase">Unsere Philosophie</p>
              <h2 className="text-3xl md:text-4xl font-semibold tracking-tight">
                Aus Frustration geboren
              </h2>
            </div>
            <div className="md:col-span-7 space-y-6 opacity-0 animate-fade-in-up animate-delay-200" style={{ animationFillMode: 'forwards' }}>
              <p className="text-muted-foreground leading-relaxed text-lg">
                Die Welt des Weins ist von Experten-Gatekeeping und verkaufsgetriebener Komplexität überladen. 
                Die meisten Wein-Apps zwingen Sie, entweder wie ein Sommelier zu sprechen oder wie ein Kunde zu kaufen.
              </p>
              <p className="text-muted-foreground leading-relaxed text-lg">
                Wir bringen die Logik des Sommeliers in Ihre Küche – basierend auf 30 Jahren Expertise und der 
                systemischen Analyse von Säure, Bitterkeit und Süße. Menschlich im Kern, präzise in der Ausführung.
              </p>
              <blockquote className="border-l-4 border-accent pl-6 py-2 font-accent text-xl italic text-foreground/80">
                „Planen Sie nicht um den Wein herum. Beginnen Sie mit dem Essen."
              </blockquote>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-16 px-6 md:px-12 lg:px-24 bg-secondary/30">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: Utensils,
                title: 'Intelligentes Pairing',
                description: 'Geben Sie Ihr Gericht ein und erhalten Sie die perfekte Weinempfehlung – aus Ihrem Keller oder allgemein.'
              },
              {
                icon: Camera,
                title: 'Etiketten-Scanner',
                description: 'Fotografieren Sie Ihre Weinetiketten und lassen Sie die KI alle wichtigen Informationen erfassen.'
              },
              {
                icon: MessageCircle,
                title: 'Persönlicher Sommelier',
                description: 'Fragen Sie unseren virtuellen Sommelier alles rund um Wein – persönlich und ohne Verkaufsdruck.'
              }
            ].map((feature, idx) => (
              <Card key={idx} className="bg-card/50 backdrop-blur-sm border-border/50 hover-lift" data-testid={`feature-card-${idx}`}>
                <CardHeader>
                  <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                    <feature.icon className="w-6 h-6 text-primary" strokeWidth={1.5} />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

// ===================== WINE PAIRING PAGE =====================
const PairingPage = () => {
  const [dish, setDish] = useState('');
  const [useCellar, setUseCellar] = useState(false);
  const [wineTypeFilter, setWineTypeFilter] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

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
      toast.error('Bitte geben Sie ein Gericht ein');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post(`${API}/pairing`, {
        dish: dish,
        use_cellar: useCellar,
        wine_type_filter: wineTypeFilter || null
      });
      setResult(response.data);
      fetchHistory();
      toast.success('Empfehlung erhalten!');
    } catch (error) {
      toast.error('Fehler bei der Empfehlung');
      console.error('Pairing error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen pb-24 pt-8 px-6 md:px-12 lg:px-24" data-testid="pairing-page">
      <div className="container mx-auto max-w-4xl">
        <header className="text-center mb-12">
          <p className="text-accent font-accent text-sm tracking-widest uppercase mb-2">Wein-Pairing</p>
          <h1 className="text-3xl md:text-4xl font-semibold tracking-tight mb-4">Was möchten Sie essen?</h1>
          <p className="text-muted-foreground max-w-xl mx-auto">
            Beschreiben Sie Ihr Gericht und unser virtueller Sommelier empfiehlt den perfekten Wein.
          </p>
        </header>

        <Card className="bg-card/50 backdrop-blur-sm border-border/50 mb-8">
          <CardContent className="p-8 space-y-6">
            <div>
              <label className="block text-sm font-medium mb-3">Ihr Gericht</label>
              <Textarea
                value={dish}
                onChange={(e) => setDish(e.target.value)}
                placeholder="z.B. Gegrilltes Rinderfilet mit Rosmarin-Kartoffeln und Rotwein-Jus..."
                className="min-h-[100px] resize-none"
                data-testid="dish-input"
              />
            </div>

            <div className="flex flex-wrap gap-4">
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={useCellar}
                  onChange={(e) => setUseCellar(e.target.checked)}
                  className="w-5 h-5 rounded border-border text-primary focus:ring-primary"
                  data-testid="use-cellar-checkbox"
                />
                <span className="text-sm">Aus meinem Keller empfehlen</span>
              </label>

              {useCellar && (
                <Select value={wineTypeFilter} onValueChange={setWineTypeFilter}>
                  <SelectTrigger className="w-[180px]" data-testid="wine-type-filter">
                    <SelectValue placeholder="Alle Weinarten" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Alle Weinarten</SelectItem>
                    <SelectItem value="rot">Rotwein</SelectItem>
                    <SelectItem value="weiss">Weißwein</SelectItem>
                    <SelectItem value="rose">Rosé</SelectItem>
                    <SelectItem value="schaumwein">Schaumwein</SelectItem>
                  </SelectContent>
                </Select>
              )}
            </div>

            <Button
              onClick={handlePairing}
              disabled={loading || !dish.trim()}
              className="w-full rounded-full py-6 text-sm font-medium tracking-wide"
              data-testid="get-pairing-btn"
            >
              {loading ? (
                <><Loader2 className="mr-2 h-4 w-4 animate-spin" />Sommelier denkt nach...</>
              ) : (
                <><Wine className="mr-2 h-4 w-4" />Empfehlung erhalten</>
              )}
            </Button>
          </CardContent>
        </Card>

        {/* Result */}
        {result && (
          <Card className="pairing-card border-border/50 mb-8 animate-fade-in-up" data-testid="pairing-result">
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="sommelier-avatar w-10 h-10 rounded-full flex items-center justify-center">
                  <Wine className="w-5 h-5 text-white" />
                </div>
                <div>
                  <CardTitle className="text-lg">Sommelier-Empfehlung</CardTitle>
                  <CardDescription>für „{result.dish}"</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="prose prose-sm max-w-none text-foreground/90 leading-relaxed whitespace-pre-wrap">
                {result.recommendation}
              </div>
              {result.cellar_matches && result.cellar_matches.length > 0 && (
                <div className="mt-6 pt-6 border-t border-border/50">
                  <p className="text-sm font-medium mb-3">Passende Weine aus Ihrem Keller:</p>
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
            <h3 className="text-lg font-medium mb-4">Letzte Empfehlungen</h3>
            <div className="space-y-3">
              {history.map((item) => (
                <Card key={item.id} className="bg-secondary/30 border-border/30 hover:bg-secondary/50 transition-colors cursor-pointer" data-testid="history-item">
                  <CardContent className="p-4">
                    <p className="font-medium">{item.dish}</p>
                    <p className="text-sm text-muted-foreground line-clamp-2 mt-1">
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
  const [wines, setWines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [showScanDialog, setShowScanDialog] = useState(false);
  const [newWine, setNewWine] = useState({ name: '', type: 'rot', region: '', year: '', grape: '', notes: '', image_base64: '' });
  const [scanning, setScanning] = useState(false);
  const fileInputRef = useRef(null);
  const scanInputRef = useRef(null);

  useEffect(() => {
    fetchWines();
  }, [filter]);

  const fetchWines = async () => {
    try {
      const params = filter !== 'all' ? `?type_filter=${filter}` : '';
      const response = await axios.get(`${API}/wines${params}`);
      setWines(response.data);
    } catch (error) {
      toast.error('Fehler beim Laden der Weine');
    } finally {
      setLoading(false);
    }
  };

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
      setNewWine({
        ...response.data,
        year: response.data.year?.toString() || '',
        image_base64: imageBase64
      });
      setShowScanDialog(false);
      setShowAddDialog(true);
      toast.success('Etikett erfolgreich gescannt!');
    } catch (error) {
      toast.error('Fehler beim Scannen des Etiketts');
    } finally {
      setScanning(false);
    }
  };

  const handleAddWine = async () => {
    if (!newWine.name.trim()) {
      toast.error('Bitte geben Sie einen Weinnamen ein');
      return;
    }

    try {
      await axios.post(`${API}/wines`, {
        ...newWine,
        year: newWine.year ? parseInt(newWine.year) : null
      });
      toast.success('Wein hinzugefügt!');
      setShowAddDialog(false);
      setNewWine({ name: '', type: 'rot', region: '', year: '', grape: '', notes: '', image_base64: '' });
      fetchWines();
    } catch (error) {
      toast.error('Fehler beim Hinzufügen');
    }
  };

  const handleToggleFavorite = async (wineId) => {
    try {
      await axios.post(`${API}/wines/${wineId}/favorite`);
      fetchWines();
    } catch (error) {
      toast.error('Fehler');
    }
  };

  const handleDeleteWine = async (wineId) => {
    try {
      await axios.delete(`${API}/wines/${wineId}`);
      toast.success('Wein gelöscht');
      fetchWines();
    } catch (error) {
      toast.error('Fehler beim Löschen');
    }
  };

  const getWineTypeBadgeClass = (type) => {
    const classes = {
      rot: 'badge-rot',
      weiss: 'badge-weiss',
      rose: 'badge-rose',
      schaumwein: 'badge-schaumwein'
    };
    return classes[type] || 'bg-secondary';
  };

  return (
    <div className="min-h-screen pb-24 pt-8 px-6 md:px-12 lg:px-24" data-testid="cellar-page">
      <div className="container mx-auto">
        <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
          <div>
            <p className="text-accent font-accent text-sm tracking-widest uppercase mb-2">Mein Weinkeller</p>
            <h1 className="text-3xl md:text-4xl font-semibold tracking-tight">Ihre Schatzkammer</h1>
          </div>
          <div className="flex flex-wrap gap-3">
            <Select value={filter} onValueChange={setFilter}>
              <SelectTrigger className="w-[160px]" data-testid="cellar-filter">
                <SelectValue placeholder="Filter" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Alle Weine</SelectItem>
                <SelectItem value="rot">Rotwein</SelectItem>
                <SelectItem value="weiss">Weißwein</SelectItem>
                <SelectItem value="rose">Rosé</SelectItem>
                <SelectItem value="schaumwein">Schaumwein</SelectItem>
              </SelectContent>
            </Select>
            
            <Dialog open={showScanDialog} onOpenChange={setShowScanDialog}>
              <DialogTrigger asChild>
                <Button variant="outline" className="rounded-full" data-testid="scan-label-btn">
                  <Camera className="mr-2 h-4 w-4" />Etikett scannen
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Weinetikett scannen</DialogTitle>
                  <DialogDescription>Fotografieren Sie das Etikett, um den Wein automatisch zu erfassen.</DialogDescription>
                </DialogHeader>
                <div 
                  className="upload-zone rounded-lg p-12 text-center cursor-pointer"
                  onClick={() => scanInputRef.current?.click()}
                >
                  {scanning ? (
                    <div className="flex flex-col items-center gap-3">
                      <Loader2 className="h-8 w-8 animate-spin text-primary" />
                      <p className="text-sm text-muted-foreground">Analysiere Etikett...</p>
                    </div>
                  ) : (
                    <>
                      <Camera className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                      <p className="text-sm text-muted-foreground">Klicken Sie hier, um ein Foto aufzunehmen</p>
                    </>
                  )}
                </div>
                <input
                  ref={scanInputRef}
                  type="file"
                  accept="image/*"
                  capture="environment"
                  className="hidden"
                  onChange={(e) => handleImageUpload(e, true)}
                />
              </DialogContent>
            </Dialog>

            <Dialog open={showAddDialog} onOpenChange={setShowAddDialog}>
              <DialogTrigger asChild>
                <Button className="rounded-full" data-testid="add-wine-btn">
                  <Plus className="mr-2 h-4 w-4" />Wein hinzufügen
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-md">
                <DialogHeader>
                  <DialogTitle>Neuen Wein hinzufügen</DialogTitle>
                  <DialogDescription>Fügen Sie einen Wein zu Ihrem Keller hinzu.</DialogDescription>
                </DialogHeader>
                <div className="space-y-4">
                  <Input
                    placeholder="Weinname *"
                    value={newWine.name}
                    onChange={(e) => setNewWine({ ...newWine, name: e.target.value })}
                    data-testid="wine-name-input"
                  />
                  <Select value={newWine.type} onValueChange={(v) => setNewWine({ ...newWine, type: v })}>
                    <SelectTrigger data-testid="wine-type-select">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="rot">Rotwein</SelectItem>
                      <SelectItem value="weiss">Weißwein</SelectItem>
                      <SelectItem value="rose">Rosé</SelectItem>
                      <SelectItem value="schaumwein">Schaumwein</SelectItem>
                    </SelectContent>
                  </Select>
                  <div className="grid grid-cols-2 gap-4">
                    <Input
                      placeholder="Region"
                      value={newWine.region}
                      onChange={(e) => setNewWine({ ...newWine, region: e.target.value })}
                    />
                    <Input
                      placeholder="Jahrgang"
                      type="number"
                      value={newWine.year}
                      onChange={(e) => setNewWine({ ...newWine, year: e.target.value })}
                    />
                  </div>
                  <Input
                    placeholder="Rebsorte"
                    value={newWine.grape}
                    onChange={(e) => setNewWine({ ...newWine, grape: e.target.value })}
                  />
                  <Textarea
                    placeholder="Notizen"
                    value={newWine.notes}
                    onChange={(e) => setNewWine({ ...newWine, notes: e.target.value })}
                  />
                  
                  {/* Image Upload */}
                  <div 
                    className="upload-zone rounded-lg p-6 text-center cursor-pointer"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    {newWine.image_base64 ? (
                      <div className="relative">
                        <img 
                          src={`data:image/jpeg;base64,${newWine.image_base64}`} 
                          alt="Preview" 
                          className="max-h-32 mx-auto rounded"
                        />
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setNewWine({ ...newWine, image_base64: '' });
                          }}
                          className="absolute -top-2 -right-2 bg-destructive text-white rounded-full p-1"
                        >
                          <X className="h-3 w-3" />
                        </button>
                      </div>
                    ) : (
                      <>
                        <Upload className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
                        <p className="text-sm text-muted-foreground">Bild hochladen (optional)</p>
                      </>
                    )}
                  </div>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={(e) => handleImageUpload(e, false)}
                  />

                  <Button onClick={handleAddWine} className="w-full rounded-full" data-testid="save-wine-btn">
                    Wein speichern
                  </Button>
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
            <CardContent className="py-16 text-center">
              <Wine className="h-16 w-16 mx-auto mb-4 text-muted-foreground" strokeWidth={1} />
              <h3 className="text-xl font-medium mb-2">Ihr Keller ist noch leer</h3>
              <p className="text-muted-foreground mb-6">Fügen Sie Ihren ersten Wein hinzu oder scannen Sie ein Etikett.</p>
              <Button onClick={() => setShowAddDialog(true)} className="rounded-full">
                <Plus className="mr-2 h-4 w-4" />Ersten Wein hinzufügen
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6" data-testid="wine-grid">
            {wines.map((wine) => (
              <Card key={wine.id} className="wine-card bg-card/50 backdrop-blur-sm border-border/50 overflow-hidden group" data-testid="wine-card">
                {wine.image_base64 ? (
                  <div className="aspect-[4/3] overflow-hidden bg-secondary/30">
                    <img
                      src={`data:image/jpeg;base64,${wine.image_base64}`}
                      alt={wine.name}
                      className="w-full h-full object-cover"
                    />
                  </div>
                ) : (
                  <div className="aspect-[4/3] bg-secondary/30 flex items-center justify-center">
                    <Wine className="h-16 w-16 text-muted-foreground/30" strokeWidth={1} />
                  </div>
                )}
                <CardContent className="p-4">
                  <div className="flex items-start justify-between mb-2">
                    <Badge className={`${getWineTypeBadgeClass(wine.type)} border-0 text-xs`}>
                      {wine.type === 'rot' ? 'Rotwein' : wine.type === 'weiss' ? 'Weißwein' : wine.type === 'rose' ? 'Rosé' : 'Schaumwein'}
                    </Badge>
                    <button
                      onClick={() => handleToggleFavorite(wine.id)}
                      className="text-muted-foreground hover:text-primary transition-colors"
                      data-testid="favorite-btn"
                    >
                      <Star className={`h-5 w-5 ${wine.is_favorite ? 'fill-accent text-accent' : ''}`} />
                    </button>
                  </div>
                  <h3 className="font-medium text-lg leading-tight mb-1">{wine.name}</h3>
                  <div className="text-sm text-muted-foreground space-y-0.5">
                    {wine.region && <p>{wine.region}</p>}
                    <div className="flex gap-2">
                      {wine.year && <span>{wine.year}</span>}
                      {wine.grape && <span>• {wine.grape}</span>}
                    </div>
                  </div>
                  <div className="flex gap-2 mt-4 opacity-0 group-hover:opacity-100 transition-opacity">
                    <Button
                      variant="destructive"
                      size="sm"
                      className="flex-1 rounded-full"
                      onClick={() => handleDeleteWine(wine.id)}
                      data-testid="delete-wine-btn"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// ===================== SOMMELIER CHAT PAGE =====================
const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [imageBase64, setImageBase64] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

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
        image_base64: imageBase64
      });

      setSessionId(response.data.session_id);
      setMessages((prev) => [...prev, { role: 'assistant', content: response.data.response }]);
      setImageBase64(null);
    } catch (error) {
      toast.error('Fehler im Chat');
      console.error('Chat error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImageBase64(reader.result.split(',')[1]);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="min-h-screen pb-24 pt-8 px-6 md:px-12 lg:px-24" data-testid="chat-page">
      <div className="container mx-auto max-w-3xl h-[calc(100vh-180px)] flex flex-col">
        <header className="text-center mb-6">
          <div className="sommelier-avatar w-16 h-16 rounded-full mx-auto mb-4 flex items-center justify-center">
            <MessageCircle className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-2xl md:text-3xl font-semibold tracking-tight">Ihr Sommelier</h1>
          <p className="text-muted-foreground text-sm mt-2">
            30 Jahre Erfahrung, keine Verkaufsabsicht – nur ehrliche Beratung.
          </p>
        </header>

        <Card className="flex-1 bg-card/50 backdrop-blur-sm border-border/50 flex flex-col overflow-hidden">
          <ScrollArea className="flex-1 p-6">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center py-12">
                <Wine className="h-12 w-12 text-muted-foreground/30 mb-4" strokeWidth={1} />
                <p className="text-muted-foreground">Stellen Sie mir eine Frage über Wein...</p>
                <div className="flex flex-wrap gap-2 mt-6 justify-center">
                  {['Welcher Wein zu Pasta?', 'Rotwein oder Weißwein?', 'Was ist ein Terroir?'].map((q) => (
                    <button
                      key={q}
                      onClick={() => setInput(q)}
                      className="px-4 py-2 bg-secondary/50 rounded-full text-sm hover:bg-secondary transition-colors"
                    >
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] p-4 ${
                        msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-assistant'
                      }`}
                      data-testid={`chat-message-${msg.role}`}
                    >
                      {msg.image && (
                        <img
                          src={`data:image/jpeg;base64,${msg.image}`}
                          alt="Uploaded"
                          className="max-w-[200px] rounded mb-2"
                        />
                      )}
                      <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="flex justify-start">
                    <div className="chat-bubble-assistant p-4">
                      <Loader2 className="h-5 w-5 animate-spin" />
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </ScrollArea>

          <div className="p-4 border-t border-border/50">
            {imageBase64 && (
              <div className="mb-3 relative inline-block">
                <img
                  src={`data:image/jpeg;base64,${imageBase64}`}
                  alt="Preview"
                  className="h-16 rounded"
                />
                <button
                  onClick={() => setImageBase64(null)}
                  className="absolute -top-2 -right-2 bg-destructive text-white rounded-full p-1"
                >
                  <X className="h-3 w-3" />
                </button>
              </div>
            )}
            <div className="flex gap-3">
              <button
                onClick={() => fileInputRef.current?.click()}
                className="p-3 rounded-full bg-secondary hover:bg-secondary/80 transition-colors"
                data-testid="chat-upload-btn"
              >
                <Camera className="h-5 w-5" />
              </button>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handleImageUpload}
              />
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Fragen Sie den Sommelier..."
                className="flex-1 rounded-full"
                data-testid="chat-input"
              />
              <Button
                onClick={handleSend}
                disabled={loading || (!input.trim() && !imageBase64)}
                className="rounded-full px-6"
                data-testid="chat-send-btn"
              >
                <Send className="h-5 w-5" />
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
    <div className="App" data-testid="wine-pairing-app">
      <Toaster position="top-center" richColors />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<><HomePage /><Navigation /></>} />
          <Route path="/pairing" element={<><PairingPage /><Navigation /></>} />
          <Route path="/cellar" element={<><CellarPage /><Navigation /></>} />
          <Route path="/chat" element={<><ChatPage /><Navigation /></>} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
