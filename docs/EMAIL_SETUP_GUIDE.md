# 📧 E-Mail-Funktionalität (Resend) - Komplette Anleitung

**Erstellt:** 07.01.2026  
**Basierend auf:** 2 Tage Debugging-Erfahrung mit Wine Pairing App  
**Ziel:** Passwort-Reset und andere E-Mail-Funktionen zuverlässig implementieren

---

## 🎯 Übersicht

Diese Anleitung beschreibt, wie man E-Mail-Versand mit **Resend** in einer Emergent-App (FastAPI + React + MongoDB) korrekt einrichtet.

---

## Teil 1: Resend Account & Domain Setup

### 1.1 Resend Account erstellen
1. Gehe zu **https://resend.com**
2. Erstelle einen Account
3. Gehe zu **API Keys** → Erstelle einen neuen API Key
4. Kopiere den Key (beginnt mit `re_...`)

### 1.2 Domain hinzufügen
1. In Resend: **Domains** → **Add Domain**
2. Gib deine Domain ein (z.B. `meine-app.online`)
3. Wähle Region (EU empfohlen: `eu-west-1`)
4. Resend zeigt dir die benötigten DNS-Einträge

---

## Teil 2: DNS-Konfiguration (KRITISCH!)

### 2.1 Erforderliche DNS-Einträge

Bei deinem Domain-Provider (z.B. Infomaniak) müssen **4 Einträge** hinzugefügt werden:

| # | Typ | Name/Quelle | Wert/Ziel | Priorität |
|---|-----|-------------|-----------|-----------|
| 1 | **TXT** | `resend._domainkey` | (von Resend bereitgestellt - DKIM Key) | - |
| 2 | **MX** | `send` | `feedback-smtp.eu-west-1.amazonses.com` | 10 |
| 3 | **TXT** | `send` | `v=spf1 include:amazonses.com ~all` | - |
| 4 | **TXT** | `_dmarc` | `v=DMARC1;p=none` | - |

### 2.2 Wichtige Hinweise zu DNS

⚠️ **DMARC-Einstellung:**
- Verwende `p=none` (nicht `p=reject`!)
- `p=reject` blockiert E-Mails!

⚠️ **Wartezeit:**
- DNS-Änderungen brauchen bis zu 24-48 Stunden
- In Resend auf "Verify" klicken um Status zu prüfen

### 2.3 Verifizierung in Resend
Nach DNS-Setup sollten alle Einträge als **"Verified"** erscheinen:
- ✅ DKIM - Verified
- ✅ MX (send) - Verified  
- ✅ SPF (send) - Verified

---

## Teil 3: Backend-Implementation

### 3.1 Dependencies installieren
```bash
pip install resend
```

In `requirements.txt` hinzufügen:
```
resend
```

### 3.2 Environment Variables (.env)
```env
# Resend Email Service
RESEND_API_KEY=re_DEIN_API_KEY_HIER
SENDER_EMAIL=noreply@deine-domain.online
```

### 3.3 Backend Code (server.py)

**⚠️ KRITISCH: Diese Fehler vermeiden!**

```python
import resend
import secrets
from datetime import datetime, timezone, timedelta

# ===== GLOBAL INITIALIZATION (AM ANFANG DER DATEI) =====
RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'noreply@deine-domain.online')

# API Key EINMAL global setzen - NICHT in Funktionen!
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY


# ===== PASSWORT VERGESSEN ENDPOINT =====
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
    
    # Reset URL - DOMAIN HARDCODEN für Deployment-Stabilität!
    reset_url = f"https://DEINE-DOMAIN.online/reset-password?token={reset_token}"
    
    # Email senden
    # ⚠️ WICHTIG: resend.api_key NICHT hier setzen! Verursacht Probleme in Produktion!
    try:
        resend.Emails.send({
            "from": f"App Name <{SENDER_EMAIL}>",
            "to": [email],
            "subject": "Passwort zurücksetzen",
            "html": f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #333;">Passwort zurücksetzen</h2>
                <p>Klicken Sie auf den Button um ein neues Passwort zu erstellen:</p>
                <p style="margin: 30px 0;">
                    <a href="{reset_url}" 
                       style="background-color: #007bff; color: white; padding: 15px 30px; 
                              text-decoration: none; border-radius: 5px;">
                        Neues Passwort erstellen
                    </a>
                </p>
                <p style="color: #666; font-size: 13px;">
                    Link gültig für 1 Stunde. Falls Sie dies nicht angefordert haben, ignorieren Sie diese E-Mail.
                </p>
            </div>
            """
        })
        logger.info(f"Password reset email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send reset email: {e}")
    
    return success_message


# ===== TOKEN VERIFIZIEREN =====
@api_router.get("/auth/verify-reset-token/{token}")
async def verify_reset_token(token: str):
    """Prüft ob Reset-Token gültig ist."""
    # Token suchen (ohne Expiry-Check in Query wegen Timezone-Problemen)
    user = await db.users.find_one({"password_reset_token": token})
    
    if not user:
        raise HTTPException(status_code=400, detail="Ungültiger Link")
    
    # Expiry manuell prüfen (Timezone-sicher!)
    expiry = user.get("password_reset_expiry")
    if expiry:
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
        if expiry <= datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Link abgelaufen")
    
    return {"valid": True, "email": user.get("email", "")[:3] + "***"}


# ===== PASSWORT ZURÜCKSETZEN =====
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

## Teil 4: Frontend-Implementation

### 4.1 ForgotPasswordPage.js
```jsx
import React, { useState } from 'react';
import axios from 'axios';
import { API } from '@/config/api';

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
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div>
        <h2>E-Mail gesendet!</h2>
        <p>Falls ein Account existiert, haben wir einen Reset-Link gesendet.</p>
        <p><strong>Bitte prüfen Sie auch Ihren Spam-Ordner!</strong></p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Passwort vergessen</h2>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Ihre E-Mail-Adresse"
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Wird gesendet...' : 'Reset-Link anfordern'}
      </button>
    </form>
  );
}
```

### 4.2 ResetPasswordPage.js
```jsx
import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API } from '@/config/api';

function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');
  
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [tokenValid, setTokenValid] = useState(null);
  const [loading, setLoading] = useState(true);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    // Token verifizieren
    const verifyToken = async () => {
      try {
        await axios.get(`${API}/auth/verify-reset-token/${token}`);
        setTokenValid(true);
      } catch {
        setTokenValid(false);
      } finally {
        setLoading(false);
      }
    };
    
    if (token) verifyToken();
    else setLoading(false);
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert('Passwörter stimmen nicht überein');
      return;
    }
    
    try {
      await axios.post(`${API}/auth/reset-password`, {
        token,
        new_password: password
      });
      setSuccess(true);
      setTimeout(() => navigate('/login'), 3000);
    } catch (error) {
      alert(error.response?.data?.detail || 'Fehler beim Zurücksetzen');
    }
  };

  if (loading) return <p>Laden...</p>;
  if (!token || !tokenValid) return <p>Ungültiger oder abgelaufener Link.</p>;
  if (success) return <p>Passwort geändert! Weiterleitung zum Login...</p>;

  return (
    <form onSubmit={handleSubmit}>
      <h2>Neues Passwort setzen</h2>
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Neues Passwort"
        minLength={6}
        required
      />
      <input
        type="password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
        placeholder="Passwort bestätigen"
        required
      />
      <button type="submit">Passwort ändern</button>
    </form>
  );
}
```

### 4.3 Routes (App.js)
```jsx
<Route path="/forgot-password" element={<ForgotPasswordPage />} />
<Route path="/reset-password" element={<ResetPasswordPage />} />
```

---

## Teil 5: Häufige Fehler & Lösungen

### ❌ Fehler 1: E-Mails werden nicht gesendet (Produktion)
**Ursache:** `resend.api_key = ...` wird innerhalb der Funktion gesetzt
**Lösung:** API Key NUR einmal global am Anfang der Datei setzen!

### ❌ Fehler 2: "Ungültiger Link" obwohl Token existiert
**Ursache:** Timezone-Mismatch bei Expiry-Vergleich
**Lösung:** Expiry manuell prüfen mit `expiry.replace(tzinfo=timezone.utc)`

### ❌ Fehler 3: E-Mails landen im Spam
**Ursache:** Fehlende DNS-Einträge
**Lösung:** Alle 4 DNS-Einträge hinzufügen (DKIM, MX, SPF, DMARC)

### ❌ Fehler 4: Reset-URL führt zu falscher Domain
**Ursache:** `FRONTEND_URL` wird vom Deployment überschrieben
**Lösung:** Domain im Code hardcoden: `f"https://DEINE-DOMAIN.online/reset-password?token={token}"`

### ❌ Fehler 5: Yahoo/Bluewin empfangen keine E-Mails
**Ursache:** Strenge Spam-Filter dieser Provider
**Lösung:** 
1. DMARC mit `p=none` konfigurieren
2. Emoji aus Betreff entfernen
3. Benutzer auf Spam-Ordner hinweisen
4. Gmail funktioniert zuverlässiger

---

## Teil 6: Test-Checkliste

Nach Implementation diese Tests durchführen:

- [ ] E-Mail an Gmail senden → muss ankommen
- [ ] E-Mail an Yahoo senden → prüfen (oft Spam)
- [ ] E-Mail an Bluewin senden → prüfen (oft Spam)
- [ ] Reset-Link anklicken → Formular muss erscheinen
- [ ] Neues Passwort setzen → muss funktionieren
- [ ] Mit neuem Passwort einloggen → muss funktionieren
- [ ] Alten Link nochmal verwenden → muss "Ungültig" zeigen

---

## Teil 7: Resend Dashboard

Unter **https://resend.com/emails** siehst du:
- Alle gesendeten E-Mails
- Status: `Delivered`, `Bounced`, `Complained`
- Wenn "Delivered" aber nicht angekommen → Spam-Ordner!

---

## Zusammenfassung

| Schritt | Was tun |
|---------|---------|
| 1 | Resend Account + API Key erstellen |
| 2 | Domain in Resend hinzufügen |
| 3 | 4 DNS-Einträge konfigurieren (DKIM, MX, SPF, DMARC) |
| 4 | In Resend verifizieren (alle grün) |
| 5 | Backend-Code implementieren (API Key GLOBAL setzen!) |
| 6 | Frontend-Seiten erstellen |
| 7 | Testen mit verschiedenen E-Mail-Providern |

---

**Erstellt basierend auf realer Debugging-Erfahrung mit Wine Pairing App.**  
**Bei Fragen: Diese Anleitung befolgen vermeidet 2 Tage Debugging!**
