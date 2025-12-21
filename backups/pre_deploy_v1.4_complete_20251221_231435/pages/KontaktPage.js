import React from 'react';
import { MapPin, Phone, Mail, Globe } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { useLanguage } from '@/contexts/LanguageContext';
import Footer from '@/components/Footer';

const KontaktPage = () => {
  const { t } = useLanguage();

  return (
    <div className="min-h-screen pb-20 md:pb-24" data-testid="kontakt-page">
      <div className="container mx-auto px-4 py-12 md:py-16">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-semibold mb-8">
            {t('kontakt_title') || 'Kontakt'}
          </h1>
          
          <Card className="bg-card/50 backdrop-blur-sm border-border/50">
            <CardContent className="p-6 md:p-8 space-y-6">
              <p className="text-muted-foreground">
                {t('kontakt_intro') || 'Haben Sie Fragen zu wine-pairing.online? Wir freuen uns über Ihre Nachricht.'}
              </p>
              
              <div className="space-y-4">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <MapPin className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <p className="font-medium">MYSYMP AG</p>
                    <p className="text-muted-foreground">Studenstrasse 14B</p>
                    <p className="text-muted-foreground">CH-6207 Nottwil</p>
                    <p className="text-muted-foreground">Schweiz</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <Phone className="w-5 h-5 text-primary" />
                  </div>
                  <a 
                    href="tel:+41794710625" 
                    className="text-muted-foreground hover:text-foreground transition-colors"
                  >
                    +41 79 471 06 25
                  </a>
                </div>
                
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <Mail className="w-5 h-5 text-primary" />
                  </div>
                  <a 
                    href="mailto:info@mysymp.ch" 
                    className="text-muted-foreground hover:text-foreground transition-colors"
                  >
                    info@mysymp.ch
                  </a>
                </div>
                
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <Globe className="w-5 h-5 text-primary" />
                  </div>
                  <a 
                    href="https://mysymp.ch" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-muted-foreground hover:text-foreground transition-colors"
                  >
                    www.mysymp.ch
                  </a>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default KontaktPage;
