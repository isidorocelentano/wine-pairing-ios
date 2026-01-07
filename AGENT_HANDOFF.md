# 🍷 WINE PAIRING APP - Agent Handoff

**Letzte Aktualisierung: 07.01.2026 12:18 UTC* 28.12.2025 23:36 UTC  
**Version:** 1.8.3

---

## 📊 Aktueller Status

| Komponente | Status |
|------------|--------|
| Backend | ✅ Läuft |
| Frontend | ✅ Läuft |
| Datenbank | ✅ Verbunden |
| Gutschein-System | ✅ 99 Codes verfügbar |

---

## 🆕 Letzte Änderungen (28.12.2025)

### v1.8.3 - Gutschein-Funktion verbessert
- 🎁 Prominenter Gutschein-Banner auf `/pricing`
- Direkte Einlösung ohne separate Seite
- Mehrsprachig (DE/EN/FR)

### v1.8.2 - Wine Save Bug Fix
- 🐛 iOS Safari Speicher-Bug behoben
- Native fetch statt axios
- Bessere Fehlerbehandlung

---

## 📁 Wichtige Dateien

| Datei | Beschreibung |
|-------|--------------|
| `/app/frontend/src/pages/PricingPage.js` | Pricing mit Gutschein-Banner |
| `/app/frontend/src/pages/CellarPage.js` | Weinkeller (iOS Fix) |
| `/app/frontend/src/pages/CouponPage.js` | Separate Gutschein-Seite |
| `/app/docs/APP_DOKUMENTATION_KOMPLETT.md` | Hauptdokumentation |
| `/app/docs/CHANGELOG_v1.8.md` | Änderungshistorie |

---

## 🔗 URLs

| Umgebung | URL |
|----------|-----|
| **Live** | https://wine-pairing.online |
| **Preview** | https://winetrak.preview.emergentagent.com |
| **Pricing** | /pricing |
| **Gutschein** | /coupon |

---

## ⏳ Offene Aufgaben

### Priorität 1 (Anstehend)
- [ ] "Tipp der Woche" Archiv-Funktion

### Priorität 2 (Zukünftig)
- [ ] "Schon probiert?" Social-Proof-Sektion
- [ ] PayPal-Integration

### Blockiert
- [ ] Passwort-Reset (DNS-Einträge für Resend fehlen)

---

## 🔐 Test-Zugangsdaten

| Umgebung | Email | Passwort |
|----------|-------|----------|
| Preview | isicel@bluewin.ch | WeinAdmin2025! |
| Live | isicel@bluewin.ch | WeinPairing2025! |

---

## 📦 Backups

| Version | Pfad |
|---------|------|
| v1.8.3 | `/app/backups/v1.8.3_gutschein_feature_20251228_233551/` |
| v1.8.2 | `/app/backups/v1.8.2_before_fix_20251228_180131/` |

---

## 🗣️ Benutzer-Sprache

Der Benutzer kommuniziert auf **DEUTSCH**. Alle Antworten auf Deutsch!

---

*Letzte Aktualisierung: 07.01.2026 12:18 UTC*
