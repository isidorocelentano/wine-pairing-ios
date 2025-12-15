import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { useLanguage } from '@/contexts/LanguageContext';
import { Loader2, RefreshCw, PlusCircle } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const GrapeAdminPage = () => {
  const { t, language } = useLanguage();
  const [grapes, setGrapes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('');
  const [genName, setGenName] = useState('');
  const [genType, setGenType] = useState('auto');
  const [genHint, setGenHint] = useState('');
  const [generating, setGenerating] = useState(false);
  const [normalizeLoading, setNormalizeLoading] = useState(false);
  const [lastGenerated, setLastGenerated] = useState(null);

  const fetchGrapes = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/grapes`);
      setGrapes(response.data);
    } catch (error) {
      console.error('Error fetching grapes:', error);
      toast.error(t('admin_grapes_error_load'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGrapes();
  }, []);

  const filteredGrapes = grapes.filter((g) => {
    if (!filter.trim()) return true;
    const needle = filter.toLowerCase();
    return (
      g.name.toLowerCase().includes(needle) ||
      (g.synonyms || []).some((s) => s.toLowerCase().includes(needle))
    );
  });

  const handleGenerate = async () => {
    if (!genName.trim()) {
      toast.error(t('admin_grapes_error_name_required'));
      return;
    }
    setGenerating(true);
    try {
      const payload = {
        name: genName.trim(),
      };
      if (genType !== 'auto') {
        payload.grape_type = genType;
      }
      if (genHint.trim()) {
        payload.style_hint = genHint.trim();
      }
      const response = await axios.post(`${API}/admin/grapes/generate`, payload);
      setLastGenerated(response.data);
      toast.success(t('admin_grapes_generate_success'));
      setGenName('');
      setGenHint('');
      setGenType('auto');
      fetchGrapes();
    } catch (error) {
      console.error('Error generating grape:', error);
      toast.error(t('admin_grapes_generate_error'));
    } finally {
      setGenerating(false);
    }
  };

  const handleNormalize = async () => {
    setNormalizeLoading(true);
    try {
      const response = await axios.post(`${API}/admin/grapes/normalize`);
      toast.success(t('admin_grapes_normalize_done', { count: response.data.normalized }));
      fetchGrapes();
    } catch (error) {
      console.error('Error normalizing grapes:', error);
      toast.error(t('admin_grapes_normalize_error'));
    } finally {
      setNormalizeLoading(false);
    }
  };

  const typeLabel = (type) => {
    if (type === 'rot') return t('grapes_red');
    if (type === 'weiss') return t('grapes_white');
    return type;
  };

  return (
    <div className="min-h-screen pb-20 md:pb-24 pt-6 md:pt-8 px-4 md:px-12 lg:px-24" data-testid="grape-admin-page">
      <div className="container mx-auto max-w-6xl space-y-8">
        {/* Header */}
        <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <p className="text-accent font-accent text-sm tracking-widest uppercase mb-1">
              {t('admin_grapes_tagline')}
            </p>
            <h1 className="text-2xl md:text-3xl font-semibold tracking-tight">
              {t('admin_grapes_title')}
            </h1>
            <p className="text-muted-foreground text-sm mt-1 max-w-xl">
              {t('admin_grapes_description')}
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={fetchGrapes} disabled={loading}>
              {loading ? (
                <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{t('admin_grapes_refreshing')}</>
              ) : (
                <><RefreshCw className="w-4 h-4 mr-2" />{t('admin_grapes_refresh')}</>
              )}
            </Button>
          </div>
        </header>

        {/* Normalization */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between text-base md:text-lg">
              <span>{t('admin_grapes_normalize_title')}</span>
              <Button
                variant="outline"
                size="sm"
                onClick={handleNormalize}
                disabled={normalizeLoading}
                data-testid="normalize-grapes-btn"
              >
                {normalizeLoading ? (
                  <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{t('admin_grapes_normalizing')}</>
                ) : (
                  <><RefreshCw className="w-4 h-4 mr-2" />{t('admin_grapes_normalize_button')}</>
                )}
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground max-w-2xl">
              {t('admin_grapes_normalize_help')}
            </p>
          </CardContent>
        </Card>

        {/* Generator */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base md:text-lg">
              <PlusCircle className="w-5 h-5" />
              <span>{t('admin_grapes_generate_title')}</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div className="md:col-span-1">
                <label className="block text-xs font-medium mb-1">
                  {t('admin_grapes_generate_name')}
                </label>
                <Input
                  value={genName}
                  onChange={(e) => setGenName(e.target.value)}
                  placeholder={t('admin_grapes_generate_name_placeholder')}
                />
              </div>
              <div>
                <label className="block text-xs font-medium mb-1">
                  {t('admin_grapes_generate_type')}
                </label>
                <select
                  className="w-full border rounded-md px-2 py-2 bg-background"
                  value={genType}
                  onChange={(e) => setGenType(e.target.value)}
                >
                  <option value="auto">{t('admin_grapes_generate_type_auto')}</option>
                  <option value="rot">{t('grapes_red')}</option>
                  <option value="weiss">{t('grapes_white')}</option>
                </select>
              </div>
              <div className="md:col-span-1">
                <label className="block text-xs font-medium mb-1">
                  {t('admin_grapes_generate_hint')}
                </label>
                <Input
                  value={genHint}
                  onChange={(e) => setGenHint(e.target.value)}
                  placeholder={t('admin_grapes_generate_hint_placeholder')}
                />
              </div>
            </div>
            <div className="flex justify-end">
              <Button onClick={handleGenerate} disabled={generating} data-testid="generate-grape-btn">
                {generating ? (
                  <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{t('admin_grapes_generate_running')}</>
                ) : (
                  <><PlusCircle className="w-4 h-4 mr-2" />{t('admin_grapes_generate_button')}</>
                )}
              </Button>
            </div>

            {lastGenerated && (
              <div className="mt-4 border-t pt-4">
                <p className="text-xs font-medium text-muted-foreground mb-2">
                  {t('admin_grapes_last_generated')}
                </p>
                <div className="flex flex-col md:flex-row gap-4">
                  <div className="flex-1">
                    <h3 className="text-sm font-semibold mb-1">{lastGenerated.name}</h3>
                    <p className="text-xs text-muted-foreground mb-2">
                      {lastGenerated.description?.slice(0, 220)}{lastGenerated.description?.length > 220 ? '…' : ''}
                    </p>
                    <div className="flex flex-wrap gap-2 text-xs">
                      <Badge variant="secondary">{typeLabel(lastGenerated.type)}</Badge>
                      {lastGenerated.body && (
                        <Badge variant="outline">{lastGenerated.body}</Badge>
                      )}
                      {lastGenerated.acidity && (
                        <Badge variant="outline">{t('grapes_acidity')}: {lastGenerated.acidity}</Badge>
                      )}
                      {lastGenerated.tannin && (
                        <Badge variant="outline">{t('grapes_tannin')}: {lastGenerated.tannin}</Badge>
                      )}
                    </div>
                  </div>
                  <div className="flex-1 text-xs text-muted-foreground space-y-1">
                    <p><span className="font-semibold">{t('grapes_primary_aromas')}:</span> {(lastGenerated.primary_aromas || []).join(', ')}</p>
                    <p><span className="font-semibold">{t('grapes_tertiary_aromas')}:</span> {(lastGenerated.tertiary_aromas || []).join(', ')}</p>
                    <p><span className="font-semibold">{t('grapes_perfect_pairings')}:</span> {(lastGenerated.perfect_pairings || []).join(', ')}</p>
                    <p><span className="font-semibold">{t('grapes_main_regions')}:</span> {(lastGenerated.main_regions || []).join(', ')}</p>
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Existing grapes list */}
        <Card>
          <CardHeader>
            <CardTitle className="flex flex-col md:flex-row md:items-center md:justify-between gap-3 text-base md:text-lg">
              <span>{t('admin_grapes_list_title')}</span>
              <div className="flex items-center gap-2 w-full md:w-auto">
                <Input
                  value={filter}
                  onChange={(e) => setFilter(e.target.value)}
                  placeholder={t('admin_grapes_filter_placeholder')}
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
            ) : filteredGrapes.length === 0 ? (
              <p className="text-sm text-muted-foreground py-4">
                {t('admin_grapes_list_empty')}
              </p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" data-testid="admin-grapes-grid">
                {filteredGrapes.map((grape) => (
                  <Card key={grape.id} className="bg-card/50 border-border/60">
                    <CardContent className="p-4 space-y-2">
                      <div className="flex items-center justify-between gap-2">
                        <h3 className="text-sm font-semibold truncate">{grape.name}</h3>
                        <Badge className={grape.type === 'rot' ? 'badge-rot border-0' : 'badge-weiss border-0'}>
                          {typeLabel(grape.type)}
                        </Badge>
                      </div>
                      <p className="text-xs text-muted-foreground line-clamp-3">
                        {grape.description?.slice(0, 140)}{grape.description?.length > 140 ? '…' : ''}
                      </p>
                      <div className="flex flex-wrap gap-1 text-[10px] text-muted-foreground mt-1">
                        {grape.body && <span>{t('grapes_body')}: {grape.body}</span>}
                        {grape.acidity && <span>· {t('grapes_acidity')}: {grape.acidity}</span>}
                        {grape.tannin && <span>· {t('grapes_tannin')}: {grape.tannin}</span>}
                      </div>
                      <div className="text-[10px] text-muted-foreground mt-1 truncate">
                        {(grape.main_regions || []).slice(0, 3).join(', ')}
                      </div>
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

export default GrapeAdminPage;
