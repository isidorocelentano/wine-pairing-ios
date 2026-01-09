import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Shield, Mail, Lock, Database, Cookie, UserX } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const PrivacyPage = () => {
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-b from-primary/10 to-background py-8 px-4">
        <div className="max-w-4xl mx-auto">
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={() => navigate(-1)}
            className="mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Zurück
          </Button>
          
          <div className="flex items-center gap-3 mb-4">
            <Shield className="w-10 h-10 text-primary" />
            <h1 className="text-3xl font-bold">Datenschutzerklärung</h1>
          </div>
          <p className="text-muted-foreground">
            Letzte Aktualisierung: 09. Januar 2026
          </p>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="prose prose-invert max-w-none space-y-8">
          
          {/* Einleitung */}
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Shield className="w-5 h-5 text-primary" />
                1. Einleitung
              </h2>
              <p className="text-muted-foreground leading-relaxed">
                Der Schutz Ihrer persönlichen Daten ist uns wichtig. Diese Datenschutzerklärung informiert Sie über Art, Umfang und Zweck der Verarbeitung personenbezogener Daten innerhalb unserer App "Wine Pairing" und der zugehörigen Website wine-pairing.online.
              </p>
              <p className="text-muted-foreground leading-relaxed mt-4">
                <strong className="text-foreground">Verantwortlicher:</strong><br />
                Wine Pairing Online<br />
                E-Mail: info@wine-pairing.online<br />
                Website: https://wine-pairing.online
              </p>
            </CardContent>
          </Card>

          {/* Erhobene Daten */}
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Database className="w-5 h-5 text-primary" />
                2. Welche Daten wir erheben
              </h2>
              <div className="space-y-4 text-muted-foreground">
                <div>
                  <h3 className="font-medium text-foreground">Kontodaten (bei Registrierung):</h3>
                  <ul className="list-disc list-inside mt-2 space-y-1">
                    <li>E-Mail-Adresse</li>
                    <li>Name (optional)</li>
                    <li>Passwort (verschlüsselt gespeichert)</li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-medium text-foreground">Nutzungsdaten:</h3>
                  <ul className="list-disc list-inside mt-2 space-y-1">
                    <li>Ihre Weinsammlung (Weinkeller)</li>
                    <li>Pairing-Anfragen und -Ergebnisse</li>
                    <li>Geschmacksprofil (Sommelier-Kompass)</li>
                    <li>Gespeicherte Favoriten</li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-medium text-foreground">Technische Daten:</h3>
                  <ul className="list-disc list-inside mt-2 space-y-1">
                    <li>IP-Adresse (anonymisiert)</li>
                    <li>Browser-Typ und -Version</li>
                    <li>Gerätetyp</li>
                    <li>Zugriffszeit</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Zweck der Verarbeitung */}
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Lock className="w-5 h-5 text-primary" />
                3. Zweck der Datenverarbeitung
              </h2>
              <div className="text-muted-foreground space-y-2">
                <p>Wir verarbeiten Ihre Daten zu folgenden Zwecken:</p>
                <ul className="list-disc list-inside space-y-1 mt-2">
                  <li>Bereitstellung und Verbesserung unserer Dienste</li>
                  <li>Personalisierte Weinempfehlungen</li>
                  <li>Verwaltung Ihres Benutzerkontos</li>
                  <li>Kommunikation (z.B. Passwort-Reset)</li>
                  <li>Analyse zur Verbesserung der App (Google Analytics)</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Google Analytics */}
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Cookie className="w-5 h-5 text-primary" />
                4. Google Analytics
              </h2>
              <div className="text-muted-foreground space-y-4">
                <p>
                  Wir nutzen Google Analytics 4, einen Webanalysedienst der Google LLC. Google Analytics verwendet Cookies und ähnliche Technologien, um Informationen über die Nutzung unserer Website zu sammeln.
                </p>
                <p>
                  <strong className="text-foreground">Erfasste Daten:</strong> Seitenaufrufe, Verweildauer, Gerätetyp, ungefährer Standort (Land/Stadt), Referrer.
                </p>
                <p>
                  <strong className="text-foreground">Rechtsgrundlage:</strong> Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an der Analyse des Nutzerverhaltens).
                </p>
                <p>
                  Sie können die Erfassung durch Google Analytics verhindern, indem Sie das Browser-Add-on zur Deaktivierung von Google Analytics installieren: 
                  <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline ml-1">
                    Google Analytics Opt-out
                  </a>
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Datenweitergabe */}
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4">5. Datenweitergabe an Dritte</h2>
              <div className="text-muted-foreground space-y-4">
                <p>Wir geben Ihre personenbezogenen Daten nicht an Dritte weiter, außer:</p>
                <ul className="list-disc list-inside space-y-1">
                  <li>Mit Ihrer ausdrücklichen Einwilligung</li>
                  <li>Zur Erfüllung gesetzlicher Verpflichtungen</li>
                  <li>An Dienstleister, die uns bei der Bereitstellung unserer Dienste unterstützen (z.B. Hosting, E-Mail-Versand)</li>
                </ul>
                <p className="mt-4">
                  <strong className="text-foreground">Eingesetzte Dienstleister:</strong>
                </p>
                <ul className="list-disc list-inside space-y-1">
                  <li>MongoDB Atlas (Datenbank) - USA, EU-Standardvertragsklauseln</li>
                  <li>Resend (E-Mail-Versand) - USA, EU-Standardvertragsklauseln</li>
                  <li>Stripe (Zahlungsabwicklung) - USA, EU-Standardvertragsklauseln</li>
                  <li>Google Analytics - USA, EU-Standardvertragsklauseln</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Datensicherheit */}
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Lock className="w-5 h-5 text-primary" />
                6. Datensicherheit
              </h2>
              <div className="text-muted-foreground space-y-2">
                <p>Wir setzen technische und organisatorische Sicherheitsmaßnahmen ein, um Ihre Daten zu schützen:</p>
                <ul className="list-disc list-inside space-y-1 mt-2">
                  <li>SSL/TLS-Verschlüsselung für alle Datenübertragungen</li>
                  <li>Verschlüsselte Speicherung von Passwörtern (bcrypt)</li>
                  <li>Regelmäßige Sicherheitsupdates</li>
                  <li>Zugriffsbeschränkungen für Mitarbeiter</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Ihre Rechte */}
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <UserX className="w-5 h-5 text-primary" />
                7. Ihre Rechte
              </h2>
              <div className="text-muted-foreground space-y-4">
                <p>Sie haben folgende Rechte bezüglich Ihrer personenbezogenen Daten:</p>
                <ul className="list-disc list-inside space-y-1">
                  <li><strong className="text-foreground">Auskunft:</strong> Sie können Auskunft über Ihre gespeicherten Daten verlangen.</li>
                  <li><strong className="text-foreground">Berichtigung:</strong> Sie können die Berichtigung unrichtiger Daten verlangen.</li>
                  <li><strong className="text-foreground">Löschung:</strong> Sie können die Löschung Ihrer Daten verlangen ("Recht auf Vergessenwerden").</li>
                  <li><strong className="text-foreground">Einschränkung:</strong> Sie können die Einschränkung der Verarbeitung verlangen.</li>
                  <li><strong className="text-foreground">Datenübertragbarkeit:</strong> Sie können Ihre Daten in einem gängigen Format erhalten.</li>
                  <li><strong className="text-foreground">Widerspruch:</strong> Sie können der Verarbeitung widersprechen.</li>
                </ul>
                <p className="mt-4">
                  Zur Ausübung Ihrer Rechte kontaktieren Sie uns bitte unter: 
                  <a href="mailto:info@wine-pairing.online" className="text-primary hover:underline ml-1">
                    info@wine-pairing.online
                  </a>
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Kontolöschung */}
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4">8. Kontolöschung</h2>
              <div className="text-muted-foreground space-y-2">
                <p>
                  Sie können Ihr Konto jederzeit löschen. Dabei werden alle Ihre personenbezogenen Daten unwiderruflich gelöscht, einschließlich:
                </p>
                <ul className="list-disc list-inside space-y-1 mt-2">
                  <li>Kontoinformationen (E-Mail, Name)</li>
                  <li>Gespeicherte Weine im Weinkeller</li>
                  <li>Pairing-Verlauf</li>
                  <li>Geschmacksprofil</li>
                </ul>
                <p className="mt-4">
                  Um Ihr Konto zu löschen, gehen Sie zu <strong className="text-foreground">Profil → Einstellungen → Konto löschen</strong> oder kontaktieren Sie uns per E-Mail.
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Cookies */}
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Cookie className="w-5 h-5 text-primary" />
                9. Cookies
              </h2>
              <div className="text-muted-foreground space-y-4">
                <p>Unsere Website verwendet folgende Arten von Cookies:</p>
                <div className="overflow-x-auto">
                  <table className="w-full mt-2 text-sm">
                    <thead>
                      <tr className="border-b border-border">
                        <th className="text-left py-2 text-foreground">Cookie</th>
                        <th className="text-left py-2 text-foreground">Zweck</th>
                        <th className="text-left py-2 text-foreground">Dauer</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr className="border-b border-border/50">
                        <td className="py-2">Session</td>
                        <td className="py-2">Login-Status</td>
                        <td className="py-2">Sitzung</td>
                      </tr>
                      <tr className="border-b border-border/50">
                        <td className="py-2">_ga, _gid</td>
                        <td className="py-2">Google Analytics</td>
                        <td className="py-2">2 Jahre / 24h</td>
                      </tr>
                      <tr>
                        <td className="py-2">theme</td>
                        <td className="py-2">Design-Einstellung</td>
                        <td className="py-2">1 Jahr</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Änderungen */}
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4">10. Änderungen dieser Datenschutzerklärung</h2>
              <p className="text-muted-foreground">
                Wir behalten uns vor, diese Datenschutzerklärung anzupassen, um sie an geänderte Rechtslagen oder bei Änderungen unserer Dienste anzupassen. Die aktuelle Version finden Sie immer auf dieser Seite.
              </p>
            </CardContent>
          </Card>

          {/* Kontakt */}
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Mail className="w-5 h-5 text-primary" />
                11. Kontakt
              </h2>
              <p className="text-muted-foreground">
                Bei Fragen zur Verarbeitung Ihrer personenbezogenen Daten oder zur Ausübung Ihrer Rechte kontaktieren Sie uns bitte:
              </p>
              <div className="mt-4 p-4 bg-muted/30 rounded-lg">
                <p className="text-foreground font-medium">Wine Pairing Online</p>
                <p className="text-muted-foreground">E-Mail: info@wine-pairing.online</p>
                <p className="text-muted-foreground">Website: https://wine-pairing.online</p>
              </div>
            </CardContent>
          </Card>

        </div>
      </div>

      {/* Footer */}
      <div className="max-w-4xl mx-auto px-4 py-8 text-center text-sm text-muted-foreground border-t border-border mt-8">
        <p>© 2026 Wine Pairing Online. Alle Rechte vorbehalten.</p>
      </div>
    </div>
  );
};

export default PrivacyPage;
