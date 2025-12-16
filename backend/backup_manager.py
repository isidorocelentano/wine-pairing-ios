"""
WINE-PAIRING BACKUP MANAGER
===========================
Automatisches Backup-System für alle MongoDB Collections.
Version 3.0 - Verhindert Datenverlust bei Deployments.

Funktionen:
- Automatisches Backup beim Server-Start
- Manuelles Backup über API
- Wiederherstellung aus Backup
- Schutz von User-Daten vor Überschreibung
"""

import asyncio
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


class MongoJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder für MongoDB ObjectId und datetime"""
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class BackupManager:
    """
    Verwaltet Backups für die Wine-Pairing Datenbank.
    
    KRITISCHE USER-COLLECTIONS (werden NIEMALS überschrieben):
    - users: Benutzerkonten
    - wines: Persönlicher Weinkeller
    - pairings: Pairing-History
    - chats: Chat-Verläufe
    - wine_favorites: Favoriten
    - user_sessions: Session-Daten
    - payment_transactions: Zahlungen
    
    SYSTEM-COLLECTIONS (können bei Bedarf neu geladen werden):
    - blog_posts, public_wines, grape_varieties, etc.
    """
    
    # KRITISCH: Diese Collections enthalten User-Daten und werden NIEMALS überschrieben!
    USER_COLLECTIONS = [
        'users',
        'wines',
        'pairings',
        'chats',
        'wine_favorites',
        'user_sessions',
        'payment_transactions',
    ]
    
    # System-Collections können bei Bedarf neu geladen werden
    SYSTEM_COLLECTIONS = [
        'blog_posts',
        'public_wines',
        'grape_varieties',
        'regional_pairings',
        'dishes',
        'feed_posts',
        'wine_database',
        'seo_pairings',
        'coupons',
    ]
    
    def __init__(self, db: AsyncIOMotorDatabase, data_dir: Path):
        self.db = db
        self.data_dir = data_dir
        self.backup_dir = data_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
    async def create_full_backup(self) -> Dict[str, Any]:
        """
        Erstellt ein vollständiges Backup aller Collections.
        Wird beim Server-Start automatisch aufgerufen.
        """
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f"backup_{timestamp}"
        backup_path.mkdir(exist_ok=True)
        
        manifest = {
            'version': '3.0',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'backup_dir': str(backup_path),
            'collections': {}
        }
        
        all_collections = self.USER_COLLECTIONS + self.SYSTEM_COLLECTIONS
        
        logger.info(f"📦 Erstelle Backup: {backup_path}")
        
        for collection_name in all_collections:
            try:
                docs = await self.db[collection_name].find({}).to_list(None)
                
                # Entferne _id für sauberen Re-Import
                clean_docs = []
                for doc in docs:
                    if '_id' in doc:
                        del doc['_id']
                    clean_docs.append(doc)
                
                count = len(clean_docs)
                
                # Speichere in JSON
                backup_file = backup_path / f"{collection_name}.json"
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(clean_docs, f, cls=MongoJSONEncoder, ensure_ascii=False, indent=2)
                
                manifest['collections'][collection_name] = {
                    'count': count,
                    'file': f'{collection_name}.json',
                    'is_user_data': collection_name in self.USER_COLLECTIONS
                }
                
                # Status-Icon
                icon = '🔒' if collection_name in self.USER_COLLECTIONS else '📄'
                logger.info(f"   {icon} {collection_name}: {count} Dokumente")
                
            except Exception as e:
                logger.error(f"   ❌ {collection_name}: {e}")
                manifest['collections'][collection_name] = {'count': 0, 'error': str(e)}
        
        # Speichere Manifest
        manifest_file = backup_path / "manifest.json"
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        # Aktualisiere Haupt-Manifest
        await self._update_main_manifest(manifest)
        
        return manifest
    
    async def _update_main_manifest(self, backup_manifest: Dict[str, Any]):
        """Aktualisiert das Haupt-Manifest mit den neuesten Backup-Daten"""
        main_manifest = {
            'version': '3.0',
            'timestamp': backup_manifest['timestamp'],
            'last_backup': backup_manifest['backup_dir'],
            'expected': {
                col: info['count'] 
                for col, info in backup_manifest['collections'].items()
            }
        }
        
        manifest_path = self.data_dir / "backup_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(main_manifest, f, ensure_ascii=False, indent=2)
    
    async def backup_user_data_only(self) -> Dict[str, Any]:
        """
        Erstellt ein Backup nur der kritischen User-Daten.
        Schneller als ein vollständiges Backup.
        """
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f"user_backup_{timestamp}"
        backup_path.mkdir(exist_ok=True)
        
        manifest = {
            'version': '3.0',
            'type': 'user_data_only',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'backup_dir': str(backup_path),
            'collections': {}
        }
        
        logger.info(f"🔒 Erstelle User-Data Backup: {backup_path}")
        
        for collection_name in self.USER_COLLECTIONS:
            try:
                docs = await self.db[collection_name].find({}).to_list(None)
                
                clean_docs = []
                for doc in docs:
                    if '_id' in doc:
                        del doc['_id']
                    clean_docs.append(doc)
                
                count = len(clean_docs)
                
                backup_file = backup_path / f"{collection_name}.json"
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(clean_docs, f, cls=MongoJSONEncoder, ensure_ascii=False, indent=2)
                
                manifest['collections'][collection_name] = {'count': count}
                logger.info(f"   🔒 {collection_name}: {count} Dokumente")
                
            except Exception as e:
                logger.error(f"   ❌ {collection_name}: {e}")
        
        # Speichere Manifest
        manifest_file = backup_path / "manifest.json"
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        return manifest
    
    async def restore_from_backup(self, backup_path: str, restore_user_data: bool = False) -> Dict[str, Any]:
        """
        Stellt Daten aus einem Backup wieder her.
        
        WICHTIG: User-Daten werden standardmäßig NICHT überschrieben!
        Set restore_user_data=True nur bei komplettem Datenverlust.
        """
        backup_dir = Path(backup_path)
        
        if not backup_dir.exists():
            raise ValueError(f"Backup-Verzeichnis nicht gefunden: {backup_path}")
        
        manifest_file = backup_dir / "manifest.json"
        if not manifest_file.exists():
            raise ValueError(f"Manifest nicht gefunden: {manifest_file}")
        
        with open(manifest_file, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        results = {
            'restored': [],
            'skipped': [],
            'errors': []
        }
        
        logger.info(f"📥 Wiederherstellung aus: {backup_path}")
        
        for collection_name, info in manifest.get('collections', {}).items():
            try:
                # KRITISCH: User-Daten nur wiederherstellen wenn explizit erlaubt
                if collection_name in self.USER_COLLECTIONS and not restore_user_data:
                    existing_count = await self.db[collection_name].count_documents({})
                    if existing_count > 0:
                        logger.info(f"   🔒 {collection_name}: {existing_count} Dokumente GESCHÜTZT")
                        results['skipped'].append(collection_name)
                        continue
                
                backup_file = backup_dir / info.get('file', f'{collection_name}.json')
                if not backup_file.exists():
                    logger.warning(f"   ⚠️ {collection_name}: Backup-Datei fehlt")
                    continue
                
                with open(backup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if data:
                    await self.db[collection_name].delete_many({})
                    await self.db[collection_name].insert_many(data)
                    logger.info(f"   ✅ {collection_name}: {len(data)} Dokumente wiederhergestellt")
                    results['restored'].append(collection_name)
                    
            except Exception as e:
                logger.error(f"   ❌ {collection_name}: {e}")
                results['errors'].append({'collection': collection_name, 'error': str(e)})
        
        return results
    
    async def get_backup_status(self) -> Dict[str, Any]:
        """
        Gibt den aktuellen Backup-Status zurück.
        """
        status = {
            'backups': [],
            'user_data_counts': {},
            'system_data_counts': {}
        }
        
        # Liste alle Backups
        if self.backup_dir.exists():
            for backup in sorted(self.backup_dir.iterdir(), reverse=True):
                if backup.is_dir() and backup.name.startswith('backup_'):
                    manifest_file = backup / "manifest.json"
                    if manifest_file.exists():
                        with open(manifest_file, 'r') as f:
                            manifest = json.load(f)
                        status['backups'].append({
                            'name': backup.name,
                            'timestamp': manifest.get('timestamp'),
                            'type': manifest.get('type', 'full')
                        })
        
        # Aktuelle Daten-Counts
        for col in self.USER_COLLECTIONS:
            status['user_data_counts'][col] = await self.db[col].count_documents({})
        
        for col in self.SYSTEM_COLLECTIONS:
            status['system_data_counts'][col] = await self.db[col].count_documents({})
        
        return status
    
    async def cleanup_old_backups(self, keep_count: int = 5) -> int:
        """
        Löscht alte Backups, behält die neuesten `keep_count`.
        """
        if not self.backup_dir.exists():
            return 0
        
        backups = sorted(
            [d for d in self.backup_dir.iterdir() if d.is_dir() and d.name.startswith('backup_')],
            reverse=True
        )
        
        deleted = 0
        for backup in backups[keep_count:]:
            try:
                import shutil
                shutil.rmtree(backup)
                deleted += 1
                logger.info(f"🗑️ Altes Backup gelöscht: {backup.name}")
            except Exception as e:
                logger.error(f"❌ Konnte Backup nicht löschen: {backup.name} - {e}")
        
        return deleted


async def create_startup_backup(db: AsyncIOMotorDatabase, data_dir: Path) -> BackupManager:
    """
    Factory-Funktion für den BackupManager.
    Erstellt automatisch ein Backup beim Server-Start.
    """
    manager = BackupManager(db, data_dir)
    
    # Erstelle automatisches Backup beim Start
    try:
        await manager.create_full_backup()
        logger.info("✅ Automatisches Startup-Backup erstellt")
    except Exception as e:
        logger.error(f"⚠️ Startup-Backup fehlgeschlagen: {e}")
    
    # Cleanup alte Backups (behalte die letzten 5)
    try:
        deleted = await manager.cleanup_old_backups(keep_count=5)
        if deleted > 0:
            logger.info(f"🗑️ {deleted} alte Backups gelöscht")
    except Exception as e:
        logger.error(f"⚠️ Backup-Cleanup fehlgeschlagen: {e}")
    
    return manager
