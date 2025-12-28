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
