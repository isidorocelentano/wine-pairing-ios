# 📦 Wine-Pairing Backup System

## Übersicht

Das Backup-System schützt alle Benutzerdaten vor Datenverlust bei Deployments.

## Geschützte User-Collections (werden NIEMALS überschrieben)

| Collection | Beschreibung |
|------------|--------------|
| `users` | Benutzerkonten, Passwörter, Abo-Status |
| `wines` | Persönlicher Weinkeller |
| `pairings` | Pairing-Historie |
| `chats` | Chat-Verläufe mit dem Sommelier |
| `wine_favorites` | Favorisierte Weine |
| `user_sessions` | Aktive Sessions |
| `payment_transactions` | Zahlungshistorie |

## API Endpoints

### GET /api/backup/status
Zeigt den aktuellen Backup-Status und alle verfügbaren Backups.

### POST /api/backup/create
Erstellt ein neues Backup.
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
