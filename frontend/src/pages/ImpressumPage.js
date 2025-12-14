import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { useLanguage } from '@/contexts/LanguageContext';
import Footer from '@/components/Footer';

const ImpressumPage = () => {
  const { t } = useLanguage();

  return (
    <div className="min-h-screen pb-20 md:pb-24" data-testid="impressum-page">
      <div className="container mx-auto px-4 py-12 md:py-16">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-semibold mb-8">
            {t('impressum_title') || 'Impressum'}
          </h1>
          
          <Card className="bg-card/50 backdrop-blur-sm border-border/50">
            <CardContent className="p-6 md:p-8 space-y-8">
              <section>
                <h2 className="text-xl font-semibold mb-4">Kontaktdaten</h2>
                <div className="text-muted-foreground space-y-1">
                  <p className="font-medium text-foreground">MYSYMP AG</p>
                  <p>Oberdorfstrasse 18a</p>
                  <p>6207 Nottwil</p>
                  <p>Schweiz</p>
                  <p className="mt-4">E-Mail: <a href="mailto:info@mysymp.ch" className="hover:text-foreground transition-colors">info@mysymp.ch</a></p>
                  <p>Web: <a href="https://www.mysymp.ch" target="_blank" rel="noopener noreferrer" className="hover:text-foreground transition-colors">www.mysymp.ch</a></p>
                  <p>Telefon: <a href="tel:+41794710625" className="hover:text-foreground transition-colors">+41 79 471 06 25</a></p>
                </div>
              </section>
              
              <section>
                <h2 className="text-xl font-semibold mb-4">Vertretungsberechtigte Person</h2>
                <div className="text-muted-foreground">
                  <p className="font-medium text-foreground">Isidoro Celentano</p>
                  <p>CEO / Founder</p>
                </div>
              </section>
              
              <section>
                <h2 className="text-xl font-semibold mb-4">Handelsregistereintrag</h2>
                <div className="text-muted-foreground space-y-1">
                  <p><span className="text-foreground">Eingetragener Firmenname:</span> MYSYMP AG</p>
                  <p><span className="text-foreground">Nummer:</span> CHE-192.170.455</p>
                  <p><span className="text-foreground">Handelsregisteramt:</span> Nottwil</p>
                </div>
              </section>
              
              <section>
                <h2 className="text-xl font-semibold mb-4">Mehrwertsteuernummer</h2>
                <p className="text-muted-foreground">CHE-192.170.455 MWST</p>
              </section>
              
              <section>
                <h2 className="text-xl font-semibold mb-4">Haftungsausschluss</h2>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  Der Autor übernimmt keinerlei Gewähr hinsichtlich der inhaltlichen Richtigkeit, Genauigkeit, 
                  Aktualität, Zuverlässigkeit und Vollständigkeit der Informationen. Haftungsansprüche gegen 
                  den Autor wegen Schäden materieller oder immaterieller Art, welche aus dem Zugriff oder 
                  der Nutzung bzw. Nichtnutzung der veröffentlichten Informationen, durch Missbrauch der 
                  Verbindung oder durch technische Störungen entstanden sind, werden ausgeschlossen.
                </p>
              </section>
            </CardContent>
          </Card>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default ImpressumPage;
