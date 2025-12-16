# 📦 Wine-Pairing Backup System v3.0

## Übersicht

Das Backup-System schützt **ALLE** Daten vor Datenverlust bei Deployments.

⚠️ **WICHTIG:** Seit Version 3.0 werden **ALLE Collections geschützt** - nicht nur User-Daten!

## Schutz-Mechanismus

**REGEL:** Existierende Daten werden **NIEMALS** überschrieben!
- Nur **komplett leere** Collections werden aus dem Backup gefüllt
- Collections mit Daten bleiben **immer** unverändert

## Geschützte Collections (ALLE)

### User-Collections
| Collection | Beschreibung |
|------------|--------------|
| `users` | 🔒 Benutzerkonten, Passwörter, Abo-Status |
| `wines` | 🔒 Persönlicher Weinkeller |
| `pairings` | 🔒 Pairing-Historie |
| `chats` | 🔒 Chat-Verläufe mit dem Sommelier |
| `wine_favorites` | 🔒 Favorisierte Weine |
| `user_sessions` | 🔒 Aktive Sessions |
| `payment_transactions` | 🔒 Zahlungshistorie |

### Content-Collections
| Collection | Beschreibung |
|------------|--------------|
| `public_wines` | 📄 Weindatenbank (1821 Weine) |
| `grape_varieties` | 📄 Rebsorten (140 Sorten) |
| `blog_posts` | 📄 Blog-Artikel (233 Beiträge) |
| `feed_posts` | 📄 Community Feed (268 Posts) |
| `regional_pairings` | 📄 Sommelier-Kompass (44 Pairings) |
| `dishes` | 📄 Gerichte-Datenbank |
| `wine_database` | 📄 Erweiterte Wein-DB |
| `seo_pairings` | 📄 SEO-Pairings |
| `coupons` | 📄 Gutschein-Codes |

## Automatische Backups (v3.1)

**ALLE 6 STUNDEN** wird automatisch ein vollständiges Backup erstellt!

- Backups werden beim Server-Start und dann alle 6 Stunden erstellt
- Die letzten 10 Backups werden aufbewahrt (ca. 2.5 Tage)
- Ältere Backups werden automatisch gelöscht

## API Endpoints

### GET /api/backup/status
Zeigt den aktuellen Backup-Status, alle verfügbaren Backups und Auto-Backup-Info.

**Beispiel-Response:**
```json
{
  "auto_backup": {
    "enabled": true,
    "interval_hours": 6,
    "next_backup": "2025-12-17T05:19:57"
  }
}
```

### POST /api/backup/create
Erstellt ein neues Backup manuell.
- `?user_data_only=true` - Nur User-Daten sichern (schneller)
- `?user_data_only=false` - Vollständiges Backup (default)

### GET /api/backup/user-data-counts
Schnelle Übersicht der User-Daten für Health-Checks.

## Backup-Verzeichnisse

```
/app/backend/data/
├── backups/
│   ├── backup_YYYYMMDD_HHMMSS/  # Vollständige Backups
│   └── user_backup_YYYYMMDD_HHMMSS/  # Nur User-Daten
├── backup_manifest.json  # Aktuelles Manifest
├── users.json  # Aktuelles User-Backup
├── wines.json  # Aktuelles Weinkeller-Backup
└── ...
```

## Automatische Sicherungen

- Beim Server-Start wird der Backup-Manager initialisiert
- Alte Backups werden automatisch aufgeräumt (max. 5 behalten)

## Wiederherstellung

Im Notfall kann ein Backup über die BackupManager-Klasse wiederhergestellt werden:

```python
from backup_manager import BackupManager

manager = BackupManager(db, data_dir)
await manager.restore_from_backup(
    "/app/backend/data/backups/backup_YYYYMMDD_HHMMSS",
    restore_user_data=True  # ACHTUNG: Überschreibt aktuelle User-Daten!
)
```

## Wichtige Hinweise

⚠️ **NIEMALS** die folgenden Dateien manuell löschen:
- `/app/backend/data/users.json`
- `/app/backend/data/wines.json`
- `/app/backend/data/backup_manifest.json`

⚠️ Bei einem Deployment werden User-Daten **NICHT** überschrieben, solange sie existieren.
