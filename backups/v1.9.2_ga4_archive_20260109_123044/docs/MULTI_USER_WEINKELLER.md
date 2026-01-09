# 🍷 Multi-User Weinkeller - Technische Dokumentation

## Überblick

Der Weinkeller ist jetzt **user-spezifisch**. Jeder registrierte Benutzer hat seinen eigenen, privaten Weinkeller, der von anderen Benutzern isoliert ist.

## Änderungen

### Backend (server.py)

#### 1. Wine Model erweitert
```python
class Wine(BaseModel):
    id: str
    user_id: str  # NEU: Verknüpfung zum Benutzer
    name: str
    type: str  # rot, weiss, rose, schaumwein
    # ... weitere Felder
```

#### 2. API Endpoints aktualisiert

| Endpoint | Änderung |
|----------|----------|
| `GET /api/wines` | Erfordert Auth, filtert nach `user_id` |
| `GET /api/wines/{id}` | Prüft ob Wein dem User gehört |
| `POST /api/wines` | Setzt `user_id` automatisch |
| `PUT /api/wines/{id}` | Prüft Besitz vor Update |
| `DELETE /api/wines/{id}` | Prüft Besitz vor Löschung |
| `POST /api/wines/{id}/favorite` | Prüft Besitz |

#### 3. Datenbank-Index
```python
# Für Performance bei vielen Usern
await db.wines.create_index("user_id")
```

### Frontend (CellarPage.js)

#### 1. Auth-Integration
```javascript
import { useAuth } from "@/contexts/AuthContext";
const { user, isAuthenticated, loading: authLoading } = useAuth();
```

#### 2. Credentials bei API-Calls
```javascript
const authAxios = axios.create({
  withCredentials: true  // Sendet Cookies für Auth
});
```

#### 3. Login-Aufforderung für nicht-eingeloggte User
- Benutzer ohne Login sehen eine freundliche Aufforderung zur Anmeldung
- Button führt direkt zur Login-Seite

## Sicherheit

✅ **Isolation**: User A kann keine Weine von User B sehen/ändern/löschen
✅ **Validierung**: Jeder API-Call prüft den Besitz
✅ **Keine Leaks**: Fehlerhafte IDs geben "nicht gefunden" zurück

## Skalierbarkeit

- **Index auf `user_id`**: Schnelle Abfragen auch bei 10.000+ Usern
- **Limit pro Query**: Max. 1000 Weine pro Anfrage
- **Keine Bilder in Listen**: `image_base64` wird bei Listen-Abfragen ausgeschlossen

## Freemium-Integration

- **Basic User**: Max. 10 Weine im Keller
- **Pro User**: Unbegrenzte Weine
- Die Prüfung erfolgt bei `POST /api/wines`

## Migration bestehender Daten

Falls alte Weine ohne `user_id` existieren:
```javascript
// Diese sind für alle User unsichtbar
// Option: Admin-Migration zu einem Default-User
```

## Test-Verifizierung

```bash
# User A registrieren und Wein hinzufügen
curl -c /tmp/userA.txt -X POST "$API/auth/register" -d '...'
curl -b /tmp/userA.txt -X POST "$API/wines" -d '{"name":"Wein A"}'

# User B kann Wein nicht sehen
curl -c /tmp/userB.txt -X POST "$API/auth/register" -d '...'
curl -b /tmp/userB.txt -X GET "$API/wines"  # Leeres Array []
```

---
*Implementiert am: 2025-12-17*
*Status: ✅ Getestet und funktionsfähig*
