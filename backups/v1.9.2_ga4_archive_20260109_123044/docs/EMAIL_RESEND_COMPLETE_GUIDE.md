# 📧 E-Mail-Funktionalität mit Resend - Komplette Anleitung

**Version:** 1.0  
**Erstellt:** 07.01.2026  
**Basierend auf:** 2 Tage Debugging-Erfahrung mit Wine Pairing App  
**Technologie:** FastAPI + React + MongoDB (Emergent Platform)

---

# Inhaltsverzeichnis

1. [Übersicht](#1-übersicht)
2. [Resend Setup (Schritt für Schritt)](#2-resend-setup)
3. [Infomaniak DNS-Konfiguration (Schritt für Schritt)](#3-infomaniak-dns-konfiguration)
4. [Backend-Implementation](#4-backend-implementation)
5. [Frontend-Implementation](#5-frontend-implementation)
6. [Häufige Fehler & Lösungen](#6-häufige-fehler--lösungen)
7. [Test-Checkliste](#7-test-checkliste)
8. [Troubleshooting](#8-troubleshooting)

---

# 1. Übersicht

Diese Anleitung beschreibt, wie man E-Mail-Versand (z.B. Passwort-Reset) mit **Resend** in einer Emergent-App korrekt einrichtet.

### Zeitaufwand
- Resend Setup: ~10 Minuten
- DNS-Konfiguration: ~15 Minuten
- Code-Implementation: ~30 Minuten
- DNS-Propagation: bis zu 24-48 Stunden

### Voraussetzungen
- Eigene Domain (z.B. `meine-app.online`)
- Zugang zum Domain-Provider (z.B. Infomaniak)
- Emergent App mit FastAPI Backend

---

# 2. Resend Setup

## 2.1 Account erstellen

1. Gehe zu **https://resend.com**
2. Klicke auf **"Get Started"** oder **"Sign Up"**
3. Registriere dich mit E-Mail oder GitHub
4. Bestätige deine E-Mail-Adresse

## 2.2 API Key erstellen

1. Nach dem Login: Klicke links auf **"API Keys"**
2. Klicke auf **"Create API Key"**
3. Name eingeben (z.B. `production-key`)
4. Permission: **"Full Access"** auswählen
5. Klicke **"Create"**
6. **WICHTIG:** Kopiere den Key sofort! Er beginnt mit `re_...`
   - Beispiel: `re_DsA4rNBr_AX6qpJX6xheVogMKCzKZ4XF6`
   - Der Key wird nur einmal angezeigt!

## 2.3 Domain hinzufügen

1. Klicke links auf **"Domains"**
2. Klicke auf **"Add Domain"**
3. Gib deine Domain ein: `meine-app.online` (ohne www oder https)
4. Region auswählen:
   - **EU (Ireland) - eu-west-1** ← empfohlen für europäische Nutzer
   - oder US East (N. Virginia) - us-east-1
5. Klicke **"Add"**

## 2.4 DNS-Einträge anzeigen

Nach dem Hinzufügen zeigt Resend eine Tabelle mit **3 DNS-Einträgen**:

| Type | Name | Value | Status |
|------|------|-------|--------|
| TXT | resend._domainkey | p=MIGfMA0GCSq... (langer Key) | Pending |
| MX | send | feedback-smtp.eu-west-1.amazonses.com | Pending |
| TXT | send | v=spf1 include:amazonses.com ~all | Pending |

**Diese Werte brauchst du für den nächsten Schritt!**

---

# 3. Infomaniak DNS-Konfiguration

## 3.1 Zum DNS-Manager navigieren

1. Gehe zu **https://manager.infomaniak.com**
2. Logge dich ein
3. Klicke auf **"Web & Domain"** oder **"Domains"**
4. Wähle deine Domain (z.B. `meine-app.online`)
5. Klicke auf **"DNS-Zone"** oder **"DNS verwalten"**

## 3.2 DKIM-Eintrag hinzufügen (Eintrag 1/4)

1. Klicke auf **"Eintrag hinzufügen"**
2. Fülle die Felder aus:

| Feld | Wert |
|------|------|
| **Typ** | `TXT` |
| **Quelle/Name** | `resend._domainkey` |
| **Ziel/Inhalt** | Den langen Key von Resend kopieren (beginnt mit `p=MIGfMA0...`) |
| **TTL** | `1 Stunde` (Standard) |

3. Klicke **"Speichern"**

## 3.3 MX-Eintrag hinzufügen (Eintrag 2/4)

1. Klicke auf **"Eintrag hinzufügen"**
2. Fülle die Felder aus:

| Feld | Wert |
|------|------|
| **Typ** | `MX` |
| **Quelle/Name** | `send` |
| **Ziel** | `feedback-smtp.eu-west-1.amazonses.com` |
| **Priorität** | `10` |
| **TTL** | `1 Stunde` |

3. Klicke **"Speichern"**

## 3.4 SPF-Eintrag hinzufügen (Eintrag 3/4)

1. Klicke auf **"Eintrag hinzufügen"**
2. Fülle die Felder aus:

| Feld | Wert |
|------|------|
| **Typ** | `TXT` |
| **Quelle/Name** | `send` |
| **Ziel/Inhalt** | `v=spf1 include:amazonses.com ~all` |
| **TTL** | `1 Stunde` |

3. Klicke **"Speichern"**

## 3.5 DMARC-Eintrag hinzufügen (Eintrag 4/4) - WICHTIG!

1. Klicke auf **"Eintrag hinzufügen"**
2. **Option A:** Falls Infomaniak einen DMARC-Assistenten hat:
   - Typ: **DMARC**
   - Regel für die Domain: **"Keine"** (NICHT "Zurückweisung"!)
   
3. **Option B:** Manuell als TXT:

| Feld | Wert |
|------|------|
| **Typ** | `TXT` |
| **Quelle/Name** | `_dmarc` |
| **Ziel/Inhalt** | `v=DMARC1;p=none` |
| **TTL** | `1 Stunde` |

4. Klicke **"Speichern"**

⚠️ **KRITISCH:** Verwende `p=none` - NIEMALS `p=reject`!
- `p=none` = E-Mails werden zugestellt
- `p=reject` = E-Mails werden blockiert!

## 3.6 DNS-Einträge überprüfen

Deine DNS-Zone sollte jetzt diese Einträge enthalten:

| Typ | Name | Wert |
|-----|------|------|
| TXT | resend._domainkey | p=MIGfMA0GCSq... |
| MX | send | feedback-smtp.eu-west-1.amazonses.com (Priorität 10) |
| TXT | send | v=spf1 include:amazonses.com ~all |
| TXT | _dmarc | v=DMARC1;p=none |

## 3.7 In Resend verifizieren

1. Gehe zurück zu **Resend → Domains**
2. Klicke auf deine Domain
3. Klicke auf **"Verify DNS Records"** oder warte
4. Alle Einträge sollten **"Verified"** (grün) zeigen:
   - ✅ DKIM - Verified
   - ✅ MX - Verified
   - ✅ SPF - Verified

**Hinweis:** DNS-Änderungen können 5 Minuten bis 48 Stunden dauern!

---

# 4. Backend-Implementation

## 4.1 Dependencies

```bash
pip install resend
```

In `/app/backend/requirements.txt` hinzufügen:
```
resend
```

## 4.2 Environment Variables

In `/app/backend/.env` hinzufügen:
```env
# Resend Email Service
RESEND_API_KEY=re_DEIN_API_KEY_HIER
SENDER_EMAIL=noreply@meine-app.online
```

## 4.3 Server.py - Globale Initialisierung

**⚠️ KRITISCH: Am Anfang der Datei, nach den Imports:**

```python
import resend
import secrets
from datetime import datetime, timezone, timedelta
import logging

logger = logging.getLogger(__name__)

# ===== E-MAIL KONFIGURATION =====
RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'noreply@meine-app.online')

# API Key EINMAL global setzen - NIEMALS in Funktionen!
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY
```

## 4.4 Pydantic Models

```python
class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
```

## 4.5 Forgot Password Endpoint

```python
@api_router.post("/auth/forgot-password")
async def forgot_password(req: PasswordResetRequest):
    """Passwort vergessen - sendet Reset-Email."""
    email = req.email.lower().strip()
    
    # Sicherheit: Immer gleiche Antwort (verhindert Email-Enumeration)
    success_message = {
        "message": "Falls ein Account existiert, wurde ein Reset-Link gesendet. Bitte prüfen Sie auch Ihren Spam-Ordner.",
        "message_en": "If an account exists, a reset link has been sent. Please also check your spam folder."
    }
    
    # User suchen
    user = await db.users.find_one({"email": email})
    if not user:
        return success_message
    
    # Token generieren
    reset_token = secrets.token_urlsafe(32)
    reset_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    
    # Token in DB speichern
    await db.users.update_one(
        {"email": email},
        {"$set": {
            "password_reset_token": reset_token,
            "password_reset_expiry": reset_expiry
        }}
    )
    
    # ⚠️ WICHTIG: Domain HARDCODEN - nicht aus Environment Variable!
    reset_url = f"https://meine-app.online/reset-password?token={reset_token}"
    
    # Email senden
    # ⚠️ WICHTIG: resend.api_key hier NICHT setzen!
    try:
        resend.Emails.send({
            "from": f"Meine App <{SENDER_EMAIL}>",
            "to": [email],
            "subject": "Passwort zurücksetzen",
            "html": f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #ffffff;">
                <div style="text-align: center; padding: 20px 0;">
                    <h1 style="color: #333; margin: 0;">Meine App</h1>
                </div>
                <div style="padding: 30px; background-color: #f9f9f9; border-radius: 10px;">
                    <h2 style="color: #333; margin-top: 0;">Passwort zurücksetzen</h2>
                    <p style="color: #555; line-height: 1.6;">Guten Tag,</p>
                    <p style="color: #555; line-height: 1.6;">Sie haben angefordert, Ihr Passwort zurückzusetzen. Klicken Sie auf den Button unten:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_url}" 
                           style="background-color: #007bff; color: #ffffff; padding: 15px 30px; 
                                  text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">
                            Neues Passwort erstellen
                        </a>
                    </div>
                    <p style="color: #888; font-size: 13px; line-height: 1.5;">
                        Dieser Link ist 1 Stunde gültig. Falls Sie dies nicht angefordert haben, ignorieren Sie diese E-Mail.
                    </p>
                </div>
                <div style="text-align: center; padding: 20px; color: #999; font-size: 12px;">
                    <p><a href="https://meine-app.online" style="color: #007bff;">meine-app.online</a></p>
                </div>
            </div>
            """
        })
        logger.info(f"Password reset email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send reset email to {email}: {e}")
    
    return success_message
```

## 4.6 Verify Token Endpoint

```python
@api_router.get("/auth/verify-reset-token/{token}")
async def verify_reset_token(token: str):
    """Prüft ob Reset-Token gültig ist."""
    # Token suchen (ohne Expiry-Check wegen Timezone-Problemen!)
    user = await db.users.find_one({"password_reset_token": token})
    
    if not user:
        raise HTTPException(status_code=400, detail="Ungültiger Link")
    
    # ⚠️ WICHTIG: Expiry manuell prüfen (Timezone-sicher!)
    expiry = user.get("password_reset_expiry")
    if expiry:
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
        if expiry <= datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Link abgelaufen")
    
    return {"valid": True, "email": user.get("email", "")[:3] + "***"}
```

## 4.7 Reset Password Endpoint

```python
@api_router.post("/auth/reset-password")
async def reset_password(req: PasswordResetConfirm):
    """Setzt das Passwort mit dem Reset-Token zurück."""
    if len(req.new_password) < 6:
        raise HTTPException(status_code=400, detail="Passwort muss mindestens 6 Zeichen haben")
    
    # User mit Token finden
    user = await db.users.find_one({"password_reset_token": req.token})
    
    if not user:
        raise HTTPException(status_code=400, detail="Ungültiger Link")
    
    # Expiry prüfen (Timezone-sicher!)
    expiry = user.get("password_reset_expiry")
    if expiry:
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
        if expiry <= datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Link abgelaufen")
    
    # Passwort aktualisieren
    new_hash = hash_password(req.new_password)
    await db.users.update_one(
        {"_id": user["_id"]},
        {
            "$set": {"password": new_hash},
            "$unset": {"password_reset_token": "", "password_reset_expiry": ""}
        }
    )
    
    return {"message": "Passwort erfolgreich geändert!"}
```

---

# 5. Frontend-Implementation

## 5.1 ForgotPasswordPage.js

```jsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { API } from '@/config/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { toast } from 'sonner';

function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await axios.post(`${API}/auth/forgot-password`, { email });
      setSubmitted(true);
    } catch (error) {
      toast.error('Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.');
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow">
        <h2 className="text-2xl font-bold mb-4">E-Mail gesendet!</h2>
        <p className="text-gray-600 mb-4">
          Falls ein Account mit dieser E-Mail existiert, haben wir einen Reset-Link gesendet.
        </p>
        <p className="text-amber-600 font-medium mb-4">
          ⚠️ Bitte prüfen Sie auch Ihren Spam-Ordner!
        </p>
        <Link to="/login" className="text-blue-600 hover:underline">
          Zurück zum Login
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-4">Passwort vergessen</h2>
      <p className="text-gray-600 mb-6">
        Geben Sie Ihre E-Mail-Adresse ein und wir senden Ihnen einen Link zum Zurücksetzen.
      </p>
      
      <form onSubmit={handleSubmit}>
        <Input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Ihre E-Mail-Adresse"
          required
          className="mb-4"
        />
        
        <Button type="submit" disabled={loading} className="w-full">
          {loading ? 'Wird gesendet...' : 'Reset-Link anfordern'}
        </Button>
      </form>
      
      <div className="mt-4 text-center">
        <Link to="/login" className="text-sm text-gray-500 hover:underline">
          Zurück zum Login
        </Link>
      </div>
    </div>
  );
}

export default ForgotPasswordPage;
```

## 5.2 ResetPasswordPage.js

```jsx
import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { API } from '@/config/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { toast } from 'sonner';

function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');
  
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [tokenValid, setTokenValid] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const verifyToken = async () => {
      if (!token) {
        setTokenValid(false);
        setLoading(false);
        return;
      }
      
      try {
        await axios.get(`${API}/auth/verify-reset-token/${token}`);
        setTokenValid(true);
      } catch {
        setTokenValid(false);
      } finally {
        setLoading(false);
      }
    };
    
    verifyToken();
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      toast.error('Passwörter stimmen nicht überein');
      return;
    }
    
    if (password.length < 6) {
      toast.error('Passwort muss mindestens 6 Zeichen haben');
      return;
    }
    
    setSubmitting(true);
    
    try {
      await axios.post(`${API}/auth/reset-password`, {
        token,
        new_password: password
      });
      setSuccess(true);
      toast.success('Passwort erfolgreich geändert!');
      setTimeout(() => navigate('/login'), 3000);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Fehler beim Zurücksetzen');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-md mx-auto mt-10 p-6 text-center">
        <p>Laden...</p>
      </div>
    );
  }

  if (!token || !tokenValid) {
    return (
      <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow">
        <h2 className="text-2xl font-bold text-red-600 mb-4">Ungültiger Link</h2>
        <p className="text-gray-600 mb-4">
          Dieser Link ist ungültig oder abgelaufen. Bitte fordern Sie einen neuen Link an.
        </p>
        <Link to="/forgot-password">
          <Button className="w-full">Neuen Link anfordern</Button>
        </Link>
      </div>
    );
  }

  if (success) {
    return (
      <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow">
        <h2 className="text-2xl font-bold text-green-600 mb-4">Passwort geändert!</h2>
        <p className="text-gray-600">
          Sie werden zum Login weitergeleitet...
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-4">Neues Passwort setzen</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <Input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Neues Passwort"
            minLength={6}
            required
          />
        </div>
        
        <div className="mb-6">
          <Input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Passwort bestätigen"
            required
          />
        </div>
        
        <Button type="submit" disabled={submitting} className="w-full">
          {submitting ? 'Wird gespeichert...' : 'Passwort ändern'}
        </Button>
      </form>
    </div>
  );
}

export default ResetPasswordPage;
```

## 5.3 Routes (App.js)

```jsx
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import ResetPasswordPage from './pages/ResetPasswordPage';

// In den Routes:
<Route path="/forgot-password" element={<ForgotPasswordPage />} />
<Route path="/reset-password" element={<ResetPasswordPage />} />
```

## 5.4 Login-Seite Link

Füge auf der Login-Seite einen Link hinzu:
```jsx
<Link to="/forgot-password" className="text-sm text-gray-500 hover:underline">
  Passwort vergessen?
</Link>
```

---

# 6. Häufige Fehler & Lösungen

## ❌ Fehler 1: E-Mails werden in Produktion nicht gesendet

**Symptom:** Preview funktioniert, Live-Seite nicht

**Ursache:** `resend.api_key` wird innerhalb einer Funktion gesetzt

**Lösung:** 
```python
# ❌ FALSCH - nicht in Funktion setzen!
async def forgot_password():
    resend.api_key = RESEND_API_KEY  # ← NICHT HIER!
    resend.Emails.send(...)

# ✅ RICHTIG - nur global am Anfang der Datei!
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY

async def forgot_password():
    resend.Emails.send(...)  # ← Einfach nutzen
```

## ❌ Fehler 2: "Ungültiger Link" obwohl Token existiert

**Symptom:** Token ist in DB, aber Verifizierung schlägt fehl

**Ursache:** Timezone-Mismatch bei Expiry-Vergleich

**Lösung:**
```python
# ❌ FALSCH - MongoDB Query mit Timezone-Problem
user = await db.users.find_one({
    "password_reset_token": token,
    "password_reset_expiry": {"$gt": datetime.now(timezone.utc)}
})

# ✅ RICHTIG - Erst finden, dann manuell prüfen
user = await db.users.find_one({"password_reset_token": token})
if user:
    expiry = user.get("password_reset_expiry")
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)
    if expiry <= datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Link abgelaufen")
```

## ❌ Fehler 3: Reset-URL führt zu falscher Domain

**Symptom:** Link in E-Mail zeigt auf alte Preview-URL

**Ursache:** `FRONTEND_URL` wird vom Deployment überschrieben

**Lösung:**
```python
# ❌ FALSCH - Environment Variable wird überschrieben
reset_url = f"{os.environ.get('FRONTEND_URL')}/reset-password?token={token}"

# ✅ RICHTIG - Domain hardcoden
reset_url = f"https://meine-app.online/reset-password?token={reset_token}"
```

## ❌ Fehler 4: E-Mails landen im Spam

**Ursache:** Fehlende oder falsche DNS-Einträge

**Lösung:**
1. Alle 4 DNS-Einträge prüfen (DKIM, MX, SPF, DMARC)
2. DMARC mit `p=none` (nicht `p=reject`)
3. Emoji aus Betreff entfernen
4. In Resend Dashboard "Verified" Status prüfen

## ❌ Fehler 5: Bestimmte Provider (Yahoo, Bluewin) empfangen keine E-Mails

**Symptom:** Gmail funktioniert, andere nicht

**Ursache:** Strenge Spam-Filter bei manchen Providern

**Lösung:**
1. DMARC korrekt konfigurieren
2. Hinweis "Bitte Spam-Ordner prüfen" anzeigen
3. Benutzer bitten, Absender zu Kontakten hinzuzufügen
4. Alternative: Benutzer ermutigen, Gmail zu verwenden

---

# 7. Test-Checkliste

Nach Implementation diese Tests durchführen:

## Funktionale Tests

- [ ] E-Mail an Gmail senden → muss ankommen
- [ ] E-Mail an Yahoo senden → prüfen (oft Spam)
- [ ] E-Mail an Outlook/Hotmail senden → prüfen
- [ ] Reset-Link in E-Mail anklicken → Formular erscheint
- [ ] Ungültigen Token eingeben → Fehlermeldung
- [ ] Abgelaufenen Token verwenden → Fehlermeldung
- [ ] Neues Passwort setzen → Erfolg
- [ ] Mit neuem Passwort einloggen → funktioniert
- [ ] Alten Reset-Link nochmal verwenden → "Ungültig"

## Technische Checks

- [ ] Resend Dashboard: Alle E-Mails zeigen "Delivered"
- [ ] Backend Logs: Keine Fehler bei E-Mail-Versand
- [ ] DNS: Alle 4 Einträge in Resend "Verified"
- [ ] Token wird nach Passwort-Änderung gelöscht

---

# 8. Troubleshooting

## Resend Dashboard prüfen

1. Gehe zu **https://resend.com/emails**
2. Prüfe Status der E-Mails:
   - **Delivered** = Erfolgreich zugestellt (wenn nicht im Posteingang → Spam!)
   - **Bounced** = Adresse existiert nicht
   - **Complained** = Als Spam markiert

## DNS-Einträge prüfen

Online-Tools:
- https://mxtoolbox.com/SuperTool.aspx
- https://dnschecker.org

Prüfen:
- MX Record für `send.meine-app.online`
- TXT Record für `send.meine-app.online` (SPF)
- TXT Record für `resend._domainkey.meine-app.online` (DKIM)
- TXT Record für `_dmarc.meine-app.online` (DMARC)

## Backend Logs prüfen

```bash
tail -n 100 /var/log/supervisor/backend.err.log | grep -i "email\|resend\|reset"
```

## Häufige Log-Meldungen

```
✅ "Password reset email sent to user@example.com" → Alles OK
❌ "Failed to send reset email: API key is invalid" → API Key prüfen
❌ "Failed to send reset email: Domain not verified" → DNS prüfen
```

---

# Zusammenfassung

| Schritt | Aktion | Dauer |
|---------|--------|-------|
| 1 | Resend Account + API Key | 5 min |
| 2 | Domain in Resend hinzufügen | 2 min |
| 3 | 4 DNS-Einträge bei Infomaniak | 10 min |
| 4 | Warten auf Verifizierung | 5 min - 48h |
| 5 | Backend-Code implementieren | 15 min |
| 6 | Frontend-Seiten erstellen | 15 min |
| 7 | Testen | 10 min |

## Die 4 wichtigsten Regeln

1. 🔴 `resend.api_key` **NUR GLOBAL** setzen, nie in Funktionen
2. 🔴 Reset-URL Domain **HARDCODEN**, nicht aus Environment
3. 🔴 Token-Expiry **MANUELL** mit Timezone prüfen
4. 🔴 DMARC mit `p=none` (nie `p=reject`)

---

**Bei Problemen: Diese Anleitung Schritt für Schritt durchgehen spart 2 Tage Debugging!**

---

*Dokumentation erstellt basierend auf realer Debugging-Erfahrung.*
*Wine Pairing App - Januar 2026*
