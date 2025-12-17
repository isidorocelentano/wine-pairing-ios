import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { Helmet } from 'react-helmet-async';
import { ArrowLeft, Wine, Utensils, MapPin, Grape, ChevronRight, Loader2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useLanguage } from '@/contexts/LanguageContext';
import Breadcrumb from '@/components/Breadcrumb';
import Footer from '@/components/Footer';

import { API_URL as BACKEND_URL, API } from '@/config/api';

const DynamicPairingPage = () => {
  const { slug } = useParams();
  const navigate = useNavigate();
  const { language } = useLanguage();
  const [pairing, setPairing] = useState(null);
  const [loading, setLoading] = useState(true);
  const [relatedPairings, setRelatedPairings] = useState([]);

  useEffect(() => {
    const fetchPairing = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`${API}/seo-pairings/${slug}`);
        setPairing(response.data);

        // Lade verwandte Pairings
        const relatedResponse = await axios.get(`${API}/seo-pairings`, {
          params: {
            category: response.data.dish?.category,
            limit: 4
          }
        });
        setRelatedPairings(
          relatedResponse.data.pairings.filter(p => p.slug !== slug).slice(0, 3)
        );
      } catch (error) {
        console.error('Error loading pairing:', error);
      } finally {
        setLoading(false);
      }
    };

    if (slug) {
      fetchPairing();
    }
  }, [slug]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!pairing) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="pt-6 text-center">
            <p className="text-muted-foreground">Pairing nicht gefunden</p>
            <Button onClick={() => navigate('/pairing')} className="mt-4">
              Zurück zur Pairing-Suche
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const lang = language || 'de';
  const dishName = pairing.dish?.[`name_${lang}`] || pairing.dish?.name_de;
  const wineName = pairing.wine?.name;
  const description = pairing.pairing_description?.[lang] || pairing.pairing_description?.de;
  const seoTitle = pairing.seo?.[`title_${lang}`] || pairing.seo?.title_de;
  const seoDescription = pairing.seo?.[`description_${lang}`] || pairing.seo?.description_de;

  // Schema.org für SEO
  const schemaData = {
    "@context": "https://schema.org",
    "@type": "Recipe",
    "name": `${dishName} mit ${wineName}`,
    "description": seoDescription,
    "author": {
      "@type": "Organization",
      "name": "wine-pairing.online"
    },
    "datePublished": pairing.created_at,
    "keywords": pairing.seo?.keywords?.join(", "),
    "recipeCategory": pairing.dish?.category,
    "recipeCuisine": pairing.dish?.cuisine
  };

  return (
    <>
      <Helmet>
        <title>{seoTitle} | wine-pairing.online</title>
        <meta name="description" content={seoDescription} />
        <meta property="og:title" content={seoTitle} />
        <meta property="og:description" content={seoDescription} />
        <meta property="og:type" content="article" />
        <meta property="og:url" content={pairing.url} />
        <link rel="canonical" href={pairing.url} />
        <script type="application/ld+json">
          {JSON.stringify(schemaData)}
        </script>
      </Helmet>

      <div className="min-h-screen pb-20 md:pb-24" data-testid="dynamic-pairing-page">
        <div className="container mx-auto px-4 py-8 md:py-12 max-w-4xl">
          
          {/* Breadcrumb */}
          <Breadcrumb 
            items={[
              { name: 'Home', url: 'https://wine-pairing.online/' },
              { name: 'Pairing', url: 'https://wine-pairing.online/pairing' },
              { name: `${dishName} & ${wineName}`, url: pairing.url, isLast: true }
            ]}
          />

          {/* Back Button */}
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate(-1)}
            className="mb-6"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Zurück
          </Button>

          {/* Main Content */}
          <article className="space-y-8">
            
            {/* Header */}
            <header className="space-y-4">
              <div className="flex flex-wrap gap-2">
                <Badge variant="outline">{pairing.dish?.cuisine}</Badge>
                <Badge variant="outline">{pairing.dish?.category}</Badge>
                <Badge className="bg-primary/10 text-primary">{pairing.wine?.color}</Badge>
              </div>
              
              <h1 className="text-2xl md:text-4xl font-bold tracking-tight">
                {dishName}
                <span className="text-primary"> & </span>
                {wineName}
              </h1>
              
              <p className="text-lg text-muted-foreground">
                {seoDescription}
              </p>
            </header>

            {/* Pairing Cards */}
            <div className="grid md:grid-cols-2 gap-6">
              
              {/* Dish Card */}
              <Card className="bg-card/50 backdrop-blur-sm border-border/50">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Utensils className="h-5 w-5 text-primary" />
                    {lang === 'de' ? 'Das Gericht' : lang === 'en' ? 'The Dish' : 'Le Plat'}
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <h3 className="text-xl font-semibold">{dishName}</h3>
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="secondary">{pairing.dish?.cuisine}</Badge>
                    <Badge variant="secondary">{pairing.dish?.category}</Badge>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {pairing.dish?.keywords?.map((kw, i) => (
                      <span key={i} className="text-xs text-muted-foreground bg-secondary px-2 py-1 rounded">
                        {kw}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Wine Card */}
              <Card className="bg-card/50 backdrop-blur-sm border-border/50">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Wine className="h-5 w-5 text-primary" />
                    {lang === 'de' ? 'Der Wein' : lang === 'en' ? 'The Wine' : 'Le Vin'}
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <h3 className="text-xl font-semibold">{wineName}</h3>
                  <div className="space-y-2 text-sm text-muted-foreground">
                    <p className="flex items-center gap-2">
                      <MapPin className="h-4 w-4" />
                      {pairing.wine?.region}, {pairing.wine?.country}
                    </p>
                    {pairing.wine?.grape && (
                      <p className="flex items-center gap-2">
                        <Grape className="h-4 w-4" />
                        {pairing.wine?.grape}
                      </p>
                    )}
                  </div>
                  <Badge className="bg-primary/10 text-primary">{pairing.wine?.color}</Badge>
                </CardContent>
              </Card>
            </div>

            {/* Pairing Description */}
            <Card className="bg-secondary/30">
              <CardHeader>
                <CardTitle>
                  {lang === 'de' ? 'Warum dieses Pairing funktioniert' : 
                   lang === 'en' ? 'Why This Pairing Works' : 
                   'Pourquoi Cet Accord Fonctionne'}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-lg leading-relaxed">{description}</p>
              </CardContent>
            </Card>

            {/* Wine Description */}
            {pairing.wine?.[`description_${lang}`] && (
              <Card>
                <CardHeader>
                  <CardTitle>
                    {lang === 'de' ? 'Über den Wein' : 
                     lang === 'en' ? 'About the Wine' : 
                     'À Propos du Vin'}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{pairing.wine[`description_${lang}`]}</p>
                </CardContent>
              </Card>
            )}

            {/* CTA */}
            <Card className="bg-primary/5 border-primary/20">
              <CardContent className="py-6 text-center">
                <h3 className="text-lg font-semibold mb-2">
                  {lang === 'de' ? 'Möchten Sie mehr Pairings entdecken?' : 
                   lang === 'en' ? 'Want to discover more pairings?' : 
                   'Envie de découvrir plus d\'accords?'}
                </h3>
                <Button onClick={() => navigate('/pairing')} className="mt-2">
                  {lang === 'de' ? 'Eigenes Pairing finden' : 
                   lang === 'en' ? 'Find Your Own Pairing' : 
                   'Trouvez Votre Accord'}
                </Button>
              </CardContent>
            </Card>

            {/* Related Pairings */}
            {relatedPairings.length > 0 && (
              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  {lang === 'de' ? 'Weitere Empfehlungen' : 
                   lang === 'en' ? 'More Recommendations' : 
                   'Plus de Recommandations'}
                </h2>
                <div className="grid md:grid-cols-3 gap-4">
                  {relatedPairings.map((p) => (
                    <Link 
                      key={p.slug} 
                      to={`/pairing/${p.slug}`}
                      className="block"
                    >
                      <Card className="h-full hover:border-primary/50 transition-colors">
                        <CardContent className="pt-4">
                          <p className="font-medium line-clamp-2">
                            {p.dish?.[`name_${lang}`] || p.dish?.name_de}
                          </p>
                          <p className="text-sm text-muted-foreground mt-1 line-clamp-1">
                            {p.wine?.name}
                          </p>
                          <div className="flex items-center text-primary text-sm mt-2">
                            <span>Mehr erfahren</span>
                            <ChevronRight className="h-4 w-4" />
                          </div>
                        </CardContent>
                      </Card>
                    </Link>
                  ))}
                </div>
              </section>
            )}
          </article>
        </div>
        <Footer />
      </div>
    </>
  );
};

export default DynamicPairingPage;
