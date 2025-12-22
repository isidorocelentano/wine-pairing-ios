# 🤖 AGENT HANDOFF - WINE PAIRING APP

**WICHTIG: Diese Datei MUSS bei jedem Fork/Deployment gelesen werden!**

---

## 📊 AKTUELLER STAND (18.12.2025)

### Datenbank-Statistik:
| Collection | Anzahl | Beschreibung |
|------------|--------|--------------|
| `public_wines` | 7,078 | Öffentliche Wein-Datenbank (wächst dynamisch) |
| `wine_database` | 494 | Erweiterte Wein-Infos |
| `grape_varieties` | 313 | Rebsorten-Lexikon |
| `regional_pairings` | 1,779 | Sommelier Kompass |
| `blog_posts` | 233 | Blog-Artikel |
| `feed_posts` | 268 | Community-Beiträge |
| `dishes` | 40 | Gerichte für Pairing |
| `seo_pairings` | 500 | SEO-optimierte Pairings |
| `users` | ~20 | Benutzerkonten |
| `wines` | ~42 | Persönliche Weinkeller (user_id!) |
| `coupons` | 100 | Gutscheine |
| **GESAMT** | **~10,870** | |

---

## ⚠️ KRITISCHE INFORMATIONEN

### 1. MULTI-USER WEINKELLER
- Jeder User hat seinen **eigenen privaten Weinkeller**
- Alle `wines` haben ein `user_id` Feld
- NIEMALS Weine ohne `user_id` Query abrufen/ändern!
- Datenbank-Index auf `user_id` für Performance

### 2. BACKUP-SYSTEM
- Automatische Backups alle 6 Stunden
- Auto-Restore bei leerem Server aus `/app/backend/data/*.json`
- Verifiziertes Backup-Skript: `python3 /app/backend/scripts/create_verified_backup.py`

### 3. DYNAMISCHES WEIN-WACHSTUM
- Bei Pairing-Empfehlungen werden neue Weine automatisch zur DB hinzugefügt
- Die Wein-Datenbank wächst organisch durch KI-Empfehlungen

### 4. FREEMIUM-SYSTEM
- Basic: 5 Pairings/Tag, 5 Chats/Tag, 10 Weine im Keller
- Pro: Unbegrenzt (4,99€/Monat oder 39,99€/Jahr)
- Stripe integriert

---

## 📁 WICHTIGE DATEIEN

### Dokumentation:
- `/app/docs/APP_DOKUMENTATION_KOMPLETT.md` - Vollständige Feature-Dokumentation
- `/app/docs/BACKUP_UND_WIEDERHERSTELLUNG.md` - Backup-Anleitung
- `/app/docs/DATENVERLUST_PRAEVENTION.md` - Strategie gegen Datenverlust
- `/app/docs/MULTI_USER_WEINKELLER.md` - Multi-User Implementation

### Backend:
- `/app/backend/server.py` - Haupt-Server (FastAPI)
- `/app/backend/backup_manager.py` - Backup-System
- `/app/backend/scripts/create_verified_backup.py` - Manuelles Backup

### Daten:
- `/app/backend/data/*.json` - Backup-Dateien (für Auto-Restore)
- `/app/backend/data/backups/` - Automatische Backups

---

## 🔗 DOWNLOAD-ENDPOINTS

### Dokumentation:
- Word: `/api/docs/download-word`
- Excel: `/api/docs/download`
- Markdown: `/api/docs/download-md`

### Datenbank-Export:
- Excel: `/api/export/excel/{collection_name}`
- JSON: `/api/backup/download/{collection_name}.json`
- Alle Links: `/api/export/excel-links`

---

## 🚨 VOR JEDEM DEPLOYMENT

1. ✅ Backup erstellen: `POST /api/backup/create`
2. ✅ Zahlen notieren (siehe oben)
3. ✅ Excel-Exports herunterladen
4. ✅ Nach Deployment: Zahlen verifizieren
5. ✅ Bei Abweichung: SOFORT Restore!

---

## 📞 BENUTZER-SPRACHE

Der Benutzer kommuniziert auf **DEUTSCH**. Alle Antworten auf Deutsch!

---

## 🔧 TECH-STACK

- Frontend: React + Tailwind CSS + shadcn/ui
- Backend: FastAPI (Python)
- Datenbank: MongoDB
- KI: Claude via Emergent LLM Key
- Zahlungen: Stripe
- Mehrsprachig: DE, EN, FR

---

## ❌ HÄUFIGE FEHLER VERMEIDEN

1. **NIEMALS** Wine-Endpoints ohne `user_id` Query
2. **NIEMALS** Daten überschreiben ohne Backup
3. **NIEMALS** `public_wines` Collection leeren
4. **IMMER** Backup vor größeren Änderungen
5. **IMMER** Nach Import/Merge Zahlen verifizieren

---

## 📈 LETZTE ÄNDERUNGEN

### 18.12.2025 (China & Griechenland Sommelier Kompass Import):

#### 🇬🇷 Griechenland Sommelier Kompass:
- **46 griechische Gerichte** mit vollständigen Weinempfehlungen importiert
- Regionen: Überall (Klassiker), Peloponnes, Attika, Kreta, Nordgriechenland, Santorin, Küstenregionen
- Griechische Weine: Xinomavro, Assyrtiko, Agiorgitiko, Moschofilero, Malagousia, etc.
- **Total Griechenland Gerichte jetzt: 51**
- Skript: `/app/backend/scripts/import_greece_complete.py`

### 18.12.2025 (China Sommelier Kompass Import):

#### 🇨🇳 China Sommelier Kompass:
- **50 chinesische Gerichte** mit vollständigen Weinempfehlungen importiert
- Regionen: Nordchina (Peking, Shandong), Ostchina (Shanghai), Südchina (Guangdong, Fujian), Westchina (Sichuan, Hunan, Yunnan), International
- **Vollständige Übersetzungen** für alle Gerichte und Weinbeschreibungen (DE, EN, FR)
- Emotionale Weinbeschreibungen erklärt WARUM jedes Pairing funktioniert
- **Total China Gerichte jetzt: 88**
- Skript: `/app/backend/scripts/import_china_complete.py`

### 18.12.2025 (Große Datenbereinigung):

#### 🔧 Filter-System verbessert:
- **Region/Appellation Trennung**: Regionen und Appellationen werden jetzt sauber getrennt in separaten Dropdowns angezeigt
- Code-Änderung in `/app/backend/server.py` (Zeilen 3797-3810):
  - Länder mit sauberen Regionen: Frankreich, Deutschland, Österreich, Schweiz, Spanien, Italien
  - Diese zeigen NUR echte Regionen im Region-Dropdown
  - Appellationen werden separat im Appellation-Dropdown angezeigt
- **Appellation-Filter korrigiert**: Verwendet jetzt korrekten MongoDB `$regex` Operator

#### 🇫🇷 Frankreich (1.861 Weine):
- 74 Non-Breaking Spaces (NBSP) korrigiert
- Alle Duplikate entfernt (Saint-Emilion → Saint-Émilion, etc.)
- **10 saubere Regionen**: Bordeaux, Burgund, Champagne, Rhône, Elsass, Loire, Beaujolais, Provence, Languedoc-Roussillon, Südwest-Frankreich
- **107 Appellationen** (z.B. Bordeaux → 33 Appellationen wie Pauillac, Saint-Émilion, Margaux)
- Script: `/app/backend/scripts/cleanup_french_wines.py`

#### 🇮🇹 Italien (1.551 Weine):
- 459 Weine korrigiert
- Regionen vereinheitlicht: Piemonte → Piemont, Toscana → Toskana, Venetien → Veneto
- Appellationen als Region korrigiert (Barolo, Barbaresco → Region Piemont)
- **17 saubere Regionen**: Piemont, Toskana, Veneto, Campania, Lombardia, etc.
- **70 Appellationen** (z.B. Piemont → Barolo, Barbaresco, Barbera)

#### 🇪🇸 Spanien (1.209 Weine):
- penedes → Penedès, Rias Baixas → Rías Baixas
- **24 Regionen**, 0 ohne Region

#### 🇩🇪 Deutschland (678 Weine):
- Sub-Regionen vereinfacht (Pfalz - Deidesheim → Pfalz)
- 108 Weine korrigiert
- **14 Hauptregionen**: Franken, Rheingau, Mosel, Pfalz, Nahe, etc.

#### 🇦🇹 Österreich (678 Weine):
- Duplikate vereinfacht
- **17 Regionen**: Wachau, Kamptal, Weinviertel, Kremstal, etc.

#### 🇦🇺 Australien:
- LANGHORNE CREEK → Langhorne Creek

#### 🔧 Pydantic-Model Standardisierung:
- **Migration durchgeführt:**
  - `grape` → `grape_variety` (4.311 Weine migriert)
  - `color` → `wine_color` (4.553 Weine migriert)
- **Alte Felder entfernt** aus der Datenbank
- **Pydantic-Model vereinfacht** in `/app/backend/server.py`:
  - `model_validator` hinzugefügt für Rückwärtskompatibilität
  - Alte Feld-Definitionen entfernt
- **Ergebnis:** 
  - `grape_variety`: 6.219 Weine
  - `wine_color`: 6.461 Weine
  - Keine alten Felder mehr vorhanden

#### 📱 Community Feed - Social Sharing:
- **Neue Share-Funktion** in `/app/frontend/src/pages/FeedPage.js`:
  - Facebook Share Button (öffnet Facebook Sharer)
  - Instagram Share Button (kopiert Text und öffnet Instagram)
  - Link kopieren Button
- **Features:**
  - Share-Dropdown-Menü bei jedem Post
  - Automatisch formatierter Share-Text mit Wein, Gericht, Bewertung und Hashtags
  - Mehrsprachig (DE/EN/FR)
  - Mobile-optimiert (öffnet native Apps auf Mobilgeräten)

#### 🇺🇸 USA Sommelier Kompass:
- **45 USA-Gerichte** mit vollständigen Weinempfehlungen hinzugefügt
- Kategorien: Fast Food, BBQ, Meeresfrüchte, Cajun, Desserts, Regionales
- **Vollständige Übersetzungen** für alle Weinbeschreibungen:
  - 🇩🇪 Deutsch (Originaltext)
  - 🇬🇧 Englisch (wine_description_en)
  - 🇫🇷 Französisch (wine_description_fr)
- Jedes Gericht enthält: wine_name, wine_type, wine_description in 3 Sprachen

### 17.12.2025:
- Smart Merge: 7,066 Weine importiert (aus Weindatenbank.xlsx)
- Smart Merge: 313 Rebsorten importiert (aus REBSORTEN_PRODUKTION.csv)
- Multi-User Weinkeller implementiert (user_id Isolation)
- Excel/Word/MD Export-Endpoints erstellt
- Vollständige App-Dokumentation erstellt

### 17.12.2025 (Abend):
- **Pairing-Seite UX verbessert:**
  - Zurück-Button: Wein-Details inline anzeigen statt wegnavigieren
  - Auto-Add: Neue Weine werden automatisch zur DB hinzugefügt
  - Upgrade-Prompt: Bei Limit-Erreichen schöne Upgrade-Karte statt Fehler
- **Weindatenbank Filter gefixt:**
  - Filter sucht jetzt in region, appellation UND anbaugebiet
  - Barbaresco und andere Appellationen werden gefunden
  - Tippfehler "Barabaresco" korrigiert
- **Zum Weinkeller hinzufügen gefixt:**
  - Auth-Credentials werden jetzt mitgesendet
  - Zurück-Button im Wein-Detail-Dialog hinzugefügt

---

*Letzte Aktualisierung: 22.12.2025 21:43 UTC*
