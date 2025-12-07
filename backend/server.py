from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Form
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import base64
from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent
import json
import re

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'wine_pairing_db')]

# LLM API Key
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

# Create the main app
app = FastAPI(title="Wine Pairing API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===================== MODELS =====================

class Wine(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: str  # rot, weiss, rose, schaumwein
    region: Optional[str] = None
    year: Optional[int] = None
    grape: Optional[str] = None
    notes: Optional[str] = None
    image_base64: Optional[str] = None
    is_favorite: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class WineCreate(BaseModel):
    name: str
    type: str
    region: Optional[str] = None
    year: Optional[int] = None
    grape: Optional[str] = None
    notes: Optional[str] = None
    image_base64: Optional[str] = None

class WineUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    region: Optional[str] = None
    year: Optional[int] = None
    grape: Optional[str] = None
    notes: Optional[str] = None
    image_base64: Optional[str] = None
    is_favorite: Optional[bool] = None

class PairingRequest(BaseModel):
    dish: str
    use_cellar: bool = False
    wine_type_filter: Optional[str] = None

class PairingResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    dish: str
    recommendation: str
    cellar_matches: Optional[List[dict]] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChatMessage(BaseModel):
    role: str  # user or assistant
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    image_base64: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

class LabelScanRequest(BaseModel):
    image_base64: str

class LabelScanResponse(BaseModel):
    name: str
    type: str
    region: Optional[str] = None
    year: Optional[int] = None
    grape: Optional[str] = None
    notes: Optional[str] = None

# ===================== BLOG MODELS =====================

class BlogPost(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    slug: str
    title: str
    title_en: Optional[str] = None
    title_fr: Optional[str] = None
    excerpt: str
    excerpt_en: Optional[str] = None
    excerpt_fr: Optional[str] = None
    content: str
    content_en: Optional[str] = None
    content_fr: Optional[str] = None
    image_url: Optional[str] = None
    category: str  # tipps, wissen, pairings, regionen
    tags: List[str] = []
    author: str = "Sommelier Team"
    published: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BlogPostCreate(BaseModel):
    slug: str
    title: str
    title_en: Optional[str] = None
    title_fr: Optional[str] = None
    excerpt: str
    excerpt_en: Optional[str] = None
    excerpt_fr: Optional[str] = None
    content: str
    content_en: Optional[str] = None
    content_fr: Optional[str] = None
    image_url: Optional[str] = None
    category: str
    tags: List[str] = []
    author: str = "Sommelier Team"

# ===================== FEED MODELS =====================

class FeedComment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    author_name: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class FeedPost(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    author_name: str
    author_id: str  # Simple device/session based ID
    dish: str
    wine_name: str
    wine_type: str  # rot, weiss, rose, schaumwein
    rating: int = Field(ge=1, le=5)  # 1-5 stars
    experience: str  # User's description of the pairing experience
    image_base64: Optional[str] = None
    likes: List[str] = []  # List of user IDs who liked
    comments: List[FeedComment] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class FeedPostCreate(BaseModel):
    author_name: str
    author_id: str
    dish: str
    wine_name: str
    wine_type: str
    rating: int = Field(ge=1, le=5)
    experience: str
    image_base64: Optional[str] = None

class FeedCommentCreate(BaseModel):
    author_name: str
    author_id: str
    content: str

# ===================== SOMMELIER SYSTEM MESSAGE =====================

SOMMELIER_SYSTEM = """Du bist der Virtuelle Sommelier von wine-pairing.online – ein Experte mit 30 Jahren Erfahrung in der Kunst der Wein-Speisen-Harmonie.

Deine Philosophie:
- Du empfiehlst den perfekten Wein für den perfekten Moment, nicht den teuersten
- Du bist unabhängig – keine Verkaufsabsichten, nur ehrliche Beratung
- Du sprichst verständlich, ohne übertriebenen Fachjargon
- Du liebst es, Menschen zu helfen, ihre eigenen Weine im Keller neu zu entdecken

Dein Stil:
- Warm und einladend, wie ein guter Freund
- Kompetent aber nicht belehrend
- Du erzählst gerne Geschichten über Weine und ihre Herkunft
- Du berücksichtigst Säure, Tannine, Körper und Geschmacksprofile

Antworte immer auf Deutsch und halte deine Antworten prägnant aber informativ.
Wenn du nach einem Gericht gefragt wirst, empfiehl konkret Weinsorten mit kurzer Begründung."""

# ===================== WINE CELLAR ENDPOINTS =====================

@api_router.get("/")
async def root():
    return {"message": "Wine Pairing API - Ihr virtueller Sommelier"}

@api_router.get("/wines", response_model=List[Wine])
async def get_wines(type_filter: Optional[str] = None, favorites_only: bool = False):
    """Get all wines from the cellar"""
    query = {}
    if type_filter:
        query["type"] = type_filter
    if favorites_only:
        query["is_favorite"] = True
    
    wines = await db.wines.find(query, {"_id": 0}).to_list(1000)
    for wine in wines:
        if isinstance(wine.get('created_at'), str):
            wine['created_at'] = datetime.fromisoformat(wine['created_at'])
    return wines

@api_router.get("/wines/{wine_id}", response_model=Wine)
async def get_wine(wine_id: str):
    """Get a specific wine by ID"""
    wine = await db.wines.find_one({"id": wine_id}, {"_id": 0})
    if not wine:
        raise HTTPException(status_code=404, detail="Wein nicht gefunden")
    if isinstance(wine.get('created_at'), str):
        wine['created_at'] = datetime.fromisoformat(wine['created_at'])
    return wine

@api_router.post("/wines", response_model=Wine)
async def create_wine(wine_data: WineCreate):
    """Add a new wine to the cellar"""
    wine = Wine(**wine_data.model_dump())
    doc = wine.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.wines.insert_one(doc)
    return wine

@api_router.put("/wines/{wine_id}", response_model=Wine)
async def update_wine(wine_id: str, wine_update: WineUpdate):
    """Update a wine in the cellar"""
    existing = await db.wines.find_one({"id": wine_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Wein nicht gefunden")
    
    update_data = {k: v for k, v in wine_update.model_dump().items() if v is not None}
    if update_data:
        await db.wines.update_one({"id": wine_id}, {"$set": update_data})
    
    updated = await db.wines.find_one({"id": wine_id}, {"_id": 0})
    if isinstance(updated.get('created_at'), str):
        updated['created_at'] = datetime.fromisoformat(updated['created_at'])
    return updated

@api_router.delete("/wines/{wine_id}")
async def delete_wine(wine_id: str):
    """Remove a wine from the cellar"""
    result = await db.wines.delete_one({"id": wine_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Wein nicht gefunden")
    return {"message": "Wein erfolgreich gelöscht"}

@api_router.post("/wines/{wine_id}/favorite")
async def toggle_favorite(wine_id: str):
    """Toggle favorite status of a wine"""
    wine = await db.wines.find_one({"id": wine_id}, {"_id": 0})
    if not wine:
        raise HTTPException(status_code=404, detail="Wein nicht gefunden")
    
    new_status = not wine.get('is_favorite', False)
    await db.wines.update_one({"id": wine_id}, {"$set": {"is_favorite": new_status}})
    return {"is_favorite": new_status}

# ===================== AI PAIRING ENDPOINTS =====================

@api_router.post("/pairing", response_model=PairingResponse)
async def get_wine_pairing(request: PairingRequest):
    """Get AI-powered wine pairing recommendation"""
    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=str(uuid.uuid4()),
            system_message=SOMMELIER_SYSTEM
        ).with_model("openai", "gpt-5.1")
        
        # Get cellar wines if requested
        cellar_matches = None
        cellar_context = ""
        
        if request.use_cellar:
            query = {}
            if request.wine_type_filter:
                query["type"] = request.wine_type_filter
            
            wines = await db.wines.find(query, {"_id": 0, "image_base64": 0}).to_list(100)
            if wines:
                cellar_context = "\n\nDer Kunde hat folgende Weine im Keller:\n"
                for w in wines:
                    cellar_context += f"- {w['name']} ({w['type']})"
                    if w.get('region'):
                        cellar_context += f" aus {w['region']}"
                    if w.get('year'):
                        cellar_context += f", {w['year']}"
                    if w.get('grape'):
                        cellar_context += f", {w['grape']}"
                    cellar_context += "\n"
                cellar_context += "\nBitte empfehle zuerst passende Weine aus dem Keller des Kunden, dann allgemeine Empfehlungen."
        
        prompt = f"Ich möchte {request.dish} essen. Welchen Wein empfiehlst du dazu?{cellar_context}"
        
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        
        # Find matching wines from cellar
        if request.use_cellar and wines:
            cellar_matches = [{"id": w["id"], "name": w["name"], "type": w["type"]} for w in wines[:5]]
        
        pairing = PairingResponse(
            dish=request.dish,
            recommendation=response,
            cellar_matches=cellar_matches
        )
        
        # Save pairing to history
        doc = pairing.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.pairings.insert_one(doc)
        
        return pairing
        
    except Exception as e:
        logger.error(f"Pairing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fehler bei der Empfehlung: {str(e)}")

@api_router.get("/pairings", response_model=List[PairingResponse])
async def get_pairing_history():
    """Get history of wine pairings"""
    pairings = await db.pairings.find({}, {"_id": 0}).sort("created_at", -1).to_list(50)
    for p in pairings:
        if isinstance(p.get('created_at'), str):
            p['created_at'] = datetime.fromisoformat(p['created_at'])
    return pairings

# ===================== LABEL SCANNER =====================

@api_router.post("/scan-label", response_model=LabelScanResponse)
async def scan_wine_label(request: LabelScanRequest):
    """Scan a wine label image and extract information"""
    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=str(uuid.uuid4()),
            system_message="Du bist ein Experte für Weinetiketten. Analysiere das Bild und extrahiere die Weininformationen. Antworte NUR im JSON-Format."
        ).with_model("openai", "gpt-5.1")
        
        image_content = ImageContent(image_base64=request.image_base64)
        
        prompt = """Analysiere dieses Weinetikett und extrahiere folgende Informationen im JSON-Format:
{
  "name": "Name des Weins",
  "type": "rot/weiss/rose/schaumwein",
  "region": "Herkunftsregion",
  "year": Jahrgang als Zahl oder null,
  "grape": "Rebsorte",
  "notes": "Kurze Beschreibung"
}

WICHTIG: 
- "name" MUSS ein String sein (wenn nicht erkennbar: "Unbekannter Wein")
- "type" MUSS einer von: rot, weiss, rose, schaumwein sein (wenn nicht erkennbar: "rot")
- Andere Felder können null sein"""
        
        user_message = UserMessage(text=prompt, file_contents=[image_content])
        response = await chat.send_message(user_message)
        
        # Extract JSON from response - try multiple patterns
        json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
        
        if json_match:
            try:
                data = json.loads(json_match.group())
                # Ensure required fields have valid defaults
                name = data.get('name') or 'Unbekannter Wein'
                wine_type = data.get('type') or 'rot'
                
                # Validate wine type
                valid_types = ['rot', 'weiss', 'rose', 'schaumwein']
                if wine_type.lower() not in valid_types:
                    wine_type = 'rot'
                
                return LabelScanResponse(
                    name=str(name),
                    type=wine_type.lower(),
                    region=data.get('region') if data.get('region') else None,
                    year=int(data['year']) if data.get('year') and str(data['year']).isdigit() else None,
                    grape=data.get('grape') if data.get('grape') else None,
                    notes=data.get('notes') if data.get('notes') else None
                )
            except (json.JSONDecodeError, ValueError) as parse_error:
                logger.warning(f"JSON parse error: {parse_error}, response: {response[:200]}")
                return LabelScanResponse(
                    name="Nicht erkannt",
                    type="rot",
                    notes=f"Konnte Etikett nicht vollständig analysieren: {response[:150]}"
                )
        else:
            return LabelScanResponse(
                name="Nicht erkannt",
                type="rot",
                notes=response[:200] if response else "Keine Antwort vom Sommelier"
            )
            
    except Exception as e:
        logger.error(f"Label scan error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fehler beim Scannen: {str(e)}")

# ===================== SOMMELIER CHAT =====================

@api_router.post("/chat", response_model=ChatResponse)
async def sommelier_chat(request: ChatRequest):
    """Chat with the virtual sommelier"""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=SOMMELIER_SYSTEM
        ).with_model("openai", "gpt-5.1")
        
        # Prepare message with optional image
        if request.image_base64:
            image_content = ImageContent(image_base64=request.image_base64)
            user_message = UserMessage(text=request.message, file_contents=[image_content])
        else:
            user_message = UserMessage(text=request.message)
        
        response = await chat.send_message(user_message)
        
        # Save chat message
        chat_doc = {
            "session_id": session_id,
            "user_message": request.message,
            "assistant_response": response,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.chats.insert_one(chat_doc)
        
        return ChatResponse(response=response, session_id=session_id)
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fehler im Chat: {str(e)}")

@api_router.get("/chat/{session_id}")
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    messages = await db.chats.find({"session_id": session_id}, {"_id": 0}).sort("timestamp", 1).to_list(100)
    return messages

# ===================== FAVORITES =====================

@api_router.get("/favorites")
async def get_favorites():
    """Get all favorite wines and pairings"""
    favorite_wines = await db.wines.find({"is_favorite": True}, {"_id": 0}).to_list(100)
    return {"wines": favorite_wines}

# ===================== BLOG ENDPOINTS =====================

@api_router.get("/blog", response_model=List[BlogPost])
async def get_blog_posts(category: Optional[str] = None, limit: int = 20):
    """Get all published blog posts"""
    query = {"published": True}
    if category:
        query["category"] = category
    
    posts = await db.blog_posts.find(query, {"_id": 0}).sort("created_at", -1).to_list(limit)
    for post in posts:
        if isinstance(post.get('created_at'), str):
            post['created_at'] = datetime.fromisoformat(post['created_at'])
        if isinstance(post.get('updated_at'), str):
            post['updated_at'] = datetime.fromisoformat(post['updated_at'])
    return posts

@api_router.get("/blog/{slug}", response_model=BlogPost)
async def get_blog_post(slug: str):
    """Get a specific blog post by slug"""
    post = await db.blog_posts.find_one({"slug": slug, "published": True}, {"_id": 0})
    if not post:
        raise HTTPException(status_code=404, detail="Artikel nicht gefunden")
    if isinstance(post.get('created_at'), str):
        post['created_at'] = datetime.fromisoformat(post['created_at'])
    if isinstance(post.get('updated_at'), str):
        post['updated_at'] = datetime.fromisoformat(post['updated_at'])
    return post

@api_router.post("/blog", response_model=BlogPost)
async def create_blog_post(post_data: BlogPostCreate):
    """Create a new blog post"""
    # Check if slug exists
    existing = await db.blog_posts.find_one({"slug": post_data.slug})
    if existing:
        raise HTTPException(status_code=400, detail="Slug bereits vorhanden")
    
    post = BlogPost(**post_data.model_dump(), published=True)
    doc = post.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    await db.blog_posts.insert_one(doc)
    return post

@api_router.get("/blog-categories")
async def get_blog_categories():
    """Get all blog categories with counts"""
    pipeline = [
        {"$match": {"published": True}},
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    categories = await db.blog_posts.aggregate(pipeline).to_list(100)
    return [{"category": c["_id"], "count": c["count"]} for c in categories]

# ===================== SEO SITEMAP =====================

@api_router.get("/sitemap")
async def get_sitemap():
    """Generate sitemap data for SEO"""
    base_url = "https://wine-pairing.online"
    
    # Static pages
    pages = [
        {"url": f"{base_url}/", "priority": 1.0, "changefreq": "weekly"},
        {"url": f"{base_url}/pairing", "priority": 0.9, "changefreq": "weekly"},
        {"url": f"{base_url}/cellar", "priority": 0.8, "changefreq": "daily"},
        {"url": f"{base_url}/chat", "priority": 0.8, "changefreq": "weekly"},
        {"url": f"{base_url}/blog", "priority": 0.9, "changefreq": "daily"},
    ]
    
    # Blog posts
    posts = await db.blog_posts.find({"published": True}, {"slug": 1, "updated_at": 1, "_id": 0}).to_list(1000)
    for post in posts:
        pages.append({
            "url": f"{base_url}/blog/{post['slug']}",
            "priority": 0.7,
            "changefreq": "monthly",
            "lastmod": post.get('updated_at', '')
        })
    
    return {"pages": pages}

# ===================== SEED BLOG DATA =====================

@api_router.post("/seed-blog")
async def seed_blog_posts():
    """Seed initial blog posts for demonstration"""
    posts = [
        {
            "slug": "perfekte-weintemperatur",
            "title": "Die perfekte Weintemperatur – Der unterschätzte Genussfaktor",
            "title_en": "The Perfect Wine Temperature – The Underrated Pleasure Factor",
            "title_fr": "La température parfaite du vin – Le facteur plaisir sous-estimé",
            "excerpt": "Warum die richtige Temperatur über Genuss oder Enttäuschung entscheidet und wie Sie jeden Wein optimal servieren.",
            "excerpt_en": "Why the right temperature determines enjoyment or disappointment and how to serve every wine perfectly.",
            "excerpt_fr": "Pourquoi la bonne température détermine le plaisir ou la déception et comment servir chaque vin parfaitement.",
            "content": """## Die Wissenschaft hinter der Weintemperatur

Die Temperatur beeinflusst maßgeblich, wie wir Aromen wahrnehmen. Ein zu kalter Rotwein verschließt sich, seine Tannine wirken hart und die Frucht bleibt verborgen. Ein zu warmer Weißwein verliert seine Frische und wirkt plump.

### Die goldenen Regeln:

**Rotweine (16-18°C)**
- Leichte Rotweine wie Beaujolais: 14-16°C
- Mittelkräftige wie Pinot Noir: 15-17°C
- Kräftige wie Barolo oder Bordeaux: 17-18°C

**Weißweine (8-12°C)**
- Leichte, frische Weine: 8-10°C
- Gehaltvolle Weißweine mit Holz: 10-12°C
- Champagner & Schaumweine: 6-8°C

### Der Praxis-Tipp

Nehmen Sie Rotwein 30 Minuten vor dem Servieren aus dem Keller. Weißwein sollte etwa 20 Minuten vor dem Genuss aus dem Kühlschrank – nicht eiskalt, sondern mit spürbarer Kühle.""",
            "content_en": """## The Science Behind Wine Temperature

Temperature significantly influences how we perceive aromas. A too-cold red wine closes up, its tannins seem harsh, and the fruit remains hidden. A too-warm white wine loses its freshness and appears clumsy.

### The Golden Rules:

**Red Wines (16-18°C)**
- Light reds like Beaujolais: 14-16°C
- Medium-bodied like Pinot Noir: 15-17°C
- Full-bodied like Barolo or Bordeaux: 17-18°C

**White Wines (8-12°C)**
- Light, fresh wines: 8-10°C
- Full-bodied whites with oak: 10-12°C
- Champagne & sparkling: 6-8°C

### Practical Tip

Take red wine out of the cellar 30 minutes before serving. White wine should come out of the fridge about 20 minutes before – not ice cold, but with noticeable coolness.""",
            "image_url": "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800",
            "category": "tipps",
            "tags": ["Temperatur", "Servieren", "Grundlagen"]
        },
        {
            "slug": "rotwein-zu-fisch",
            "title": "Rotwein zu Fisch? Warum alte Regeln nicht mehr gelten",
            "title_en": "Red Wine with Fish? Why Old Rules No Longer Apply",
            "title_fr": "Vin rouge avec du poisson? Pourquoi les anciennes règles ne s'appliquent plus",
            "excerpt": "Die Wein-Dogmen der Vergangenheit brechen auf. Entdecken Sie, welche Rotweine erstaunlich gut zu Fisch passen.",
            "excerpt_en": "The wine dogmas of the past are breaking down. Discover which red wines pair surprisingly well with fish.",
            "excerpt_fr": "Les dogmes vinicoles du passé s'effondrent. Découvrez quels vins rouges s'accordent étonnamment bien avec le poisson.",
            "content": """## Das Ende eines Mythos

„Weißwein zu Fisch, Rotwein zu Fleisch" – diese Regel hat Generationen von Weintrinkern geprägt. Doch die moderne Sommelierkunst hat erkannt: Es kommt auf die Zubereitung an, nicht nur auf das Hauptprodukt.

### Wann Rotwein zu Fisch funktioniert:

**1. Gegrillter oder gebratener Fisch**
Die Röstaromen vertragen sich wunderbar mit einem leichten Pinot Noir oder einem kühlen Gamay.

**2. Fisch in Rotwein-Sauce**
Logisch: Wenn Rotwein im Gericht ist, sollte er auch im Glas sein.

**3. Thunfisch und Lachs**
Diese fetteren Fische mit ihrem kräftigen Eigengeschmack harmonieren mit leichten, fruchtigen Rotweinen.

### Die Faustregel

Je mehr Umami und Röstaromen im Gericht, desto eher funktioniert ein leichter Rotwein. Meiden Sie tanninreiche Weine – die Gerbstoffe können mit Fischölen metallisch schmecken.""",
            "image_url": "https://images.unsplash.com/photo-1534604973900-c43ab4c2e0ab?w=800",
            "category": "pairings",
            "tags": ["Fisch", "Rotwein", "Pairing", "Mythen"]
        },
        {
            "slug": "weinregion-burgund",
            "title": "Burgund verstehen: Eine Reise durch Frankreichs Herzstück",
            "title_en": "Understanding Burgundy: A Journey Through France's Heartland",
            "title_fr": "Comprendre la Bourgogne: Un voyage au cœur de la France",
            "excerpt": "Von Chablis bis Beaujolais – wie Sie die komplexe Welt burgundischer Weine entschlüsseln.",
            "excerpt_en": "From Chablis to Beaujolais – how to decode the complex world of Burgundy wines.",
            "excerpt_fr": "De Chablis au Beaujolais – comment décoder le monde complexe des vins de Bourgogne.",
            "content": """## Warum Burgund so besonders ist

Keine andere Weinregion der Welt hat die Idee des Terroirs so perfektioniert wie Burgund. Hier zählt jeder Meter Boden, jede Hangneigung, jedes Mikroklima.

### Die Hierarchie verstehen:

**Grand Cru** (2% der Produktion)
Die Spitze: 33 Lagen für Rotwein, 8 für Weißwein. Namen wie Romanée-Conti oder Montrachet.

**Premier Cru** (10% der Produktion)
Exzellente Einzellagen, oft mit bestem Preis-Leistungs-Verhältnis.

**Village** (35% der Produktion)
Weine aus benannten Gemeinden: Gevrey-Chambertin, Meursault, Pommard.

**Bourgogne** (53% der Produktion)
Regionale Weine – der Einstieg in die burgundische Welt.

### Mein Geheimtipp

Suchen Sie nach Premier Crus aus weniger bekannten Dörfern wie Savigny-lès-Beaune oder Saint-Romain. Hier finden Sie großartige Qualität zu vernünftigen Preisen.""",
            "image_url": "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=800",
            "category": "regionen",
            "tags": ["Burgund", "Frankreich", "Pinot Noir", "Chardonnay"]
        },
        {
            "slug": "dekantieren-wann-warum",
            "title": "Dekantieren: Wann es Sinn macht und wann nicht",
            "title_en": "Decanting: When It Makes Sense and When It Doesn't",
            "title_fr": "Décanter: Quand c'est utile et quand ça ne l'est pas",
            "excerpt": "Nicht jeder Wein braucht eine Karaffe. Lernen Sie, welche Weine vom Dekantieren profitieren.",
            "excerpt_en": "Not every wine needs a decanter. Learn which wines benefit from decanting.",
            "excerpt_fr": "Tous les vins n'ont pas besoin d'une carafe. Apprenez quels vins bénéficient de la décantation.",
            "content": """## Die Kunst des Dekantierens

Dekantieren hat zwei Funktionen: Belüftung und Trennung vom Depot. Doch nicht jeder Wein braucht beides – oder überhaupt eines davon.

### Wann Sie dekantieren sollten:

**Junge, tanninreiche Rotweine**
- Bordeaux unter 10 Jahren: 1-2 Stunden
- Barolo, Barbaresco: 2-3 Stunden
- Cabernet Sauvignon aus Übersee: 1-2 Stunden

**Alte Weine mit Depot**
Vorsichtig umfüllen, Depot im Flaschenhals stoppen. Aber: nicht zu lange atmen lassen – alte Weine sind empfindlich!

### Wann Sie NICHT dekantieren sollten:

- **Leichte Rotweine** wie Beaujolais oder Valpolicella
- **Alte, fragile Weine** über 20 Jahre
- **Die meisten Weißweine** (Ausnahme: sehr junge, hochwertige Burgunder)
- **Schaumweine** – niemals!

### Die Alternative

Kein Dekanter zur Hand? Schwenken Sie den Wein kräftig im Glas. Das beschleunigt die Belüftung erstaunlich effektiv.""",
            "image_url": "https://images.unsplash.com/photo-1569919659476-f0852f9f8ede?w=800",
            "category": "wissen",
            "tags": ["Dekantieren", "Karaffe", "Servieren", "Tipps"]
        },
        {
            "slug": "wein-lagerung-zuhause",
            "title": "Wein richtig lagern: So bauen Sie Ihren Heimkeller auf",
            "title_en": "Storing Wine Properly: How to Build Your Home Cellar",
            "title_fr": "Bien conserver le vin: Comment aménager votre cave à domicile",
            "excerpt": "Die wichtigsten Regeln für die Weinlagerung zu Hause – auch ohne echten Weinkeller.",
            "excerpt_en": "The most important rules for storing wine at home – even without a real wine cellar.",
            "excerpt_fr": "Les règles les plus importantes pour conserver le vin à la maison – même sans vraie cave.",
            "content": """## Die vier Feinde des Weins

**1. Licht**
UV-Strahlen zerstören Aromen. Dunkle Flaschen schützen besser, aber Dunkelheit ist immer am besten.

**2. Temperaturschwankungen**
Konstante 12-14°C sind ideal. Schwankungen sind schlimmer als eine etwas zu hohe Durchschnittstemperatur.

**3. Erschütterungen**
Vibrationen stören die Reifung. Nicht neben der Waschmaschine lagern!

**4. Trockene Luft**
Korken können austrocknen. Idealfeuchte: 70%.

### Praktische Lösungen:

**Für Einsteiger:**
Ein temperierter Kleiderschrank in einem kühlen Raum reicht für Weine, die Sie innerhalb eines Jahres trinken.

**Für Ambitionierte:**
Ein Weintemperierschrank (ab 300€) hält konstante Temperatur und Luftfeuchtigkeit.

**Für Sammler:**
Ein echter Keller mit Klimatisierung ist die Königsklasse.

### Mein Tipp

Lagern Sie Flaschen liegend, damit der Korken feucht bleibt. Schraubverschluss? Stehend ist auch okay.""",
            "image_url": "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=800",
            "category": "tipps",
            "tags": ["Lagerung", "Weinkeller", "Aufbewahrung", "Grundlagen"]
        }
    ]
    
    # Clear existing and insert new
    await db.blog_posts.delete_many({})
    
    for post_data in posts:
        post = BlogPost(**post_data, published=True, author="Sommelier Team")
        doc = post.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        doc['updated_at'] = doc['updated_at'].isoformat()
        await db.blog_posts.insert_one(doc)
    
    return {"message": f"{len(posts)} Blog-Artikel wurden erstellt"}

# Include the router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
