# Backup Manifest v1.8.3

## Backup Datum
$(date '+%Y-%m-%d %H:%M:%S UTC')

## Enthaltene Änderungen

### v1.8.2 - Wine Save Bug Fix
- CellarPage.js: Alle authAxios Aufrufe durch native fetch ersetzt
- iOS Safari Kompatibilität verbessert
- Bessere Fehlerbehandlung

### v1.8.3 - Gutschein-Funktion verbessert
- PricingPage.js: Prominenter Gutschein-Banner hinzugefügt
- Direkte Gutschein-Einlösung auf der Pricing-Seite
- Mehrsprachig (DE/EN/FR)

## Dateien
- server.py - Backend
- CellarPage.js - Weinkeller (Bug Fix)
- PricingPage.js - Pricing mit Gutschein-Banner
- CouponPage.js - Separate Gutschein-Seite
- AuthContext.js - Authentifizierung
- APP_DOKUMENTATION_KOMPLETT.md - Dokumentation
- frontend.env / backend.env - Umgebungsvariablen

## Wiederherstellung
Um diese Version wiederherzustellen:
1. Dateien aus diesem Ordner in die entsprechenden Verzeichnisse kopieren
2. Frontend neu starten: sudo supervisorctl restart frontend
3. Backend neu starten: sudo supervisorctl restart backend
