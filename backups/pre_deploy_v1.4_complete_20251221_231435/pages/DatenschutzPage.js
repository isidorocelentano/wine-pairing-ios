import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { useLanguage } from '@/contexts/LanguageContext';
import Footer from '@/components/Footer';

const DatenschutzPage = () => {
  const { t } = useLanguage();

  return (
    <div className="min-h-screen pb-20 md:pb-24" data-testid="datenschutz-page">
      <div className="container mx-auto px-4 py-12 md:py-16">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-semibold mb-8">
            {t('datenschutz_title') || 'Datenschutzerklärung'}
          </h1>
          
          <Card className="bg-card/50 backdrop-blur-sm border-border/50">
            <CardContent className="p-6 md:p-8 prose prose-sm max-w-none dark:prose-invert">
              <section className="mb-8">
                <h2 className="text-xl font-semibold mb-4">1. Worum geht es in dieser Datenschutzerklärung?</h2>
                <p className="text-muted-foreground leading-relaxed">
                  Die MYSYMP AG bearbeitet Personendaten, die Sie oder andere Personen betreffen, in unterschiedlicher 
                  Weise und für unterschiedliche Zwecke. Diese Datenschutzerklärung erläutert unsere Bearbeitung von 
                  Personendaten, wenn Sie unsere Website wine-pairing.online besuchen, unsere Dienstleistungen nutzen 
                  oder anderweitig mit uns in Kontakt stehen.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-xl font-semibold mb-4">2. Wer ist für die Bearbeitung Ihrer Daten verantwortlich?</h2>
                <div className="text-muted-foreground space-y-2">
                  <p><strong className="text-foreground">Verantwortliche Stelle:</strong></p>
                  <p>MYSYMP AG</p>
                  <p>Studenstrasse 14B</p>
                  <p>6207 Nottwil</p>
                  <p>Schweiz</p>
                  <p className="mt-4">E-Mail: <a href="mailto:info@mysymp.ch" className="text-primary hover:underline">info@mysymp.ch</a></p>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="text-xl font-semibold mb-4">3. Welche Personendaten bearbeiten wir?</h2>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  Wir bearbeiten je nach Anlass und Zweck verschiedene Kategorien von Personendaten:
                </p>
                <ul className="list-disc pl-5 text-muted-foreground space-y-2">
                  <li><strong className="text-foreground">Stammdaten:</strong> Name, Kontaktdetails, E-Mail-Adresse, Sprachpräferenzen</li>
                  <li><strong className="text-foreground">Nutzungsdaten:</strong> Informationen über Ihre Nutzung unserer Website und Dienste</li>
                  <li><strong className="text-foreground">Technische Daten:</strong> IP-Adresse, Browsertyp, Geräteinformationen</li>
                  <li><strong className="text-foreground">Kommunikationsdaten:</strong> Inhalte Ihrer Korrespondenz mit uns</li>
                </ul>
              </section>

              <section className="mb-8">
                <h2 className="text-xl font-semibold mb-4">4. Zu welchen Zwecken bearbeiten wir Ihre Daten?</h2>
                <ul className="list-disc pl-5 text-muted-foreground space-y-2">
                  <li>Bereitstellung und Verbesserung unserer Dienste (KI-Weinempfehlungen, Sommelier-Chat)</li>
                  <li>Personalisierung Ihrer Nutzererfahrung</li>
                  <li>Kommunikation mit Ihnen</li>
                  <li>Gewährleistung der IT-Sicherheit</li>
                  <li>Einhaltung rechtlicher Anforderungen</li>
                </ul>
              </section>

              <section className="mb-8">
                <h2 className="text-xl font-semibold mb-4">5. Verwendung von Cookies</h2>
                <p className="text-muted-foreground leading-relaxed">
                  Unsere Website verwendet Cookies, um die Benutzerfreundlichkeit zu verbessern. Cookies sind kleine 
                  Textdateien, die auf Ihrem Gerät gespeichert werden. Sie können Ihren Browser so einstellen, dass 
                  er Sie über das Setzen von Cookies informiert und Cookies nur im Einzelfall erlauben.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-xl font-semibold mb-4">6. Datenweitergabe an Dritte</h2>
                <p className="text-muted-foreground leading-relaxed">
                  Wir können Personendaten an Dienstleister weitergeben, die uns bei der Erbringung unserer 
                  Dienstleistungen unterstützen (z.B. Hosting-Anbieter, KI-Dienste). Diese Dienstleister sind 
                  vertraglich verpflichtet, Ihre Daten vertraulich zu behandeln und nur für die vereinbarten 
                  Zwecke zu verwenden.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-xl font-semibold mb-4">7. Ihre Rechte</h2>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  Sie haben im Rahmen des anwendbaren Datenschutzrechts folgende Rechte:
                </p>
                <ul className="list-disc pl-5 text-muted-foreground space-y-2">
                  <li><strong className="text-foreground">Auskunftsrecht:</strong> Sie können Informationen über Ihre gespeicherten Daten verlangen</li>
                  <li><strong className="text-foreground">Berichtigungsrecht:</strong> Sie können unrichtige Daten korrigieren lassen</li>
                  <li><strong className="text-foreground">Löschungsrecht:</strong> Sie können die Löschung Ihrer Daten verlangen</li>
                  <li><strong className="text-foreground">Widerspruchsrecht:</strong> Sie können der Datenbearbeitung widersprechen</li>
                </ul>
              </section>

              <section className="mb-8">
                <h2 className="text-xl font-semibold mb-4">8. Datensicherheit</h2>
                <p className="text-muted-foreground leading-relaxed">
                  Wir treffen angemessene technische und organisatorische Sicherheitsmassnahmen, um Ihre 
                  Personendaten vor unbefugtem Zugriff, Verlust oder Missbrauch zu schützen.
                </p>
              </section>

              <section>
                <h2 className="text-xl font-semibold mb-4">9. Änderungen dieser Datenschutzerklärung</h2>
                <p className="text-muted-foreground leading-relaxed">
                  Wir können diese Datenschutzerklärung jederzeit ändern. Die aktuelle Version ist stets auf 
                  unserer Website verfügbar. Wir empfehlen Ihnen, diese Datenschutzerklärung regelmässig zu überprüfen.
                </p>
                <p className="text-muted-foreground mt-4 text-sm">
                  Stand: Dezember 2025
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

export default DatenschutzPage;
