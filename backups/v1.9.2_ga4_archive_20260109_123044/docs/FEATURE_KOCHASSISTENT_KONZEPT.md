# 🍳 Feature-Konzept: Kochassistent / Kochpartner

**Status:** 📋 GEPLANT (nicht implementiert)  
**Erstellt:** 08. Januar 2026  
**Priorität:** P3 (Backlog)  
**Zielgruppe:** Pro-User  

---

## 📖 Übersicht

Ein KI-gestützter Kochassistent, der Benutzer bei der Menü-Auswahl und beim Kochen unterstützt. Das Feature verbindet sich nahtlos mit der bestehenden Weinempfehlung und schafft ein ganzheitliches kulinarisches Erlebnis.

### Kernidee
> User wählt Küche → bekommt Rezeptvorschläge → wählt Gericht → erhält Rezept + passenden Wein

---

## 🎯 MVP-Umfang (Phase 1)

### Enthalten ✅
- Küchen-Auswahl (6-8 Optionen)
- 3 Rezeptvorschläge basierend auf Küche
- Vollständiges Rezept mit Zutaten & Anleitung
- Kurze Geschichte zum Gericht
- Integrierte Weinempfehlung (nutzt bestehende Pairing-Logik)

### Nicht enthalten ❌ (Phase 2+)
- Zutaten-basierte Suche ("Was kann ich mit X kochen?")
- Nutritional Information
- Dietary Variations (glutenfrei, vegan)
- Präsentations-Tipps
- Multi-Turn-Konversation für Rückfragen

---

## 🤖 MVP-Prompt (Vereinfacht)

```
<role>
Du bist ein freundlicher Kochpartner und Experte für internationale Küche. Du hilfst Benutzern, das perfekte Gericht zu finden und führst sie Schritt für Schritt durch das Rezept. Am Ende empfiehlst du passende Weine.
</role>

<context>
Der Benutzer nutzt wine-pairing.online und möchte kochen. Er hat eine Küche gewählt und erwartet konkrete, umsetzbare Rezepte mit Weinempfehlung.
</context>

<input>
Küche: {cuisine}
Sprache: {language}
</input>

<instructions>
1. Begrüße den Benutzer kurz und bestätige die gewählte Küche.

2. Präsentiere genau 3 Rezeptvorschläge als nummerierte Liste:
   - Titel des Gerichts
   - 1 Satz Beschreibung
   - Schwierigkeit (⭐ Einfach / ⭐⭐ Mittel / ⭐⭐⭐ Anspruchsvoll)
   - Zeitaufwand

3. Frage: "Welches Gericht möchtest du kochen? (1, 2 oder 3)"

4. Nach der Auswahl, liefere das vollständige Rezept im format unten.
</instructions>

<output_format>
# 🍽️ {Rezeptname}

## ⏱️ Übersicht
- **Schwierigkeit:** {⭐/⭐⭐/⭐⭐⭐}
- **Zubereitungszeit:** {XX} Minuten
- **Portionen:** {X} Personen

## 🛒 Zutaten
- {Zutat 1}: {Menge}
- {Zutat 2}: {Menge}
- ...

## 👨‍🍳 Zubereitung
1. {Schritt 1 mit Zeit/Temperatur wenn nötig}
2. {Schritt 2}
3. ...

## 📜 Geschichte
{2-3 Sätze zur Herkunft und Tradition des Gerichts}

## 🍷 Weinempfehlung
**Perfekter Begleiter:** {Weintyp/Region}
{1-2 Sätze warum dieser Wein passt}

**Alternative:** {Zweite Option}
</output_format>

<constraints>
- Halte die Rezepte realistisch für Hobbyköche
- Verwende gängige Zutaten (keine Spezialitäten ohne Hinweis)
- Gib präzise Mengen, Zeiten und Temperaturen an
- Die Weinempfehlung muss zum Gericht passen
- Antworte in der Sprache des Benutzers
</constraints>
```

---

## 🖥️ UI/UX-Konzept

### Navigation
```
Bestehende Navigation:
☰ | 🏠 | 🍽️ Pairing | 🍷 Keller | 👥 Community | 👤 Profil | 🤖 Claude

Neu (für Pro-User):
☰ | 🏠 | 🍽️ Pairing | 🍳 Kochen | 🍷 Keller | 👥 Community | 👤 Profil | 🤖 Claude
                        ^^^^^^^^
                        NEU (Pro)
```

### Seiten-Flow

**Seite 1: Küchen-Auswahl** (`/kochen` oder `/cook`)
```
┌─────────────────────────────────────────┐
│  🍳 Was möchtest du heute kochen?       │
│                                         │
│  Wähle eine Küche:                      │
│                                         │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │
│  │ 🇮🇹  │ │ 🇯🇵  │ │ 🇲🇽  │ │ 🇮🇳  │       │
│  │Ital.│ │Japan│ │Mex. │ │Ind. │       │
│  └─────┘ └─────┘ └─────┘ └─────┘       │
│                                         │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │
│  │ 🇬🇷  │ │ 🇹🇭  │ │ 🇫🇷  │ │ 🇩🇪  │       │
│  │Grie.│ │Thai │ │Franz│ │Deut.│       │
│  └─────┘ └─────┘ └─────┘ └─────┘       │
│                                         │
│  ⭐ Pro-Feature                         │
└─────────────────────────────────────────┘
```

**Seite 2: Rezeptvorschläge** (nach Küchen-Auswahl)
```
┌─────────────────────────────────────────┐
│  🇮🇹 Italienische Küche                 │
│                                         │
│  Hier sind 3 Vorschläge für dich:       │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │ 1. Ossobuco alla Milanese       │    │
│  │    Geschmorte Kalbshaxe         │    │
│  │    ⭐⭐ Mittel · 2.5 Std         │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │ 2. Pasta Cacio e Pepe           │    │
│  │    Römische Käse-Pfeffer-Pasta  │    │
│  │    ⭐ Einfach · 25 Min          │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │ 3. Saltimbocca alla Romana      │    │
│  │    Kalbsschnitzel mit Salbei    │    │
│  │    ⭐⭐ Mittel · 45 Min          │    │
│  └─────────────────────────────────┘    │
│                                         │
└─────────────────────────────────────────┘
```

**Seite 3: Vollständiges Rezept** (nach Auswahl)
```
┌─────────────────────────────────────────┐
│  🍽️ Pasta Cacio e Pepe                  │
│                                         │
│  ⏱️ 25 Min · 👥 4 Portionen · ⭐ Einfach │
│                                         │
│  ─────────────────────────────────────  │
│                                         │
│  🛒 ZUTATEN                             │
│  · 400g Spaghetti                       │
│  · 200g Pecorino Romano                 │
│  · 2 TL schwarzer Pfeffer               │
│  · Salz, Olivenöl                       │
│                                         │
│  ─────────────────────────────────────  │
│                                         │
│  👨‍🍳 ZUBEREITUNG                         │
│  1. Wasser aufkochen, salzen...         │
│  2. Pfeffer rösten (2 Min)...           │
│  3. ...                                 │
│                                         │
│  ─────────────────────────────────────  │
│                                         │
│  📜 GESCHICHTE                          │
│  Cacio e Pepe stammt aus Rom...         │
│                                         │
│  ─────────────────────────────────────  │
│                                         │
│  🍷 WEINEMPFEHLUNG                      │
│  ┌─────────────────────────────────┐    │
│  │ Frascati Superiore              │    │
│  │ Frischer Weißwein aus Latium    │    │
│  │                                 │    │
│  │ [🍷 Mehr Weinoptionen]          │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ─────────────────────────────────────  │
│                                         │
│  [📤 Rezept teilen] [🔖 Speichern]      │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🔗 Integration mit bestehenden Features

### 1. Weinempfehlung-Verknüpfung
```javascript
// Nach Rezept-Generierung: Automatisch Pairing aufrufen
const wineRecommendation = await getPairing({
  dish: recipe.name,
  cuisine: selectedCuisine,
  useWineCellar: user.hasWinesInCellar
});
```

### 2. "Aus meinem Keller" Option
- Wenn User Weine im Keller hat → Option anzeigen
- "Hast du einen passenden Wein? Schau in deinem Keller!"

### 3. Rezept-Speicherung
- Neue Collection: `saved_recipes`
- User kann Lieblingsrezepte speichern
- Später: Einkaufsliste generieren

### 4. Share-Integration
- Rezept + Weinempfehlung teilen
- Nutzt bestehende ShareButtons-Komponente

---

## 💰 Kosten-Kalkulation

### Token-Verbrauch (geschätzt)
| Phase | Input Tokens | Output Tokens | Gesamt |
|-------|--------------|---------------|--------|
| Rezeptvorschläge | ~500 | ~300 | ~800 |
| Vollständiges Rezept | ~200 | ~800 | ~1000 |
| **Total pro Nutzung** | ~700 | ~1100 | **~1800** |

### Vergleich mit bestehenden Features
| Feature | Tokens/Nutzung |
|---------|----------------|
| Standard Pairing | ~500-800 |
| Chat (pro Nachricht) | ~300-500 |
| **Kochassistent** | **~1800** |

### Empfehlung
- **Pro-Only Feature** (rechtfertigt höhere Kosten)
- Oder: **3 Kochassistent-Nutzungen/Tag für Basic**

---

## 📁 Technische Implementation (für später)

### Neue Dateien
```
frontend/src/pages/CookingAssistantPage.js    # Hauptseite
frontend/src/components/CuisineSelector.js    # Küchen-Auswahl Grid
frontend/src/components/RecipeCard.js         # Rezept-Vorschau Karte
frontend/src/components/FullRecipe.js         # Vollständiges Rezept

backend/server.py                             # Neue Endpoints
  - POST /api/cooking/suggestions             # Rezeptvorschläge
  - POST /api/cooking/recipe                  # Vollständiges Rezept
  - GET  /api/cooking/saved                   # Gespeicherte Rezepte
  - POST /api/cooking/save                    # Rezept speichern
```

### Datenbank-Schema
```javascript
// Collection: saved_recipes
{
  id: "uuid",
  user_id: "user-uuid",
  recipe_name: "Pasta Cacio e Pepe",
  cuisine: "italian",
  difficulty: "easy",
  prep_time: 25,
  servings: 4,
  ingredients: [...],
  instructions: [...],
  history: "...",
  wine_pairing: {
    primary: "Frascati Superiore",
    alternative: "Vermentino"
  },
  created_at: "2026-01-08T...",
  times_cooked: 0  // User kann markieren wenn gekocht
}
```

### API-Endpoints

```python
# POST /api/cooking/suggestions
# Request:
{
  "cuisine": "italian",
  "language": "de"
}

# Response:
{
  "cuisine": "italian",
  "cuisine_name": "Italienisch",
  "suggestions": [
    {
      "id": 1,
      "name": "Ossobuco alla Milanese",
      "description": "Geschmorte Kalbshaxe mit Gremolata",
      "difficulty": "medium",
      "prep_time": 150,
      "difficulty_stars": "⭐⭐"
    },
    // ... 2 weitere
  ]
}

# POST /api/cooking/recipe
# Request:
{
  "cuisine": "italian",
  "recipe_id": 2,
  "language": "de"
}

# Response:
{
  "name": "Pasta Cacio e Pepe",
  "difficulty": "easy",
  "prep_time": 25,
  "servings": 4,
  "ingredients": [
    {"item": "Spaghetti", "amount": "400g"},
    // ...
  ],
  "instructions": [
    {"step": 1, "text": "Wasser aufkochen...", "time": "10 Min"},
    // ...
  ],
  "history": "Cacio e Pepe ist ein traditionelles...",
  "wine_pairing": {
    "primary": {
      "name": "Frascati Superiore",
      "type": "Weißwein",
      "reason": "Die frische Säure..."
    },
    "alternative": {
      "name": "Vermentino",
      "type": "Weißwein",
      "reason": "..."
    }
  }
}
```

---

## 🌍 Mehrsprachigkeit

### Küchen-Namen
| Code | DE | EN | FR |
|------|----|----|-----|
| italian | Italienisch | Italian | Italien |
| japanese | Japanisch | Japanese | Japonais |
| mexican | Mexikanisch | Mexican | Mexicain |
| indian | Indisch | Indian | Indien |
| greek | Griechisch | Greek | Grec |
| thai | Thailändisch | Thai | Thaïlandais |
| french | Französisch | French | Français |
| german | Deutsch | German | Allemand |

### UI-Texte
```javascript
const texts = {
  de: {
    title: "Was möchtest du heute kochen?",
    subtitle: "Wähle eine Küche:",
    suggestions_title: "Hier sind 3 Vorschläge für dich:",
    difficulty: { easy: "Einfach", medium: "Mittel", hard: "Anspruchsvoll" },
    sections: {
      ingredients: "Zutaten",
      instructions: "Zubereitung",
      history: "Geschichte",
      wine: "Weinempfehlung"
    },
    pro_badge: "Pro-Feature"
  },
  en: { ... },
  fr: { ... }
};
```

---

## 📅 Roadmap

### Phase 1: MVP (wenn aktiviert)
- [ ] Küchen-Auswahl (8 Küchen)
- [ ] 3 Rezeptvorschläge pro Küche
- [ ] Vollständiges Rezept
- [ ] Basis-Weinempfehlung
- [ ] Pro-Only Gate

### Phase 2: Erweiterung
- [ ] Zutaten-basierte Suche
- [ ] Rezept-Speicherung
- [ ] Einkaufsliste generieren
- [ ] Mehr Küchen (12-15)

### Phase 3: Premium
- [ ] Nutritional Information
- [ ] Dietary Variations
- [ ] Schritt-für-Schritt Modus mit Timer
- [ ] Foto-Upload von Ergebnis

---

## ✅ Checkliste für Go-Live

- [ ] Backend-Endpoints implementiert
- [ ] Frontend-Seite erstellt
- [ ] Navigation-Link hinzugefügt (Pro-Only)
- [ ] Prompt getestet und optimiert
- [ ] Mehrsprachigkeit vollständig
- [ ] Token-Kosten überwacht
- [ ] Pro-Gate funktioniert
- [ ] Mobile-Optimierung
- [ ] Dokumentation aktualisiert

---

## 📝 Notizen

**Original-Prompt vom Benutzer:** Der ursprüngliche, ausführliche Prompt ist sehr gut durchdacht. Für Phase 2+ können folgende Elemente hinzugefügt werden:
- Nutritional Information
- Dietary Variations (glutenfrei, vegan)
- Präsentations-Tipps
- Pantry-Check für spezielle Zutaten

**Entscheidung am 08.01.2026:** Feature wird vorerst zurückgestellt, um die App nicht zu überladen. Kann jederzeit aktiviert werden, wenn gewünscht.

---

*Dokument erstellt: 08.01.2026*  
*Letzte Aktualisierung: 08.01.2026*
