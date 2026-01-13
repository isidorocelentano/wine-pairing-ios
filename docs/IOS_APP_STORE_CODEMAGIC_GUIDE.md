# iOS App Store Einreichung mit Codemagic - Vollständige Dokumentation

**Erstellt:** 13. Januar 2026  
**App:** Wine Pairing PWA  
**Bundle ID:** online.wine-pairing  
**Team ID:** 9EXPJ92538

---

## Inhaltsverzeichnis

1. [Voraussetzungen](#1-voraussetzungen)
2. [Apple Developer Account Einrichtung](#2-apple-developer-account-einrichtung)
3. [App Store Connect Konfiguration](#3-app-store-connect-konfiguration)
4. [GitHub Repository Setup](#4-github-repository-setup)
5. [Codemagic Einrichtung](#5-codemagic-einrichtung)
6. [Zertifikate und Provisioning Profiles](#6-zertifikate-und-provisioning-profiles)
7. [codemagic.yaml Konfiguration](#7-codemagicyaml-konfiguration)
8. [Build und Deployment](#8-build-und-deployment)
9. [Fehlerbehebung](#9-fehlerbehebung)
10. [Wichtige Daten und Passwörter](#10-wichtige-daten-und-passwörter)

---

## 1. Voraussetzungen

### Erforderliche Accounts

| Account | URL | Kosten |
|---------|-----|--------|
| Apple Developer Account | https://developer.apple.com | $99/Jahr |
| GitHub Account | https://github.com | Kostenlos |
| Codemagic Account | https://codemagic.io | Kostenlos (500 Min/Monat) |

### Erforderliche Software (lokal)

- **GitHub Desktop** - https://desktop.github.com/
- **Texteditor** (Notepad, VS Code, etc.)

### Kein Mac erforderlich!

Diese Anleitung ermöglicht die iOS-App-Einreichung **ohne Mac** durch Nutzung von:
- **PWA Builder** für die iOS-App-Generierung
- **Codemagic** für das Bauen und Signieren in der Cloud

---

## 2. Apple Developer Account Einrichtung

### 2.1 App ID erstellen

1. Öffnen Sie: https://developer.apple.com/account/resources/identifiers/list
2. Klicken Sie auf **"+"** neben "Identifiers"
3. Wählen Sie **"App IDs"** → **Continue**
4. Wählen Sie **"App"** → **Continue**
5. Füllen Sie aus:

| Feld | Wert |
|------|------|
| Description | `Wine Pairing PWA` |
| Bundle ID (Explicit) | `online.wine-pairing` |

6. **Capabilities aktivieren** (wichtig!):
   - ✅ Associated Domains
   - ✅ Push Notifications
   
7. Klicken Sie auf **"Continue"** → **"Register"**

### 2.2 API Key erstellen (für Codemagic)

1. Öffnen Sie: https://appstoreconnect.apple.com
2. Klicken Sie auf **"Benutzer und Zugriff"** → **"Integration"**
3. Klicken Sie auf **"API-Schlüssel erstellen"**
4. Eingaben:

| Feld | Wert |
|------|------|
| Name | `Codemagic` |
| Zugriff | `Admin` |

5. Klicken Sie auf **"Erstellen"**
6. **WICHTIG:** Laden Sie die **.p8 Datei** sofort herunter (nur einmal möglich!)
7. Notieren Sie:
   - **Issuer ID:** `69a6de84-bc2a-47e3-e053-5b8c7c11a4d1`
   - **Key ID:** `F83CCT659H`

---

## 3. App Store Connect Konfiguration

### 3.1 Neue App erstellen

1. Öffnen Sie: https://appstoreconnect.apple.com
2. Klicken Sie auf **"Apps"** → **"+"** → **"Neue App"**
3. Füllen Sie aus:

| Feld | Wert |
|------|------|
| Plattformen | iOS |
| Name | `Wine Pairing PWA` |
| Primärsprache | Deutsch |
| Bundle-ID | `online.wine-pairing` (aus Dropdown) |
| SKU | `winepairing002` |

4. Klicken Sie auf **"Erstellen"**

---

## 4. GitHub Repository Setup

### 4.1 iOS Projekt von PWA Builder

1. Öffnen Sie: https://www.pwabuilder.com/
2. Geben Sie Ihre URL ein: `https://wine-pairing.online`
3. Klicken Sie auf **"Start"**
4. Klicken Sie auf **"Package for stores"**
5. Wählen Sie **"iOS"**
6. Laden Sie das Xcode-Projekt herunter (.zip)

### 4.2 GitHub Repository erstellen

1. Öffnen Sie: https://github.com
2. Klicken Sie auf **"New"** (neues Repository)
3. Eingaben:

| Feld | Wert |
|------|------|
| Repository name | `wine-pairing-ios` |
| Description | `iOS App für Wine Pairing` |
| Public/Private | Nach Wahl |

4. Klicken Sie auf **"Create repository"**

### 4.3 Dateien hochladen (via GitHub Desktop)

1. Öffnen Sie **GitHub Desktop**
2. Klicken Sie auf **"Clone a repository"**
3. Wählen Sie `wine-pairing-ios`
4. Wählen Sie einen lokalen Ordner
5. Klicken Sie auf **"Clone"**
6. Öffnen Sie den Repository-Ordner im Explorer
7. Kopieren Sie **alle Dateien** aus dem PWA Builder `src` Ordner hierher
8. In GitHub Desktop:
   - Summary: `Initial iOS project`
   - Klicken Sie auf **"Commit to main"**
   - Klicken Sie auf **"Push origin"**

### 4.4 Repository-Struktur

```
wine-pairing-ios/
├── Wine Pairing.xcodeproj/
├── Wine Pairing.xcworkspace/
├── Wine Pairing/
│   ├── Assets.xcassets/
│   ├── Info.plist
│   └── ...
├── Podfile
├── codemagic.yaml          ← Wird später erstellt
├── launch-64.png
├── launch-128.png
└── ...
```

---

## 5. Codemagic Einrichtung

### 5.1 Account erstellen

1. Öffnen Sie: https://codemagic.io/
2. Klicken Sie auf **"Sign up with GitHub"**
3. Autorisieren Sie Codemagic für GitHub

### 5.2 App hinzufügen

1. Klicken Sie auf **"Add application"**
2. Wählen Sie **"GitHub"**
3. Wählen Sie `wine-pairing-ios`
4. Wählen Sie **"iOS App"** als Projekttyp
5. Klicken Sie auf **"Finish: Add application"**

### 5.3 Apple Integration verbinden

1. Klicken Sie auf **"Teams"** → **"Personal Account"**
2. Klicken Sie auf **"Integrations"**
3. Bei **"Developer Portal"** klicken Sie auf **"Connect"**
4. Füllen Sie aus:

| Feld | Wert |
|------|------|
| API key name | `Codemagic` |
| Issuer ID | `69a6de84-bc2a-47e3-e053-5b8c7c11a4d1` |
| Key ID | `F83CCT659H` |
| API key | Die .p8 Datei hochladen |

5. Klicken Sie auf **"Save"**

---

## 6. Zertifikate und Provisioning Profiles

### 6.1 Distribution Certificate erstellen (in Codemagic)

**WICHTIG:** Alle alten Distribution Certificates bei Apple zuerst widerrufen!

1. In Codemagic: **"Teams"** → **"Personal Account"** → **"Code signing identities"**
2. Klicken Sie auf **"Generate certificate"**
3. Füllen Sie aus:

| Feld | Wert |
|------|------|
| Reference name | `WinePairingDist` |
| Certificate type | `iOS Distribution` |
| App Store Connect API key | `Codemagic` |

4. Klicken Sie auf **"Create certificate"**
5. **WICHTIG:** Notieren Sie das Passwort und laden Sie die .p12 Datei herunter!

### 6.2 Provisioning Profile erstellen (bei Apple)

1. Öffnen Sie: https://developer.apple.com/account/resources/profiles/list
2. Klicken Sie auf **"+"**
3. Wählen Sie **"App Store Connect"** (unter Distribution) → **Continue**
4. Wählen Sie **"Wine Pairing PWA"** (online.wine-pairing) → **Continue**
5. Wählen Sie das Distribution Certificate → **Continue**
6. Name: `WinePairingPWADist`
7. Klicken Sie auf **"Generate"**

### 6.3 Provisioning Profile in Codemagic laden

1. In Codemagic: **"Teams"** → **"Personal Account"** → **"Code signing identities"**
2. Klicken Sie auf **"iOS provisioning profiles"**
3. Klicken Sie auf **"Fetch profiles"**
4. Wählen Sie **"WinePairingPWADist"**
5. Reference name: `WinePairingPWADist`
6. Klicken Sie auf **"Download selected"**

### 6.4 Überprüfung

Nach erfolgreicher Einrichtung sollten Sie sehen:

**iOS certificates:**
- WinePairingDist ✅

**iOS provisioning profiles:**
- WinePairingPWADist ✅ (mit grünem Haken bei Certificate)

---

## 7. codemagic.yaml Konfiguration

### 7.1 Datei erstellen

Erstellen Sie die Datei `codemagic.yaml` im Root-Verzeichnis des Repositories:

```yaml
workflows:
  ios-workflow:
    name: iOS App Store Build
    max_build_duration: 60
    instance_type: mac_mini_m2
    integrations:
      app_store_connect: Codemagic
    environment:
      ios_signing:
        provisioning_profiles:
          - WinePairingPWADist
        certificates:
          - WinePairingDist
      vars:
        XCODE_WORKSPACE: "Wine Pairing.xcworkspace"
        XCODE_SCHEME: "Wine Pairing"
        TEAM_ID: "9EXPJ92538"
      xcode: latest
      cocoapods: default
    scripts:
      - name: Install CocoaPods dependencies
        script: |
          pod install
      - name: Set Team ID in project
        script: |
          sed -i '' 's/DEVELOPMENT_TEAM = "";/DEVELOPMENT_TEAM = 9EXPJ92538;/g' "Wine Pairing.xcodeproj/project.pbxproj"
          sed -i '' 's/DEVELOPMENT_TEAM = .*;/DEVELOPMENT_TEAM = 9EXPJ92538;/g' "Wine Pairing.xcodeproj/project.pbxproj"
      - name: Set up keychain and profiles
        script: |
          keychain initialize
          keychain add-certificates
          xcode-project use-profiles
      - name: Build iOS App
        script: |
          xcodebuild -workspace "$XCODE_WORKSPACE" \
            -scheme "$XCODE_SCHEME" \
            -configuration Release \
            -archivePath build/Wine\ Pairing.xcarchive \
            DEVELOPMENT_TEAM="9EXPJ92538" \
            archive
      - name: Create IPA
        script: |
          xcode-project build-ipa --workspace "$XCODE_WORKSPACE" --scheme "$XCODE_SCHEME"
    artifacts:
      - build/ios/ipa/*.ipa
      - build/*.xcarchive
    publishing:
      app_store_connect:
        auth: integration
        submit_to_testflight: true
```

### 7.2 Wichtige Anpassungen

Ersetzen Sie folgende Werte mit Ihren eigenen:

| Placeholder | Ihr Wert |
|-------------|----------|
| `WinePairingPWADist` | Ihr Provisioning Profile Reference Name |
| `WinePairingDist` | Ihr Certificate Reference Name |
| `Wine Pairing.xcworkspace` | Ihr Workspace-Name |
| `Wine Pairing.xcodeproj` | Ihr Projekt-Name |
| `Wine Pairing` | Ihr Scheme-Name |
| `9EXPJ92538` | Ihre Team ID |

---

## 8. Build und Deployment

### 8.1 Build starten

1. Öffnen Sie: https://codemagic.io/apps
2. Klicken Sie auf Ihre App
3. Klicken Sie auf **"Start new build"**
4. Wählen Sie:
   - Branch: `main`
   - Workflow: `iOS App Store Build`
5. Klicken Sie auf **"Start new build"**

### 8.2 Build-Prozess

Der Build durchläuft folgende Schritte:

| Schritt | Beschreibung | Dauer |
|---------|--------------|-------|
| Preparing build machine | Mac Mini M2 wird gestartet | ~20s |
| Fetching app sources | Code von GitHub laden | ~2s |
| Set up code signing | Zertifikate laden | ~2s |
| Install CocoaPods | Dependencies installieren | ~25s |
| Set Team ID | Team ID im Projekt setzen | <1s |
| Set up keychain | Keychain konfigurieren | ~2s |
| Build iOS App | App kompilieren | ~45s |
| Create IPA | IPA-Datei erstellen | ~20s |
| Publishing | Zu TestFlight hochladen | ~35s |

**Gesamtdauer:** ca. 2-3 Minuten

### 8.3 Nach dem Build

1. Öffnen Sie: https://appstoreconnect.apple.com
2. Wählen Sie Ihre App
3. Klicken Sie auf **"TestFlight"**
4. Die neue Version sollte unter "Build-Uploads" erscheinen
5. Status: **"Bereit zur Übermittlung"**

---

## 9. Fehlerbehebung

### 9.1 "No profiles for bundle identifier found"

**Ursache:** Bundle ID stimmt nicht überein

**Lösung:**
1. Prüfen Sie die Bundle ID im Xcode-Projekt
2. Prüfen Sie die Bundle ID bei Apple (App ID)
3. Prüfen Sie die Bundle ID in codemagic.yaml
4. Alle drei müssen identisch sein!

### 9.2 "Did not find any certificates"

**Ursache:** Zertifikate nicht korrekt geladen

**Lösung:**
1. Alle alten Zertifikate bei Apple widerrufen
2. In Codemagic: Alle alten Zertifikate löschen
3. Neues Zertifikat in Codemagic **generieren** (nicht fetchen!)
4. Provisioning Profile neu erstellen
5. Provisioning Profile in Codemagic neu laden

### 9.3 "Provisioning profile doesn't include capability"

**Ursache:** App ID hat nicht alle benötigten Capabilities

**Lösung:**
1. Apple Developer Portal → Identifiers
2. App ID bearbeiten
3. Fehlende Capabilities aktivieren:
   - Associated Domains
   - Push Notifications
4. Provisioning Profile löschen und neu erstellen

### 9.4 "Signing requires a development team"

**Ursache:** Team ID fehlt im Xcode-Projekt

**Lösung:**
Der `sed` Befehl in codemagic.yaml setzt die Team ID:
```yaml
- name: Set Team ID in project
  script: |
    sed -i '' 's/DEVELOPMENT_TEAM = "";/DEVELOPMENT_TEAM = IHRE_TEAM_ID;/g' "Projekt.xcodeproj/project.pbxproj"
```

### 9.5 "Cannot save Signing Certificates without private key"

**Ursache:** Versucht, ein bestehendes Zertifikat zu fetchen

**Lösung:**
1. Alle Distribution Certificates bei Apple widerrufen
2. Neues Zertifikat in Codemagic **generieren**
3. Codemagic erstellt und speichert den Private Key automatisch

---

## 10. Wichtige Daten und Passwörter

### Apple Developer Account

| Info | Wert |
|------|------|
| Team ID | `9EXPJ92538` |
| Team Name | Isidoro Celentano |
| Bundle ID | `online.wine-pairing` |

### App Store Connect API

| Info | Wert |
|------|------|
| Key Name | `Codemagic` |
| Issuer ID | `69a6de84-bc2a-47e3-e053-5b8c7c11a4d1` |
| Key ID | `F83CCT659H` |
| .p8 Datei | `AuthKey_F83CCT659H.p8` (sicher aufbewahren!) |

### Codemagic Code Signing

| Info | Wert |
|------|------|
| Certificate Name | `WinePairingDist` |
| Certificate Password | `l9TguP3M` |
| Provisioning Profile | `WinePairingPWADist` |

### GitHub

| Info | Wert |
|------|------|
| Repository | `isidorocelentano/wine-pairing-ios` |
| Branch | `main` |

---

## Anhang: Nützliche Links

- **Apple Developer Portal:** https://developer.apple.com/account
- **App Store Connect:** https://appstoreconnect.apple.com
- **Codemagic:** https://codemagic.io
- **PWA Builder:** https://www.pwabuilder.com
- **GitHub Desktop:** https://desktop.github.com
- **Codemagic Dokumentation:** https://docs.codemagic.io/yaml-code-signing/signing-ios/

---

## Changelog

| Datum | Änderung |
|-------|----------|
| 13.01.2026 | Dokumentation erstellt |
| 12.01.2026 | Erste erfolgreiche Build und TestFlight-Upload |

---

*Diese Dokumentation wurde erstellt für Wine Pairing PWA. Passen Sie die Werte entsprechend Ihrem Projekt an.*
