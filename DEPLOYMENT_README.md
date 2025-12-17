# 🚀 Wine-Pairing.online Deployment Guide

## Automatische Funktionen bei jedem Deployment

### 1. Dynamische API-URL (`/frontend/src/config/api.js`)
Die App erkennt automatisch die Domain und verwendet die korrekte Backend-URL:
- `wine-pairing.online` → `https://wine-pairing.online/api`
- `*.emergentagent.com` → Verwendet die Umgebungsvariable
- `localhost` → `http://localhost:8001/api`

**Keine manuelle Konfiguration nötig!**

### 2. Automatische Daten-Wiederherstellung
Beim Server-Start prüft das Backend automatisch, ob User-Daten vorhanden sind.
Wenn eine Collection leer ist, wird sie aus den Backup-Dateien wiederhergestellt.

**Geschützte Collections:**
| Collection | Backup-Datei | Inhalt |
|------------|--------------|--------|
| users | users.json | Benutzerkonten |
| wines | wines.json | Persönlicher Weinkeller |
| pairings | pairings.json | Pairing-Historie |
| chats | chats.json | Chat-Verläufe |
| wine_favorites | wine_favorites.json | Favoriten |
| payment_transactions | payment_transactions.json | Zahlungen |
| regional_pairings | regional_pairings.json | Sommelier-Kompass (1652 Gerichte) |

### 3. Automatisches Backup (alle 6 Stunden)
Das Backend erstellt automatisch Backups aller User-Daten.

---

## Wichtige Routen

| Route | Beschreibung |
|-------|--------------|
| `/` | Homepage |
| `/weinkeller` | Persönlicher Weinkeller |
| `/cellar` | Alias für Weinkeller |
| `/pairing` | Wein-Pairing |
| `/sommelier-kompass` | Gerichte nach Ländern |
| `/grapes` | Rebsorten |
| `/blog` | Blog |
| `/login` | Anmeldung |
| `/subscription` | Abo-Verwaltung |

---

## Health Check

Nach dem Deployment prüfen:
```bash
curl https://wine-pairing.online/api/health
```

Erwartete Antwort:
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "3.1"
}
```

---

## Troubleshooting

### Problem: Weinkeller ist leer
**Ursache:** Die Daten wurden nicht aus dem Backup wiederhergestellt.
**Lösung:** Server neu starten - die Auto-Restore-Logik wird die Daten laden.

### Problem: API gibt 500 Fehler
**Ursache:** Backend-URL ist falsch konfiguriert.
**Lösung:** Die dynamische API-Konfiguration sollte dies automatisch beheben.
Prüfen Sie die Browser-Konsole für die verwendete API-URL.

### Problem: "No routes matched"
**Ursache:** Die Route existiert nicht.
**Lösung:** Prüfen Sie `/app/frontend/src/App.js` für die definierten Routen.

---

## Kontakt

Bei Problemen: Prüfen Sie zuerst die Browser-Konsole (F12) für Fehlermeldungen.
