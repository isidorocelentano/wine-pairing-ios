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
