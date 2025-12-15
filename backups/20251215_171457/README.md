# Wine-Pairing.online - Datenbank Backup

## Stand: 14. Dezember 2025

### Erwartete Daten (Manifest v2.0)

| Collection | Dokumente | Beschreibung |
|------------|-----------|--------------|
| blog_posts | 233 | Blog-Artikel (84 Regionen, 144 Rebsorten) |
| public_wines | 1751 | Öffentliche Weindatenbank |
| grape_varieties | 140 | Rebsorten mit korrekten Weinbildern |
| regional_pairings | 44 | Sommelier Kompass - Regionale Paarungen |
| dishes | 40 | Gerichte für Pairing |
| feed_posts | 268 | Community Feed |
| wine_database | 494 | Zusätzliche Weindaten |

### Automatisches Seeding

Der Server prüft bei jedem Start automatisch:
1. Sind alle Collections vorhanden?
2. Haben sie die erwartete Anzahl an Dokumenten?
3. Sind die Blog-Kategorien korrekt (84 in "regionen")?

Wenn IRGENDETWAS nicht stimmt, werden ALLE Daten aus den JSON-Backup-Dateien neu geladen.

### Backup-Dateien

- `blog_posts.json` - 233 Artikel
- `public_wines.json` - 1751 Weine
- `grape_varieties.json` - 140 Rebsorten (korrigierte Bilder)
- `regional_pairings.json` - 44 Paarungen (Sommelier Kompass)
- `dishes.json` - 40 Gerichte
- `feed_posts.json` - 268 Posts
- `wine_database.json` - 494 Weine
- `backup_manifest.json` - Prüfsummen und erwartete Werte

### Bei Problemen

Falls nach einem Deployment Daten fehlen:
1. Server-Logs prüfen auf Seeding-Meldungen
2. Die Startup-Logik lädt automatisch alle Daten neu
3. Manuelles Seeding: Backend neu starten

### Version History

- v2.0 (14.12.2025): Robustes Seeding mit Manifest-Prüfung
- v1.0: Basis-Seeding wenn Collection leer
