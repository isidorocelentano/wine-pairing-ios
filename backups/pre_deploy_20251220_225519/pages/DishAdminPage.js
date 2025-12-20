import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { useLanguage } from '@/contexts/LanguageContext';
import { Loader2, RefreshCw, PlusCircle } from 'lucide-react';
import { toast } from 'sonner';

import { API_URL as BACKEND_URL, API } from '@/config/api';

const DishAdminPage = () => {
  const { t } = useLanguage();
  const [dishes, setDishes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('');
  const [genName, setGenName] = useState('');
  const [genCountry, setGenCountry] = useState('');
  const [genTrend, setGenTrend] = useState('');
  const [genCategory, setGenCategory] = useState('');
  const [generating, setGenerating] = useState(false);
  const [seedLoading, setSeedLoading] = useState(false);
  const [lastGenerated, setLastGenerated] = useState(null);

  const fetchDishes = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/dishes`);
      setDishes(response.data);
    } catch (error) {
      console.error('Error fetching dishes:', error);
      toast.error(t('admin_dishes_error_load'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDishes();
  }, []);

  const filteredDishes = dishes.filter((d) => {
    if (!filter.trim()) return true;
    const needle = filter.toLowerCase();
    return (
      (d.name_de || '').toLowerCase().includes(needle) ||
      (d.name_en || '').toLowerCase().includes(needle) ||
      (d.name_fr || '').toLowerCase().includes(needle) ||
      (d.country || '').toLowerCase().includes(needle) ||
      (d.bestseller_category || '').toLowerCase().includes(needle)
    );
  });

  const handleGenerate = async () => {
    if (!genName.trim()) {
      toast.error(t('admin_dishes_error_name_required'));
      return;
    }
    setGenerating(true);
    try {
      const payload = {
        base_name: genName.trim(),
      };
      if (genCountry.trim()) payload.country_hint = genCountry.trim().toLowerCase();
      if (genTrend.trim()) payload.trend_hint = genTrend.trim().toLowerCase();
      if (genCategory.trim()) payload.bestseller_category = genCategory.trim().toLowerCase();

      const response = await axios.post(`${API}/admin/dishes/generate`, payload);
      setLastGenerated(response.data);
      toast.success(t('admin_dishes_generate_success'));
      setGenName('');
      setGenCountry('');
      setGenTrend('');
      setGenCategory('');
      fetchDishes();
    } catch (error) {
      console.error('Error generating dish:', error);
      toast.error(t('admin_dishes_generate_error'));
    } finally {
      setGenerating(false);
    }
  };

  const handleSeedBatch = async () => {
    setSeedLoading(true);
    try {
      const response = await axios.post(`${API}/admin/dishes/seed-batch`);
      toast.success(t('admin_dishes_seed_started', { count: response.data.count }));
    } catch (error) {
      console.error('Error starting dish seed batch:', error);
      toast.error(t('admin_dishes_seed_error'));
    } finally {
      setSeedLoading(false);
    }
  };

  const intensityLabel = (val) => val || '';

  return (
    <div className="min-h-screen pb-20 md:pb-24 pt-6 md:pt-8 px-4 md:px-12 lg:px-24" data-testid="dish-admin-page">
      <div className="container mx-auto max-w-6xl space-y-8">
        {/* Header */}
        <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <p className="text-accent font-accent text-sm tracking-widest uppercase mb-1">
              {t('admin_dishes_tagline')}
            </p>
            <h1 className="text-2xl md:text-3xl font-semibold tracking-tight">
              {t('admin_dishes_title')}
            </h1>
            <p className="text-muted-foreground text-sm mt-1 max-w-xl">
              {t('admin_dishes_description')}
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={fetchDishes} disabled={loading}>
              {loading ? (
                <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{t('admin_dishes_refreshing')}</>
              ) : (
                <><RefreshCw className="w-4 h-4 mr-2" />{t('admin_dishes_refresh')}</>
              )}
            </Button>
          </div>
        </header>

        {/* Seed Batch */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between text-base md:text-lg">
              <span>{t('admin_dishes_seed_title')}</span>
              <Button
                variant="outline"
                size="sm"
                onClick={handleSeedBatch}
                disabled={seedLoading}
                data-testid="seed-dishes-btn"
              >
                {seedLoading ? (
                  <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{t('admin_dishes_seed_running')}</>
                ) : (
                  <><RefreshCw className="w-4 h-4 mr-2" />{t('admin_dishes_seed_button')}</>
                )}
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground max-w-2xl">
              {t('admin_dishes_seed_help')}
            </p>
          </CardContent>
        </Card>

        {/* Generator */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base md:text-lg">
              <PlusCircle className="w-5 h-5" />
              <span>{t('admin_dishes_generate_title')}</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
              <div className="md:col-span-1">
                <label className="block text-xs font-medium mb-1">
                  {t('admin_dishes_generate_name')}
                </label>
                <Input
                  value={genName}
                  onChange={(e) => setGenName(e.target.value)}
                  placeholder={t('admin_dishes_generate_name_placeholder')}
                />
              </div>
              <div>
                <label className="block text-xs font-medium mb-1">
                  {t('admin_dishes_generate_country')}
                </label>
                <Input
                  value={genCountry}
                  onChange={(e) => setGenCountry(e.target.value)}
                  placeholder={t('admin_dishes_generate_country_placeholder')}
                />
              </div>
              <div>
                <label className="block text-xs font-medium mb-1">
                  {t('admin_dishes_generate_trend')}
                </label>
                <Input
                  value={genTrend}
                  onChange={(e) => setGenTrend(e.target.value)}
                  placeholder={t('admin_dishes_generate_trend_placeholder')}
                />
              </div>
              <div>
                <label className="block text-xs font-medium mb-1">
                  {t('admin_dishes_generate_category')}
                </label>
                <Input
                  value={genCategory}
                  onChange={(e) => setGenCategory(e.target.value)}
                  placeholder={t('admin_dishes_generate_category_placeholder')}
                />
              </div>
            </div>
            <div className="flex justify-end">
              <Button onClick={handleGenerate} disabled={generating} data-testid="generate-dish-btn">
                {generating ? (
                  <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{t('admin_dishes_generate_running')}</>
                ) : (
                  <><PlusCircle className="w-4 h-4 mr-2" />{t('admin_dishes_generate_button')}</>
                )}
              </Button>
            </div>

            {lastGenerated && (
              <div className="mt-4 border-t pt-4">
                <p className="text-xs font-medium text-muted-foreground mb-2">
                  {t('admin_dishes_last_generated')}
                </p>
                <div className="flex flex-col md:flex-row gap-4">
                  <div className="flex-1">
                    <h3 className="text-sm font-semibold mb-1">{lastGenerated.name_de}</h3>
                    <p className="text-xs text-muted-foreground mb-2">
                      {lastGenerated.name_en || ''}
                    </p>
                    <div className="flex flex-wrap gap-2 text-xs">
                      {lastGenerated.country && (
                        <Badge variant="secondary">{lastGenerated.country}</Badge>
                      )}
                      {lastGenerated.bestseller_category && (
                        <Badge variant="outline">{lastGenerated.bestseller_category}</Badge>
                      )}
                      {lastGenerated.intensity && (
                        <Badge variant="outline">{intensityLabel(lastGenerated.intensity)}</Badge>
                      )}
                    </div>
                  </div>
                  <div className="flex-1 text-xs text-muted-foreground space-y-1">
                    <p><span className="font-semibold">{t('admin_dishes_labels_protein')}:</span> {lastGenerated.protein}</p>
                    <p><span className="font-semibold">{t('admin_dishes_labels_method')}:</span> {lastGenerated.cooking_method}</p>
                    <p><span className="font-semibold">{t('admin_dishes_labels_sauce')}:</span> {lastGenerated.sauce_base}</p>
                    <p><span className="font-semibold">{t('admin_dishes_labels_aromas')}:</span> {(lastGenerated.key_aromas || []).join(', ')}</p>
                    <p><span className="font-semibold">{t('admin_dishes_labels_texture')}:</span> {(lastGenerated.texture || []).join(', ')}</p>
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Existing dishes list */}
        <Card>
          <CardHeader>
            <CardTitle className="flex flex-col md:flex-row md:items-center md:justify-between gap-3 text-base md:text-lg">
              <span>{t('admin_dishes_list_title')}</span>
              <div className="flex items-center gap-2 w-full md:w-auto">
                <Input
                  value={filter}
                  onChange={(e) => setFilter(e.target.value)}
                  placeholder={t('admin_dishes_filter_placeholder')}
                  className="md:w-64"
                />
              </div>
            </CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex items-center justify-center py-10">
                <Loader2 className="w-6 h-6 animate-spin text-primary" />
              </div>
            ) : filteredDishes.length === 0 ? (
              <p className="text-sm text-muted-foreground py-4">
                {t('admin_dishes_list_empty')}
              </p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" data-testid="admin-dishes-grid">
                {filteredDishes.map((dish) => (
                  <Card key={dish.id} className="bg-card/50 border-border/60">
                    <CardContent className="p-4 space-y-2">
                      <div className="flex items-center justify-between gap-2">
                        <h3 className="text-sm font-semibold truncate">{dish.name_de}</h3>
                        {dish.bestseller_category && (
                          <Badge variant="secondary" className="text-[10px] uppercase tracking-wide">
                            {dish.bestseller_category}
                          </Badge>
                        )}
                      </div>
                      <p className="text-xs text-muted-foreground line-clamp-2">
                        {dish.country}{dish.region ? ` · ${dish.region}` : ''}
                      </p>
                      <div className="flex flex-wrap gap-1 text-[10px] text-muted-foreground mt-1">
                        {dish.intensity && <span>{t('admin_dishes_labels_intensity')}: {dish.intensity}</span>}
                        {dish.spice_level && <span>· {t('admin_dishes_labels_spice')}: {dish.spice_level}</span>}
                        {dish.fat_level && <span>· {t('admin_dishes_labels_fat')}: {dish.fat_level}</span>}
                      </div>
                      <div className="text-[10px] text-muted-foreground mt-1 truncate">
                        {(dish.trend_cuisines || []).join(', ')}
                      </div>

                      {/* Expandable technical details */}
                      <details className="mt-2 text-[11px] text-muted-foreground">
                        <summary className="cursor-pointer list-none text-primary/80 hover:text-primary font-medium flex items-center gap-1">
                          {t('admin_dishes_more_details')}
                        </summary>
                        <div className="mt-2 space-y-1">
                          <p>
                            <span className="font-semibold">{t('admin_dishes_labels_protein')}:</span>{' '}
                            {dish.protein || '-'}
                          </p>
                          <p>
                            <span className="font-semibold">{t('admin_dishes_labels_method')}:</span>{' '}
                            {dish.cooking_method || '-'}
                          </p>
                          <p>
                            <span className="font-semibold">{t('admin_dishes_labels_sauce')}:</span>{' '}
                            {dish.sauce_base || '-'}
                          </p>
                          <p>
                            <span className="font-semibold">{t('admin_dishes_labels_aromas')}:</span>{' '}
                            {(dish.key_aromas || []).join(', ') || '-'}
                          </p>
                          <p>
                            <span className="font-semibold">{t('admin_dishes_labels_texture')}:</span>{' '}
                            {(dish.texture || []).join(', ') || '-'}
                          </p>
                        </div>
                      </details>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default DishAdminPage;
