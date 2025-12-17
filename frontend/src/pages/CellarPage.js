import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import axios from "axios";
import { toast } from 'sonner';
import { Wine, Camera, Upload, X, Loader2, Plus, Trash2, Star, Edit, Minus, LogIn } from 'lucide-react';
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

// Axios instance mit credentials für auth
const authAxios = axios.create({
  withCredentials: true
});

const CellarPage = () => {
  const { t, language } = useLanguage();
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [wines, setWines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [inStockOnly, setInStockOnly] = useState(false);
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [showScanDialog, setShowScanDialog] = useState(false);
  const [showEditDialog, setShowEditDialog] = useState(false);
  const [editingWine, setEditingWine] = useState(null);
  const [newWine, setNewWine] = useState({ name: '', type: 'rot', region: '', year: '', grape: '', description: '', notes: '', image_base64: '', quantity: 1 });
  const [scanning, setScanning] = useState(false);
  const [updatingQuantity, setUpdatingQuantity] = useState(null); // Track which wine is being updated
  const fileInputRef = useRef(null);
  const scanInputRef = useRef(null);

  // Calculate cellar statistics
  const cellarStats = useMemo(() => {
    const totalBottles = wines.reduce((sum, wine) => sum + (wine.quantity || 0), 0);
    const byType = wines.reduce((acc, wine) => {
      const type = wine.type || 'other';
      acc[type] = (acc[type] || 0) + (wine.quantity || 0);
      return acc;
    }, {});
    const uniqueWines = wines.length;
    return { totalBottles, byType, uniqueWines };
  }, [wines]);

  const fetchWines = useCallback(async () => {
    try {
      const params = [];
      if (filter !== 'all') {
        params.push(`type_filter=${filter}`);
      }
      if (inStockOnly) {
        params.push('in_stock_only=true');
      }
      const query = params.length ? `?${params.join('&')}` : '';
      const response = await axios.get(`${API}/wines${query}`);
      setWines(response.data);
    } catch (error) {
      toast.error(t('error_general'));
    } finally {
      setLoading(false);
    }
  }, [filter, inStockOnly, t]);


  useEffect(() => {
    fetchWines();
  }, [fetchWines]);

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
      setNewWine((prev) => ({
        ...prev,
        ...response.data,
        year: response.data.year?.toString() || '',
        image_base64: imageBase64,
        quantity: typeof prev.quantity === 'number' ? prev.quantity : 1,
      }));
      setShowScanDialog(false);
      setShowAddDialog(true);
      toast.success(t('success_label_scanned'));
    } catch (error) {
      toast.error(t('error_general'));
    } finally {
      setScanning(false);
    }
  };

  const handleAddWine = async () => {
    if (!newWine.name.trim()) {
      toast.error(t('error_wine_name'));
      return;
    }

    try {
      await axios.post(`${API}/wines`, {
        ...newWine,
        year: newWine.year ? parseInt(newWine.year) : null,
        quantity: newWine.quantity ? parseInt(newWine.quantity, 10) : 1,
      });
      toast.success(t('success_wine_added'));
      setShowAddDialog(false);
      setNewWine({ name: '', type: 'rot', region: '', year: '', grape: '', description: '', notes: '', image_base64: '', quantity: 1 });
      fetchWines();
    } catch (error) {
      toast.error(t('error_general'));
    }
  };

  // Quick quantity update (+/- buttons)
  const handleQuickQuantityChange = async (wineId, delta) => {
    const wine = wines.find(w => w.id === wineId);
    if (!wine) return;
    
    const newQuantity = Math.max(0, (wine.quantity || 0) + delta);
    setUpdatingQuantity(wineId);
    
    try {
      await axios.put(`${API}/wines/${wineId}`, {
        ...wine,
        quantity: newQuantity,
      });
      // Optimistic update
      setWines(prev => prev.map(w => 
        w.id === wineId ? { ...w, quantity: newQuantity } : w
      ));
      if (delta > 0) {
        toast.success(`+${delta} Flasche${delta > 1 ? 'n' : ''} hinzugefügt`);
      } else {
        toast.success(`${Math.abs(delta)} Flasche${Math.abs(delta) > 1 ? 'n' : ''} entfernt`);
      }
    } catch (error) {
      toast.error(t('error_general'));
      fetchWines(); // Revert on error
    } finally {
      setUpdatingQuantity(null);
    }
  };

  const handleToggleFavorite = async (wineId) => {
    try {
      await axios.post(`${API}/wines/${wineId}/favorite`);
      fetchWines();
    } catch (error) {
      toast.error(t('error_general'));
    }
  };

  const handleDeleteWine = async (wineId) => {
    try {
      await axios.delete(`${API}/wines/${wineId}`);
      toast.success(t('success_wine_deleted'));
      fetchWines();
    } catch (error) {
      toast.error(t('error_general'));
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
      description: wine.description || '',  // Include description field
      notes: wine.notes || '',
      quantity: typeof wine.quantity === 'number' ? wine.quantity : 1,
    });
    setShowEditDialog(true);
  };

  const handleUpdateWine = async () => {
    try {
      await axios.put(`${API}/wines/${editingWine.id}`, {
        name: editingWine.name,
        type: editingWine.type,
        region: editingWine.region || null,
        year: editingWine.year ? parseInt(editingWine.year) : null,
        grape: editingWine.grape || null,
        notes: editingWine.notes || null,
        quantity: typeof editingWine.quantity === 'number' ? editingWine.quantity : parseInt(editingWine.quantity || '1', 10),
      });
      toast.success('Wein erfolgreich aktualisiert!');
      setShowEditDialog(false);
      setEditingWine(null);
      fetchWines();
    } catch (error) {
      toast.error(t('error_general'));
    }
  };

  const getWineTypeBadgeClass = (type) => {
    const classes = { rot: 'badge-rot', weiss: 'badge-weiss', rose: 'badge-rose', schaumwein: 'badge-schaumwein' };
    return classes[type] || 'bg-secondary';
  };

  const getWineTypeLabel = (type) => {
    const labels = { rot: t('pairing_red'), weiss: t('pairing_white'), rose: t('pairing_rose'), schaumwein: t('pairing_sparkling') };
    return labels[type] || type;
  };

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
              <span className="text-primary/60 text-4xl md:text-5xl font-serif">"</span>
              {language === 'de' 
                ? 'Nicht nur Wein, sondern die perfekte Kombination – für dich, aus deinem Keller, mit deinem Geschmack.'
                : language === 'en'
                ? 'Not just wine, but the perfect combination – for you, from your cellar, tailored to your taste.'
                : 'Pas seulement du vin, mais la combinaison parfaite – pour vous, de votre cave, selon vos goûts.'}
              <span className="text-primary/60 text-4xl md:text-5xl font-serif">"</span>
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
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-6" data-testid="wine-grid">
            {wines.map((wine) => (
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
