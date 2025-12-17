# 🛡️ STRATEGIE GEGEN DATENVERLUST

## ⚠️ PROBLEM
Daten (insbesondere 6000+ Weine) gingen mehrfach verloren. Das darf NIE WIEDER passieren.

---

## 🔐 SOFORT-MASSNAHMEN (AB JETZT AKTIV)

### 1. DREIFACHE BACKUP-STRATEGIE

| Ebene | Ort | Frequenz | Verantwortlich |
|-------|-----|----------|----------------|
| **Lokal** | `/app/backend/data/` | Alle 6h automatisch | Server |
| **Git** | GitHub Repository | Bei jedem Save | Emergent Platform |
| **Export** | Manueller Download | Vor jedem Deployment | SIE |

### 2. VOR JEDEM DEPLOYMENT - PFLICHT-CHECKLISTE

```
□ Backup erstellen: python3 /app/backend/scripts/create_verified_backup.py
□ Backup-Zahlen notieren (Weine, Blogs, etc.)
□ JSON-Dateien herunterladen (siehe unten)
□ Deployment durchführen
□ SOFORT nach Deployment: Zahlen verifizieren
□ Bei Abweichung: STOPP und Restore
```

### 3. DOWNLOAD-LINKS FÜR MANUELLE SICHERUNG

Nach jedem wichtigen Meilenstein diese Dateien herunterladen:

```
https://[IHRE-DOMAIN]/api/backup/download/public_wines.json
https://[IHRE-DOMAIN]/api/backup/download/wine_database.json
https://[IHRE-DOMAIN]/api/backup/download/blog_posts.json
https://[IHRE-DOMAIN]/api/backup/download/grape_varieties.json
https://[IHRE-DOMAIN]/api/backup/download/regional_pairings.json
```

---

## 🚨 WARUM GEHEN DATEN VERLOREN?

### Hauptursachen:
1. **Deployment auf neuen Server** → Datenbank ist leer
2. **Auto-Seeding überschreibt** → Alte Seed-Daten ersetzen neue
3. **Kein persistenter Speicher** → Preview-Server sind temporär
4. **Backup nicht in Git** → Nur Code wird gesichert, nicht DB

### Lösung implementiert:
- ✅ Auto-Restore aus JSON-Dateien bei leerem Server
- ✅ JSON-Dateien werden in Git committed
- ✅ Schutz vor Überschreiben existierender Daten
- ✅ Regelmäßige automatische Backups

---

## 📋 AKTUELLE DATEN (17.12.2025)

| Daten | Anzahl | Status |
|-------|--------|--------|
| Weine (public_wines) | 1,889 | ✅ Gesichert |
| Weine (wine_database) | 494 | ✅ Gesichert |
| Blog-Artikel | 233 | ✅ Gesichert |
| Rebsorten | 140 | ✅ Gesichert |
| Sommelier Kompass | 1,652 | ✅ Gesichert |
| Community Feed | 268 | ✅ Gesichert |
| **GESAMT** | **5,565** | ✅ |

---

## ❓ ZU DEN 6000+ WEINEN

Die 6000+ Weine existieren **NICHT** in:
- Aktuelle Datenbank
- Git-History (alle 1,202 Commits geprüft)
- Lokale Backups
- Excel-Dateien

**Mögliche Quellen:**
1. Externes System/API das nicht mehr verfügbar ist
2. Anderes Repository (wine-companion-3 etc.)
3. Manuell erstellte Daten die nie committed wurden

**Um diese wiederherzustellen brauche ich:**
- Die Original-Quelldatei (JSON, CSV, Excel)
- Oder Zugang zum ursprünglichen System
- Oder die Daten müssen neu erstellt/gekauft werden

---

## 🔧 TECHNISCHE SICHERUNGEN (AKTIV)

### Im Server implementiert:
```python
# server.py - Startup
# 1. Prüft ob Collections leer sind
# 2. Wenn ja: Restore aus /backend/data/*.json
# 3. Erstellt sofort Backup
# 4. Startet 6-Stunden Backup-Timer
```

### Backup-Manager:
```python
# backup_manager.py
# - Automatisches Backup alle 6 Stunden
# - Behält letzte 10 Backups
# - Verifiziert Datenintegrität
```

### Git-Integration:
```
# Alle JSON-Dateien in /backend/data/ werden committed
# Bei GitHub-Sync: Daten sind im Repository
```

---

## 📞 BEI DATENVERLUST

1. **NICHT** den Server neu starten
2. Backup-Ordner prüfen: `ls /app/backend/data/backups/`
3. Neuestes Backup mit korrekten Zahlen finden
4. Manuell wiederherstellen (siehe BACKUP_UND_WIEDERHERSTELLUNG.md)

---

## ✅ EMPFEHLUNG

**Für die 6000+ Weine:**
Wenn Sie die Original-Quelldatei haben (von wo Sie die Weine gekauft haben), kann ich diese importieren und DAUERHAFT sichern.

Bitte senden Sie mir:
- Die Datei (JSON, CSV, Excel)
- Oder den Link zur Quelle

Ich werde dann:
1. Import durchführen
2. Dreifach sichern (Lokal + Git + Download für Sie)
3. Verifizieren dass alle Daten korrekt sind

---

*Erstellt: 17.12.2025*
*Status: AKTIV*
