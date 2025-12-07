import React from 'react';
import { useLanguage } from '@/contexts/LanguageContext';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { SEO } from '@/components/SEO';
import PairingSeoPageExport from '@/pages/PairingSeoPage';

// Reuse the templates from PairingSeoPage via named export
const { PAIRING_TEMPLATES } = PairingSeoPageExport;

const SeoPairingExplorerPage = () => {
  const { t, language } = useLanguage();
  const navigate = useNavigate();
  const lang = language || 'de';

  const entries = Object.entries(PAIRING_TEMPLATES).map(([slug, tpl]) => ({ slug, tpl }));

  return (
    <div className="min-h-screen pb-20 md:pb-24 pt-6 md:pt-8 px-4 md:px-12 lg:px-24">
      <SEO
        title="SEO Pairing Explorer"
        description="Interner Überblick über alle statischen Pairing-Landingpages"
        url="https://wine-pairing.online/seo/pairings"
      />
      <div className="container mx-auto max-w-5xl space-y-6">
        <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <p className="text-accent font-accent text-xs tracking-widest uppercase mb-1">SEO Tools</p>
            <h1 className="text-2xl md:text-3xl font-semibold tracking-tight">SEO Pairing Explorer</h1>
            <p className="text-sm text-muted-foreground mt-1 max-w-2xl">
              Übersicht aller aktuell hinterlegten Pairing-Landingpages. Ideal für Review, Testing und spätere Programmatic-SEO-Skalierung.
            </p>
          </div>
        </header>

        <Card>
          <CardHeader>
            <CardTitle className="text-base md:text-lg">Aktuelle Pairings</CardTitle>
          </CardHeader>
          <CardContent>
            {entries.length === 0 ? (
              <p className="text-sm text-muted-foreground">Noch keine Pairings hinterlegt.</p>
            ) : (
              <div className="space-y-3" data-testid="seo-pairing-list">
                {entries.map(({ slug, tpl }) => (
                  <div
                    key={slug}
                    className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-border/40 pb-3 last:border-b-0"
                  >
                    <div className="space-y-1 text-sm">
                      <p className="text-xs uppercase tracking-wide text-muted-foreground">Slug</p>
                      <p className="font-mono text-xs break-all">/pairing/{slug}</p>
                      <p className="mt-1 font-semibold">
                        {tpl.page.title[lang] || tpl.page.title.de}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        Gericht: {tpl.recipe.name[lang] || tpl.recipe.name.de} · Wein: {tpl.wine.name[lang] || tpl.wine.name.de}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => navigate(`/pairing/${slug}`)}
                        data-testid="open-seo-pairing-btn"
                      >
                        Seite öffnen
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default SeoPairingExplorerPage;
