"""
Create Chardonnay Blog Post with translations
"""
import asyncio
import os
import json
import re
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from emergentintegrations.llm.chat import LlmChat, UserMessage
import uuid
from datetime import datetime, timezone

# Load environment
ROOT_DIR = Path(__file__).parent
with open(ROOT_DIR / '.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value.strip('"')

# MongoDB connection
client = AsyncIOMotorClient(os.environ.get('MONGO_URL'))
db = client[os.environ.get('DB_NAME', 'test_database')]
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

# ===================== GERMAN CONTENT =====================

CHARDONNAY_TITLE_DE = "Das Chardonnay-Chameleon: Ein Liebesbrief an den König der Weißweine"

CHARDONNAY_EXCERPT_DE = "Keine andere weiße Rebsorte verkörpert Vielseitigkeit und Prestige wie das wundersame Chardonnay-Chameleon. Von kühlen Burgunder-Kellern bis zur sengenden Sonne Kaliforniens – entdecken Sie, warum dieser Kultwein niemals langweilig wird."

CHARDONNAY_CONTENT_DE = """## Liebe Weinliebhaber, Geniesser und Weltenbummler des Geschmacks!

Es gibt Rebsorten, die flüstern. Und es gibt den Chardonnay, der Geschichten erzählt – von kühlen Burgunder-Kellern, der sengenden Sonne Kaliforniens und dem pulsierenden Leben in einem Glas Champagner. Keine andere weiße Rebsorte verkörpert Vielseitigkeit und Prestige wie dieses wundersame Chardonnay-Chameleon.

Vergessen Sie trockene Fachbücher und chemische Analysen. Beim Chardonnay geht es um pure Trinkfreude, um Textur, um das Gefühl von Eleganz und Luxus auf der Zunge. Lassen Sie uns gemeinsam entdecken, warum dieser Kultwein niemals langweilig wird.

## 1. Der Globetrotter im Glas: Wo der Chardonnay zu Hause ist

Der Chardonnay hat keine Angst vor langen Reisen. Er ist ein echter Weltenbummler und passt sich überall an, nimmt das Terroir seiner Heimat auf und verwandelt es in unverwechselbaren Charakter.

**Frankreich (Burgund & Champagne):** Dies ist seine Wiege und das Epizentrum der Finesse und Mineralität. Im Chablis schmeckt er nach Feuerstein, Kreide und purer Klarheit. An der Côte de Beaune (Puligny-Montrachet!) erreicht er eine majestätische Dichte und Struktur, die ihn zum Maßstab für alle anderen macht. Ohne ihn gäbe es auch keinen Champagner – seine Säure und Eleganz sind die Basis für den Luxus.

**USA (Kalifornien):** Hier liebt er es warm und sonnig. Die Weine sind oft vollmundiger, opulenter und zeigen intensive Noten von reifen Ananas, Mango und Honigmelone.

**Australien & Neuseeland:** Von den kühlen Lagen (Margaret River, Adelaide Hills) kommen balancierte, lebendige Stile, während wärmere Regionen oft zugängliche, fruchtbetonte Blockbuster liefern.

**Italien (Südtirol), Österreich und Chile/Südafrika:** Überall auf der Welt produziert er charakterstarke, spannende Weißweine, die seine Fähigkeit, das Klima zu spiegeln, eindrucksvoll unter Beweis stellen.

## 2. Der Tanz der Ausbaustufen: Vom Stahltank zum Butterfass

Das Geheimnis des Chardonnays liegt in seiner Fähigkeit, sich der Vorstellungskraft des Winzers hinzugeben. Die zwei wichtigsten Ausbaustufen bestimmen, ob Sie einen knackigen, frischen Wein oder ein cremiges, samtiges Erlebnis im Glas haben:

### Der Purist: Ausbau im Stahltank (Stainless Steel)

Wenn der Chardonnay im Stahltank ausgebaut wird, geht es um die Reinsubstanz. Der Winzer schützt die primären, sauberen Fruchtaromen.

**Geschmackserlebnis:** Hier erleben Sie reine Klarheit und spritzige Mineralität. Der Wein schmeckt nach grünem Apfel, Zitrus und frisch aufgeschnittenem Pfirsich. Er ist der perfekte Aperitif und der Inbegriff von Trinkfreude.

### Der Verführer: Ausbau im Holzfass (Oaked/Barrique)

Sobald das Holz ins Spiel kommt, verändert sich alles. Die Reifung, oft kombiniert mit der Malolaktischen Gärung (die Säureumwandlung, die den Wein weicher macht), verleiht dem Wein Tiefe und Textur.

**Geschmackserlebnis:** Hier entfaltet sich die wahre Cremigkeit. Wir sprechen von Buttertoast, gerösteten Haselnüssen, Vanillenote und einem Gefühl von Opulenz. Diese Weine sind vollmundig und haben eine beeindruckende Textur, die fast schon ölig wirkt – der perfekte Genuss für kalte Abende.

## 3. Pairing-Empfehlungen: Der perfekte Partner für den Chardonnay

Der Chardonnay ist ein Traumpartner am Tisch, da seine Bandbreite von leicht bis üppig fast jedes Gericht begleiten kann.

| Gericht | Chardonnay-Stil | Warum es funktioniert |
|---|---|---|
| **Gedämpfter Lachs mit Zitronenbutter-Sauce** | Holzausbau (Volle Cremigkeit) | Der Buttertoast und die cremige Textur des Weins verschmelzen mit der Buttersauce und dem Fett des Lachses. Es ist ein dekadentes, harmonisches Genuss-Erlebnis. |
| **Hähnchenbrust vom Grill mit frischen Kräutern** | Stahltank (Frisch & Mineralisch) | Die Mineralität und die helle Säure des Chardonnays durchdringen die leichte Fettigkeit des Hähnchens und betonen die Kräuterfinesse der Marinade. Der Wein wirkt als perfekter Gaumenreiniger. |
| **Indisches Chicken Korma (mild-cremig)** | Holzausbau (Opulente Frucht & Vanille) | Die opulente Frucht (Pfirsich/Mango) und die leichte Süße der Vanillenoten im gehaltvollen Chardonnay fangen die Cremigkeit des Korma (Kokosmilch/Joghurt) auf. Der Wein bildet einen weichen Puffer zur Gewürzaromatik. |

## 4. FAQ – 10 Fragen für Chardonnay-Liebhaber

**❓ Ist Chardonnay immer trocken?**
Fast immer. Chardonnay wird in der Regel trocken ausgebaut. Selbst wenn Sie Noten von reifer Mango oder Ananas schmecken, kommt diese Süße von der Frucht, nicht vom Zucker.

**❓ Was bedeutet "Malolaktische Gärung" für den Geschmack?**
Im einfachen Sinne: Die scharfe Apfelsäure wird in weiche Milchsäure umgewandelt. Das Ergebnis ist die berühmte, buttrige Textur und das Aroma, das viele mit Popcorn oder Buttertoast assoziieren – der Inbegriff von Cremigkeit.

**❓ Muss Chardonnay gekühlt werden?**
Ja, aber die Temperatur ist entscheidend: Ein Stahltank-Chardonnay (z.B. Chablis) liebt es kühl (ca. 8–10 °C). Ein Holz-Chardonnay sollte etwas wärmer (ca. 12–14 °C) serviert werden, damit seine reichen, komplexen Aromen zur Geltung kommen.

**❓ Schmeckt Chardonnay wie Eiche?**
Ein gut gemachter Holz-Chardonnay schmeckt nicht nach Baum, sondern nach Vanillenote, Gewürz, Nuss und gerösteten Aromen, die sich harmonisch in die Frucht integrieren. Winzer nutzen Eiche, um die Textur und Komplexität zu erhöhen.

**❓ Was ist der Unterschied zwischen Chardonnay und Chablis?**
Chablis ist Chardonnay! Es ist ein kühles Weinbaugebiet in Burgund, in dem der Chardonnay traditionell fast ausschließlich im Stahltank ausgebaut wird. Chablis ist also der puristische, mineralische Ausdruck der Rebsorte.

**❓ Ist Chardonnay ein "leichter" oder "schwerer" Wein?**
Er kann beides sein – daher der Name Chameleon! Ein Chablis ist leicht und frisch, während ein kalifornischer Chardonnay im Holzfass vollmundig und "schwer" ist, fast wie ein Rotwein.

**❓ Wird Chardonnay in Champagner verwendet?**
Absolut! Er ist neben Pinot Noir und Pinot Meunier eine der drei Hauptrebsorten. Flaschen, die nur aus Chardonnay bestehen, werden als Blanc de Blancs bezeichnet und sind bekannt für ihre Eleganz und Finesse.

**❓ Ist Chardonnay eine einfache Rebsorte?**
Im Weinberg ist sie relativ robust und anpassungsfähig. Im Keller ist sie jedoch anspruchsvoll, da der Winzer die Balance zwischen Säure, Holz und Frucht perfekt beherrschen muss, um diesen Kultwein zu kreieren.

**❓ Warum wird Chardonnay oft als "Buttrig" beschrieben?**
Wegen der Malolaktischen Gärung, die das sogenannte Diacetyl produziert – ein Nebenprodukt, das denselben Geschmack wie Butter und Buttertoast hat.

**❓ Wie lange kann ich einen guten Chardonnay lagern?**
Hochwertige Weine aus Burgund, Kalifornien oder Australien (speziell die holzgereiften) können problemlos 5 bis 10 Jahre oder länger reifen und entwickeln dabei faszinierende, nussige Tertiäraromen und behalten ihre Finesse.
"""

# ===================== TRANSLATION PROMPT =====================

TRANSLATION_PROMPT = """Übersetze den folgenden deutschen Weinblog-Artikel ins {target_language}.

## WICHTIGE REGELN:
1. Behalte die gesamte Struktur und Formatierung (Markdown) bei
2. Behalte alle Emoji bei (❓ etc.)
3. Übersetze Weinnamen und Regionen NICHT (z.B. "Chablis", "Puligny-Montrachet", "Champagne", "Côte de Beaune")
4. Übersetze Fachbegriffe korrekt
5. Passe die Anrede an die Zielsprache an (Du-Form → You / Vous)
6. Tabellen-Format beibehalten (| ... | ... |)
7. Der Ton soll warm, einladend und leidenschaftlich bleiben
8. Übersetze auch den Titel und das Excerpt

## FORMAT DER AUSGABE:
Gib die Übersetzung als JSON zurück:
{{
  "title": "Übersetzter Titel",
  "excerpt": "Übersetztes Excerpt (1-2 Sätze)",
  "content": "Übersetzter vollständiger Artikel"
}}

## DEUTSCHER ORIGINAL-ARTIKEL:

### Titel:
{title}

### Excerpt:
{excerpt}

### Inhalt:
{content}
"""


async def translate_content(target_language: str, language_name: str):
    """Translate the blog post to target language"""
    print(f"🌍 Übersetze nach {language_name}...")
    
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=str(uuid.uuid4()),
        system_message="Du bist ein professioneller Übersetzer für Wein-Content. Übersetze präzise und behalte den poetischen, leidenschaftlichen Ton bei."
    ).with_model("openai", "gpt-5.1")
    
    prompt = TRANSLATION_PROMPT.format(
        target_language=target_language,
        title=CHARDONNAY_TITLE_DE,
        excerpt=CHARDONNAY_EXCERPT_DE,
        content=CHARDONNAY_CONTENT_DE
    )
    
    response = await chat.send_message(UserMessage(text=prompt))
    
    # Extract JSON
    json_match = re.search(r"\{[\s\S]*\}", response)
    if json_match:
        try:
            data = json.loads(json_match.group())
            print(f"  ✓ {language_name} Übersetzung fertig")
            return data
        except json.JSONDecodeError as e:
            print(f"  ❌ JSON Parse-Fehler: {e}")
            return None
    else:
        print(f"  ❌ Kein JSON gefunden")
        return None


async def create_blog_post():
    """Create the Chardonnay blog post with translations"""
    print("=" * 60)
    print("📝 CHARDONNAY BLOG POST ERSTELLEN")
    print("=" * 60)
    
    # Check if post already exists
    existing = await db.blog_posts.find_one({"slug": "chardonnay-chameleon-koenig-weissweine"})
    if existing:
        print("⚠️  Blog-Post existiert bereits. Lösche alten Post...")
        await db.blog_posts.delete_one({"slug": "chardonnay-chameleon-koenig-weissweine"})
    
    # Translate to English
    en_translation = await translate_content("Englisch (British English)", "Englisch")
    
    # Translate to French
    fr_translation = await translate_content("Französisch", "Französisch")
    
    # Create blog post document
    blog_post = {
        "id": str(uuid.uuid4()),
        "slug": "chardonnay-chameleon-koenig-weissweine",
        "title": CHARDONNAY_TITLE_DE,
        "title_en": en_translation.get("title", "") if en_translation else "",
        "title_fr": fr_translation.get("title", "") if fr_translation else "",
        "excerpt": CHARDONNAY_EXCERPT_DE,
        "excerpt_en": en_translation.get("excerpt", "") if en_translation else "",
        "excerpt_fr": fr_translation.get("excerpt", "") if fr_translation else "",
        "content": CHARDONNAY_CONTENT_DE,
        "content_en": en_translation.get("content", "") if en_translation else "",
        "content_fr": fr_translation.get("content", "") if fr_translation else "",
        "image_url": "https://images.unsplash.com/photo-1566995541428-f2246c17cda1?w=1200",
        "category": "wissen",
        "tags": ["chardonnay", "weisswein", "rebsorten", "burgund", "champagner", "weinwissen", "food-pairing"],
        "author": "Sommelier Team",
        "published": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    # Insert into database
    await db.blog_posts.insert_one(blog_post)
    print("\n✅ Blog-Post erfolgreich erstellt!")
    
    # Show summary
    print("\n📊 Zusammenfassung:")
    print(f"   Slug: {blog_post['slug']}")
    print(f"   Titel (DE): {blog_post['title'][:50]}...")
    print(f"   Titel (EN): {blog_post['title_en'][:50]}..." if blog_post['title_en'] else "   Titel (EN): -")
    print(f"   Titel (FR): {blog_post['title_fr'][:50]}..." if blog_post['title_fr'] else "   Titel (FR): -")
    print(f"   Kategorie: {blog_post['category']}")
    print(f"   Tags: {', '.join(blog_post['tags'])}")
    
    return blog_post


async def main():
    post = await create_blog_post()
    
    print("\n" + "=" * 60)
    print("🎉 FERTIG!")
    print("=" * 60)
    print(f"\n🔗 Blog-Post URL: /blog/{post['slug']}")


if __name__ == "__main__":
    asyncio.run(main())
