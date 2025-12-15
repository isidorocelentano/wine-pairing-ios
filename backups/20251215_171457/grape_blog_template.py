# AI Blog Post Template für Rebsorten
# =====================================
# Dieses Template kann verwendet werden, um mit AI (GPT-5.1) 
# hochwertige Blog-Posts für beliebige Rebsorten zu generieren.

## VERWENDUNG
# 1. Kopiere den GENERATION_PROMPT unten
# 2. Ersetze {grape_name} mit der gewünschten Rebsorte
# 3. Füge optionale Informationen in {grape_info} ein
# 4. Sende an GPT-5.1 oder ein ähnliches LLM

## BEISPIEL-AUFRUF (Python):
# ```python
# from emergentintegrations.llm.chat import LlmChat, UserMessage
# 
# chat = LlmChat(
#     api_key=EMERGENT_LLM_KEY,
#     session_id="grape-blog-gen",
#     system_message="Du bist ein leidenschaftlicher Sommelier und Weinautor."
# ).with_model("openai", "gpt-5.1")
#
# prompt = GENERATION_PROMPT.format(
#     grape_name="Pinot Noir",
#     grape_info="Bekannt für Burgund, elegante Rotweine, Aromen von roten Beeren"
# )
# response = await chat.send_message(UserMessage(text=prompt))
# ```

# ===================== GENERATION PROMPT =====================

GENERATION_PROMPT = """
Du bist ein leidenschaftlicher Sommelier und Weinautor. Schreibe einen ausführlichen, emotionalen Blog-Artikel über die Rebsorte "{grape_name}".

## STRUKTUR UND INHALT (Halte dich strikt an diese Gliederung):

### 1. TITEL
Erstelle einen poetischen, einprägsamen Titel mit einem passenden Beinamen für die Rebsorte.
Format: "[Beiname] [Rebsorte]: [Untertitel]"
Beispiel: "Das Chardonnay-Chameleon: Ein Liebesbrief an den König der Weißweine"

### 2. EINLEITUNG (2-3 Absätze)
- Emotionale, einladende Begrüßung der Leser ("Liebe Weinliebhaber...")
- Was macht diese Rebsorte besonders/einzigartig?
- Wecke Neugier und Vorfreude auf die Entdeckungsreise
- Verwende bildhafte Sprache und Metaphern

### 3. DER GLOBETROTTER: Anbaugebiete (1 Hauptabschnitt)
Überschrift: "## 1. Der Globetrotter im Glas: Wo der [Rebsorte] zu Hause ist"

Beschreibe die wichtigsten Anbauregionen mit:
- Ursprungsland/Heimat der Rebsorte (fett hervorheben)
- 3-5 wichtige Anbauländer/-regionen
- Für jede Region: Charakteristischer Stil des Weins
- Terroir-Einfluss auf den Geschmack
- Verwende Ländernamen mit Klammern für Regionen: **Frankreich (Burgund & Champagne):**

### 4. AUSBAUSTUFEN (1 Hauptabschnitt)
Überschrift: "## 2. Der Tanz der Ausbaustufen: [Passender Untertitel]"

Erkläre die verschiedenen Ausbaustile:
- Stahltank vs. Holzfass (mit Unterüberschriften ###)
- Geschmacksunterschiede detailliert beschreiben
- Für welchen Anlass welcher Stil?
- Verwende **Geschmackserlebnis:** für die Beschreibung

### 5. FOOD PAIRING (1 Hauptabschnitt mit Tabelle)
Überschrift: "## 3. Pairing-Empfehlungen: Der perfekte Partner für den [Rebsorte]"

Erstelle eine Markdown-Tabelle mit mindestens 3 Gerichten:
| Gericht | [Rebsorte]-Stil | Warum es funktioniert |
|---|---|---|
| **[Gericht 1]** | [Stil] | [Emotionale Erklärung] |

Erkläre emotional, warum die Kombinationen harmonieren.

### 6. FAQ (10 Fragen)
Überschrift: "## 4. FAQ – 10 Fragen für [Rebsorte]-Liebhaber"

Beantworte typische Fragen zu dieser Rebsorte:
Format: **❓ [Frage]**
Antwort direkt darunter (keine Nummerierung)

Themen:
1. Trocken oder süß?
2. Serviertemperatur?
3. Lagerungspotenzial?
4. Geschmacksprofil?
5. Verwandte Rebsorten/Synonyme?
6. Preis-Leistungs-Tipps?
7. Besondere Eigenschaften?
8. Häufige Missverständnisse?
9. Regionale Unterschiede?
10. Perfekte Trinksituationen?

## STILRICHTLINIEN:

1. **Tonalität:** Leidenschaftlich, einladend, poetisch – aber nicht übertrieben
2. **Zielgruppe:** Weinliebhaber und Neugierige, keine Experten
3. **Sprache:** Deutsch, Du-Form, lebhaft und bildhaft
4. **Emoji-Nutzung:** Sparsam, nur bei FAQ-Fragen (❓)
5. **Fachbegriffe:** Immer erklären, nicht voraussetzen
6. **Länge:** Ca. 1500-2000 Wörter
7. **Markdown:** Verwende ##, ###, **, |, - für Formatierung

## ZUSÄTZLICHE INFORMATIONEN ZUR REBSORTE:
{grape_info}

## OUTPUT FORMAT:
Gib den fertigen Artikel zurück, beginnend mit dem Titel (ohne ##).
Verwende durchgehend Markdown-Formatierung.
"""

# ===================== TRANSLATION PROMPT =====================

TRANSLATION_PROMPT = """
Übersetze den folgenden deutschen Weinblog-Artikel ins {target_language}.

## WICHTIGE REGELN:
1. Behalte die gesamte Struktur und Formatierung (Markdown) bei
2. Behalte alle Emoji bei (❓ etc.)
3. Übersetze Weinnamen und Regionen NICHT (z.B. "Chablis", "Puligny-Montrachet", "Champagne")
4. Übersetze Fachbegriffe korrekt und füge ggf. kurze Erklärungen hinzu
5. Passe die Anrede an die Zielsprache an:
   - Deutsch: Du-Form
   - Englisch: You
   - Französisch: Vous (formal) oder Tu (informal, je nach Kontext)
6. Tabellen-Format beibehalten (| ... | ... |)
7. Der Ton soll warm, einladend und leidenschaftlich bleiben

## FORMAT DER AUSGABE:
Gib die Übersetzung als JSON zurück:
{{
  "title": "Übersetzter Titel",
  "excerpt": "Übersetztes Excerpt (1-2 Sätze, max 200 Zeichen)",
  "content": "Übersetzter vollständiger Artikel im Markdown-Format"
}}

## DEUTSCHER ORIGINAL-ARTIKEL:

### Titel:
{title}

### Excerpt:
{excerpt}

### Inhalt:
{content}

## OUTPUT:
Gib NUR das JSON zurück, keine zusätzlichen Kommentare oder Erklärungen.
"""

# ===================== BLOG POST METADATA TEMPLATE =====================

BLOG_POST_TEMPLATE = {
    "slug": "",  # kebab-case-ohne-umlaute, z.B. "pinot-noir-koenigin-rotweine"
    "title": "",  # Deutscher Titel
    "title_en": "",  # Englischer Titel
    "title_fr": "",  # Französischer Titel
    "excerpt": "",  # Kurze Zusammenfassung (DE)
    "excerpt_en": "",
    "excerpt_fr": "",
    "content": "",  # Vollständiger Artikel (DE, Markdown)
    "content_en": "",
    "content_fr": "",
    "image_url": "",  # Unsplash URL oder eigenes Bild
    "category": "wissen",  # wissen, tipps, pairings, regionen
    "tags": [],  # z.B. ["pinot-noir", "rotwein", "burgund", "rebsorten"]
    "author": "Sommelier Team",
    "published": True
}

# ===================== BEISPIEL: VOLLSTÄNDIGER WORKFLOW =====================

EXAMPLE_WORKFLOW = """
## Vollständiger Workflow zur Blog-Post-Erstellung:

1. ARTIKEL GENERIEREN (Deutsch):
   prompt = GENERATION_PROMPT.format(
       grape_name="Riesling",
       grape_info="Deutsche Königin der Weißweine, Mosel, Rheingau, von trocken bis edelsüß"
   )
   german_article = await chat.send_message(UserMessage(text=prompt))

2. TITEL UND EXCERPT EXTRAHIEREN:
   - Titel: Erste Zeile des Artikels
   - Excerpt: Erste 1-2 Sätze der Einleitung

3. ÜBERSETZEN (Englisch):
   en_prompt = TRANSLATION_PROMPT.format(
       target_language="Englisch (British English)",
       title=german_title,
       excerpt=german_excerpt,
       content=german_article
   )
   en_translation = await chat.send_message(UserMessage(text=en_prompt))

4. ÜBERSETZEN (Französisch):
   fr_prompt = TRANSLATION_PROMPT.format(
       target_language="Französisch",
       title=german_title,
       excerpt=german_excerpt,
       content=german_article
   )
   fr_translation = await chat.send_message(UserMessage(text=fr_prompt))

5. IN DATENBANK SPEICHERN:
   blog_post = {
       "id": str(uuid.uuid4()),
       "slug": "riesling-koenigin-weissweine",
       "title": german_title,
       "title_en": en_translation["title"],
       "title_fr": fr_translation["title"],
       ...
   }
   await db.blog_posts.insert_one(blog_post)

6. BACKUP ERSTELLEN:
   python3 database_backup.py
"""

# ===================== REBSORTEN-IDEEN FÜR ZUKÜNFTIGE POSTS =====================

FUTURE_BLOG_IDEAS = [
    ("Pinot Noir", "Die elegante Königin von Burgund, bekannt für Finesse und rote Beeren"),
    ("Riesling", "Deutschlands Stolz, von knochentrocken bis edelsüß, Petrolnote"),
    ("Cabernet Sauvignon", "Der kraftvolle König von Bordeaux, Cassis und Zedernholz"),
    ("Merlot", "Der samtweiche Verführer, Pflaumen und Schokolade"),
    ("Sauvignon Blanc", "Der frische Weckruf, Stachelbeere und grüne Paprika"),
    ("Syrah/Shiraz", "Zwei Gesichter einer Traube, von elegant bis opulent"),
    ("Grüner Veltliner", "Österreichs Signature, weißer Pfeffer und Würze"),
    ("Nebbiolo", "Der Aristokrat des Piemonts, Rosen und Teer"),
    ("Tempranillo", "Spaniens roter Stolz, Rioja und Ribera del Duero"),
    ("Sangiovese", "Das Herz der Toskana, Kirschen und Kräuter"),
]
