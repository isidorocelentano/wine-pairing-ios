import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { toast } from 'sonner';
import { Wine, Camera, Upload, X, Loader2, Plus, Trash2, Star, Edit, Minus, LogIn, Sparkles, Grape, Thermometer, UtensilsCrossed, Clock, Crown, Search } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogDescription } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useLanguage } from "@/contexts/LanguageContext";
import { useAuth } from "@/contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { API_URL, API } from "@/config/api";

const CellarPage = () => {
  const { t, language } = useLanguage();
  const { user, isAuthenticated, loading: authLoading, isPro } = useAuth();
  const navigate = useNavigate();
  const [wines, setWines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [priceFilter, setPriceFilter] = useState('all');
  const [inStockOnly, setInStockOnly] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [showScanDialog, setShowScanDialog] = useState(false);
  const [showEditDialog, setShowEditDialog] = useState(false);
  const [editingWine, setEditingWine] = useState(null);
  const [newWine, setNewWine] = useState({ name: '', type: 'rot', region: '', year: '', grape: '', description: '', notes: '', image_base64: '', quantity: 1, price_category: '' });
  const [scanning, setScanning] = useState(false);
  const [updatingQuantity, setUpdatingQuantity] = useState(null);
  const [enrichingWine, setEnrichingWine] = useState(null);
  const [showWineDetail, setShowWineDetail] = useState(null);
  const fileInputRef = useRef(null);

  // Price category labels
  const priceCategoryLabels = {
    '1': { emoji: '🍷', label: language === 'de' ? 'bis €20' : language === 'en' ? 'up to €20' : 'jusqu\'à €20' },
    '2': { emoji: '🍷🍷', label: language === 'de' ? '€20-50' : '€20-50' },
    '3': { emoji: '🍷🍷🍷', label: language === 'de' ? 'ab €50' : language === 'en' ? '€50+' : 'à partir de €50' }
  };
  const scanInputRef = useRef(null);

  // Normalize wine type for consistent display and counting
  const normalizeWineType = (type) => {
    if (!type) return 'other';
    const normalized = type.toLowerCase().trim();
    // Map all variations to standard types
    if (normalized === 'rot' || normalized === 'rotwein' || normalized === 'red') return 'rot';
    if (normalized === 'weiss' || normalized === 'weiß' || normalized === 'weisswein' || normalized === 'weißwein' || normalized === 'white' || normalized === 'blanc') return 'weiss';
    if (normalized === 'rose' || normalized === 'rosé' || normalized === 'rosewein' || normalized === 'roséwein') return 'rose';
    if (normalized === 'schaumwein' || normalized === 'sparkling' || normalized === 'champagne' || normalized === 'sekt' || normalized === 'prosecco' || normalized === 'cava') return 'schaumwein';
    if (normalized === 'suesswein' || normalized === 'süsswein' || normalized === 'dessert' || normalized === 'sweet') return 'suesswein';
    return 'other';
  };

  // Calculate cellar statistics
  const cellarStats = useMemo(() => {
    const totalBottles = wines.reduce((sum, wine) => sum + (wine.quantity || 0), 0);
    const byType = wines.reduce((acc, wine) => {
      const type = normalizeWineType(wine.type);
      acc[type] = (acc[type] || 0) + (wine.quantity || 0);
      return acc;
    }, {});
    const uniqueWines = wines.length;
    return { totalBottles, byType, uniqueWines };
  }, [wines]);

  // Filter wines by search query and filters
  const filteredWines = useMemo(() => {
    let result = wines;
    
    // Text search across multiple fields
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase().trim();
      result = result.filter(wine => {
        const searchFields = [
          wine.name,
          wine.region,
          wine.grape,
          wine.description,
          wine.notes,
          wine.appellation,
          wine.year?.toString(),
          wine.grape_varieties?.join(' ')
        ].filter(Boolean).join(' ').toLowerCase();
        return searchFields.includes(query);
      });
    }
    
    // Type filter
    if (filter !== 'all') {
      result = result.filter(wine => normalizeWineType(wine.type) === filter);
    }
    
    // Price filter
    if (priceFilter !== 'all') {
      result = result.filter(wine => wine.price_category === priceFilter);
    }
    
    // In stock filter
    if (inStockOnly) {
      result = result.filter(wine => (wine.quantity || 0) > 0);
    }
    
    return result;
  }, [wines, searchQuery, filter, priceFilter, inStockOnly]);

  const fetchWines = useCallback(async () => {
    // Nicht laden wenn nicht eingeloggt
    if (!isAuthenticated) {
      setLoading(false);
      return;
    }
    
    try {
      const token = localStorage.getItem('wine_auth_token');
      if (!token) {
        setLoading(false);
        return;
      }
      
      const params = [];
      if (filter !== 'all') {
        params.push(`type_filter=${filter}`);
      }
      if (inStockOnly) {
        params.push('in_stock_only=true');
      }
      const query = params.length ? `?${params.join('&')}` : '';
      
      const response = await fetch(`${API}/wines${query}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setWines(data);
      } else if (response.status === 401) {
        toast.error(t('error_login_required') || 'Bitte melden Sie sich an');
      }
    } catch (error) {
      console.error('Fetch wines error:', error);
      toast.error(t('error_general'));
    } finally {
      setLoading(false);
    }
  }, [filter, inStockOnly, t, isAuthenticated]);


  useEffect(() => {
    fetchWines();
  }, [fetchWines]);

  // Einfache Bildkomprimierung für iOS Safari
  const compressImageSimple = (dataUrl) => {
    return new Promise((resolve) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const MAX = 800;
        let w = img.width;
        let h = img.height;
        if (w > h && w > MAX) { h = h * MAX / w; w = MAX; }
        else if (h > MAX) { w = w * MAX / h; h = MAX; }
        canvas.width = w;
        canvas.height = h;
        canvas.getContext('2d').drawImage(img, 0, 0, w, h);
        resolve(canvas.toDataURL('image/jpeg', 0.5).split(',')[1]);
      };
      img.src = dataUrl;
    });
  };

  const handleImageUpload = (e, isScan = false) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = async (event) => {
      try {
        const base64 = await compressImageSimple(event.target.result);
        
        if (isScan) {
          // Setze Bild sofort
          setNewWine(prev => ({ ...prev, image_base64: base64 }));
          setScanning(true);
          
          // API Call
          try {
            const token = localStorage.getItem('wine_auth_token');
            const resp = await fetch(`${API}/scan-label`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                ...(token ? { 'Authorization': `Bearer ${token}` } : {})
              },
              body: JSON.stringify({ image_base64: base64 })
            });
            
            if (resp.ok) {
              const data = await resp.json();
              setNewWine(prev => ({
                ...prev,
                name: data.name || '',
                type: data.type || 'rot',
                region: data.region || '',
                year: data.year?.toString() || '',
                grape: data.grape || '',
                notes: data.notes || '',
              }));
              toast.success(t('success_label_scanned'));
            } else {
              toast.error('Scan fehlgeschlagen');
            }
          } catch (err) {
            toast.error('Scan fehlgeschlagen');
          }
          
          setScanning(false);
          setShowScanDialog(false);
          setShowAddDialog(true);
        } else {
          setNewWine(prev => ({ ...prev, image_base64: base64 }));
        }
      } catch (err) {
        toast.error('Fehler beim Verarbeiten');
      }
    };
    reader.readAsDataURL(file);
  };

  const handleAddWine = async () => {
    if (!newWine.name.trim()) {
      toast.error(t('error_wine_name'));
      return;
    }

    try {
      // Explizit Token aus localStorage holen (iOS Safari kompatibel)
      const token = localStorage.getItem('wine_auth_token');
      
      if (!token) {
        toast.error(language === 'de' ? 'Bitte melden Sie sich erneut an' : 'Please log in again');
        return;
      }
      
      const wineData = {
        ...newWine,
        year: newWine.year ? parseInt(newWine.year) : null,
        quantity: newWine.quantity ? parseInt(newWine.quantity, 10) : 1,
      };
      
      // Fetch statt axios für bessere iOS Safari Kompatibilität
      const response = await fetch(`${API}/wines`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(wineData)
      });
      
      if (response.ok) {
        toast.success(t('success_wine_added'));
        setShowAddDialog(false);
        setNewWine({ name: '', type: 'rot', region: '', year: '', grape: '', description: '', notes: '', image_base64: '', quantity: 1 });
        fetchWines();
      } else {
        const errorData = await response.json().catch(() => ({}));
        const errorMsg = errorData.detail || (language === 'de' ? 'Fehler beim Speichern' : 'Error saving wine');
        toast.error(errorMsg);
      }
    } catch (error) {
      console.error('Wine save error:', error);
      toast.error(language === 'de' ? 'Verbindungsfehler - bitte erneut versuchen' : 'Connection error - please try again');
    }
  };

  // Quick quantity update (+/- buttons)
  const handleQuickQuantityChange = async (wineId, delta) => {
    const wine = wines.find(w => w.id === wineId);
    if (!wine) return;
    
    const newQuantity = Math.max(0, (wine.quantity || 0) + delta);
    setUpdatingQuantity(wineId);
    
    try {
      const token = localStorage.getItem('wine_auth_token');
      if (!token) {
        toast.error(language === 'de' ? 'Bitte melden Sie sich erneut an' : 'Please log in again');
        return;
      }
      
      const response = await fetch(`${API}/wines/${wineId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ ...wine, quantity: newQuantity })
      });
      
      if (response.ok) {
        // Optimistic update
        setWines(prev => prev.map(w => 
          w.id === wineId ? { ...w, quantity: newQuantity } : w
        ));
        if (delta > 0) {
          toast.success(`+${delta} Flasche${delta > 1 ? 'n' : ''} hinzugefügt`);
        } else {
          toast.success(`${Math.abs(delta)} Flasche${Math.abs(delta) > 1 ? 'n' : ''} entfernt`);
        }
      } else {
        toast.error(t('error_general'));
        fetchWines();
      }
    } catch (error) {
      console.error('Quantity update error:', error);
      toast.error(t('error_general'));
      fetchWines(); // Revert on error
    } finally {
      setUpdatingQuantity(null);
    }
  };

  const handleToggleFavorite = async (wineId) => {
    try {
      const token = localStorage.getItem('wine_auth_token');
      if (!token) return;
      
      const response = await fetch(`${API}/wines/${wineId}/favorite`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        fetchWines();
      }
    } catch (error) {
      toast.error(t('error_general'));
    }
  };

  const handleDeleteWine = async (wineId) => {
    try {
      const token = localStorage.getItem('wine_auth_token');
      if (!token) return;
      
      const response = await fetch(`${API}/wines/${wineId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        toast.success(t('success_wine_deleted'));
        fetchWines();
      } else {
        toast.error(t('error_general'));
      }
    } catch (error) {
      toast.error(t('error_general'));
    }
  };

  // Enrich wine with AI-generated details
  const handleEnrichWine = async (wineId) => {
    if (!isPro) {
      toast.error(language === 'de' ? 'Wein-Anreicherung ist ein Pro-Feature' : 'Wine enrichment is a Pro feature');
      return;
    }
    
    setEnrichingWine(wineId);
    
    try {
      const token = localStorage.getItem('wine_auth_token');
      const response = await fetch(`${API}/wines/${wineId}/enrich`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      const data = await response.json();
      
      if (response.ok) {
        if (data.status === 'already_enriched') {
          toast.info(language === 'de' ? 'Dieser Wein wurde bereits angereichert' : 'This wine is already enriched');
        } else {
          toast.success(language === 'de' ? '🍷 Wein-Details erfolgreich geladen!' : '🍷 Wine details loaded successfully!');
          fetchWines();
        }
        // Show detail view
        setShowWineDetail(data.wine);
      } else {
        toast.error(data.detail || (language === 'de' ? 'Fehler beim Anreichern' : 'Enrichment failed'));
      }
    } catch (error) {
      console.error('Enrich error:', error);
      toast.error(language === 'de' ? 'Verbindungsfehler' : 'Connection error');
    } finally {
      setEnrichingWine(null);
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
      description: wine.description || '',
      notes: wine.notes || '',
      quantity: typeof wine.quantity === 'number' ? wine.quantity : 1,
      image_base64: wine.image_base64 || '',
    });
    setShowEditDialog(true);
  };

  // Handle image upload for editing
  const handleEditImageUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.error(language === 'de' ? 'Bild zu groß (max. 5MB)' : 'Image too large (max 5MB)');
      return;
    }
    
    try {
      const reader = new FileReader();
      reader.onload = () => {
        const base64 = reader.result.split(',')[1];
        setEditingWine(prev => ({ ...prev, image_base64: base64 }));
        toast.success(language === 'de' ? 'Bild hinzugefügt!' : 'Image added!');
      };
      reader.readAsDataURL(file);
    } catch (error) {
      console.error('Image upload error:', error);
      toast.error(language === 'de' ? 'Fehler beim Hochladen' : 'Upload error');
    }
  };

  const handleUpdateWine = async () => {
    try {
      const token = localStorage.getItem('wine_auth_token');
      if (!token) {
        toast.error(language === 'de' ? 'Bitte melden Sie sich erneut an' : 'Please log in again');
        return;
      }
      
      const updateData = {
        name: editingWine.name,
        type: editingWine.type,
        region: editingWine.region || null,
        year: editingWine.year ? parseInt(editingWine.year) : null,
        grape: editingWine.grape || null,
        notes: editingWine.notes || null,
        quantity: typeof editingWine.quantity === 'number' ? editingWine.quantity : parseInt(editingWine.quantity || '1', 10),
      };
      
      // Include image if it exists
      if (editingWine.image_base64) {
        updateData.image_base64 = editingWine.image_base64;
      }
      
      const response = await fetch(`${API}/wines/${editingWine.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(updateData)
      });
      
      if (response.ok) {
        toast.success('Wein erfolgreich aktualisiert!');
        setShowEditDialog(false);
        setEditingWine(null);
        fetchWines();
      } else {
        const errorData = await response.json().catch(() => ({}));
        toast.error(errorData.detail || t('error_general'));
      }
    } catch (error) {
      console.error('Update wine error:', error);
      toast.error(t('error_general'));
    }
  };

  const getWineTypeBadgeClass = (type) => {
    const normalizedType = normalizeWineType(type);
    const classes = { rot: 'badge-rot', weiss: 'badge-weiss', rose: 'badge-rose', schaumwein: 'badge-schaumwein', suesswein: 'badge-schaumwein' };
    return classes[normalizedType] || 'bg-secondary';
  };

  const getWineTypeLabel = (type) => {
    const normalizedType = normalizeWineType(type);
    const labels = { rot: t('pairing_red'), weiss: t('pairing_white'), rose: t('pairing_rose'), schaumwein: t('pairing_sparkling'), suesswein: language === 'de' ? 'Süß' : 'Sweet' };
    return labels[normalizedType] || type;
  };

  // Auth Loading State
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  // Not authenticated - show login prompt
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen pb-20 md:pb-24 relative" data-testid="cellar-page">
        <div className="fixed inset-0 z-0 pointer-events-none" aria-hidden="true">
          <img 
            src="https://images.unsplash.com/photo-1561906814-23da9a8bfee0?auto=format&fit=crop&w=1920&q=80"
            alt=""
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-background/95 via-background/90 to-background/95"></div>
        </div>
        
        <div className="relative z-10 pt-6 md:pt-8 px-4 md:px-12 lg:px-24">
          <div className="container mx-auto max-w-lg">
            <Card className="mt-20 p-8 text-center">
              <Wine className="h-16 w-16 mx-auto text-primary/60 mb-6" />
              <h1 className="text-2xl font-semibold mb-4">
                {language === 'de' ? 'Ihr persönlicher Weinkeller' : language === 'en' ? 'Your Personal Wine Cellar' : 'Votre Cave Personnelle'}
              </h1>
              <p className="text-muted-foreground mb-6">
                {language === 'de' 
                  ? 'Melden Sie sich an, um Ihre Weinsammlung zu verwalten und personalisierte Empfehlungen zu erhalten.'
                  : language === 'en'
                  ? 'Sign in to manage your wine collection and get personalized recommendations.'
                  : 'Connectez-vous pour gérer votre collection de vins et obtenir des recommandations personnalisées.'}
              </p>
              <Button 
                onClick={() => navigate('/login')}
                className="rounded-full px-8 py-6"
              >
                <LogIn className="mr-2 h-5 w-5" />
                {language === 'de' ? 'Anmelden' : language === 'en' ? 'Sign In' : 'Se connecter'}
              </Button>
            </Card>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-20 md:pb-24 relative" data-testid="cellar-page">
      {/* Background Image */}
      <div 
        className="fixed inset-0 z-0 pointer-events-none"
        aria-hidden="true"
      >
        <img 
          src="https://images.unsplash.com/photo-1561906814-23da9a8bfee0?auto=format&fit=crop&w=1920&q=80"
          alt=""
          className="w-full h-full object-cover"
        />
        {/* Dark overlay for readability */}
        <div className="absolute inset-0 bg-gradient-to-b from-background/95 via-background/90 to-background/95"></div>
      </div>
      
      <div className="relative z-10 pt-6 md:pt-8 px-4 md:px-12 lg:px-24">
        <div className="container mx-auto">
        
        {/* Hero Slogan */}
        <div className="mb-8 md:mb-12 text-center">
          <div className="inline-block relative">
            <div className="absolute inset-0 bg-gradient-to-r from-primary/20 via-accent/20 to-primary/20 blur-3xl opacity-50"></div>
            <blockquote className="relative text-lg md:text-2xl lg:text-3xl font-light italic text-foreground/90 leading-relaxed max-w-4xl mx-auto px-4">
              <span className="text-primary/60 text-4xl md:text-5xl font-serif">&ldquo;</span>
              {language === 'de' 
                ? 'Nicht nur Wein, sondern die perfekte Kombination – für dich, aus deinem Keller, mit deinem Geschmack.'
                : language === 'en'
                ? 'Not just wine, but the perfect combination – for you, from your cellar, tailored to your taste.'
                : 'Pas seulement du vin, mais la combinaison parfaite – pour vous, de votre cave, selon vos goûts.'}
              <span className="text-primary/60 text-4xl md:text-5xl font-serif">&rdquo;</span>
            </blockquote>
            <div className="mt-4 flex items-center justify-center gap-3">
              <div className="h-px w-12 bg-gradient-to-r from-transparent via-primary/40 to-transparent"></div>
              <Wine className="h-5 w-5 text-primary/60" />
              <div className="h-px w-12 bg-gradient-to-r from-transparent via-primary/40 to-transparent"></div>
            </div>
          </div>
        </div>

        <header className="flex flex-col gap-4 mb-6 md:mb-8">
          <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
            <div>
              <p className="text-accent font-accent text-sm tracking-widest uppercase mb-2">{t('cellar_tagline')}</p>
              <h1 className="text-2xl md:text-4xl font-semibold tracking-tight">{t('cellar_title')}</h1>
            </div>
            
            {/* Cellar Statistics Card */}
            {wines.length > 0 && (
              <Card className="bg-primary/5 border-primary/20 min-w-[200px]">
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="flex items-center justify-center gap-2 mb-2">
                      <Wine className="h-5 w-5 text-primary" />
                      <span className="text-3xl font-bold text-primary">{cellarStats.totalBottles}</span>
                    </div>
                    <p className="text-sm text-muted-foreground font-medium">
                      {cellarStats.totalBottles === 1 ? 'Flasche' : 'Flaschen'} total
                    </p>
                    <p className="text-xs text-muted-foreground mt-1">
                      {cellarStats.uniqueWines} {cellarStats.uniqueWines === 1 ? 'Wein' : 'verschiedene Weine'}
                    </p>
                    {/* Mini breakdown by type */}
                    <div className="flex flex-wrap justify-center gap-2 mt-3">
                      {cellarStats.byType.rot > 0 && (
                        <Badge variant="outline" className="text-xs badge-rot border-0">{cellarStats.byType.rot}x Rot</Badge>
                      )}
                      {cellarStats.byType.weiss > 0 && (
                        <Badge variant="outline" className="text-xs badge-weiss border-0">{cellarStats.byType.weiss}x Weiß</Badge>
                      )}
                      {cellarStats.byType.rose > 0 && (
                        <Badge variant="outline" className="text-xs badge-rose border-0">{cellarStats.byType.rose}x Rosé</Badge>
                      )}
                      {cellarStats.byType.schaumwein > 0 && (
                        <Badge variant="outline" className="text-xs badge-schaumwein border-0">{cellarStats.byType.schaumwein}x Schaum</Badge>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
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

          {/* Search Input */}
          <div className="relative w-full md:w-auto">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder={language === 'de' ? 'Wein suchen...' : language === 'fr' ? 'Rechercher...' : 'Search wines...'}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 pr-8 h-10 w-full md:w-[200px] lg:w-[250px]"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-2 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>

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
        ) : filteredWines.length === 0 ? (
          <Card className="bg-secondary/30 border-dashed border-2 border-border">
            <CardContent className="py-12 md:py-16 text-center">
              <Search className="h-12 md:h-16 w-12 md:w-16 mx-auto mb-4 text-muted-foreground" strokeWidth={1} />
              <h3 className="text-lg md:text-xl font-medium mb-2">
                {language === 'de' ? 'Keine Weine gefunden' : language === 'fr' ? 'Aucun vin trouvé' : 'No wines found'}
              </h3>
              <p className="text-muted-foreground mb-6 text-sm md:text-base">
                {language === 'de' ? 'Versuchen Sie eine andere Suche oder Filter' : language === 'fr' ? 'Essayez une autre recherche' : 'Try a different search or filter'}
              </p>
              <Button variant="outline" onClick={() => { setSearchQuery(''); setFilter('all'); setPriceFilter('all'); setInStockOnly(false); }} className="rounded-full">
                <X className="mr-2 h-4 w-4" />
                {language === 'de' ? 'Filter zurücksetzen' : language === 'fr' ? 'Réinitialiser' : 'Reset filters'}
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-6" data-testid="wine-grid">
            {filteredWines.map((wine) => (
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
                    
                    {/* Quick Quantity Controls with +/- Buttons */}
                    <div className="flex items-center justify-between mt-2 py-2 px-1 bg-secondary/30 rounded-lg">
                      <button
                        onClick={(e) => { e.stopPropagation(); handleQuickQuantityChange(wine.id, -1); }}
                        disabled={updatingQuantity === wine.id || (wine.quantity || 0) <= 0}
                        className="w-8 h-8 flex items-center justify-center rounded-full bg-background hover:bg-destructive/10 hover:text-destructive disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        data-testid="quantity-minus-btn"
                      >
                        <Minus className="h-4 w-4" />
                      </button>
                      <div className="flex flex-col items-center">
                        <span className="text-lg font-bold text-foreground">
                          {updatingQuantity === wine.id ? (
                            <Loader2 className="h-4 w-4 animate-spin" />
                          ) : (
                            wine.quantity || 0
                          )}
                        </span>
                        <span className="text-[10px] text-muted-foreground">Flaschen</span>
                      </div>
                      <button
                        onClick={(e) => { e.stopPropagation(); handleQuickQuantityChange(wine.id, 1); }}
                        disabled={updatingQuantity === wine.id}
                        className="w-8 h-8 flex items-center justify-center rounded-full bg-background hover:bg-primary/10 hover:text-primary disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        data-testid="quantity-plus-btn"
                      >
                        <Plus className="h-4 w-4" />
                      </button>
                    </div>

                    <div className="flex gap-2 mt-1">
                      {wine.year && <span>{wine.year}</span>}
                      {wine.grape && <span className="hidden md:inline">• {wine.grape}</span>}
                    </div>
                  </div>
                  <div className="flex gap-2 mt-3 md:mt-4 opacity-100 md:opacity-0 md:group-hover:opacity-100 transition-opacity">
                    {/* Enrich Button - Only for Pro users */}
                    {isPro && !wine.is_enriched && (
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="flex-1 rounded-full text-xs bg-amber-50 border-amber-300 hover:bg-amber-100 text-amber-700"
                        onClick={() => handleEnrichWine(wine.id)}
                        disabled={enrichingWine === wine.id}
                      >
                        {enrichingWine === wine.id ? (
                          <Loader2 className="h-3 w-3 animate-spin" />
                        ) : (
                          <Sparkles className="h-3 w-3" />
                        )}
                      </Button>
                    )}
                    {/* Show detail for enriched wines */}
                    {wine.is_enriched && (
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="flex-1 rounded-full text-xs bg-green-50 border-green-300 hover:bg-green-100 text-green-700"
                        onClick={() => setShowWineDetail(wine)}
                      >
                        <Wine className="h-3 w-3" />
                      </Button>
                    )}
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

        {/* Wine Detail Modal (Enriched) */}
        <Dialog open={!!showWineDetail} onOpenChange={(open) => !open && setShowWineDetail(null)}>
          <DialogContent className="mx-4 max-w-lg max-h-[90vh] overflow-y-auto">
            {showWineDetail && (
              <>
                <DialogHeader>
                  <div className="flex items-center gap-2">
                    {showWineDetail.is_enriched && (
                      <Badge className="bg-green-100 text-green-700 border-green-300">
                        <Sparkles className="w-3 h-3 mr-1" />
                        Angereichert
                      </Badge>
                    )}
                  </div>
                  <DialogTitle className="text-xl">{showWineDetail.name}</DialogTitle>
                  <DialogDescription>
                    {showWineDetail.year && `${showWineDetail.year} • `}
                    {showWineDetail.region}
                    {showWineDetail.appellation && ` • ${showWineDetail.appellation}`}
                  </DialogDescription>
                </DialogHeader>
                
                <div className="space-y-4 pt-4">
                  {/* Emotional Description */}
                  {showWineDetail.description && (
                    <div className="bg-gradient-to-r from-primary/5 to-primary/10 p-4 rounded-lg border border-primary/20">
                      <p className="text-sm italic leading-relaxed">{showWineDetail.description}</p>
                    </div>
                  )}
                  
                  {/* Grape Varieties */}
                  {showWineDetail.grape_varieties?.length > 0 && (
                    <div>
                      <h4 className="text-sm font-semibold flex items-center gap-2 mb-2">
                        <Grape className="w-4 h-4 text-purple-600" />
                        Rebsorten
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {showWineDetail.grape_varieties.map((grape, i) => (
                          <Badge key={i} variant="outline">{grape}</Badge>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {/* Taste Profile */}
                  {showWineDetail.taste_profile && (
                    <div>
                      <h4 className="text-sm font-semibold mb-2">Geschmacksprofil</h4>
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        {showWineDetail.taste_profile.body && (
                          <div className="bg-secondary/50 p-2 rounded">
                            <span className="text-muted-foreground">Körper:</span> {showWineDetail.taste_profile.body}
                          </div>
                        )}
                        {showWineDetail.taste_profile.tannins && (
                          <div className="bg-secondary/50 p-2 rounded">
                            <span className="text-muted-foreground">Tannine:</span> {showWineDetail.taste_profile.tannins}
                          </div>
                        )}
                        {showWineDetail.taste_profile.acidity && (
                          <div className="bg-secondary/50 p-2 rounded">
                            <span className="text-muted-foreground">Säure:</span> {showWineDetail.taste_profile.acidity}
                          </div>
                        )}
                        {showWineDetail.taste_profile.finish && (
                          <div className="bg-secondary/50 p-2 rounded">
                            <span className="text-muted-foreground">Abgang:</span> {showWineDetail.taste_profile.finish}
                          </div>
                        )}
                      </div>
                      {showWineDetail.taste_profile.aromas?.length > 0 && (
                        <div className="mt-2">
                          <span className="text-sm text-muted-foreground">Aromen: </span>
                          <span className="text-sm">{showWineDetail.taste_profile.aromas.join(", ")}</span>
                        </div>
                      )}
                    </div>
                  )}
                  
                  {/* Serving Info */}
                  <div className="grid grid-cols-2 gap-3">
                    {showWineDetail.serving_temp && (
                      <div className="flex items-center gap-2 bg-blue-50 p-3 rounded-lg">
                        <Thermometer className="w-4 h-4 text-blue-600" />
                        <div>
                          <div className="text-xs text-muted-foreground">Temperatur</div>
                          <div className="text-sm font-medium">{showWineDetail.serving_temp}</div>
                        </div>
                      </div>
                    )}
                    {showWineDetail.drinking_window && (
                      <div className="flex items-center gap-2 bg-amber-50 p-3 rounded-lg">
                        <Clock className="w-4 h-4 text-amber-600" />
                        <div>
                          <div className="text-xs text-muted-foreground">Trinkreife</div>
                          <div className="text-sm font-medium">{showWineDetail.drinking_window}</div>
                        </div>
                      </div>
                    )}
                  </div>
                  
                  {/* Food Pairings */}
                  {showWineDetail.food_pairings?.length > 0 && (
                    <div>
                      <h4 className="text-sm font-semibold flex items-center gap-2 mb-2">
                        <UtensilsCrossed className="w-4 h-4 text-orange-600" />
                        Passt hervorragend zu
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {showWineDetail.food_pairings.map((food, i) => (
                          <Badge key={i} variant="secondary">{food}</Badge>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {/* Winery Info */}
                  {showWineDetail.winery_info && (
                    <div className="border-t pt-4">
                      <h4 className="text-sm font-semibold mb-2">Über das Weingut</h4>
                      <p className="text-sm text-muted-foreground">{showWineDetail.winery_info}</p>
                    </div>
                  )}
                </div>
                
                <div className="flex gap-2 pt-4">
                  <Button variant="outline" onClick={() => setShowWineDetail(null)} className="flex-1">
                    Schließen
                  </Button>
                  <Button onClick={() => { setShowWineDetail(null); navigate(`/pairing?wine=${showWineDetail.name}`); }} className="flex-1">
                    <UtensilsCrossed className="w-4 h-4 mr-2" />
                    Pairing finden
                  </Button>
                </div>
              </>
            )}
          </DialogContent>
        </Dialog>

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
    </div>
  );
};

export default CellarPage;
