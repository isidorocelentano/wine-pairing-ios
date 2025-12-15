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
      name: { de: 'Säure', en: 'Acidity', fr: 'Acidité' },
      icon: Droplets,
      color: 'text-yellow-500',
      bgColor: 'bg-yellow-500/10',
      scale: { 
        de: ['Niedrig', 'Mittel', 'Hoch', 'Sehr Hoch'],
        en: ['Low', 'Medium', 'High', 'Very High'],
        fr: ['Faible', 'Moyen', 'Élevé', 'Très élevé']
      },
      description: {
        de: 'Essentiell, um Fett zu "schneiden" und Frische zu verleihen. Hohe Säure passt zu fettreichen Speisen.',
        en: 'Essential for cutting through fat and adding freshness. High acidity pairs with rich, fatty dishes.',
        fr: 'Essentielle pour couper le gras et apporter de la fraîcheur. Une acidité élevée accompagne les plats riches.'
      },
      example: { de: 'Riesling (Hoch) → Schweinebraten', en: 'Riesling (High) → Pork Roast', fr: 'Riesling (Élevé) → Rôti de porc' }
    },
    {
      id: 'tannin',
      name: { de: 'Tannin', en: 'Tannin', fr: 'Tanin' },
      icon: Leaf,
      color: 'text-red-700',
      bgColor: 'bg-red-700/10',
      scale: {
        de: ['Keine', 'Gering', 'Mittel', 'Hoch'],
        en: ['None', 'Low', 'Medium', 'High'],
        fr: ['Aucun', 'Faible', 'Moyen', 'Élevé']
      },
      description: {
        de: 'Steuert das Pairing mit Proteinen. Hohe Tannine brauchen Fett und Eiweiß, um weich zu wirken.',
        en: 'Controls pairing with proteins. High tannins need fat and protein to soften.',
        fr: 'Contrôle l\'accord avec les protéines. Les tanins élevés ont besoin de gras et de protéines.'
      },
      example: { de: 'Cabernet Sauvignon (Hoch) → Ribeye Steak', en: 'Cabernet Sauvignon (High) → Ribeye Steak', fr: 'Cabernet Sauvignon (Élevé) → Entrecôte' }
    },
    {
      id: 'sweetness',
      name: { de: 'Restzucker', en: 'Sweetness', fr: 'Sucre résiduel' },
      icon: CircleDot,
      color: 'text-pink-500',
      bgColor: 'bg-pink-500/10',
      scale: {
        de: ['Trocken', 'Halbtrocken', 'Lieblich', 'Süß'],
        en: ['Dry', 'Off-dry', 'Semi-sweet', 'Sweet'],
        fr: ['Sec', 'Demi-sec', 'Moelleux', 'Doux']
      },
      description: {
        de: 'Der Wein muss immer süßer sein als das Dessert, sonst wirkt er bitter und flach.',
        en: 'Wine must always be sweeter than dessert, otherwise it tastes bitter and flat.',
        fr: 'Le vin doit toujours être plus sucré que le dessert, sinon il paraît amer et plat.'
      },
      example: { de: 'Sauternes (Süß) → Crème Brûlée', en: 'Sauternes (Sweet) → Crème Brûlée', fr: 'Sauternes (Doux) → Crème brûlée' }
    },
    {
      id: 'body',
      name: { de: 'Körper', en: 'Body', fr: 'Corps' },
      icon: Scale,
      color: 'text-purple-500',
      bgColor: 'bg-purple-500/10',
      scale: {
        de: ['Leicht', 'Mittel', 'Vollmundig'],
        en: ['Light', 'Medium', 'Full-bodied'],
        fr: ['Léger', 'Moyen', 'Corsé']
      },
      description: {
        de: 'Stellt sicher, dass Wein und Speise sich nicht gegenseitig überwältigen. Gleichgewicht ist der Schlüssel.',
        en: 'Ensures wine and food don\'t overpower each other. Balance is key.',
        fr: 'Garantit que le vin et le plat ne se dominent pas mutuellement. L\'équilibre est essentiel.'
      },
      example: { de: 'Pinot Noir (Mittel) → Entenbrust', en: 'Pinot Noir (Medium) → Duck Breast', fr: 'Pinot Noir (Moyen) → Magret de canard' }
    },
    {
      id: 'aroma',
      name: { de: 'Aromen', en: 'Aromas', fr: 'Arômes' },
      icon: Beaker,
      color: 'text-green-500',
      bgColor: 'bg-green-500/10',
      scale: {
        de: ['Frucht', 'Erde', 'Würze', 'Holz', 'Blumen'],
        en: ['Fruit', 'Earth', 'Spice', 'Oak', 'Floral'],
        fr: ['Fruit', 'Terre', 'Épices', 'Bois', 'Floral']
      },
      description: {
        de: 'Harmonisches Aroma-Pairing: Erdige Weine zu Pilzen, fruchtige Weine zu leichten Gerichten.',
        en: 'Harmonious aroma pairing: Earthy wines with mushrooms, fruity wines with light dishes.',
        fr: 'Accord aromatique harmonieux: vins terreux avec champignons, vins fruités avec plats légers.'
      },
      example: { de: 'Burgunder (Erde) → Pilzrisotto', en: 'Burgundy (Earth) → Mushroom Risotto', fr: 'Bourgogne (Terre) → Risotto aux champignons' }
    },
    {
      id: 'oak',
      name: { de: 'Holzeinfluss', en: 'Oak Influence', fr: 'Influence du bois' },
      icon: Flame,
      color: 'text-amber-600',
      bgColor: 'bg-amber-600/10',
      scale: {
        de: ['Kein', 'Subtil', 'Kräftig'],
        en: ['None', 'Subtle', 'Strong'],
        fr: ['Aucun', 'Subtil', 'Prononcé']
      },
      description: {
        de: 'Geröstete Aromen vom Barrique passen perfekt zu gegrilltem oder geröstetem Fleisch.',
        en: 'Toasted aromas from barrique pair perfectly with grilled or roasted meat.',
        fr: 'Les arômes grillés de la barrique s\'accordent parfaitement avec les viandes grillées ou rôties.'
      },
      example: { de: 'Oaked Chardonnay → Gegrillter Lachs', en: 'Oaked Chardonnay → Grilled Salmon', fr: 'Chardonnay boisé → Saumon grillé' }
    }
  ];

  // Gericht-Variablen
  const dishVariables = [
    {
      id: 'fat',
      name: { de: 'Fett-Index', en: 'Fat Index', fr: 'Indice de gras' },
      icon: Droplets,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-600/10',
      scale: {
        de: ['Mager', 'Mittel', 'Fettig', 'Sehr Reichhaltig'],
        en: ['Lean', 'Medium', 'Fatty', 'Very Rich'],
        fr: ['Maigre', 'Moyen', 'Gras', 'Très riche']
      },
      description: {
        de: 'Je höher der Fett-Index, desto höher muss die Säure oder das Tannin des Weins sein.',
        en: 'The higher the fat index, the higher the wine\'s acidity or tannin must be.',
        fr: 'Plus l\'indice de gras est élevé, plus l\'acidité ou les tanins du vin doivent être élevés.'
      },
      rule: { de: 'Fett-Index ≥ Hoch → Säure-Index ≥ Mittel', en: 'Fat Index ≥ High → Acidity ≥ Medium', fr: 'Indice gras ≥ Élevé → Acidité ≥ Moyen' },
      example: { de: 'Sahnesauce → Sauvignon Blanc', en: 'Cream sauce → Sauvignon Blanc', fr: 'Sauce crème → Sauvignon Blanc' }
    },
    {
      id: 'sauce',
      name: { de: 'Sauce/Basis', en: 'Sauce Base', fr: 'Base de sauce' },
      icon: Thermometer,
      color: 'text-orange-500',
      bgColor: 'bg-orange-500/10',
      scale: {
        de: ['Vinaigrette', 'Sahne', 'Braune Sauce', 'Süß-Sauer', 'Keine'],
        en: ['Vinaigrette', 'Cream', 'Brown Sauce', 'Sweet-Sour', 'None'],
        fr: ['Vinaigrette', 'Crème', 'Sauce brune', 'Aigre-doux', 'Aucune']
      },
      description: {
        de: 'DIE Hauptinteraktion! Die Sauce bestimmt mehr als das Protein selbst.',
        en: 'THE main interaction! The sauce determines more than the protein itself.',
        fr: 'L\'interaction principale! La sauce détermine plus que la protéine elle-même.'
      },
      rule: { de: 'Sahne-Sauce → Körper ≥ Mittel', en: 'Cream Sauce → Body ≥ Medium', fr: 'Sauce crème → Corps ≥ Moyen' },
      example: { de: 'Béarnaise → Chardonnay', en: 'Béarnaise → Chardonnay', fr: 'Béarnaise → Chardonnay' }
    },
    {
      id: 'protein',
      name: { de: 'Protein-Intensität', en: 'Protein Intensity', fr: 'Intensité protéique' },
      icon: Utensils,
      color: 'text-red-500',
      bgColor: 'bg-red-500/10',
      scale: {
        de: ['Fisch (Mager)', 'Geflügel', 'Schwein', 'Rind', 'Wild'],
        en: ['Fish (Lean)', 'Poultry', 'Pork', 'Beef', 'Game'],
        fr: ['Poisson (Maigre)', 'Volaille', 'Porc', 'Bœuf', 'Gibier']
      },
      description: {
        de: 'Steuert den nötigen Tannin-Index und Körper des Weins.',
        en: 'Controls the required tannin index and body of the wine.',
        fr: 'Contrôle l\'indice de tanin et le corps du vin nécessaires.'
      },
      rule: { de: 'Protein = Wild → Tannin ≥ Mittel', en: 'Protein = Game → Tannin ≥ Medium', fr: 'Protéine = Gibier → Tanin ≥ Moyen' },
      example: { de: 'Wildschwein → Barolo', en: 'Wild Boar → Barolo', fr: 'Sanglier → Barolo' }
    },
    {
      id: 'aroma_dish',
      name: { de: 'Dominante Aromen', en: 'Dominant Aromas', fr: 'Arômes dominants' },
      icon: Leaf,
      color: 'text-green-600',
      bgColor: 'bg-green-600/10',
      scale: {
        de: ['Erde (Pilze)', 'Würzig (Curry)', 'Kräuter', 'Rauch (BBQ)'],
        en: ['Earth (Mushrooms)', 'Spicy (Curry)', 'Herbs', 'Smoke (BBQ)'],
        fr: ['Terre (Champignons)', 'Épicé (Curry)', 'Herbes', 'Fumé (BBQ)']
      },
      description: {
        de: 'Komplementär oder kongruent: Gleiche oder ergänzende Aromen verstärken das Erlebnis.',
        en: 'Complementary or congruent: Same or complementary aromas enhance the experience.',
        fr: 'Complémentaire ou congruent: les mêmes arômes ou des arômes complémentaires améliorent l\'expérience.'
      },
      rule: { de: 'Erde-Aromen → Wein mit Erde-Noten', en: 'Earth aromas → Wine with earth notes', fr: 'Arômes terreux → Vin aux notes terreuses' },
      example: { de: 'Trüffel-Pasta → Nebbiolo', en: 'Truffle Pasta → Nebbiolo', fr: 'Pâtes aux truffes → Nebbiolo' }
    },
    {
      id: 'cooking',
      name: { de: 'Garmethode', en: 'Cooking Method', fr: 'Méthode de cuisson' },
      icon: Flame,
      color: 'text-amber-500',
      bgColor: 'bg-amber-500/10',
      scale: {
        de: ['Pochiert', 'Gedämpft', 'Gebraten', 'Gegrillt'],
        en: ['Poached', 'Steamed', 'Pan-fried', 'Grilled'],
        fr: ['Poché', 'Vapeur', 'Poêlé', 'Grillé']
      },
      description: {
        de: 'Grillen/Braten erzeugt Röstaromen, die gut zu Weinen mit Holzeinfluss passen.',
        en: 'Grilling/frying creates roasted aromas that pair well with oaked wines.',
        fr: 'Griller/frire crée des arômes grillés qui s\'accordent bien avec les vins boisés.'
      },
      rule: { de: 'Gegrillt → Holzeinfluss ≥ Subtil', en: 'Grilled → Oak ≥ Subtle', fr: 'Grillé → Bois ≥ Subtil' },
      example: { de: 'BBQ Ribs → Zinfandel', en: 'BBQ Ribs → Zinfandel', fr: 'Côtes BBQ → Zinfandel' }
    },
    {
      id: 'umami',
      name: { de: 'Umami-Index', en: 'Umami Index', fr: 'Indice umami' },
      icon: Gauge,
      color: 'text-purple-600',
      bgColor: 'bg-purple-600/10',
      scale: {
        de: ['Niedrig', 'Mittel', 'Hoch'],
        en: ['Low', 'Medium', 'High'],
        fr: ['Faible', 'Moyen', 'Élevé']
      },
      description: {
        de: 'Achtung: Hohes Umami (Parmesan, Sojasauce) macht Weine oft bitter. Benötigt mehr Frucht.',
        en: 'Caution: High umami (Parmesan, soy sauce) often makes wines bitter. Needs more fruit.',
        fr: 'Attention: un umami élevé (Parmesan, sauce soja) rend souvent les vins amers. Nécessite plus de fruit.'
      },
      rule: { de: 'Umami = Hoch → Tannin ≤ Mittel', en: 'Umami = High → Tannin ≤ Medium', fr: 'Umami = Élevé → Tanin ≤ Moyen' },
      example: { de: 'Pasta mit Parmesan → Sangiovese', en: 'Pasta with Parmesan → Sangiovese', fr: 'Pâtes au Parmesan → Sangiovese' }
    }
  ];
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
                {lang === 'de' ? '6 Wein-Variablen' : lang === 'en' ? '6 Wine Variables' : '6 Variables du vin'}
              </h2>
              <p className="text-muted-foreground">
                {lang === 'de' 
                  ? 'Diese Attribute bestimmen, wie ein Wein mit Speisen interagiert.'
                  : lang === 'en' 
                  ? 'These attributes determine how a wine interacts with food.'
                  : 'Ces attributs déterminent comment un vin interagit avec les aliments.'}
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
                        {variable.name[lang] || variable.name.en}
                      </CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <p className="text-sm text-muted-foreground">
                      {variable.description[lang] || variable.description.en}
                    </p>
                    <div className="flex flex-wrap gap-1">
                      {(variable.scale[lang] || variable.scale.en).map((s, i) => (
                        <Badge key={i} variant="outline" className="text-xs">
                          {s}
                        </Badge>
                      ))}
                    </div>
                    <p className="text-xs text-primary font-medium">
                      → {variable.example[lang] || variable.example.en}
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

        {/* Current Pairing Analysis - If coming from pairing page */}
        {currentPairing && (
          <section className="mt-12 space-y-6">
            <div className="text-center">
              <Badge className="mb-4 bg-green-500/20 text-green-600">
                {lang === 'de' ? 'Ihre aktuelle Analyse' : 'Your Current Analysis'}
              </Badge>
              <h2 className="text-2xl md:text-3xl font-semibold mb-2">
                {lang === 'de' ? `Warum diese Weine zu "${currentPairing.dish}" passen` : `Why These Wines Match "${currentPairing.dish}"`}
              </h2>
            </div>
            
            <Card className="bg-gradient-to-r from-primary/5 via-accent/5 to-primary/10 border-primary/30 max-w-4xl mx-auto">
              <CardHeader>
                <CardTitle className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center">
                    <Utensils className="h-5 w-5 text-primary" />
                  </div>
                  {currentPairing.dish}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Why Explanation */}
                {currentPairing.why_explanation && (
                  <div className="p-4 bg-background/50 rounded-lg">
                    <h4 className="font-medium text-sm mb-2 flex items-center gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-500" />
                      {lang === 'de' ? 'Wissenschaftliche Begründung:' : 'Scientific Reasoning:'}
                    </h4>
                    <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-line">
                      {currentPairing.why_explanation}
                    </p>
                  </div>
                )}
                
                {/* Key Pairing Factors */}
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  <div className="p-3 bg-background/50 rounded-lg text-center">
                    <Droplets className="h-5 w-5 text-yellow-500 mx-auto mb-1" />
                    <p className="text-xs text-muted-foreground">Säure-Balance</p>
                    <p className="text-sm font-medium">{lang === 'de' ? 'Analysiert' : 'Analyzed'}</p>
                  </div>
                  <div className="p-3 bg-background/50 rounded-lg text-center">
                    <Leaf className="h-5 w-5 text-red-700 mx-auto mb-1" />
                    <p className="text-xs text-muted-foreground">Tannin-Match</p>
                    <p className="text-sm font-medium">{lang === 'de' ? 'Analysiert' : 'Analyzed'}</p>
                  </div>
                  <div className="p-3 bg-background/50 rounded-lg text-center">
                    <Scale className="h-5 w-5 text-purple-500 mx-auto mb-1" />
                    <p className="text-xs text-muted-foreground">Körper-Balance</p>
                    <p className="text-sm font-medium">{lang === 'de' ? 'Analysiert' : 'Analyzed'}</p>
                  </div>
                  <div className="p-3 bg-background/50 rounded-lg text-center">
                    <Thermometer className="h-5 w-5 text-orange-500 mx-auto mb-1" />
                    <p className="text-xs text-muted-foreground">Fett-Index</p>
                    <p className="text-sm font-medium">{lang === 'de' ? 'Bewertet' : 'Evaluated'}</p>
                  </div>
                  <div className="p-3 bg-background/50 rounded-lg text-center">
                    <Flame className="h-5 w-5 text-amber-500 mx-auto mb-1" />
                    <p className="text-xs text-muted-foreground">Garmethode</p>
                    <p className="text-sm font-medium">{lang === 'de' ? 'Berücksichtigt' : 'Considered'}</p>
                  </div>
                  <div className="p-3 bg-background/50 rounded-lg text-center">
                    <Gauge className="h-5 w-5 text-purple-600 mx-auto mb-1" />
                    <p className="text-xs text-muted-foreground">Umami-Level</p>
                    <p className="text-sm font-medium">{lang === 'de' ? 'Geprüft' : 'Checked'}</p>
                  </div>
                </div>
                
                <div className="text-center pt-4">
                  <Link to="/pairing">
                    <Button variant="outline" className="rounded-full">
                      <Utensils className="mr-2 h-4 w-4" />
                      {lang === 'de' ? 'Neues Pairing starten' : 'Start New Pairing'}
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          </section>
        )}

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
