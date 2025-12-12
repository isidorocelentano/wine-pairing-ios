import React from 'react';
import { useNavigate } from "react-router-dom";
import { Wine, Utensils, Camera, MessageCircle, BookOpen, Users } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";

const HomePage = () => {
  const navigate = useNavigate();
  const { t } = useLanguage();

  return (
    <div className="min-h-screen pb-20 md:pb-24" data-testid="home-page">
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
        
        <div className="relative z-10 container mx-auto px-4 md:px-12 lg:px-24">
          <div className="max-w-2xl space-y-6 md:space-y-8 opacity-0 animate-fade-in-up" style={{ animationDelay: '0.2s', animationFillMode: 'forwards' }}>
            <p className="text-accent font-accent text-base md:text-lg tracking-widest uppercase">{t('hero_tagline')}</p>
            <h1 className="text-3xl md:text-5xl lg:text-6xl font-semibold leading-tight tracking-tight">
              {t('hero_title')}
            </h1>
            <p className="text-base md:text-lg text-muted-foreground leading-relaxed">
              {t('hero_description')}
            </p>
            <div className="flex items-center gap-4 pt-2">
              <img
                src="https://customer-assets.emergentagent.com/job_e57eae36-225b-4e20-a944-048ef9749606/artifacts/w9w52bm4_CLAUDE%20SOMMELIER%2001%20%284%29.png"
                alt="Claude, virtueller Sommelier"
                className="w-16 h-16 rounded-full shadow-md border border-border/60 object-cover"
              />
              <p className="text-sm md:text-base text-muted-foreground leading-snug">
                {t('claude_intro_short')}
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-3 md:gap-4 pt-2 md:pt-4">
              <Button
                onClick={() => navigate('/pairing')}
                className="rounded-full px-6 md:px-8 py-5 md:py-6 text-sm font-medium tracking-wide transition-elegant hover:scale-105 active:scale-95"
                data-testid="cta-pairing"
              >
                <Utensils className="mr-2 h-4 w-4" />
                {t('cta_pairing')}
              </Button>
              <Button
                variant="outline"
                onClick={() => navigate('/cellar')}
                className="rounded-full px-6 md:px-8 py-5 md:py-6 text-sm font-medium tracking-wide border-primary/30 hover:bg-primary/5"
                data-testid="cta-cellar"
              >
                <Wine className="mr-2 h-4 w-4" />
                {t('cta_cellar')}
              </Button>
              <Button
                variant="outline"
                onClick={() => navigate('/blog')}
                className="rounded-full px-6 md:px-8 py-5 md:py-6 text-sm font-medium tracking-wide border-primary/30 hover:bg-primary/5"
                data-testid="cta-blog"
              >
                <BookOpen className="mr-2 h-4 w-4" />
                Blog
              </Button>
              <Button
                variant="outline"
                onClick={() => navigate('/feed')}
                className="rounded-full px-6 md:px-8 py-5 md:py-6 text-sm font-medium tracking-wide border-primary/30 hover:bg-primary/5"
                data-testid="cta-feed"
              >
                <Users className="mr-2 h-4 w-4" />
                {t('nav_feed') || 'Community'}
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Philosophy Section */}
      <section className="py-16 md:py-24 px-4 md:px-12 lg:px-24">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-8 md:gap-12">
            <div className="md:col-span-5 space-y-4 md:space-y-6 opacity-0 animate-fade-in-up animate-delay-100" style={{ animationFillMode: 'forwards' }}>
              <p className="text-accent font-accent text-sm tracking-widest uppercase">{t('philosophy_tagline')}</p>
              <h2 className="text-2xl md:text-4xl font-semibold tracking-tight">
                {t('philosophy_title')}
              </h2>
            </div>
            <div className="md:col-span-7 space-y-4 md:space-y-6 opacity-0 animate-fade-in-up animate-delay-200" style={{ animationFillMode: 'forwards' }}>
              <p className="text-muted-foreground leading-relaxed text-base md:text-lg">
                {t('philosophy_text1')}
              </p>
              <p className="text-muted-foreground leading-relaxed text-base md:text-lg">
                {t('philosophy_text2')}
              </p>
              <blockquote className="border-l-4 border-accent pl-4 md:pl-6 py-2 font-accent text-lg md:text-xl italic text-foreground/80">
                {t('philosophy_quote')}
              </blockquote>
            </div>
          </div>
        </div>
      </section>
      
      {/* Manifest Section */}
      <section className="py-12 md:py-16 px-4 md:px-12 lg:px-24">
        <div className="container mx-auto max-w-4xl">
          <div className="opacity-0 animate-fade-in-up animate-delay-200" style={{ animationFillMode: 'forwards' }}>
            <p className="text-accent font-accent text-sm tracking-widest uppercase mb-2">{t('manifesto_title')}</p>
            <ul className="space-y-2 text-sm md:text-base text-muted-foreground list-disc pl-5">
              <li>{t('manifesto_point1')}</li>
              <li>{t('manifesto_point2')}</li>
              <li>{t('manifesto_point3')}</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-12 md:py-16 px-4 md:px-12 lg:px-24 bg-secondary/30">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8">
            {[
              { icon: Utensils, titleKey: 'feature_pairing_title', descKey: 'feature_pairing_desc' },
              { icon: Camera, titleKey: 'feature_scanner_title', descKey: 'feature_scanner_desc' },
              { icon: MessageCircle, titleKey: 'feature_sommelier_title', descKey: 'feature_sommelier_desc' }
            ].map((feature, idx) => (
              <Card key={idx} className="bg-card/50 backdrop-blur-sm border-border/50 hover-lift" data-testid={`feature-card-${idx}`}>
                <CardHeader>
                  <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                    <feature.icon className="w-6 h-6 text-primary" strokeWidth={1.5} />
                  </div>
                  <CardTitle className="text-lg md:text-xl">{t(feature.titleKey)}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-sm md:text-base">{t(feature.descKey)}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
