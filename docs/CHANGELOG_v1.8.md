# Changelog - Wine Pairing App

## Version 1.8.3 (28.12.2025) - Gutschein-Funktion verbessert

### 🎁 Neue Features
- **Prominenter Gutschein-Banner** auf der Pricing-Seite (`/pricing`)
  - Auffälliges Amber/Orange Design mit gestricheltem Rahmen
  - Geschenk-Icon (🎁) für visuelle Wiedererkennung
  - Ein-Klick-Eingabe: Button öffnet Eingabefeld direkt auf der Seite
  - Keine separate Seite mehr nötig für Gutschein-Einlösung
  - Mehrsprachig: Deutsch, Englisch, Französisch
  - Erfolgsmeldung mit Gültigkeitsdatum nach Einlösung
  - Erkennt bereits vorhandenen Pro-Status

### Technische Details
- Gutschein-Eingabe via native `fetch` API (iOS Safari kompatibel)
- Token-basierte Authentifizierung
- Inline-Feedback für Erfolg/Fehler
- Automatisches Refresh des User-Status nach Einlösung

### Geänderte Dateien
- `frontend/src/pages/PricingPage.js`

---

## Version 1.8.2 (28.12.2025) - Wine Save Bug Fix

### 🐛 Bug Fixes
- **Kritischer Fix:** "Ein Fehler ist aufgetreten" beim Speichern von Weinen nach Scan
- **Root Cause:** `authAxios` Interceptor funktionierte nicht zuverlässig auf iOS Safari
- **Lösung:** Native `fetch` API für alle Weinkeller-Operationen

### Geänderte Funktionen in CellarPage.js
- `handleAddWine()` - Wein hinzufügen
- `fetchWines()` - Weine laden
- `handleQuickQuantityChange()` - Menge ändern (+/-)
- `handleToggleFavorite()` - Favorit umschalten
- `handleDeleteWine()` - Wein löschen
- `handleUpdateWine()` - Wein bearbeiten

### Technische Details
```javascript
// Vorher (problematisch auf iOS Safari):
await authAxios.post(`${API}/wines`, data);

// Nachher (iOS Safari kompatibel):
const token = localStorage.getItem('wine_auth_token');
await fetch(`${API}/wines`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify(data)
});
```

### Geänderte Dateien
- `frontend/src/pages/CellarPage.js`

---

## Version 1.8.1 (27.12.2025) - Restaurant-Modus UI & UX-Verbesserungen

### 🍽️ Restaurant-Modus verbessert
- Neuer Einleitungstext für bessere Benutzerführung
- Hervorgehobenes Design mit Gradient-Box
- Größeres Eingabefeld (100px Höhe)
- Weißer Hintergrund für besseren Kontrast
- Verbesserte Bestätigungsmeldung

### 💡 "Weniger geeignet" Sektion verbessert
- Freundlicherer Titel: "Eher weniger geeignet" statt "Vermeide"
- Sanftere Farben: Amber statt Rot
- Glühbirne-Emoji (💡) statt Warnung (⚠️)
- Neutralisierungs-Tipp für besseren Genuss

---

## Version 1.8.0 (27.12.2025) - Scan-Fix & SEO-Optimierung

### 📱 Etiketten-Scan Fix für iOS Safari
- Problem gelöst: iOS Safari blockierte große Bild-Uploads still
- Bildkomprimierung implementiert: Max 800x800 Pixel, 50% JPEG Qualität
- Vereinfachter Code ohne komplexe async-Funktionen
- Sofortige Bild-Anzeige vor API-Call
- Verbesserte Fehlerbehandlung mit Toast-Nachrichten

### 🔍 SEO-Optimierung
- Neuer Title: "Wein-Pairing leicht gemacht – Genuss ohne Regeln"
- Neue Meta-Description für bessere CTR
- Erweiterte Keywords für KI-Suchmaschinen (Perplexity, ChatGPT Search)
- FAQ- und HowTo-Schema für Rich Snippets

### 🔐 Auth-Verbesserungen
- Google Login Fix: refreshAuth() nach OAuth-Callback
- Besseres Token-Handling mit localStorage

---

## Backup-Verzeichnisse

| Version | Datum | Pfad |
|---------|-------|------|
| v1.8.3 | 28.12.2025 | `/app/backups/v1.8.3_gutschein_feature_*` |
| v1.8.2 | 28.12.2025 | `/app/backups/v1.8.2_before_fix_*` |
| v1.8.1 | 27.12.2025 | `/app/backups/v1.8.1_restaurant_ui_*` |

---

## Gutschein-System

### Statistik
- **99 unbenutzte** Early Adopter Codes verfügbar
- Format: `WINE-XXXX-XXXX-XXXX`
- Wert: 1 Jahr Pro-Zugang (€39.99)

### Einlösung
- **Pricing-Seite:** `/pricing` (empfohlen - neuer Banner)
- **Separate Seite:** `/coupon`
- **Subscription-Seite:** `/subscription`

### API
- **Endpoint:** `POST /api/coupon/redeem`
- **Body:** `{"code": "WINE-XXXX-XXXX-XXXX"}`
- **Auth:** Bearer Token erforderlich

---

## Version 1.8.4 (29.12.2025) - FAQ Einwandbehandlung

### 🛡️ Neue Features
- **FAQ-Sektion komplett überarbeitet** für bessere Einwandbehandlung
- Titel geändert zu "Deine Sicherheit am Tisch"
- 5 strategische Fragen mit überzeugenden Antworten
- Trust-Badge am Ende der FAQ-Sektion

### Design-Verbesserungen
- Nummerierte Fragen mit primärfarbenen Kreisen
- Hover-Effekt mit Schatten
- Linker Rand-Akzent (border-left)
- Gradient-Hintergrund
- Mehr Whitespace für bessere Lesbarkeit

### Geänderte Dateien
- `frontend/src/pages/PricingPage.js`

---

## Version 1.8.5 (29.12.2025) - Personalisiertes Weinprofil

### 🍷 Neues Pro-Feature: Weinprofil

Personalisierte Weinempfehlungen basierend auf individuellem Geschmacksprofil.

### Profil-Kategorien

| Kategorie | Optionen |
|-----------|----------|
| **Rotwein-Stilistik** | Kräftig & Würzig, Fruchtig & Elegant, Beides |
| **Weißwein-Charakter** | Mineralisch, Cremig, Aromatisch, Alle |
| **Säure-Toleranz** | Niedrig, Mittel, Hoch |
| **Tannin-Vorliebe** | Weich & Seidig, Mittel, Markant & Griffig |
| **Süßegrad** | Knochentrocken bis Edelsüß |
| **Lieblingsregionen** | 25+ Regionen wählbar |
| **Budget Alltag** | Unter 10€ bis Über 50€ |
| **Budget Restaurant** | Unter 30€ bis Über 120€ |
| **No-Gos** | Barrique, Schwefel, bestimmte Rebsorten, etc. |
| **Kulinarischer Kontext** | Vegetarisch, Vegan, Fleisch, Asiatisch, etc. |
| **Abenteuer-Faktor** | Klassiker, Ausgewogen, Abenteuerlich |

### API-Endpunkte

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| GET | `/api/profile/wine` | Profil laden |
| PUT | `/api/profile/wine` | Profil speichern |
| DELETE | `/api/profile/wine` | Profil zurücksetzen |

### Frontend-Routes

- `/profile` - Englische Route
- `/weinprofil` - Deutsche Route

### Integration in Pairing-Engine

Das Benutzerprofil wird automatisch in die AI-Empfehlungen integriert:
- Bevorzugte Weinstile werden berücksichtigt
- No-Gos werden ausgeschlossen
- Budget-Rahmen wird eingehalten
- Abenteuer-Level beeinflusst Empfehlungsvielfalt

### Geänderte Dateien

- `backend/server.py` - WineProfile Model + API
- `frontend/src/pages/WineProfilePage.js` - NEU
- `frontend/src/App.js` - Routes hinzugefügt

---

## Version 1.8.6 (30.12.2025) - Weinprofil UI-Fixes

### 🔧 Bug Fixes

**Speichern-Button nicht sichtbar:**
- Problem: Button wurde von der Navigation überdeckt
- Lösung: `bottom-20` statt `bottom-0` für mobile Geräte
- Padding am Seitenende erhöht (`pb-40`)

**API-URL Fix:**
- `API_URL` → `API` in WineProfilePage.js
- Korrekter Pfad: `/api/profile/wine`

### ✨ Neue Features

**Navigation:**
- "Profil" Icon in der Navigation (nur für Pro-User)
- Icon: UserCog

**Benutzer-Menü:**
- "Mein Weinprofil" Link hinzugefügt
- Dreisprachig: DE/EN/FR

### Geänderte Dateien
- `frontend/src/pages/WineProfilePage.js`
- `frontend/src/components/Navigation.js`
- `frontend/src/components/UserMenu.js`
- `frontend/src/contexts/LanguageContext.js`

### Übersetzungen hinzugefügt
- `nav_profile`: "Profil" / "Profile" / "Profil"

---

## Version 1.8.7 (30.12.2025) - Navigation Redesign

### 🎨 Navigation komplett überarbeitet

**Neue Haupt-Navigation (6-7 Items):**
| Position | Icon | Funktion |
|----------|------|----------|
| 1 | ☰ | Burger-Menü |
| 2 | 🏠 | Home |
| 3 | 🍽️ | Pairing |
| 4 | 🍷 | Keller |
| 5 | 👥 | Community |
| 6 | 👤 | Profil (nur Pro-User) |
| 7 | 🤖 | Claude |

**Burger-Menü enthält:**
| Icon | Funktion |
|------|----------|
| 🗺️ | Sommelier-Kompass |
| 🍇 | Rebsorten |
| 📊 | Wein-DB |
| ❤️ | Favoriten |
| 📖 | Blog |

### Technische Details
- Burger-Menü mit Overlay und Animation
- Responsive Design für Mobile und Desktop
- Pro-User sehen zusätzliches Profil-Icon
- Sekundäre Items im 3-Spalten-Grid

### Geänderte Dateien
- `frontend/src/components/Navigation.js` - Komplettes Redesign

### Vorteile
- Übersichtlichere Navigation (6 statt 11 Items)
- Wichtigste Funktionen direkt erreichbar
- Sekundäre Funktionen im Burger-Menü
- Bessere Mobile-UX


---

## Version 1.8.8 (02.01.2026) - AI Wine Enrichment Feature

### 🍷 Neues Pro-Feature: AI Wine Enrichment

Ein leistungsstarkes Feature, das automatisch detaillierte Wein-Profile aus einem einfachen Etiketten-Scan oder manuellen Eintrag generiert.

### Wie es funktioniert

1. **Benutzer klickt "Anreichern" Button** (✨ amber) auf einer Weinkarte
2. **AI (GPT-5.1) generiert** emotionale Beschreibung und Fakten
3. **Daten werden gecacht** in der `wine_knowledge` Collection
4. **Wein wird aktualisiert** mit allen angereicherten Informationen
5. **Grüner Button** (🍷) erscheint für angereicherte Weine

### Generierte Wein-Informationen

| Feld | Beschreibung | Beispiel |
|------|--------------|----------|
| **emotional_description** | Poetische 3-4 Sätze im "WINE.PAIRING" Stil | "Ein Pinot Noir wie ein Bergabend in Südtirol..." |
| **grape_varieties** | Liste der Rebsorten | ["Pinot Noir"] |
| **appellation** | Offizielle Bezeichnung/AOC/DOC | "Alto Adige DOC / Südtirol DOC" |
| **winery_info** | 2-3 Sätze zum Weingut | Geschichte, Philosophie |
| **taste_profile** | Strukturierte Geschmacksnotizen | body, aromas, tannins, acidity, finish |
| **drinking_window** | Optimales Trinkfenster | "2020-2028" |
| **food_pairings** | Passende Gerichte | ["Gegrilltes Hähnchen", "Pilzragout"] |
| **serving_temp** | Serviertemperatur | "14-16°C" |
| **price_category** | Preiskategorie | "Mittel (15-40€)" |

### API-Endpoint

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| POST | `/api/wines/{wine_id}/enrich` | Wein mit AI anreichern |
| GET | `/api/enrichment-stats` | Nutzungsstatistik |
| GET | `/api/wine-knowledge` | Gecachte Wein-Wissen |

### Technische Details

- **Hybrid-System:** Prüft zuerst `wine_knowledge` Cache, dann AI-Aufruf
- **Monatliches Limit:** 1000 Anreicherungen pro Monat
- **Pro-Only:** Nur für Pro-Benutzer verfügbar
- **AI-Modell:** OpenAI GPT-5.1 via emergentintegrations
- **Caching:** Reduziert Kosten durch Wiederverwendung von Wein-Wissen

### Frontend UI

- **Amber Button (✨):** Nicht-angereicherte Weine können angereichert werden
- **Grüner Button (🍷):** Angereicherte Weine zeigen Detail-Modal
- **Detail-Modal:** Zeigt alle angereicherten Informationen mit schönem Design

### Geänderte Dateien

- `backend/server.py` - Enrich-Endpoint korrigiert (LlmChat statt client.chat)
- `frontend/src/pages/CellarPage.js` - UI bereits vorhanden

### Bug Fix

- **Kritischer Fix:** `client.chat.completions.create` wurde zu `LlmChat` geändert
- Der ursprüngliche Code nutzte fälschlicherweise den MongoDB-Client statt OpenAI

---

## Version 1.8.8.1 (02.01.2026) - AI Wine Knowledge Database Search

### 🔍 Neues Feature: AI-angereicherte Weine durchsuchbar

Die Wein-Datenbank wurde um einen neuen Tab erweitert, der alle AI-angereicherten Weine durchsuchbar macht.

### Zugang

Navigieren Sie zu **Wein-Datenbank** > Tab **"✨ AI-Weine"**

### Funktionen

| Feature | Beschreibung |
|---------|--------------|
| **Tab-Navigation** | Wechseln Sie zwischen "Wein-Datenbank" (normal) und "AI-Weine" (angereichert) |
| **Live-Zähler** | Tab zeigt aktuelle Anzahl AI-angereicherter Weine: "AI-Weine (2)" |
| **Suche** | Durchsuchen nach Name, Region oder Rebsorte |
| **Wein-Karten** | Amber-farbene Karten mit AI-Profil Badge |
| **Detail-Modal** | Vollständiges AI-generiertes Profil inkl. emotionaler Beschreibung |

### UI-Elemente

- **Amber Gradient Karten**: Visuell abgehoben von normalen Weinen
- **✨ AI-Profil Badge**: Kennzeichnet angereicherte Weine
- **Quick Info Pills**: Serviertemperatur, Trinkreife, Preiskategorie
- **Emotionale Beschreibung**: In Anführungszeichen im Modal

### Technische Details

- **API**: `GET /api/wine-knowledge?search=&limit=50&skip=0`
- **Datei**: `frontend/src/pages/WineDatabasePage.js`
- **Komponenten**: Tabs aus shadcn/ui, neue Icons (Sparkles, Grape, Thermometer, Calendar)


---

## Version 1.8.9 (03.01.2026) - Weinfarben & Suche Optimierung

### 🎨 Weinfarben-Zuordnung korrigiert

**Problem:** Die Statistik im Weinkeller zeigte falsche Zahlen (z.B. "6x Rot, 1x Rosé" obwohl Weißweine vorhanden waren).

**Ursache:** Weinfarben wurden inkonsistent gespeichert:
- `rot`, `Rot`, `ROT` (verschiedene Schreibweisen)
- `weiss`, `weiß`, `Weiß`, `blanc` (verschiedene Schreibweisen)

**Lösung:**

1. **Frontend (CellarPage.js):** Neue `normalizeWineType()` Funktion
```javascript
const normalizeWineType = (type) => {
  if (!type) return 'other';
  const normalized = type.toLowerCase().trim();
  if (normalized === 'rot' || normalized === 'rotwein' || normalized === 'red') return 'rot';
  if (normalized === 'weiss' || normalized === 'weiß' || normalized === 'blanc') return 'weiss';
  if (normalized === 'rose' || normalized === 'rosé') return 'rose';
  // ... weitere Mappings
};
```

2. **Backend (server.py):** Filter verwendet `$in` Query mit allen Variationen
```python
type_variations = {
    'rot': ['rot', 'Rot', 'ROT', 'rotwein', 'red'],
    'weiss': ['weiss', 'weiß', 'Weiss', 'Weiß', 'blanc'],
    # ...
}
query["type"] = {"$in": type_variations[type_filter]}
```

**Ergebnis:**
- Vorher: "6x Rot, 1x Rosé" ❌
- Nachher: "17x Rot, 4x Weiß" ✅

### 🔍 Volltext-Suche optimiert

**Problem:** Suche nach "Sauternes" fand keine Ergebnisse.

**Ursache:** Suche durchsuchte nur: name, winery, region, grape_variety

**Lösung:** Erweiterte Suche in allen relevanten Feldern:
```python
query["$or"] = [
    {"name": regex},
    {"winery": regex},
    {"region": regex},
    {"grape_variety": regex},
    {"appellation": regex},      # NEU
    {"country": regex},          # NEU
    {"anbaugebiet": regex},      # NEU
    {"description_de": regex},   # NEU
    {"description_en": regex},   # NEU
]
```

**Ergebnis:**
- ✅ "sauternes" → findet Château d'Yquem
- ✅ "margaux" → findet Château Margaux
- ✅ "italien" → findet italienische Weine

### 🔐 Wein-Hinzufügen Auth-Fix

**Problem:** "Fehler beim Hinzufügen" beim Hinzufügen von Weinen aus der Wein-Datenbank.

**Ursache:** `withCredentials: true` (Cookie-Auth) statt Bearer Token

**Lösung:**
```javascript
// Vorher (falsch):
await axios.post(`${API}/wines`, data, { withCredentials: true });

// Nachher (korrekt):
const token = localStorage.getItem('wine_auth_token');
await axios.post(`${API}/wines`, data, {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

### 💬 Verbesserte Fehlermeldungen

**Problem:** Generische Fehlermeldung "Fehler beim Hinzufügen" ohne Details.

**Lösung:** Spezifische Fehlermeldungen mit Titel und Beschreibung:

| HTTP Status | Titel | Beschreibung |
|-------------|-------|--------------|
| Kein Token | **Nicht angemeldet** | Bitte melden Sie sich an, um Weine zu speichern. |
| 401 | **Sitzung abgelaufen** | Bitte melden Sie sich erneut an. |
| 403 | **Pro-Funktion** | Upgraden Sie auf Pro, um Weine zu speichern. |
| Backend-Detail | **Fehler** | [Detail vom Backend] |
| Sonstiger | **Fehler beim Hinzufügen** | Bitte versuchen Sie es später erneut. |

### Geänderte Dateien

| Datei | Änderung |
|-------|----------|
| `frontend/src/pages/CellarPage.js` | `normalizeWineType()`, `getWineTypeBadgeClass()`, `getWineTypeLabel()` |
| `frontend/src/pages/WineDatabasePage.js` | `addToCellar()` mit Bearer Token und verbesserten Fehlermeldungen |
| `backend/server.py` | Zeile ~1301: `type_filter` mit `$in` Query für alle Variationen |
| `backend/server.py` | Zeile ~4677: Erweiterte Volltext-Suche in allen Feldern |

---

## Übersicht aller v1.8.x Änderungen

| Version | Datum | Hauptänderung |
|---------|-------|---------------|
| 1.8.2 | 28.12.2025 | Wine Save Bug Fix (iOS Safari) |
| 1.8.3 | 28.12.2025 | Gutschein-Funktion verbessert |
| 1.8.4 | 29.12.2025 | FAQ-Sektion auf Pricing-Seite |
| 1.8.5 | 29.12.2025 | Personalisiertes Weinprofil (Pro) |
| 1.8.6 | 30.12.2025 | Navigation Redesign (Burger-Menü) |
| 1.8.7 | 30.12.2025 | Blog-Link in Navigation |
| 1.8.8 | 02.01.2026 | AI Wine Enrichment Feature |
| 1.8.8.1 | 02.01.2026 | AI Wine Knowledge Database Search |
| 1.8.9 | 03.01.2026 | Weinfarben, Suche, Auth-Fix, Fehlermeldungen |
| 1.8.10 | 03.01.2026 | Weinkeller-Suche, Bild-Upload, Detail-Ansicht |

---

## Version 1.8.10 (03.01.2026) - Weinkeller Erweiterungen

### 🔍 Volltext-Suche im Weinkeller

Neues Suchfeld direkt im Weinkeller für schnelles Finden von Weinen.

**Features:**
- Suchfeld mit Lupe-Icon oben im Filter-Bereich
- Sofortige Filterung während der Eingabe
- Durchsucht: Name, Region, Rebsorte, Beschreibung, Notizen, Appellation, Jahrgang
- X-Button zum schnellen Löschen
- Kombinierbar mit anderen Filtern (Weinfarbe, Preis, Auf Lager)
- "Keine Weine gefunden" mit Reset-Button

**Beispiel-Suchen:**
- "lageder" → findet Alois Lageder
- "champagne" → findet alle Champagner
- "2015" → findet Weine vom Jahrgang 2015

### 📸 Bild nachträglich hinzufügen/ändern

Im Edit-Dialog kann jetzt ein Bild hochgeladen oder geändert werden.

**Features:**
- Bild-Sektion ganz oben im Edit-Dialog
- Vorschau des aktuellen Bildes
- "Hinzufügen" / "Ändern" / "Entfernen" Buttons
- Automatische Komprimierung (max. 1200px, 70% JPEG)
- Toast zeigt komprimierte Größe

**Komprimierung:**
```javascript
// Max 1200px Breite/Höhe, 70% Qualität
const MAX_SIZE = 1200;
canvas.toDataURL('image/jpeg', 0.7);
// Ergebnis: ~90% Größenreduktion (3MB → 200KB)
```

### 🖼️ Wein-Detail-Ansicht mit Bild

Beim Klicken auf eine Weinkarte öffnet sich eine vollständige Detail-Ansicht.

**Layout:**
1. **Bild** (oben, h-48, schwarzer Hintergrund)
2. **Header** (Badges, Name, Jahrgang, Region)
3. **Info-Karten** (Rebsorte, Appellation mit Icons)
4. **Beschreibung** (amber-farbener Hintergrund, kursiv)
5. **Weitere Details** (Rebsorten, Speiseempfehlungen, Notizen)
6. **Action-Buttons** (Bearbeiten, Pairing - fixiert unten)

**UX-Verbesserungen:**
- Gesamte Weinkarte klickbar
- Hover-Effekt (Bild zoomt leicht)
- Scrollbarer Content
- Buttons immer sichtbar

### 🐛 Bug Fixes

**Bilder werden jetzt in Übersicht angezeigt:**
- Problem: `image_base64` wurde beim Laden ausgeschlossen
- Lösung: Projection geändert von `{"image_base64": 0}` zu `{}`

**Edit-Dialog Speichern-Button überdeckt:**
- Problem: Button von Navigation überdeckt
- Lösung: Flexbox-Layout mit fixiertem Footer

### Geänderte Dateien

| Datei | Änderung |
|-------|----------|
| `frontend/src/pages/CellarPage.js` | Suchfeld, Bild-Upload, Detail-Modal, Komprimierung |
| `backend/server.py` | `image_base64` in GET /wines Response |

### Neue State-Variablen (CellarPage.js)

```javascript
const [searchQuery, setSearchQuery] = useState('');
// + filteredWines mit useMemo für Performance
```

### Neue Funktionen (CellarPage.js)

```javascript
// Bild-Komprimierung
const compressImageSimple = (dataUrl) => { ... }

// Bild-Upload im Edit-Dialog
const handleEditImageUpload = async (e) => { ... }

// Gefilterte Weine
const filteredWines = useMemo(() => { ... }, [wines, searchQuery, filter, ...]);
```
