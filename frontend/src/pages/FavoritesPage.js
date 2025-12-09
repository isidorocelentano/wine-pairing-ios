import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Heart, Bookmark, Trash2, Wine, Loader2 } from 'lucide-react';
import { Card, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { toast } from 'sonner';
import { Helmet } from 'react-helmet-async';
import { useLanguage } from '../contexts/LanguageContext';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function FavoritesPage() {
  const { t } = useContext(LanguageContext);
  const [favorites, setFavorites] = useState([]);
  const [wishlist, setWishlist] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('favorites');

  useEffect(() => {
    fetchLists();
  }, []);

  const fetchLists = async () => {
    setLoading(true);
    try {
      // Fetch favorites
      const favResponse = await axios.get(`${API}/favorites?wishlist_only=false`);
      setFavorites(favResponse.data);

      // Fetch wishlist
      const wishResponse = await axios.get(`${API}/favorites?wishlist_only=true`);
      setWishlist(wishResponse.data);
    } catch (error) {
      console.error('Error fetching lists:', error);
      toast.error('Fehler beim Laden der Listen');
    } finally {
      setLoading(false);
    }
  };

  const removeWine = async (wineId, listType) => {
    try {
      await axios.delete(`${API}/favorites/${wineId}`);
      
      if (listType === 'favorites') {
        setFavorites(prev => prev.filter(w => w.wine_id !== wineId));
        toast.success('Wein aus Favoriten entfernt');
      } else {
        setWishlist(prev => prev.filter(w => w.wine_id !== wineId));
        toast.success('Wein aus Wunschliste entfernt');
      }
    } catch (error) {
      console.error('Error removing wine:', error);
      toast.error('Fehler beim Entfernen');
    }
  };

  const moveToList = async (wine, toWishlist) => {
    try {
      await axios.post(`${API}/favorites/${wine.wine_id}?is_wishlist=${toWishlist}`);
      
      // Refresh lists
      await fetchLists();
      
      toast.success(toWishlist ? 'Zu Wunschliste verschoben' : 'Zu Favoriten verschoben');
    } catch (error) {
      console.error('Error moving wine:', error);
      toast.error('Fehler beim Verschieben');
    }
  };

  const getWineColorBadge = (color) => {
    const colorMap = {
      'rot': 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300',
      'weiss': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300',
      'rose': 'bg-pink-100 text-pink-800 dark:bg-pink-900/30 dark:text-pink-300',
      'suesswein': 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300',
      'schaumwein': 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
    };
    return colorMap[color] || 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300';
  };

  const WineCard = ({ wine, listType }) => (
    <Card className="bg-card/50 backdrop-blur-sm border-border/50 hover-lift overflow-hidden">
      <CardContent className="p-5">
        <div className="flex items-start justify-between mb-3">
          <Badge className={getWineColorBadge(wine.wine_color)}>
            {wine.wine_color}
          </Badge>
          <span className="text-xs text-muted-foreground">
            {new Date(wine.added_at).toLocaleDateString('de-DE')}
          </span>
        </div>

        <h3 className="font-bold text-lg mb-1 line-clamp-2 leading-tight">
          {wine.wine_name}
        </h3>
        <p className="text-sm text-muted-foreground mb-3">{wine.winery}</p>
        
        <div className="text-xs text-muted-foreground mb-4">
          📍 {wine.region}, {wine.country}
        </div>

        <div className="flex gap-2">
          <Button
            size="sm"
            variant="outline"
            className="flex-1"
            onClick={() => moveToList(wine, listType === 'favorites')}
          >
            {listType === 'favorites' ? (
              <>
                <Bookmark className="h-4 w-4 mr-2" />
                Zur Wunschliste
              </>
            ) : (
              <>
                <Heart className="h-4 w-4 mr-2" />
                Zu Favoriten
              </>
            )}
          </Button>
          <Button
            size="sm"
            variant="outline"
            className="text-destructive hover:bg-destructive hover:text-destructive-foreground"
            onClick={() => removeWine(wine.wine_id, listType)}
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );

  const EmptyState = ({ icon: Icon, title, description }) => (
    <Card className="bg-secondary/30 border-dashed border-2 border-border">
      <CardContent className="py-16 text-center">
        <Icon className="h-16 w-16 mx-auto mb-4 text-muted-foreground" strokeWidth={1} />
        <h3 className="text-xl font-medium mb-2">{title}</h3>
        <p className="text-muted-foreground">{description}</p>
      </CardContent>
    </Card>
  );

  return (
    <>
      <Helmet>
        <title>Meine Listen - Wine Pairing</title>
        <meta name="description" content="Verwalten Sie Ihre Lieblingsweine und Wunschliste" />
      </Helmet>

      <div className="min-h-screen pb-20 md:pb-24 pt-6 md:pt-8 px-4 md:px-12 lg:px-24">
        <div className="container mx-auto max-w-7xl">
          {/* Header */}
          <header className="text-center mb-8 md:mb-12">
            <p className="text-accent font-accent text-sm tracking-widest uppercase mb-2">
              Meine Sammlung
            </p>
            <h1 className="text-2xl md:text-4xl font-semibold tracking-tight mb-3 md:mb-4">
              Meine Weine
            </h1>
            <p className="text-muted-foreground max-w-xl mx-auto text-sm md:text-base">
              Verwalten Sie Ihre Favoriten und Wunschliste
            </p>
          </header>

          {/* Tabs */}
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-2 mb-8">
              <TabsTrigger value="favorites" className="gap-2">
                <Heart className="h-4 w-4" />
                Favoriten ({favorites.length})
              </TabsTrigger>
              <TabsTrigger value="wishlist" className="gap-2">
                <Bookmark className="h-4 w-4" />
                Wunschliste ({wishlist.length})
              </TabsTrigger>
            </TabsList>

            {/* Favorites Tab */}
            <TabsContent value="favorites">
              {loading ? (
                <div className="flex items-center justify-center py-20">
                  <Loader2 className="h-8 w-8 animate-spin text-primary" />
                </div>
              ) : favorites.length === 0 ? (
                <EmptyState
                  icon={Heart}
                  title="Noch keine Favoriten"
                  description="Fügen Sie Weine zu Ihren Favoriten hinzu, um sie hier zu sehen"
                />
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {favorites.map((wine) => (
                    <WineCard key={wine.wine_id} wine={wine} listType="favorites" />
                  ))}
                </div>
              )}
            </TabsContent>

            {/* Wishlist Tab */}
            <TabsContent value="wishlist">
              {loading ? (
                <div className="flex items-center justify-center py-20">
                  <Loader2 className="h-8 w-8 animate-spin text-primary" />
                </div>
              ) : wishlist.length === 0 ? (
                <EmptyState
                  icon={Bookmark}
                  title="Noch keine Wunschliste"
                  description="Fügen Sie Weine zu Ihrer Wunschliste hinzu, die Sie gerne probieren möchten"
                />
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {wishlist.map((wine) => (
                    <WineCard key={wine.wine_id} wine={wine} listType="wishlist" />
                  ))}
                </div>
              )}
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </>
  );
}
