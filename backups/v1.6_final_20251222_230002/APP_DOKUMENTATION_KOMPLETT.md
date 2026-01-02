# 📖 WINE PAIRING APP - Vollständige Dokumentation

**Stand:** 22. Dezember 2025  
**Version:** 1.6 (Restaurant-Modus & Style-First)  
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

### 1b. PRICING-SEITE (NEU)
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

**Funktionsweise:**
1. User gibt Gericht ein
2. KI empfiehlt passende Weine
3. **Dynamisches DB-Wachstum:** Neue Weine werden automatisch zur Datenbank hinzugefügt

**"Aus meinem Weinkeller" Option:**
- KI empfiehlt NUR Weine aus dem persönlichen Weinkeller
- Perfekt für: "Was trinke ich heute zu meinem Abendessen?"

**Filter:**
- Weintyp (Rot/Weiss/Rosé/Schaumwein)
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
- **Etiketten-Scan** (KI erkennt Wein aus Foto)
- Bearbeiten & Löschen
- Mengenverwaltung (+/-)
- Favoriten markieren
- Filter nach Typ & Verfügbarkeit
- Statistik-Dashboard

**Technisch:**
- `user_id` Verknüpfung pro Wein
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
- **Rebsorte, Weinfarbe, Preiskategorie**

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
- **Preview:** https://cellarmate-2.preview.emergentagent.com
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
