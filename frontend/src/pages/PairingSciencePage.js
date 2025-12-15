import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Wine, Utensils, Beaker, Scale, Thermometer, Droplets, 
  Flame, Leaf, ChevronRight, CheckCircle2, XCircle,
  Gauge, CircleDot, Info
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useLanguage } from '@/contexts/LanguageContext';
import Breadcrumb from '@/components/Breadcrumb';
import Footer from '@/components/Footer';

/**
 * Pairing Science Page - Erklärt die wissenschaftlichen Grundlagen des Wine-Pairings
 */
const PairingSciencePage = () => {
  const { language } = useLanguage();
  const location = useLocation();
  const [activeExample, setActiveExample] = useState(0);
  
  // Check if we have a current pairing from the pairing page
  const currentPairing = location.state?.pairing || null;

  // Wein-Variablen
  const wineVariables = [
    {
      id: 'acidity',
      name: 'Säure',
      name_en: 'Acidity',
      icon: Droplets,
      color: 'text-yellow-500',
      bgColor: 'bg-yellow-500/10',
      scale: ['Niedrig', 'Mittel', 'Hoch', 'Sehr Hoch'],
      description: 'Essentiell, um Fett zu "schneiden" und Frische zu verleihen. Hohe Säure passt zu fettreichen Speisen.',
      description_en: 'Essential for cutting through fat and adding freshness. High acidity pairs with rich, fatty dishes.',
      example: 'Riesling (Hoch) → Schweinebraten mit Sahnesauce'
    },
    {
      id: 'tannin',
      name: 'Tannin',
      name_en: 'Tannin',
      icon: Leaf,
      color: 'text-red-700',
      bgColor: 'bg-red-700/10',
      scale: ['Keine', 'Gering', 'Mittel', 'Hoch'],
      description: 'Steuert das Pairing mit Proteinen. Hohe Tannine brauchen Fett und Eiweiß, um weich zu wirken.',
      description_en: 'Controls pairing with proteins. High tannins need fat and protein to soften.',
      example: 'Cabernet Sauvignon (Hoch) → Ribeye Steak'
    },
    {
      id: 'sweetness',
      name: 'Restzucker',
      name_en: 'Sweetness',
      icon: CircleDot,
      color: 'text-pink-500',
      bgColor: 'bg-pink-500/10',
      scale: ['Trocken', 'Halbtrocken', 'Lieblich', 'Süß'],
      description: 'Der Wein muss immer süßer sein als das Dessert, sonst wirkt er bitter und flach.',
      description_en: 'Wine must always be sweeter than dessert, otherwise it tastes bitter and flat.',
      example: 'Sauternes (Süß) → Crème Brûlée'
    },
    {
      id: 'body',
      name: 'Körper',
      name_en: 'Body',
      icon: Scale,
      color: 'text-purple-500',
      bgColor: 'bg-purple-500/10',
      scale: ['Leicht', 'Mittel', 'Vollmundig'],
      description: 'Stellt sicher, dass Wein und Speise sich nicht gegenseitig überwältigen. Gleichgewicht ist der Schlüssel.',
      description_en: 'Ensures wine and food don\'t overpower each other. Balance is key.',
      example: 'Pinot Noir (Mittel) → Entenbrust'
    },
    {
      id: 'aroma',
      name: 'Aromen',
      name_en: 'Aromas',
      icon: Beaker,
      color: 'text-green-500',
      bgColor: 'bg-green-500/10',
      scale: ['Frucht', 'Erde', 'Würze', 'Holz', 'Blumen'],
      description: 'Harmonisches Aroma-Pairing: Erdige Weine zu Pilzen, fruchtige Weine zu leichten Gerichten.',
      description_en: 'Harmonious aroma pairing: Earthy wines with mushrooms, fruity wines with light dishes.',
      example: 'Burgunder (Erde) → Pilzrisotto'
    },
    {
      id: 'oak',
      name: 'Holzeinfluss',
      name_en: 'Oak Influence',
      icon: Flame,
      color: 'text-amber-600',
      bgColor: 'bg-amber-600/10',
      scale: ['Kein', 'Subtil', 'Kräftig'],
      description: 'Geröstete Aromen vom Barrique passen perfekt zu gegrilltem oder geröstetem Fleisch.',
      description_en: 'Toasted aromas from barrique pair perfectly with grilled or roasted meat.',
      example: 'Oaked Chardonnay → Gegrillter Lachs'
    }
  ];

  // Gericht-Variablen
  const dishVariables = [
    {
      id: 'fat',
      name: 'Fett-Index',
      name_en: 'Fat Index',
      icon: Droplets,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-600/10',
      scale: ['Mager', 'Mittel', 'Fettig', 'Sehr Reichhaltig'],
      description: 'Je höher der Fett-Index, desto höher muss die Säure oder das Tannin des Weins sein.',
      rule: 'Fett-Index ≥ Hoch → Säure-Index ≥ Mittel',
      example: 'Sahnesauce → Sauvignon Blanc (hohe Säure)'
    },
    {
      id: 'sauce',
      name: 'Sauce/Basis',
      name_en: 'Sauce Base',
      icon: Thermometer,
      color: 'text-orange-500',
      bgColor: 'bg-orange-500/10',
      scale: ['Vinaigrette', 'Sahne', 'Braune Sauce', 'Süß-Sauer', 'Keine'],
      description: 'DIE Hauptinteraktion! Die Sauce bestimmt mehr als das Protein selbst.',
      rule: 'Sahne-Sauce → Körper ≥ Mittel',
      example: 'Béarnaise → Chardonnay (cremig, vollmundig)'
    },
    {
      id: 'protein',
      name: 'Protein-Intensität',
      name_en: 'Protein Intensity',
      icon: Utensils,
      color: 'text-red-500',
      bgColor: 'bg-red-500/10',
      scale: ['Fisch (Mager)', 'Geflügel', 'Schwein', 'Rind', 'Wild'],
      description: 'Steuert den nötigen Tannin-Index und Körper des Weins.',
      rule: 'Protein = Wild → Tannin ≥ Mittel',
      example: 'Wildschwein → Barolo (hohe Tannine)'
    },
    {
      id: 'aroma_dish',
      name: 'Dominante Aromen',
      name_en: 'Dominant Aromas',
      icon: Leaf,
      color: 'text-green-600',
      bgColor: 'bg-green-600/10',
      scale: ['Erde (Pilze)', 'Würzig (Curry)', 'Kräuter', 'Rauch (BBQ)'],
      description: 'Komplementär oder kongruent: Gleiche oder ergänzende Aromen verstärken das Erlebnis.',
      rule: 'Erde-Aromen → Wein mit Erde-Noten',
      example: 'Trüffel-Pasta → Nebbiolo (erdig)'
    },
    {
      id: 'cooking',
      name: 'Garmethode',
      name_en: 'Cooking Method',
      icon: Flame,
      color: 'text-amber-500',
      bgColor: 'bg-amber-500/10',
      scale: ['Pochiert', 'Gedämpft', 'Gebraten', 'Gegrillt'],
      description: 'Grillen/Braten erzeugt Röstaromen, die gut zu Weinen mit Holzeinfluss passen.',
      rule: 'Gegrillt → Holzeinfluss ≥ Subtil',
      example: 'BBQ Ribs → Zinfandel (kräftiger Holzausbau)'
    },
    {
      id: 'umami',
      name: 'Umami-Index',
      name_en: 'Umami Index',
      icon: Gauge,
      color: 'text-purple-600',
      bgColor: 'bg-purple-600/10',
      scale: ['Niedrig', 'Mittel', 'Hoch'],
      description: 'Achtung: Hohes Umami (Parmesan, Sojasauce) macht Weine oft bitter. Benötigt mehr Frucht.',
      rule: 'Umami = Hoch → Tannin ≤ Mittel',
      example: 'Pasta mit Parmesan → Sangiovese (fruchtig, wenig Tannin)'
    }
  ];

  // Pairing-Regeln
  const pairingRules = [
    {
      name: 'Fett braucht Säure',
      name_en: 'Fat Needs Acid',
      icon: '⚖️',
      description: 'Säure schneidet durch Fett und erfrischt den Gaumen. Ein fettreiches Gericht braucht einen Wein mit lebendiger Säure.',
      example: 'Schweinebauch + Riesling Spätlese'
    },
    {
      name: 'Tannin liebt Protein',
      name_en: 'Tannin Loves Protein',
      icon: '🥩',
      description: 'Tannine binden an Proteine und werden dadurch weicher. Rotes Fleisch "zähmt" aggressive Tannine.',
      example: 'Ribeye Steak + Cabernet Sauvignon'
    },
    {
      name: 'Süße schlägt Schärfe',
      name_en: 'Sweet Beats Spice',
      icon: '🌶️',
      description: 'Restzucker mildert Schärfe. Bei scharfen Gerichten: leicht süße Weine mit niedriger Alkohol.',
      example: 'Thai Curry + Gewürztraminer (halbtrocken)'
    },
    {
      name: 'Gleiches zu Gleichem',
      name_en: 'Like with Like',
      icon: '🔄',
      description: 'Körper und Intensität müssen harmonieren. Leichte Gerichte zu leichten Weinen, kräftige zu kräftigen.',
      example: 'Sashimi + Champagner (beide leicht)'
    },
    {
      name: 'Regional denken',
      name_en: 'Think Regional',
      icon: '🌍',
      description: 'Was zusammen wächst, passt zusammen. Regionale Küche mit regionalen Weinen ist selten falsch.',
      example: 'Ossobuco + Barolo (beide Norditalien)'
    },
    {
      name: 'Wein süßer als Dessert',
      name_en: 'Wine Sweeter Than Dessert',
      icon: '🍰',
      description: 'Bei Desserts muss der Wein immer süßer sein, sonst wirkt er bitter und säuerlich.',
      example: 'Crème Brûlée + Sauternes'
    }
  ];

  // Interaktive Beispiele
  const pairingExamples = [
    {
      dish: 'Wiener Schnitzel',
      wine: 'Grüner Veltliner',
      matchScore: 95,
      analysis: {
        fatIndex: 4, // Fettig (paniert, gebuttert)
        wineAcidity: 4, // Hoch
        proteinIntensity: 2, // Kalb = Mittel-leicht
        wineTannin: 1, // Gering (Weißwein)
        cooking: 'Gebraten',
        wineOak: 0 // Kein Holz
      },
      reasons: [
        { match: true, text: 'Hohe Säure schneidet durch das Fett der Panade' },
        { match: true, text: 'Leichter Körper passt zum zarten Kalbfleisch' },
        { match: true, text: 'Zitrus-Aromen ergänzen die traditionelle Zitrone' },
        { match: true, text: 'Keine Tannine stören das feine Fleisch' }
      ]
    },
    {
      dish: 'Ribeye Steak',
      wine: 'Cabernet Sauvignon',
      matchScore: 98,
      analysis: {
        fatIndex: 4, // Marmoriert, fettig
        wineAcidity: 3, // Mittel-hoch
        proteinIntensity: 4, // Rind = Hoch
        wineTannin: 4, // Hoch
        cooking: 'Gegrillt',
        wineOak: 2 // Kräftig
      },
      reasons: [
        { match: true, text: 'Kräftige Tannine werden vom Protein gezähmt' },
        { match: true, text: 'Vollmundiger Körper steht dem intensiven Fleisch gegenüber' },
        { match: true, text: 'Holzaromen ergänzen die Röstaromen vom Grill' },
        { match: true, text: 'Hohe Säure balanciert das Fett der Marmorierung' }
      ]
    },
    {
      dish: 'Sushi (Lachs)',
      wine: 'Champagner Brut',
      matchScore: 92,
      analysis: {
        fatIndex: 2, // Mittel (Lachs hat Fett)
        wineAcidity: 5, // Sehr hoch
        proteinIntensity: 1, // Fisch = Leicht
        wineTannin: 0, // Keine
        cooking: 'Roh',
        wineOak: 0 // Kein Holz
      },
      reasons: [
        { match: true, text: 'Hohe Säure und Perlen reinigen den Gaumen' },
        { match: true, text: 'Leichter Körper überwältigt nicht den delikaten Fisch' },
        { match: true, text: 'Mineralität passt zum Meerescharakter' },
        { match: false, text: 'Alternativ: trockener Riesling oder Albariño' }
      ]
    }
  ];

  const lang = language || 'de';

  return (
    <div className="min-h-screen pb-20 md:pb-24" data-testid="pairing-science-page">
      <div className="container mx-auto px-4 py-8 md:py-12 max-w-6xl">
        
        {/* Breadcrumb */}
        <Breadcrumb 
          items={[
            { name: 'Home', url: 'https://wine-pairing.online/' },
            { name: lang === 'de' ? 'Wie wir pairen' : 'How We Pair', url: 'https://wine-pairing.online/pairing-science', isLast: true }
          ]}
        />

        {/* Hero Section */}
        <header className="text-center mb-12 md:mb-16">
          <Badge className="mb-4 bg-primary/10 text-primary">
            {lang === 'de' ? 'Die Wissenschaft des Genusses' : 'The Science of Taste'}
          </Badge>
          <h1 className="text-3xl md:text-5xl font-bold tracking-tight mb-4">
            {lang === 'de' ? 'Wie wir das perfekte Pairing finden' : 'How We Find the Perfect Pairing'}
          </h1>
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
            {lang === 'de' 
              ? 'Unser KI-Sommelier analysiert 12 Schlüsselvariablen – 6 für den Wein, 6 für das Gericht – um wissenschaftlich fundierte Empfehlungen zu liefern.'
              : 'Our AI sommelier analyzes 12 key variables – 6 for wine, 6 for food – to deliver scientifically grounded recommendations.'}
          </p>
        </header>

        {/* Main Content */}
        <Tabs defaultValue="wine" className="space-y-8">
          <TabsList className="grid w-full grid-cols-3 max-w-md mx-auto">
            <TabsTrigger value="wine" className="flex items-center gap-2">
              <Wine className="h-4 w-4" />
              <span className="hidden sm:inline">{lang === 'de' ? 'Wein' : 'Wine'}</span>
            </TabsTrigger>
            <TabsTrigger value="dish" className="flex items-center gap-2">
              <Utensils className="h-4 w-4" />
              <span className="hidden sm:inline">{lang === 'de' ? 'Gericht' : 'Dish'}</span>
            </TabsTrigger>
            <TabsTrigger value="rules" className="flex items-center gap-2">
              <Beaker className="h-4 w-4" />
              <span className="hidden sm:inline">{lang === 'de' ? 'Regeln' : 'Rules'}</span>
            </TabsTrigger>
          </TabsList>

          {/* Wine Variables Tab */}
          <TabsContent value="wine" className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-semibold mb-2">
                {lang === 'de' ? '6 Wein-Variablen' : '6 Wine Variables'}
              </h2>
              <p className="text-muted-foreground">
                {lang === 'de' 
                  ? 'Diese Attribute bestimmen, wie ein Wein mit Speisen interagiert.'
                  : 'These attributes determine how a wine interacts with food.'}
              </p>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {wineVariables.map((variable) => (
                <Card key={variable.id} className="bg-card/50 backdrop-blur-sm border-border/50 hover:border-primary/30 transition-all">
                  <CardHeader className="pb-2">
                    <div className="flex items-center gap-3">
                      <div className={`p-2 rounded-lg ${variable.bgColor}`}>
                        <variable.icon className={`h-5 w-5 ${variable.color}`} />
                      </div>
                      <CardTitle className="text-lg">
                        {lang === 'de' ? variable.name : variable.name_en}
                      </CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <p className="text-sm text-muted-foreground">
                      {lang === 'de' ? variable.description : variable.description_en}
                    </p>
                    <div className="flex flex-wrap gap-1">
                      {variable.scale.map((s, i) => (
                        <Badge key={i} variant="outline" className="text-xs">
                          {s}
                        </Badge>
                      ))}
                    </div>
                    <p className="text-xs text-primary font-medium">
                      → {variable.example}
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Dish Variables Tab */}
          <TabsContent value="dish" className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-semibold mb-2">
                {lang === 'de' ? '6 Gericht-Variablen' : '6 Dish Variables'}
              </h2>
              <p className="text-muted-foreground">
                {lang === 'de' 
                  ? 'Jedes Gericht wird in seine dominanten Komponenten zerlegt.'
                  : 'Each dish is broken down into its dominant components.'}
              </p>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {dishVariables.map((variable) => (
                <Card key={variable.id} className="bg-card/50 backdrop-blur-sm border-border/50 hover:border-primary/30 transition-all">
                  <CardHeader className="pb-2">
                    <div className="flex items-center gap-3">
                      <div className={`p-2 rounded-lg ${variable.bgColor}`}>
                        <variable.icon className={`h-5 w-5 ${variable.color}`} />
                      </div>
                      <CardTitle className="text-lg">
                        {lang === 'de' ? variable.name : variable.name_en}
                      </CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <p className="text-sm text-muted-foreground">
                      {variable.description}
                    </p>
                    <div className="flex flex-wrap gap-1">
                      {variable.scale.map((s, i) => (
                        <Badge key={i} variant="outline" className="text-xs">
                          {s}
                        </Badge>
                      ))}
                    </div>
                    <div className="p-2 bg-secondary/50 rounded text-xs font-mono">
                      {variable.rule}
                    </div>
                    <p className="text-xs text-primary font-medium">
                      → {variable.example}
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Rules Tab */}
          <TabsContent value="rules" className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-semibold mb-2">
                {lang === 'de' ? 'Die goldenen Pairing-Regeln' : 'The Golden Pairing Rules'}
              </h2>
              <p className="text-muted-foreground">
                {lang === 'de' 
                  ? 'Von Sommeliers über Jahrhunderte entwickelt und von der Wissenschaft bestätigt.'
                  : 'Developed by sommeliers over centuries and confirmed by science.'}
              </p>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {pairingRules.map((rule, index) => (
                <Card key={index} className="bg-card/50 backdrop-blur-sm border-border/50">
                  <CardContent className="pt-6">
                    <div className="text-3xl mb-3">{rule.icon}</div>
                    <h3 className="font-semibold text-lg mb-2">
                      {lang === 'de' ? rule.name : rule.name_en}
                    </h3>
                    <p className="text-sm text-muted-foreground mb-3">
                      {rule.description}
                    </p>
                    <Badge variant="secondary" className="text-xs">
                      {rule.example}
                    </Badge>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>

        {/* Interactive Examples Section */}
        <section className="mt-16 space-y-8">
          <div className="text-center">
            <h2 className="text-2xl md:text-3xl font-semibold mb-2">
              {lang === 'de' ? 'So analysiert unser KI-Sommelier' : 'How Our AI Sommelier Analyzes'}
            </h2>
            <p className="text-muted-foreground">
              {lang === 'de' 
                ? 'Klicken Sie auf ein Beispiel, um die detaillierte Analyse zu sehen.'
                : 'Click an example to see the detailed analysis.'}
            </p>
          </div>

          {/* Example Selector */}
          <div className="flex flex-wrap justify-center gap-3">
            {pairingExamples.map((example, index) => (
              <Button
                key={index}
                variant={activeExample === index ? "default" : "outline"}
                onClick={() => setActiveExample(index)}
                className="rounded-full"
              >
                {example.dish} + {example.wine}
              </Button>
            ))}
          </div>

          {/* Active Example Card */}
          <Card className="bg-secondary/30 max-w-3xl mx-auto">
            <CardHeader>
              <div className="flex items-center justify-between flex-wrap gap-4">
                <div>
                  <CardTitle className="text-xl">
                    {pairingExamples[activeExample].dish}
                    <span className="text-primary"> & </span>
                    {pairingExamples[activeExample].wine}
                  </CardTitle>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">Match-Score:</span>
                  <Badge className="text-lg bg-green-500/20 text-green-600">
                    {pairingExamples[activeExample].matchScore}%
                  </Badge>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Analysis Grid */}
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
                <div className="p-3 bg-background rounded-lg">
                  <p className="text-muted-foreground text-xs">Fett-Index</p>
                  <p className="font-medium">{pairingExamples[activeExample].analysis.fatIndex}/5</p>
                </div>
                <div className="p-3 bg-background rounded-lg">
                  <p className="text-muted-foreground text-xs">Wein-Säure</p>
                  <p className="font-medium">{pairingExamples[activeExample].analysis.wineAcidity}/5</p>
                </div>
                <div className="p-3 bg-background rounded-lg">
                  <p className="text-muted-foreground text-xs">Protein-Intensität</p>
                  <p className="font-medium">{pairingExamples[activeExample].analysis.proteinIntensity}/5</p>
                </div>
                <div className="p-3 bg-background rounded-lg">
                  <p className="text-muted-foreground text-xs">Wein-Tannin</p>
                  <p className="font-medium">{pairingExamples[activeExample].analysis.wineTannin}/5</p>
                </div>
                <div className="p-3 bg-background rounded-lg">
                  <p className="text-muted-foreground text-xs">Garmethode</p>
                  <p className="font-medium">{pairingExamples[activeExample].analysis.cooking}</p>
                </div>
                <div className="p-3 bg-background rounded-lg">
                  <p className="text-muted-foreground text-xs">Holzeinfluss</p>
                  <p className="font-medium">{pairingExamples[activeExample].analysis.wineOak}/3</p>
                </div>
              </div>

              {/* Reasons */}
              <div className="space-y-2">
                <h4 className="font-medium text-sm">
                  {lang === 'de' ? 'Warum dieses Pairing funktioniert:' : 'Why this pairing works:'}
                </h4>
                {pairingExamples[activeExample].reasons.map((reason, idx) => (
                  <div key={idx} className="flex items-start gap-2 text-sm">
                    {reason.match ? (
                      <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                    ) : (
                      <Info className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                    )}
                    <span className={reason.match ? '' : 'text-muted-foreground'}>{reason.text}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </section>

        {/* CTA Section */}
        <section className="mt-16 text-center">
          <Card className="bg-primary/5 border-primary/20 max-w-2xl mx-auto">
            <CardContent className="py-8">
              <h3 className="text-xl font-semibold mb-3">
                {lang === 'de' ? 'Bereit für Ihr perfektes Pairing?' : 'Ready for Your Perfect Pairing?'}
              </h3>
              <p className="text-muted-foreground mb-6">
                {lang === 'de' 
                  ? 'Unser KI-Sommelier analysiert über 1.700 Weine und findet in Sekunden die perfekte Empfehlung.'
                  : 'Our AI sommelier analyzes over 1,700 wines and finds the perfect recommendation in seconds.'}
              </p>
              <div className="flex flex-wrap justify-center gap-4">
                <Link to="/pairing">
                  <Button size="lg" className="rounded-full">
                    <Utensils className="mr-2 h-4 w-4" />
                    {lang === 'de' ? 'Pairing starten' : 'Start Pairing'}
                  </Button>
                </Link>
                <Link to="/chat">
                  <Button size="lg" variant="outline" className="rounded-full">
                    <Wine className="mr-2 h-4 w-4" />
                    {lang === 'de' ? 'Sommelier fragen' : 'Ask Sommelier'}
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </section>

      </div>
      <Footer />
    </div>
  );
};

export default PairingSciencePage;
