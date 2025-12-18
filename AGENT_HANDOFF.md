# 🤖 AGENT HANDOFF - WINE PAIRING APP

**WICHTIG: Diese Datei MUSS bei jedem Fork/Deployment gelesen werden!**

---

## 📊 AKTUELLER STAND (17.12.2025)

### Datenbank-Statistik:
| Collection | Anzahl | Beschreibung |
|------------|--------|--------------|
| `public_wines` | 7,078 | Öffentliche Wein-Datenbank (wächst dynamisch) |
| `wine_database` | 494 | Erweiterte Wein-Infos |
| `grape_varieties` | 313 | Rebsorten-Lexikon |
| `regional_pairings` | 1,652 | Sommelier Kompass |
| `blog_posts` | 233 | Blog-Artikel |
| `feed_posts` | 268 | Community-Beiträge |
| `dishes` | 40 | Gerichte für Pairing |
| `seo_pairings` | 500 | SEO-optimierte Pairings |
| `users` | ~20 | Benutzerkonten |
| `wines` | ~42 | Persönliche Weinkeller (user_id!) |
| `coupons` | 100 | Gutscheine |
| **GESAMT** | **~10,740** | |

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

*Letzte Aktualisierung: 18.12.2025 05:21 UTC*
