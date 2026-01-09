# 🔐 Backup & Wiederherstellung - Wine Pairing App

## ⚠️ KRITISCH: Dieses Dokument ist verbindlich!

Alle Daten MÜSSEN gesichert werden und MÜSSEN wiederherstellbar sein. Keine Ausnahmen.

---

## 📊 Aktuelle Datenbestände (Stand: 17.12.2025)

| Collection | Anzahl | Beschreibung |
|------------|--------|--------------|
| `public_wines` | 1,889 | Öffentliche Wein-Datenbank |
| `wine_database` | 494 | Erweiterte Wein-Infos |
| `grape_varieties` | 140 | Rebsorten-Lexikon |
| `regional_pairings` | 1,652 | Sommelier Kompass Gerichte |
| `blog_posts` | 233 | Blog-Artikel |
| `feed_posts` | 268 | Community-Beiträge |
| `dishes` | 40 | Gerichte für Pairing |
| `seo_pairings` | 500 | SEO-optimierte Pairings |
| `users` | ~20 | Benutzerkonten |
| `wines` | ~40 | Persönliche Weinkeller |

---

## 🔄 Automatisches Backup-System

### Was wird automatisch gesichert:
- **Alle 6 Stunden** automatisches Backup
- **Bei jedem Server-Start** Backup erstellt
- Speicherort: `/app/backend/data/backups/`

### Backup-Retention:
- Letzte 10 Backups werden behalten
- Ältere werden automatisch gelöscht

---

## 📥 Manuelles Backup erstellen

### Via API:
```bash
curl -X POST "https://[IHRE-DOMAIN]/api/backup/create"
```

### Via Kommandozeile:
```bash
cd /app/backend
python3 -c "
from backup_manager import BackupManager
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

async def backup():
    client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
    db = client[os.environ.get('DB_NAME')]
    manager = BackupManager(db, '/app/backend/data')
    result = await manager.create_backup()
    print(f'Backup erstellt: {result}')

asyncio.run(backup())
"
```

---

## 🔄 Wiederherstellung

### Option 1: Automatische Wiederherstellung (bei leerem Server)
Der Server stellt automatisch Daten aus `/app/backend/data/*.json` wieder her, wenn Collections leer sind.

### Option 2: Manuelle Wiederherstellung aus Backup
```bash
# 1. Backup-Ordner auswählen
ls /app/backend/data/backups/

# 2. Daten wiederherstellen (Beispiel für public_wines)
cd /app/backend
python3 << 'EOF'
import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv('.env')

async def restore_collection(collection_name, backup_file):
    client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
    db = client[os.environ.get('DB_NAME')]
    
    with open(backup_file, 'r') as f:
        data = json.load(f)
    
    if data:
        # ACHTUNG: Bestehende Daten werden NICHT überschrieben
        existing = await db[collection_name].count_documents({})
        if existing > 0:
            print(f"⚠️ {collection_name} hat bereits {existing} Dokumente!")
            print("Löschen Sie zuerst die Collection wenn Sie überschreiben wollen.")
            return
        
        await db[collection_name].insert_many(data)
        print(f"✅ {len(data)} Dokumente in {collection_name} wiederhergestellt")
    
    client.close()

# Beispiel:
# asyncio.run(restore_collection('public_wines', '/app/backend/data/backups/backup_DATUM/public_wines.json'))
EOF
```

---

## 📁 Backup-Speicherorte

| Ort | Inhalt |
|-----|--------|
| `/app/backend/data/*.json` | Haupt-Backup-Dateien (für Auto-Restore) |
| `/app/backend/data/backups/` | Automatische Backups (mit Zeitstempel) |
| `/app/backups/` | Manuelle/historische Backups |

---

## 🚨 NOTFALL-WIEDERHERSTELLUNG

Falls alle Daten verloren sind:

### Schritt 1: Prüfen welche Backups existieren
```bash
ls -la /app/backend/data/backups/
ls -la /app/backups/
```

### Schritt 2: Neuestes Backup identifizieren
```bash
# Zeigt Backup mit den meisten Weinen
for d in /app/backend/data/backups/*/; do
  count=$(python3 -c "import json; print(len(json.load(open('${d}public_wines.json'))))" 2>/dev/null || echo 0)
  echo "$d: $count Weine"
done
```

### Schritt 3: Datenbank leeren (VORSICHT!)
```bash
# NUR wenn Sie sicher sind!
python3 -c "
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio, os
async def clear():
    client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
    db = client[os.environ.get('DB_NAME')]
    await db.public_wines.delete_many({})
    print('Collection geleert')
asyncio.run(clear())
"
```

### Schritt 4: Aus Backup wiederherstellen
```bash
# Server neu starten - Auto-Restore greift
sudo supervisorctl restart backend
```

---

## ✅ Backup-Checkliste (VOR jedem Deployment)

- [ ] Manuelles Backup erstellt
- [ ] Backup-Dateien auf Vollständigkeit geprüft
- [ ] Backup-Pfad dokumentiert
- [ ] Wiederherstellung getestet (auf Test-Umgebung)

---

## 📞 Support

Bei Datenverlust:
1. NICHT paniken
2. Server NICHT neu starten
3. Backup-Ordner prüfen
4. Neuestes vollständiges Backup identifizieren
5. Wiederherstellung durchführen

---

*Letzte Aktualisierung: 17.12.2025*
*Verantwortlich: Backup-System v3.0*
