# 📖 WINE PAIRING APP - Vollständige Dokumentation

**Stand:** 27. Dezember 2025  
**Version:** 1.8.1 (Restaurant-Modus UI & UX-Verbesserungen)  
**Domain:** https://wine-pairing.online

---

## 📊 ÜBERSICHT

| Metrik | Wert |
|--------|------|
| **Weine** | 7,090 (wächst dynamisch) |
| **Rebsorten** | 313 (alle mit Bildern & Slugs) |
| **Sommelier Kompass** | 1,895 Gerichte |
| **Blog-Artikel** | 233 |
| **Community Feed** | 269 Beiträge |
| **Sprachen** | DE, EN, FR |
| **Monetarisierung** | Freemium + Stripe |
| **Zielmarkt** | Deutschland (€-Preise) |

---

## 🆕 ÄNDERUNGSHISTORIE

### Version 1.8.1 (27.12.2025) - Restaurant-Modus UI & UX-Verbesserungen

**🍽️ Restaurant-Modus verbessert:**
- ✅ **Neuer Einleitungstext:** "Such dir einfach 3-5 Weine aus der Karte aus, die dich preislich und stilistisch ansprechen – den Rest übernehme ich!"
- ✅ **Hervorgehobenes Design:** Gradient-Box mit stärkerem Rahmen
- ✅ **Größeres Eingabefeld:** 100px Höhe, bessere Lesbarkeit
- ✅ **Weißer Hintergrund:** Im Textfeld für besseren Kontrast
- ✅ **Verbesserte Bestätigung:** "Perfekt! Du erhältst jetzt eine persönliche Empfehlung aus deiner Auswahl."

**💡 "Weniger geeignet" Sektion verbessert:**
- ✅ **Freundlicherer Titel:** "Eher weniger geeignet" statt "Vermeide"
- ✅ **Sanftere Farben:** Amber statt Rot (weniger warnend)
- ✅ **Glühbirne-Emoji:** 💡 statt ⚠️ (Tipp statt Warnung)
- ✅ **Neutralisierungs-Tipp:** "Ein Schluck Wasser oder ein Stück Brot zwischendurch neutralisiert den Gaumen – so schmeckt jeder Wein wieder frisch!"

### Version 1.8.0 (27.12.2025) - Scan-Fix & SEO-Optimierung

**📱 Etiketten-Scan Fix für iOS Safari:**
- ✅ **Problem gelöst:** iOS Safari blockierte große Bild-Uploads still
- ✅ **Bildkomprimierung:** Max 800x800 Pixel, 50% JPEG Qualität
- ✅ **Vereinfachter Code:** Keine komplexen async-Funktionen mehr
- ✅ **Sofortige Bild-Anzeige:** Bild wird vor API-Call angezeigt
- ✅ **Fehlerbehandlung:** Toast-Nachrichten bei Erfolg/Fehler

**🔍 SEO-Optimierung für Google & KI-Suchmaschinen:**
- ✅ **Neuer Title:** "Wein-Pairing leicht gemacht – Genuss ohne Regeln"
- ✅ **Neue Meta-Description:** "Genuss steht an erster Stelle. Entdecke spannende Wein-Kombinationen zu deinem Lieblingsessen."
- ✅ **Haupt-Keywords:** Wein-Pairing, Wein zu Essen, welcher Wein passt, Wein-Empfehlung KI
- ✅ **Neben-Keywords:** Geschmacks-Balance, KI Sommelier, digitaler Sommelier, Online Weinberater
- ✅ **KI-Suchmaschinen-Optimierung:**
  - FAQ-Schema (Welcher Wein passt zu Pasta/Fisch?)
  - HowTo-Schema (3 Schritte zum perfekten Pairing)
  - Abstract Meta-Tag für Perplexity, ChatGPT Search, Google SGE
- ✅ **Seitenspezifische SEO:** Pairing, Cellar, Wein-DB, Tipp der Woche

**💡 Tipp der Woche Feature:**
- ✅ **Backend:** Automatische Generierung von 4 Wochen-Tipps beim Start
- ✅ **Frontend:** Neue Seite /tipp-der-woche mit Archiv
- ✅ **API:** GET /api/weekly-tips, GET /api/weekly-tips/archive

**🔐 Auth-Verbesserungen:**
- ✅ **Google Login Fix:** refreshAuth() nach Google OAuth
- ✅ **AuthContext:** Neuer refreshAuth Alias für AuthCallback
- ✅ **Token-Handling:** Bessere localStorage Integration

### Version 1.7.1 (24.12.2025) - Genuss-Philosophie & UI-Optimierungen

**🏠 Neue Homepage "Genuss-First" Hero-Section:**
- ✅ **Emotionale Headline:** "Dein Wein. Dein Essen. Dein Moment."
- ✅ **Subtitle:** "Wissenschaftlich fundierte Empfehlungen – ganz ohne Dogmen."
- ✅ **4 Philosophie-Punkte mit Emojis:**
  - ✨ Kein Richtig oder Falsch
  - 👅 Dein Geschmack weist den Weg
  - 🍞 Einfach ausprobieren
  - 🎉 Hab einfach Spaß
- ✅ **CTA-Button:** "🍷 Jetzt mein perfektes Pairing finden"
- ✅ **Vertrauens-Element:** "Powered by KI & Sommelier-Expertise"
- ✅ **Quick-Navigation:** Separate Sektion mit Buttons zu allen Features

**🍷 Neue Pairing-Seite "Genuss-Philosophie" Einleitung:**
- ✅ **Zuklappbare Sektion:** "✨ Deine Weinreise, deine Regeln"
- ✅ **3 Schritte mit Icons:**
  - 🔍 Entdecke (Lupe, lila)
  - ❤️ Probiere (Herz, rosa)
  - 💧 Neutralisiere (Wasserglas, blau)
- ✅ **Footer:** "Lass dich von deinem Geschmack leiten..."
- ✅ **Responsive:** Desktop und Mobile optimiert

**🐛 Bug Fixes:**
- ✅ **Geheimtipp-Anzeige:** Parser akzeptiert jetzt fettgedruckte Weinnamen
- ✅ **Weinart-Präferenz:** KI respektiert jetzt die Benutzer-Auswahl (Rotwein zu Fisch möglich)

---

### Version 1.7 (22.12.2025) - Preistags für Weinkeller & Weindatenbank

**🍷 Preiskategorien im Weinkeller - NEU:**
- ✅ Einheitliches **🍷-System** für den persönlichen Weinkeller:
  - 🍷 **Alltags-Genuss** (bis €20) - grünes Styling
  - 🍷🍷 **Gehobener Anlass** (€20-50) - amber Styling
  - 🍷🍷🍷 **Besonderer Moment** (ab €50) - orange Styling
- ✅ **Preiskategorie-Auswahl** beim Hinzufügen von Weinen (3 klickbare Buttons)
- ✅ **Preiskategorie bearbeiten** im Edit-Dialog
- ✅ **Preisfilter-Dropdown** in der Weinkeller-Übersicht
- ✅ **Preisbadges** auf jeder Weinkarte
- ✅ **Preisstatistiken** in der Keller-Statistikkarte

**🍷 Preiskategorien in der Weindatenbank - NEU:**
- ✅ **Automatische Preisschätzung** für 5181+ Weine basierend auf:
  - Region/Appellation (Grand Cru, Premier Cru → 🍷🍷🍷)
  - Berühmte Weingüter (Château Margaux, Romanée-Conti → 🍷🍷🍷)
  - Qualitätsstufen (Chablis, Châteauneuf-du-Pape → 🍷🍷)
- ✅ **Preisfilter** im Filter-Panel der Weindatenbank
- ✅ **Preisbadges** auf allen Weinkarten mit Farbcodierung
- ✅ **Preisbadge im Detail-Modal**
- ✅ **Kombinierte Filter** (Land + Preiskategorie)

**🔐 Authentifizierung verbessert - NEU:**
- ✅ **Google OAuth** - 1-Klick-Anmeldung über Google
- ✅ **localStorage-Token** - Löst Safari/iOS Cookie-Probleme
- ✅ **Beide Methoden parallel** - Cookie + Bearer Token

**Technische Änderungen:**
- Backend: `price_category` Feld zu Wine-Models hinzugefügt
- Backend: `POST /api/admin/estimate-wine-prices` für automatische Schätzung
- Backend: `POST /api/auth/google/session` für Google OAuth
- Backend: Token wird jetzt in Login/Register-Response zurückgegeben
- Backend: Weinart-Präferenz wird an KI-Prompt weitergegeben
- Frontend: Neue UI-Komponenten in CellarPage.js und WineDatabasePage.js
- Frontend: GoogleLoginButton.js und AuthCallback.js für Google OAuth
- Frontend: localStorage-Token-Support in AuthContext.js
- Frontend: Neue Hero-Section in HomePage.js
- Frontend: Genuss-Philosophie-Sektion in PairingPage.js

---

### Version 1.6 (22.12.2025) - Restaurant-Modus & Style-First

**🍽️ Restaurant-Modus - NEU:**
- ✅ Neues Feature: **"Im Restaurant? Weinkarte eingeben"**
- ✅ User gibt Weine von der Karte ein → KI empfiehlt konkret aus dieser Liste
- ✅ Spezielle Antwort-Struktur:
  - 🍷 **MEINE EMPFEHLUNG** - DER beste Wein aus der Liste
  - 💡 **WARUM GENAU DIESER WEIN?** - Detaillierte Begründung
  - 🔄 **ALTERNATIVE** - Zweite Option aus der Liste
  - ⚠️ **VERMEIDE** - Welchen Wein NICHT wählen
- ✅ 3-sprachig: DE/EN/FR
- ✅ Prominente Anzeige mit Restaurant-Badge

**🍷 Style-First Ansatz - NEU:**
- ✅ Neue Struktur für Standard-Empfehlungen:
  - **🍷 DER STIL** - Erklärt den passenden Weinstil
  - **💡 DAS WARUM** - Wissenschaftliche Balance zum Gericht
  - **🍷 EMPFEHLUNGEN** - Gestaffelt nach Preiskategorie
  - **💎 GEHEIMTIPP** - Günstigere Alternative aus weniger bekannter Region

**💶 Preisskala für Weinliebhaber (DE-Markt):**
- ✅ Umstellung von CHF auf **€** (Deutscher Markt größer)
- ✅ Einheitliche **🍷-Symbole** (statt 💚💛🧡)
- ✅ Neue Preisstufen für Fachhandel-Qualität:
  - 🍷 **Alltags-Genuss** (bis €20)
  - 🍷🍷 **Gehobener Anlass** (€20-50)
  - 🍷🍷🍷 **Besonderer Moment** (ab €50)
- ✅ Fokus auf konkrete Weingüter (Dönnhoff, Keller, Antinori, Gaja, etc.)

---

### Version 1.5 (20.12.2025) - € und 🍷-System

**Einheitliches Preissystem:**
- Wechsel von CHF auf € für deutschen Markt
- Einheitliche 🍷-Symbole statt Farbcodierung
- Style-First Ansatz implementiert
- Geheimtipp-Section hinzugefügt

---

### Version 1.4 (20.12.2025) - Preisbewusste Empfehlungen

**Gestaffelte Preiskategorien:**
- KI empfiehlt erschwingliche Weine zuerst
- 3 Preisstufen mit farbcodierten Karten
- "Premium anzeigen" Button für Luxus-Weine

---

### Version 1.3 (20.12.2025) - Freemium Pricing Pages

**Neue Seiten:**
- `/pricing` und `/pro` - Dedizierte Pricing-Seite
- Homepage Pricing-Teaser für Nicht-Pro-User
- Emotionales Design mit Unsplash-Bildern

---

### Version 1.2 (18.12.2025) - Rebsorten & D/A/CH

**Datenbereinigung:**
- 313 Rebsorten mit Bildern
- D/A/CH Weinfilter bereinigt
- URL-Parameter für Deep-Linking

---

## 💳 TEIL 1: FREEMIUM-SYSTEM

### Pläne

| Plan | Preis | Pairing/Tag | Chat/Tag | Weinkeller | Favoriten |
|------|-------|-------------|----------|------------|-----------|
| **Basic** | Kostenlos | 5 | 5 | Max. 10 | Max. 10 |
| **Pro Monatlich** | 4,99€/Monat | Unbegrenzt | Unbegrenzt | Unbegrenzt | Unbegrenzt |
| **Pro Jährlich** | 39,99€/Jahr | Unbegrenzt | Unbegrenzt | Unbegrenzt | Unbegrenzt |

### 🆕 Pricing-Seiten (NEU in v1.3)

**Pricing Page (`/pricing` oder `/pro`):**
| Section | Beschreibung |
|---------|--------------|
| **Hero** | Emotionaler Einstieg mit "Dein Sommelier. Immer dabei." |
| **Plan-Vergleich** | Basic vs. Pro Karten mit Feature-Liste |
| **Warum Pro?** | 3 Benefit-Karten (Keine Limits, Sofortige Antworten, Premium Features) |
| **Testimonials** | 5-Sterne Bewertungen von Nutzern |
| **FAQ** | Häufige Fragen (Kündigung, Garantie, Zahlungsmethoden) |
| **Final CTA** | Abschließender Call-to-Action mit Weinbild-Hintergrund |

**Homepage Pricing-Teaser:**
- Erscheint nach der Features-Section (nur für Nicht-Pro-Nutzer)
- Kompakte Free vs. Pro Vergleichskarten
- "Alle Vorteile ansehen" Link zur /pricing Seite

### Zahlungsintegration
- ✅ **Stripe** (aktiv)
- 🔜 **PayPal** (geplant)

### 🆕 Preisstufen für Weinliebhaber (v1.6)

**Zielgruppe:** Weinliebhaber die im Fachhandel kaufen (nicht nur Supermarkt)

| Kategorie | Preisbereich | Beschreibung |
|-----------|--------------|--------------|
| 🍷 **Alltags-Genuss** | bis €20 | Täglicher Genuss, gute Qualität |
| 🍷🍷 **Gehobener Anlass** | €20-50 | Dinner, Gäste, besondere Mahlzeiten |
| 🍷🍷🍷 **Besonderer Moment** | ab €50 | Luxus, Feiern, Sammlerstücke |

**Empfohlene Weingüter:** Dönnhoff, Keller, Trimbach, Antinori, Gaja, Guigal, Torres

**Beispiel-Output (Standard-Modus):**
```
🍷 DER STIL
Frischer, trockener Weißwein mit lebendiger Säure und mineralischen Noten.

💡 DAS WARUM
Die Säure schneidet durch das Fett der Panade und erfrischt den Gaumen.

🍷 EMPFEHLUNGEN

🍷 Alltags-Genuss (bis €20):
- Dönnhoff Riesling trocken, Nahe
- Trimbach Riesling, Elsass

🍷🍷 Gehobener Anlass (€20-50):
- Franz Hirtzberger Grüner Veltliner Smaragd

💎 GEHEIMTIPP
Côtes de Gascogne Blanc - gleiche Frische für unter €10!
```

---

### 🍽️ Restaurant-Modus (NEU in v1.6)

**Situation:** User sitzt im Restaurant und hat die Weinkarte vor sich.

**Funktionsweise:**
1. User gibt Gericht ein (z.B. "Entrecôte")
2. User klickt "Im Restaurant? Weinkarte eingeben"
3. User gibt verfügbare Weine ein (z.B. "Bordeaux 2019, Barolo, Grüner Veltliner")
4. KI empfiehlt DEN BESTEN Wein aus dieser Liste

**Antwort-Struktur:**
```
🍷 MEINE EMPFEHLUNG
Barolo Riserva 2018

💡 WARUM GENAU DIESER WEIN?
Der Barolo bringt kraftvolle Tannine und dunkle Frucht, die perfekt
zum saftigen Entrecôte passen. Seine Struktur greift das Fett auf...

🔄 ALTERNATIVE AUS DER LISTE
Bordeaux 2019 - funktioniert auch gut, etwas weicher im Tannin.

⚠️ VERMEIDE
Grüner Veltliner - zu leicht und säurebetont für rotes Fleisch.
```

**UI-Element:** Ausklappbares Textfeld unter dem Weintyp-Selektor

---

### Gutschein-System
- Route: `/coupon`
- Early Adopter Codes verfügbar

---

## 🏠 TEIL 2: KERN-FEATURES

### 1. STARTSEITE
**Route:** `/`  
**Zugriff:** 🆓 Alle

Elegante Landing Page mit Hero-Section und virtuellem Sommelier "Claude".

**NEU in v1.3:**
- Pricing-Teaser-Section nach den Features (nur für Nicht-Pro-Nutzer)
- "Dein Sommelier. Immer dabei." Tagline
- Free vs. Pro Vergleichskarten
- Link zur vollständigen Pricing-Seite

---

### 1b. HOMEPAGE - GENUSS-FIRST HERO (v1.7.1)
**Route:** `/`  
**Zugriff:** 🆓 Alle

**Neue Hero-Section mit emotionaler Ansprache:**

| Element | Inhalt |
|---------|--------|
| **Tagline** | "WEIN-PAIRING NEU GEDACHT" |
| **Headline** | "Dein Wein. Dein Essen. Dein Moment." |
| **Subtitle** | "Wissenschaftlich fundierte Empfehlungen – ganz ohne Dogmen." |

**4 Philosophie-Punkte:**
- ✨ **Kein Richtig oder Falsch** - Beim Wein-Pairing geht es nur um Genuss
- 👅 **Dein Geschmack weist den Weg** - Unsere Vorschläge sind Inspirationen
- 🍞 **Einfach ausprobieren** - Mit Wasser oder Brot neutralisieren
- 🎉 **Hab einfach Spaß** - Entdecke neue Welten, ohne Stress

**CTA:** "🍷 Jetzt mein perfektes Pairing finden" (Kostenlos, ohne Registrierung)

**Vertrauens-Element:** "Powered by KI & Sommelier-Expertise"

**Quick-Navigation:** Buttons zu Sommelier Kompass, Weindatenbank, Weinkeller, etc.

---

### 1c. PRICING-SEITE (NEU)
**Route:** `/pricing`, `/pro`  
**Zugriff:** 🆓 Alle

Dedizierte Seite für Freemium-Kommunikation.

**Sections:**
- Hero mit emotionalem Bild & Tagline
- Plan-Vergleich (Basic vs. Pro)
- "Warum Pro?" Benefits
- Testimonials mit 5-Sterne-Bewertungen
- FAQ-Bereich
- Finaler CTA

**Design:** Modern/dynamisch (nicht traditionell "staubiger Weinkeller")

---

### 2. PAIRING (Weinempfehlung)
**Route:** `/pairing`, `/pairing/:slug`  
**Zugriff:** 🆓 Basic: 5/Tag | 👑 Pro: Unbegrenzt

**🆕 Genuss-Philosophie Einleitung (v1.7.1):**
- Zuklappbare Sektion: "✨ Deine Weinreise, deine Regeln"
- 3 Schritte: Entdecke → Probiere → Neutralisiere
- Footer: "Lass dich von deinem Geschmack leiten..."

**Funktionsweise:**
1. User gibt Gericht ein
2. KI empfiehlt passende Weine
3. **Dynamisches DB-Wachstum:** Neue Weine werden automatisch zur Datenbank hinzugefügt

**"Aus meinem Weinkeller" Option:**
- KI empfiehlt NUR Weine aus dem persönlichen Weinkeller
- Perfekt für: "Was trinke ich heute zu meinem Abendessen?"

**Filter:**
- Weintyp (Rot/Weiss/Rosé/Schaumwein) - **KI respektiert Auswahl!**
- Land des Gerichts
- Trend-Gerichte / Bestseller
- Profi-Modus (4D-Werte)

**Zusätzliche Features:**
- Sprachsteuerung (Voice Input)
- Autocomplete aus Gerichte-Datenbank

---

### 3. WEINKELLER
**Route:** `/cellar`, `/weinkeller`  
**Zugriff:** 🔒 Nur eingeloggte User  
**Limits:** 🆓 Basic: 10 Weine | 👑 Pro: Unbegrenzt

**Beschreibung:**  
Jeder User hat seinen **eigenen privaten Weinkeller**. Vollständige User-Isolation.

**Features:**
- Weine manuell hinzufügen
- **Etiketten-Scan** (KI erkennt Wein aus Foto) - **NEU in v1.8: iOS Safari Fix!**
- Bearbeiten & Löschen
- Mengenverwaltung (+/-)
- Favoriten markieren

**🆕 Etiketten-Scan Technische Details (v1.8.0):**
```
Problem: iOS Safari blockiert still große fetch() Anfragen (>1-2MB)
Lösung:  Bildkomprimierung vor Upload

Komprimierung:
- Max. Größe: 800x800 Pixel
- JPEG Qualität: 50%
- Ergebnis: ~50-150KB statt 4-11MB

Code-Flow:
1. User wählt Foto → FileReader.readAsDataURL()
2. Image in Canvas laden → skalieren
3. canvas.toDataURL('image/jpeg', 0.5)
4. fetch() mit komprimiertem Base64
5. Response → Form-Felder ausfüllen
```
- Filter nach Typ & Verfügbarkeit
- **🆕 Preiskategorie-System (v1.7):**
  - 🍷 **Alltags-Genuss** (bis €20)
  - 🍷🍷 **Gehobener Anlass** (€20-50)
  - 🍷🍷🍷 **Besonderer Moment** (ab €50)
- **🆕 Preisfilter:** Filter nach Preiskategorie
- Statistik-Dashboard (mit Preisaufschlüsselung)

**Technisch:**
- `user_id` Verknüpfung pro Wein
- `price_category` Feld ('1', '2', '3' oder null)
- Datenbank-Index für Skalierung (1000+ User)

---

### 4. CHAT
**Route:** `/chat`  
**Zugriff:** 🆓 Basic: 5/Tag | 👑 Pro: Unbegrenzt

**Features:**
- Freie Konversation mit Sommelier "Claude"
- **Bildanalyse** (Etikett-Erkennung)
- Sprachsteuerung
- Session-basierte Konversation

---

## 📚 TEIL 3: DATENBANK & WISSEN

### 5. REBSORTEN-LEXIKON
**Route:** `/grapes`, `/grapes/:slug`  
**Zugriff:** 🆓 Alle  
**Anzahl:** 313 Rebsorten

**Update 18.12.2025:**
- ✅ Alle 313 Rebsorten haben jetzt hochwertige Weinbilder
- ✅ Alle Rebsorten sind klickbar (Slugs generiert)
- ✅ Navigation zur Detailseite funktioniert

**Bildverteilung nach Weintyp:**
| Typ | Anzahl | Bildmotive |
|-----|--------|------------|
| 🍷 Rotwein | 128 | Rotweingläser, dunkle Trauben |
| 🥂 Weißwein | 136 | Weißweingläser, helle Trauben |
| 🌸 Rosé | 29 | Rosé-Gläser, elegante Settings |
| 🍾 Schaumwein | 20 | Champagnergläser, Sektflaschen |

**Inhalte pro Rebsorte:**
- Beschreibung (DE/EN/FR)
- Farbe, Körper-Typ, Säure, Tannine
- Primär- & Tertiär-Aromen
- Herkunftsregionen
- Synonyme
- Passende Speisen

---

### 6. WEIN-DATENBANK
**Route:** `/wine-database`  
**Zugriff:** 🆓 Alle  
**Anzahl:** 7,084 Weine (wächst dynamisch!)

**🆕 Preiskategorien (v1.7):**
- 🍷 **Alltags-Genuss** (bis €20) - grünes Badge
- 🍷🍷 **Gehobener Anlass** (€20-50) - amber Badge
- 🍷🍷🍷 **Besonderer Moment** (ab €50) - orange Badge
- Automatische Schätzung basierend auf Region/Appellation
- 5181+ Weine mit Preiskategorien versehen

**Länder (bereinigt am 18.12.2025):**
| Land | Weine | Regionen | Appellationen |
|------|-------|----------|---------------|
| 🇫🇷 Frankreich | 1,861 | 10 | 107 |
| 🇮🇹 Italien | 1,551 | 17 | 70 |
| 🇪🇸 Spanien | 1,209 | 24 | 34 |
| 🇨🇭 Schweiz | 751 | **13** (bereinigt) | 24 |
| 🇩🇪 Deutschland | 678 | **10** (bereinigt) | 16 |
| 🇦🇹 Österreich | 678 | **16** (bereinigt) | 32 |
| Weitere | ~356 | - | - |

**D/A/CH Bereinigung (18.12.2025):**
- 943 Weine korrigiert
- Tippfehler behoben (Wuejrttemberg, Rheinessen, Graubuenden)
- Sub-Regionen zu Hauptregionen konsolidiert
- Ungültige Appellationen entfernt (Kabinett, Spätlese, Punkte-Bewertungen)

**Filter-System (verbessert):**
- **Land**: Alle verfügbaren Weinländer
- **Region**: Nur echte Regionen (sauber getrennt von Appellationen)
- **Appellation**: Aktualisiert sich basierend auf Region-Auswahl
- **Rebsorte, Weinfarbe**
- **🆕 Preiskategorie**: Filter nach 🍷/🍷🍷/🍷🍷🍷

**Beispiel Frankreich:**
- Region "Bordeaux" → zeigt 33 Appellationen (Pauillac, Saint-Émilion, Margaux, etc.)
- Region "Piemont" (Italien) → zeigt 24 Appellationen (Barolo, Barbaresco, etc.)

**Aktionen:**
- Zu Favoriten hinzufügen
- Zum Weinkeller hinzufügen

---

### 7. SOMMELIER KOMPASS
**Route:** `/sommelier-kompass`  
**Zugriff:** 🆓 Alle  
**Anzahl:** 1,895 regionale Gerichte (16 Länder)

**Länder-Übersicht:**
| Land | Gerichte |
|------|----------|
| 🇮🇹 Italien | 379 |
| 🇵🇹 Portugal | 281 |
| 🇫🇷 Frankreich | 242 |
| 🇩🇪 Deutschland | 234 |
| 🇪🇸 Spanien | 225 |
| 🇨🇭 Schweiz | 139 |
| 🇦🇹 Österreich | 113 |
| 🇨🇳 China | 88 |
| 🇬🇷 Griechenland | 51 |
| 🇺🇸 USA | 45 |
| 🇹🇭 Thailand | 22 |
| 🇯🇵 Japan | 20 |
| 🇦🇷 Argentinien | 20 |
| 🌍 International | 17 |
| 🇿🇦 Südafrika | 15 |
| 🇹🇷 Türkei | 4 |

**Features:**
- Filter nach Land & Region
- Volltextsuche
- "Load More" Pagination
- Weinempfehlungen pro Gericht
- **URL-Parameter:** z.B. `/sommelier-kompass?country=China` (NEU)

---

### 8. COMMUNITY FEED
**Route:** `/feed`  
**Zugriff:** 🆓 Lesen alle | 🔒 Posten nur eingeloggte  
**Anzahl:** 268 Beiträge

**Beschreibung:**  
User teilen ihre Wein-Erfahrungen und Pairings.

**Features:**
- Beiträge erstellen (Text + Bild)
- Liken & Kommentieren
- Kategorie-Filter

---

### 9. BLOG
**Route:** `/blog`, `/blog/:slug`  
**Zugriff:** 🆓 Alle  
**Anzahl:** 233 Artikel

**Kategorien:**
- Rebsorten (144)
- Regionen (84)
- Tipps (3)
- Weitere...

---

## 🔐 TEIL 4: BENUTZER-FEATURES

### 10. AUTHENTIFIZIERUNG
**Routes:** `/login`, `/register`

- E-Mail/Passwort Registrierung
- JWT Session-Cookie
- Automatische Session-Verwaltung

---

### 11. FAVORITEN
**Route:** `/favorites`  
**Limits:** 🆓 Basic: 10 | 👑 Pro: Unbegrenzt

Weine aus der Datenbank als Favorit speichern.

---

### 12. ABONNEMENT
**Route:** `/subscription`

Upgrade auf Pro-Plan via Stripe.

---

## 🤖 TEIL 5: TECHNISCHE FEATURES

### 13. KI-INTEGRATION

**KI:** Claude (Anthropic) via Emergent LLM Key

| Feature | Beschreibung |
|---------|--------------|
| Pairing-Empfehlungen | KI analysiert Gericht, empfiehlt Weine, fügt neue zur DB hinzu |
| Chat-Sommelier | Freie Konversation |
| Bildanalyse | Erkennt Weinetiketten |
| Etiketten-Scan | Extrahiert Wein-Infos für Weinkeller |

---

### 14. BACKUP-SYSTEM

**Automatisch:**
- Alle 6 Stunden
- Bei Server-Start
- 10 Backups werden behalten

**Auto-Restore:**
- Bei leerem Server: Daten aus JSON-Dateien wiederhergestellt
- Schützt vor Datenverlust bei Deployments

**Manuell:**
- API: `POST /api/backup/create`
- Skript: `python3 scripts/create_verified_backup.py`

**Downloads:**
- Excel: `/api/export/excel/{collection}`
- JSON: `/api/backup/download/{collection}.json`
- Übersicht: `/api/export/excel-links`

---

### 15. MEHRSPRACHIGKEIT

| Sprache | Code |
|---------|------|
| 🇩🇪 Deutsch | de (Standard) |
| 🇬🇧 Englisch | en |
| 🇫🇷 Französisch | fr |

**Übersetzt:** UI, Wein-Beschreibungen, Rebsorten, Blog, Sommelier Kompass

---

## 🔌 TEIL 6: API-ENDPOINTS

### Authentifizierung
| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| POST | `/api/auth/register` | Registrieren |
| POST | `/api/auth/login` | Einloggen |
| POST | `/api/auth/logout` | Ausloggen |
| GET | `/api/auth/me` | Aktueller User |

### Pairing & Chat
| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| POST | `/api/pairing` | Weinempfehlung |
| POST | `/api/chat` | Chat mit Sommelier |
| POST | `/api/scan-label` | Etikett scannen |

### Weinkeller (Auth erforderlich)
| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| GET | `/api/wines` | Eigene Weine |
| POST | `/api/wines` | Wein hinzufügen |
| PUT | `/api/wines/{id}` | Bearbeiten |
| DELETE | `/api/wines/{id}` | Löschen |

### Datenbanken (öffentlich)
| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| GET | `/api/public-wines` | Wein-Datenbank |
| GET | `/api/grape-varieties` | Rebsorten |
| GET | `/api/regional-pairings` | Sommelier Kompass |
| GET | `/api/blog-posts` | Blog |
| GET | `/api/feed` | Community Feed |

### Backup & Export
| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| GET | `/api/export/excel/{collection}` | Excel-Download |
| GET | `/api/backup/download/{name}.json` | JSON-Download |
| GET | `/api/export/excel-links` | Alle Links |
| POST | `/api/backup/create` | Backup erstellen |
| GET | `/api/health` | Server-Status |

---

## 🚀 TEIL 7: DEPLOYMENT

### URLs
- **Preview:** https://winery-upgrade.preview.emergentagent.com
- **Produktion:** https://wine-pairing.online

### Tech-Stack
- **Frontend:** React + Tailwind CSS + shadcn/ui
- **Backend:** FastAPI (Python)
- **Datenbank:** MongoDB
- **KI:** Claude via Emergent LLM Key
- **Zahlungen:** Stripe

### Deployment-Checkliste
- [ ] Backup erstellen
- [ ] Excel-Dateien lokal speichern
- [ ] Daten-Zahlen notieren
- [ ] Nach Deployment: Zahlen verifizieren
- [ ] Bei Abweichung: Restore durchführen

---

## 📊 TEIL 8: DATENBANK-COLLECTIONS

| Collection | Anzahl | Beschreibung | Wachstum |
|------------|--------|--------------|----------|
| `public_wines` | 7,078 | Öffentliche Weine | 📈 Dynamisch |
| `wine_database` | 494 | Erweiterte Wein-Infos | Statisch |
| `grape_varieties` | 313 | Rebsorten | Statisch |
| `regional_pairings` | 1,652 | Sommelier Kompass | Statisch |
| `blog_posts` | 233 | Blog-Artikel | Manuell |
| `feed_posts` | 268 | Community Feed | User-generiert |
| `dishes` | 40 | Gerichte für Pairing | Statisch |
| `seo_pairings` | 500 | SEO Pairings | Statisch |
| `users` | ~20 | Benutzer | User-generiert |
| `wines` | ~40 | Persönliche Weinkeller | User-generiert |
| `coupons` | 100 | Gutscheine | Manuell |
| **GESAMT** | **~10,900** | | |

---

## 📥 DOWNLOAD-LINKS

### Excel-Format
- Weine: `/api/export/excel/public_wines`
- Rebsorten: `/api/export/excel/grape_varieties`
- Sommelier Kompass: `/api/export/excel/regional_pairings`
- Blog: `/api/export/excel/blog_posts`
- Feed: `/api/export/excel/feed_posts`

### JSON-Format
- Alle: `/api/backup/download/{collection}.json`

---

*Dokumentation erstellt: 17.12.2025*  
*Letzte Aktualisierung: 17.12.2025*

### Version 1.8.2 (28.12.2025) - Wine Save Bug Fix

**🐛 Critical Bug Fix - Wine Save auf iOS Safari:**
- ✅ **Problem gelöst:** "Ein Fehler ist aufgetreten" beim Speichern nach Scan
- ✅ **Root Cause:** `authAxios` Interceptor funktionierte nicht zuverlässig auf iOS Safari
- ✅ **Lösung:** Native `fetch` API für alle Weinkeller-Operationen
- ✅ **Verbesserte Fehlerbehandlung:** Spezifische Fehlermeldungen statt generischer Fehler
- ✅ **Entfernte Abhängigkeit:** Axios aus CellarPage.js entfernt

**Geänderte Funktionen in CellarPage.js:**
- `handleAddWine()` - Wein hinzufügen
- `fetchWines()` - Weine laden
- `handleQuickQuantityChange()` - Menge ändern
- `handleToggleFavorite()` - Favorit umschalten
- `handleDeleteWine()` - Wein löschen
- `handleUpdateWine()` - Wein bearbeiten

**Technische Details:**
```
Vorher: authAxios.post(`${API}/wines`, data)
Nachher: fetch(`${API}/wines`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('wine_auth_token')}`
  },
  body: JSON.stringify(data)
})
```

### Version 1.8.3 (28.12.2025) - Gutschein-Funktion verbessert

**🎁 Gutschein-Banner auf der Pricing-Seite:**
- ✅ **Prominenter Gutschein-Banner** direkt unter den Pricing-Karten
- ✅ **Auffälliges Design:** Amber/Orange Gradient mit gestricheltem Rahmen
- ✅ **Geschenk-Icon:** Visueller Hinweis auf Gutschein-Option
- ✅ **Ein-Klick-Eingabe:** Button öffnet Eingabefeld direkt auf der Seite
- ✅ **Keine separate Seite nötig:** Gutschein kann direkt auf /pricing eingelöst werden
- ✅ **Mehrsprachig:** DE/EN/FR unterstützt
- ✅ **Erfolgsmeldung:** Zeigt Gültigkeitsdatum nach Einlösung

**Technische Details:**
- Gutschein-Eingabe via `fetch` API (iOS Safari kompatibel)
- Token-basierte Authentifizierung
- Inline-Feedback für Erfolg/Fehler
- Automatisches Refresh des User-Status nach Einlösung

**Neue Texte (DE):**
- "🎁 Gutschein-Code?"
- "Löse deinen Early Adopter Code ein und erhalte 1 Jahr Pro kostenlos!"
- "Gutschein einlösen" / "Einlösen"

**Gutschein-Statistik:**
- 99 unbenutzte Early Adopter Codes verfügbar
- Format: WINE-XXXX-XXXX-XXXX
- Wert: 1 Jahr Pro-Zugang (€39.99)

### Version 1.8.4 (29.12.2025) - FAQ Einwandbehandlung

**🛡️ Neue FAQ-Sektion "Deine Sicherheit am Tisch":**

5 strategisch formulierte Fragen zur Einwandbehandlung:

| # | Frage | Zweck |
|---|-------|-------|
| 1 | Woher weiß die KI, was in der Flasche ist? | Transparenz durch Technik-Erklärung |
| 2 | Was ist, wenn mein Geschmack anders ist? | Kontrolle zurückgeben |
| 3 | Ist der Scanner bei schlechtem Licht zuverlässig? | Technische Bedenken entkräften |
| 4 | Empfiehlt die App nur teure Weine? | Neutralität betonen |
| 5 | Kann ich meinen Weinkeller einfach verwalten? | Nutzwert demonstrieren |

**Design-Verbesserungen:**
- ✅ Nummerierte Fragen mit primärfarbenen Kreisen
- ✅ Hover-Effekt mit Schatten und Rahmen-Akzent
- ✅ Trust-Badge: "Transparent • Neutral • Datenschutz-konform"
- ✅ Gradient-Hintergrund für visuelle Hierarchie

**Mehrsprachig:** DE/EN/FR

**Psychologische Wirkung:**
- Transparenz schafft Vertrauen in die Logik
- Kontrolle über Budget und Geschmack entlastet
- Zeit- und Geldersparnis als Hauptnutzen

---

## Navigation Redesign (v1.8.7 - 30.12.2025)

### Haupt-Navigation
Die Navigation wurde für bessere Benutzerfreundlichkeit komplett überarbeitet:

**Direkt sichtbare Items:**
1. ☰ Burger-Menü
2. 🏠 Home
3. 🍽️ Pairing
4. 🍷 Keller
5. 👥 Community
6. 👤 Profil (nur Pro)
7. 🤖 Claude AI

**Im Burger-Menü:**
- Sommelier-Kompass
- Rebsorten
- Wein-Datenbank
- Favoriten
- Blog

### Design-Entscheidungen
- **6 Kern-Items** für schnellen Zugriff
- **Burger-Menü** für sekundäre Funktionen
- **Profil** nur für Pro-User sichtbar
- **Animiertes Overlay** beim Öffnen des Menüs


---

### Version 1.8.8 (02.01.2026) - AI Wine Enrichment

**🍷 Neues Pro-Feature: AI Wine Enrichment:**
- ✅ **Automatische Wein-Anreicherung:** Klick auf "Anreichern" Button generiert detaillierte Wein-Profile
- ✅ **Emotionale Beschreibungen:** Poetischer Stil wie "Ein Pinot Noir wie ein Bergabend in Südtirol..."
- ✅ **Vollständige Wein-Fakten:** Rebsorten, Geschmacksprofil, Appellation, Trinkreife, Speiseempfehlungen
- ✅ **Hybrid-Caching:** Bereits bekannte Weine werden aus Datenbank geladen (kosteneffizient)
- ✅ **Pro-Only:** Nur für Pro-Benutzer verfügbar (1000 Anreicherungen/Monat)

**UI-Elemente:**
- Amber Button (✨): Nicht-angereicherte Weine
- Grüner Button (🍷): Angereicherte Weine mit Detail-Modal

**Technische Details:**
- Backend: `POST /api/wines/{wine_id}/enrich`
- AI-Modell: GPT-5.1 via emergentintegrations
- Cache-Collection: `wine_knowledge`


---

### Version 1.8.9 (03.01.2026) - Weinfarben & Suche Optimierung

**🎨 Weinfarben-Zuordnung korrigiert:**
- ✅ Statistik zeigt jetzt korrekte Zahlen (17x Rot, 4x Weiß statt 6x Rot, 1x Rosé)
- ✅ `normalizeWineType()` Funktion normalisiert alle Schreibweisen (rot/Rot/ROT, weiss/weiß/blanc)
- ✅ Filter funktioniert jetzt für alle Varianten

**🔍 Volltext-Suche optimiert:**
- ✅ Suche durchsucht jetzt: name, winery, region, grape_variety, **appellation**, **country**, **description**
- ✅ "Sauternes" findet jetzt Château d'Yquem
- ✅ "Margaux", "Italien", "Champagne" funktionieren alle

**🔐 Wein-Hinzufügen Auth-Fix:**
- ✅ Bearer Token Authentifizierung statt Cookie-Auth
- ✅ Weine aus Datenbank können jetzt zum Keller hinzugefügt werden

**💬 Verbesserte Fehlermeldungen:**
- ✅ Spezifische Meldungen mit Titel und Beschreibung
- ✅ "Nicht angemeldet" / "Sitzung abgelaufen" / "Pro-Funktion" / Backend-Details
- ✅ 5 Sekunden sichtbar für bessere Lesbarkeit

---

## API-Referenz (Wichtige Endpoints)

### Authentifizierung
| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/auth/login` | POST | Login mit Email/Passwort |
| `/api/auth/register` | POST | Neuen Account erstellen |
| `/api/auth/me` | GET | Aktueller Benutzer |
| `/api/auth/forgot-password` | POST | Passwort zurücksetzen (Resend) |

### Weinkeller
| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/wines` | GET | Alle Weine des Users |
| `/api/wines` | POST | Neuen Wein hinzufügen |
| `/api/wines/{id}` | PUT | Wein aktualisieren |
| `/api/wines/{id}` | DELETE | Wein löschen |
| `/api/wines/{id}/enrich` | POST | Wein mit AI anreichern (Pro) |

### Wein-Datenbank (öffentlich)
| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/public-wines` | GET | Öffentliche Wein-Datenbank durchsuchen |
| `/api/public-wines-filters` | GET | Verfügbare Filter-Optionen |
| `/api/wine-knowledge` | GET | AI-angereicherte Weine |

### Pairing & Chat
| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/pairing` | POST | Wein-Pairing zu einem Gericht |
| `/api/chat` | POST | Chat mit Claude |

### Profil
| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/profile/wine` | GET/PUT | Persönliches Weinprofil (Pro) |

---

## Datenbank-Collections

| Collection | Beschreibung |
|------------|--------------|
| `users` | Benutzerkonten mit Plan und Usage |
| `wines` | Persönliche Weinkeller der Benutzer |
| `public_wines` | Öffentliche Wein-Datenbank (7175 Weine) |
| `wine_knowledge` | AI-angereicherte Wein-Profile |
| `wine_profiles` | Persönliche Geschmacksprofile |
| `pairings` | Gecachte Pairing-Ergebnisse |
| `chats` | Chat-Verläufe |
| `coupons` | Gutschein-Codes |
| `feed_posts` | Community-Beiträge |
| `blog_posts` | Blog-Artikel |

---

## Bekannte Einschränkungen

1. **Passwort-Reset (Resend):** Wartet auf DNS-Konfiguration (SPF/DKIM bei Infomaniak)
2. **Admin-Endpoint:** `/api/admin/reset-owner-password` sollte in Produktion deaktiviert werden
3. **Basic-User Limits:** Max. 10 Weine im Keller, 5 Pairings/Tag, 10 Chat-Nachrichten/Tag

