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

# ===================== GRAPE VARIETY MODELS =====================

class GrapeVariety(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    slug: str
    name: str
    type: str  # rot, weiss
    
    # Poetic descriptions (multilingual)
    description: str
    description_en: Optional[str] = None
    description_fr: Optional[str] = None
    
    # Characteristics
    synonyms: List[str] = []
    body: str  # leicht, mittel, vollmundig
    acidity: str  # niedrig, mittel, hoch
    tannin: str  # niedrig, mittel, hoch
    aging: str  # Holz, Edelstahl, etc.
    
    # Aromas
    primary_aromas: List[str] = []
    tertiary_aromas: List[str] = []
    
    # Food pairings
    perfect_pairings: List[str] = []
    perfect_pairings_en: List[str] = []
    perfect_pairings_fr: List[str] = []
    
    # Regions
    main_regions: List[str] = []
    
    # Image
    image_url: Optional[str] = None
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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
        
        # Check if response is None or empty
        if not response or not response.strip():
            logger.warning("Label scan: Received empty or None response from AI")
            return LabelScanResponse(
                name="Nicht erkannt",
                type="rot",
                notes="Keine Antwort vom Sommelier - Bitte versuchen Sie es erneut"
            )
        
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
            except (json.JSONDecodeError, ValueError, KeyError, TypeError) as parse_error:
                logger.warning(f"JSON parse error: {parse_error}, response: {response[:200]}")
                return LabelScanResponse(
                    name="Nicht erkannt",
                    type="rot",
                    notes=f"Konnte Etikett nicht vollständig analysieren: {str(parse_error)[:100]}"
                )
        else:
            logger.warning(f"Label scan: No JSON found in response: {response[:200]}")
            return LabelScanResponse(
                name="Nicht erkannt",
                type="rot",
                notes=f"Konnte keine strukturierten Daten extrahieren. Antwort: {response[:150]}"
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

# ===================== COMMUNITY FEED ENDPOINTS =====================

@api_router.get("/feed", response_model=List[FeedPost])
async def get_feed_posts(limit: int = 50, skip: int = 0):
    """Get all feed posts, newest first"""
    posts = await db.feed_posts.find({}, {"_id": 0}).sort("created_at", -1).skip(skip).to_list(limit)
    for post in posts:
        if isinstance(post.get('created_at'), str):
            post['created_at'] = datetime.fromisoformat(post['created_at'])
        # Parse comments
        if 'comments' in post:
            for comment in post['comments']:
                if isinstance(comment.get('created_at'), str):
                    comment['created_at'] = datetime.fromisoformat(comment['created_at'])
    return posts

@api_router.get("/feed/{post_id}", response_model=FeedPost)
async def get_feed_post(post_id: str):
    """Get a specific feed post"""
    post = await db.feed_posts.find_one({"id": post_id}, {"_id": 0})
    if not post:
        raise HTTPException(status_code=404, detail="Post nicht gefunden")
    if isinstance(post.get('created_at'), str):
        post['created_at'] = datetime.fromisoformat(post['created_at'])
    return post

@api_router.post("/feed", response_model=FeedPost)
async def create_feed_post(post_data: FeedPostCreate):
    """Create a new feed post"""
    post = FeedPost(**post_data.model_dump())
    doc = post.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['likes'] = []
    doc['comments'] = []
    await db.feed_posts.insert_one(doc)
    return post

@api_router.post("/feed/{post_id}/like")
async def toggle_like(post_id: str, author_id: str):
    """Toggle like on a feed post"""
    post = await db.feed_posts.find_one({"id": post_id}, {"_id": 0})
    if not post:
        raise HTTPException(status_code=404, detail="Post nicht gefunden")
    
    likes = post.get('likes', [])
    if author_id in likes:
        likes.remove(author_id)
        action = "unliked"
    else:
        likes.append(author_id)
        action = "liked"
    
    await db.feed_posts.update_one({"id": post_id}, {"$set": {"likes": likes}})
    return {"action": action, "likes_count": len(likes)}

@api_router.post("/feed/{post_id}/comment")
async def add_comment(post_id: str, comment_data: FeedCommentCreate):
    """Add a comment to a feed post"""
    post = await db.feed_posts.find_one({"id": post_id}, {"_id": 0})
    if not post:
        raise HTTPException(status_code=404, detail="Post nicht gefunden")
    
    comment = FeedComment(
        author_name=comment_data.author_name,
        content=comment_data.content
    )
    comment_doc = comment.model_dump()
    comment_doc['created_at'] = comment_doc['created_at'].isoformat()
    
    await db.feed_posts.update_one(
        {"id": post_id},
        {"$push": {"comments": comment_doc}}
    )
    return {"message": "Kommentar hinzugefügt", "comment": comment_doc}

@api_router.delete("/feed/{post_id}")
async def delete_feed_post(post_id: str, author_id: str):
    """Delete a feed post (only by author)"""
    post = await db.feed_posts.find_one({"id": post_id}, {"_id": 0})
    if not post:
        raise HTTPException(status_code=404, detail="Post nicht gefunden")
    if post.get('author_id') != author_id:
        raise HTTPException(status_code=403, detail="Nur der Autor kann diesen Post löschen")
    
    await db.feed_posts.delete_one({"id": post_id})
    return {"message": "Post gelöscht"}

@api_router.get("/feed-stats")
async def get_feed_stats():
    """Get feed statistics"""
    total_posts = await db.feed_posts.count_documents({})
    total_users = len(await db.feed_posts.distinct("author_id"))
    
    # Top rated pairings
    pipeline = [
        {"$match": {"rating": {"$gte": 4}}},
        {"$sort": {"created_at": -1}},
        {"$limit": 5},
        {"$project": {"_id": 0, "dish": 1, "wine_name": 1, "rating": 1, "author_name": 1}}
    ]
    top_pairings = await db.feed_posts.aggregate(pipeline).to_list(5)
    
    return {
        "total_posts": total_posts,
        "total_users": total_users,
        "top_pairings": top_pairings
    }

# ===================== GRAPE VARIETY ENDPOINTS =====================

@api_router.get("/grapes", response_model=List[GrapeVariety])
async def get_grape_varieties(type_filter: Optional[str] = None):
    """Get all grape varieties"""
    query = {}
    if type_filter and type_filter != 'all':
        query["type"] = type_filter
    
    grapes = await db.grape_varieties.find(query, {"_id": 0}).sort("name", 1).to_list(100)
    for grape in grapes:
        if isinstance(grape.get('created_at'), str):
            grape['created_at'] = datetime.fromisoformat(grape['created_at'])
    return grapes

@api_router.get("/grapes/{slug}", response_model=GrapeVariety)
async def get_grape_variety(slug: str):
    """Get a specific grape variety by slug"""
    grape = await db.grape_varieties.find_one({"slug": slug}, {"_id": 0})
    if not grape:
        raise HTTPException(status_code=404, detail="Rebsorte nicht gefunden")
    if isinstance(grape.get('created_at'), str):
        grape['created_at'] = datetime.fromisoformat(grape['created_at'])
    return grape

@api_router.post("/seed-grapes")
async def seed_grape_varieties():
    """Seed grape variety database with famous varieties"""
    grapes = [
        # WHITE WINES
        {
            "slug": "chardonnay",
            "name": "Chardonnay",
            "type": "weiss",
            "description": "Flüssiger Sonnenaufgang im Glas, golden schimmernd, der die Seele umarmt. In der Nase reife Pfirsiche, cremige Vanille, geröstete Haselnüsse und mineralische Kalksteinfrische. Am Gaumen buttrige Opulenz wie Seide, lebendige Säure mit Zitrone und grünem Apfel – ein Tanz von Fülle und Eleganz, der in langem, vibrierendem Finale nach mehr verlangt. Für den Kenner ein Chamäleon: burgundisch straff oder kalifornisch üppig, stets Spiegel von Winzerhand und Natur.",
            "description_en": "Liquid sunrise in a glass, golden shimmer embracing the soul. On the nose: ripe peaches, creamy vanilla, roasted hazelnuts, and mineral limestone freshness. On the palate: buttery opulence like silk, lively acidity with lemon and green apple – a dance of richness and elegance that demands more in its long, vibrating finish. For the connoisseur, a chameleon: Burgundian taut or Californian lush, always a mirror of winemaker's hand and nature.",
            "description_fr": "Lever de soleil liquide dans le verre, chatoiement doré qui embrasse l'âme. Au nez: pêches mûres, vanille crémeuse, noisettes grillées et fraîcheur minérale de calcaire. En bouche: opulence beurrée comme de la soie, acidité vive avec citron et pomme verte – une danse de richesse et d'élégance qui en redemande dans sa longue finale vibrante.",
            "synonyms": ["Morillon", "Beaunois"],
            "body": "mittel bis vollmundig",
            "acidity": "mittel bis hoch",
            "tannin": "niedrig",
            "aging": "Holz oder Edelstahl, trocken",
            "primary_aromas": ["Apfel", "Zitrone", "Pfirsich", "Melone"],
            "tertiary_aromas": ["Butter", "Vanille", "Toast", "Haselnuss"],
            "perfect_pairings": ["Gegrillter Hummer in Zitronenbutter", "Perlhuhn mit Trüffelrisotto", "Reifer Comté"],
            "perfect_pairings_en": ["Grilled lobster in lemon butter", "Guinea fowl with truffle risotto", "Aged Comté cheese"],
            "perfect_pairings_fr": ["Homard grillé au beurre citronné", "Pintade au risotto à la truffe", "Comté affiné"],
            "main_regions": ["Burgund", "Champagne", "Kalifornien", "Australien"],
            "image_url": "https://images.unsplash.com/photo-1566995541428-f2246c17cda1?w=800"
        },
        {
            "slug": "riesling",
            "name": "Riesling",
            "type": "weiss",
            "description": "Die Königin der weißen Reben – kristallklar wie ein Gebirgsbach, elektrisierend und lebendig. Ein Feuerwerk aus grünem Apfel, Limette, weißem Pfirsich und dem unverwechselbaren Hauch von Petrol, der Kennerherzen höher schlagen lässt. Am Gaumen eine Symphonie aus messerscharfer Säure und zarter Süße, perfekt balanciert wie ein Seiltänzer über den Weinbergen der Mosel. Vom knochentrocken bis edelsüß – Riesling ist der Beweis, dass wahre Eleganz zeitlos ist.",
            "description_en": "The queen of white grapes – crystal clear like a mountain stream, electrifying and alive. A firework of green apple, lime, white peach, and that unmistakable hint of petrol that makes connoisseurs' hearts beat faster. On the palate, a symphony of razor-sharp acidity and delicate sweetness, perfectly balanced like a tightrope walker above the Moselle vineyards. From bone dry to noble sweet – Riesling proves that true elegance is timeless.",
            "description_fr": "La reine des cépages blancs – cristallin comme un ruisseau de montagne, électrisant et vivant. Un feu d'artifice de pomme verte, citron vert, pêche blanche et cette touche incomparable de pétrole qui fait battre le cœur des connaisseurs. En bouche, une symphonie d'acidité tranchante et de douceur délicate, parfaitement équilibrée.",
            "synonyms": ["Rheinriesling", "Weißer Riesling"],
            "body": "leicht bis mittel",
            "acidity": "hoch",
            "tannin": "niedrig",
            "aging": "Edelstahl, trocken bis edelsüß",
            "primary_aromas": ["Grüner Apfel", "Limette", "Pfirsich", "Aprikose"],
            "tertiary_aromas": ["Petrol", "Honig", "Ingwer", "Mandel"],
            "perfect_pairings": ["Gebratene Forelle mit Mandelbutter", "Schweineschnitzel mit Spargel", "Thai-Curry mit Garnelen"],
            "perfect_pairings_en": ["Pan-fried trout with almond butter", "Pork schnitzel with asparagus", "Thai curry with shrimp"],
            "perfect_pairings_fr": ["Truite poêlée au beurre d'amandes", "Escalope de porc aux asperges", "Curry thaï aux crevettes"],
            "main_regions": ["Mosel", "Rheingau", "Elsass", "Clare Valley"],
            "image_url": "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800"
        },
        {
            "slug": "sauvignon-blanc",
            "name": "Sauvignon Blanc",
            "type": "weiss",
            "description": "Ein Weckruf für die Sinne – frisch wie der erste Frühlingsmorgen, wild wie ungezähmte Natur. Stachelbeere, frisch gemähtes Gras, Holunderblüte und ein Hauch von Feuerstein explodieren im Glas. Am Gaumen knackig und präzise, mit einer Säure, die wie ein Blitz durch den Körper fährt. Neuseeland macht ihn exotisch mit Passionsfrucht, die Loire adelt ihn mit mineralischer Tiefe. Sauvignon Blanc ist der Espresso unter den Weißweinen – kompromisslos wach machend.",
            "description_en": "A wake-up call for the senses – fresh as the first spring morning, wild as untamed nature. Gooseberry, freshly cut grass, elderflower, and a hint of flint explode in the glass. On the palate: crisp and precise, with acidity that strikes like lightning through the body. New Zealand makes it exotic with passion fruit, the Loire ennobles it with mineral depth. Sauvignon Blanc is the espresso of white wines – uncompromisingly awakening.",
            "description_fr": "Un réveil pour les sens – frais comme le premier matin de printemps, sauvage comme la nature indomptée. Groseille à maquereau, herbe fraîchement coupée, fleur de sureau et une touche de silex explosent dans le verre. En bouche: croquant et précis, avec une acidité qui frappe comme l'éclair.",
            "synonyms": ["Fumé Blanc", "Blanc Fumé"],
            "body": "leicht bis mittel",
            "acidity": "hoch",
            "tannin": "niedrig",
            "aging": "Edelstahl, trocken",
            "primary_aromas": ["Stachelbeere", "Gras", "Holunderblüte", "Limette"],
            "tertiary_aromas": ["Feuerstein", "Passionsfrucht", "Grapefruit"],
            "perfect_pairings": ["Ziegenkäse-Salat mit Walnüssen", "Austern auf Eis", "Gegrillter Wolfsbarsch mit Kräutern"],
            "perfect_pairings_en": ["Goat cheese salad with walnuts", "Oysters on ice", "Grilled sea bass with herbs"],
            "perfect_pairings_fr": ["Salade de chèvre aux noix", "Huîtres sur glace", "Bar grillé aux herbes"],
            "main_regions": ["Loire", "Neuseeland", "Bordeaux", "Chile"],
            "image_url": "https://images.unsplash.com/photo-1474722883778-792e7990302f?w=800"
        },
        {
            "slug": "gruener-veltliner",
            "name": "Grüner Veltliner",
            "type": "weiss",
            "description": "Österreichs flüssiges Gold – pfeffrig-würzig wie ein Gewürzhändler auf dem Naschmarkt, mit dem unverwechselbaren weißen Pfeffer, der Gaumenkribbeln garantiert. Grüner Apfel, Birne, weiße Kräuter und ein Hauch von Tabak vereinen sich zu einem Wein, der bodenständig und sophisticated zugleich ist. Am Gaumen cremig mit spritziger Säure, perfekt zu Wiens kulinarischen Schätzen. Das Wiener Schnitzel hat keinen besseren Freund.",
            "description_en": "Austria's liquid gold – peppery-spicy like a spice merchant at the Naschmarkt, with the unmistakable white pepper that guarantees tingling on the palate. Green apple, pear, white herbs, and a hint of tobacco unite in a wine that is down-to-earth and sophisticated at once. On the palate: creamy with zesty acidity, perfect with Vienna's culinary treasures. Wiener Schnitzel has no better friend.",
            "description_fr": "L'or liquide d'Autriche – poivré et épicé comme un marchand d'épices au Naschmarkt, avec ce poivre blanc incomparable qui garantit des picotements au palais. Pomme verte, poire, herbes blanches et une touche de tabac s'unissent dans un vin à la fois terre-à-terre et sophistiqué.",
            "synonyms": ["Weißgipfler", "Grüner Muskateller (falsch)"],
            "body": "leicht bis mittel",
            "acidity": "mittel bis hoch",
            "tannin": "niedrig",
            "aging": "Edelstahl oder großes Holz, trocken",
            "primary_aromas": ["Grüner Apfel", "Birne", "Weißer Pfeffer", "Kräuter"],
            "tertiary_aromas": ["Honig", "Tabak", "Nuss"],
            "perfect_pairings": ["Wiener Schnitzel mit Kartoffelsalat", "Spargel mit Sauce Hollandaise", "Gebackener Karpfen"],
            "perfect_pairings_en": ["Wiener Schnitzel with potato salad", "Asparagus with Hollandaise sauce", "Breaded carp"],
            "perfect_pairings_fr": ["Schnitzel viennois avec salade de pommes de terre", "Asperges sauce hollandaise", "Carpe panée"],
            "main_regions": ["Wachau", "Weinviertel", "Kamptal", "Kremstal"],
            "image_url": "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800"
        },
        {
            "slug": "gewuerztraminer",
            "name": "Gewürztraminer",
            "type": "weiss",
            "description": "Der Parfümeur unter den Rebsorten – betörend wie ein orientalischer Basar, golden wie Bernstein im Sonnenuntergang. Litschi, Rosenblätter, Muskatnuss und kandierter Ingwer umschmeicheln die Nase wie ein seidener Schleier. Am Gaumen üppig und exotisch, mit zarter Restsüße und cremiger Textur. Ein Wein für Mutige, die sich in ein aromatisches Abenteuer stürzen wollen. Perfekter Begleiter zur asiatischen Küche oder zum Käseplateau.",
            "description_en": "The perfumer among grape varieties – intoxicating like an oriental bazaar, golden like amber at sunset. Lychee, rose petals, nutmeg, and candied ginger caress the nose like a silk veil. On the palate: opulent and exotic, with delicate residual sweetness and creamy texture. A wine for the bold who want to dive into an aromatic adventure. Perfect companion for Asian cuisine or cheese platter.",
            "description_fr": "Le parfumeur parmi les cépages – enivrant comme un bazar oriental, doré comme l'ambre au coucher du soleil. Litchi, pétales de rose, muscade et gingembre confit caressent le nez comme un voile de soie. En bouche: opulent et exotique, avec une délicate sucrosité résiduelle.",
            "synonyms": ["Traminer", "Savagnin Rosé"],
            "body": "mittel bis vollmundig",
            "acidity": "niedrig bis mittel",
            "tannin": "niedrig",
            "aging": "Edelstahl oder Holz, trocken bis lieblich",
            "primary_aromas": ["Litschi", "Rose", "Mango", "Orangenschale"],
            "tertiary_aromas": ["Muskatnuss", "Ingwer", "Honig", "Zimt"],
            "perfect_pairings": ["Ente à l'Orange", "Thai-Curry mit Kokosmilch", "Münsterkäse", "Foie Gras"],
            "perfect_pairings_en": ["Duck à l'Orange", "Thai curry with coconut milk", "Munster cheese", "Foie Gras"],
            "perfect_pairings_fr": ["Canard à l'orange", "Curry thaï au lait de coco", "Munster", "Foie Gras"],
            "main_regions": ["Elsass", "Südtirol", "Deutschland", "Neuseeland"],
            "image_url": "https://images.unsplash.com/photo-1507434965515-61970f2bd7c6?w=800"
        },
        {
            "slug": "pinot-grigio",
            "name": "Pinot Grigio / Pinot Gris",
            "type": "weiss",
            "description": "Der Verwandlungskünstler – in Italien knackig-frisch wie ein Sommertag am Gardasee, im Elsass cremig-komplex wie ein herbstlicher Nebel über den Vogesen. Zitrone, grüne Birne, Mandel und weiße Blüten tanzen elegant im Glas. Unkompliziert und doch raffiniert, wie ein gut sitzender Leinenanzug an einem warmen Abend. Der perfekte Aperitivo-Wein, der aber auch zum Essen glänzt.",
            "description_en": "The transformation artist – in Italy crisp and fresh like a summer day at Lake Garda, in Alsace creamy and complex like autumn fog over the Vosges. Lemon, green pear, almond, and white blossoms dance elegantly in the glass. Uncomplicated yet refined, like a well-fitting linen suit on a warm evening. The perfect aperitivo wine that also shines with food.",
            "description_fr": "L'artiste de la transformation – en Italie frais et croquant comme un jour d'été au lac de Garde, en Alsace crémeux et complexe comme un brouillard d'automne sur les Vosges. Citron, poire verte, amande et fleurs blanches dansent élégamment dans le verre.",
            "synonyms": ["Grauburgunder", "Ruländer"],
            "body": "leicht bis mittel",
            "acidity": "mittel",
            "tannin": "niedrig",
            "aging": "Edelstahl, trocken",
            "primary_aromas": ["Zitrone", "Birne", "Apfel", "Mandel"],
            "tertiary_aromas": ["Honig", "Brioche", "Nuss"],
            "perfect_pairings": ["Carpaccio vom Lachs", "Risotto mit Meeresfrüchten", "Vitello Tonnato"],
            "perfect_pairings_en": ["Salmon carpaccio", "Seafood risotto", "Vitello Tonnato"],
            "perfect_pairings_fr": ["Carpaccio de saumon", "Risotto aux fruits de mer", "Vitello Tonnato"],
            "main_regions": ["Norditalien", "Elsass", "Oregon", "Deutschland"],
            "image_url": "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800"
        },
        # RED WINES
        {
            "slug": "pinot-noir",
            "name": "Pinot Noir",
            "type": "rot",
            "description": "Die Diva unter den roten Reben – kapriziös, anspruchsvoll, aber in perfekter Form unvergleichlich. Burgunderrot wie ein Sonnenuntergang über den Côte d'Or, mit Aromen von frischen Kirschen, Erdbeeren, Rosenblättern und feuchtem Waldboden. Am Gaumen samtweich mit seidigen Tanninen, einer vibrierenden Säure und einem Finale, das Geschichten erzählt. Pinot Noir verlangt Hingabe – vom Winzer wie vom Genießer. Der Lohn: purer, unvergesslicher Trinkgenuss.",
            "description_en": "The diva among red grapes – capricious, demanding, but incomparable in perfect form. Burgundy red like a sunset over the Côte d'Or, with aromas of fresh cherries, strawberries, rose petals, and damp forest floor. On the palate: velvet soft with silky tannins, vibrant acidity, and a finish that tells stories. Pinot Noir demands devotion – from winemaker and connoisseur alike. The reward: pure, unforgettable drinking pleasure.",
            "description_fr": "La diva des cépages rouges – capricieuse, exigeante, mais incomparable dans sa forme parfaite. Rouge bourgogne comme un coucher de soleil sur la Côte d'Or, avec des arômes de cerises fraîches, fraises, pétales de rose et sous-bois humide. En bouche: doux comme du velours avec des tanins soyeux.",
            "synonyms": ["Spätburgunder", "Blauburgunder", "Pinot Nero"],
            "body": "leicht bis mittel",
            "acidity": "mittel bis hoch",
            "tannin": "niedrig bis mittel",
            "aging": "Holz, trocken",
            "primary_aromas": ["Kirsche", "Erdbeere", "Himbeere", "Rose"],
            "tertiary_aromas": ["Waldboden", "Pilze", "Leder", "Gewürze"],
            "perfect_pairings": ["Coq au Vin", "Ente mit Kirschsauce", "Lachs mit Pinot-Noir-Reduktion", "Brie de Meaux"],
            "perfect_pairings_en": ["Coq au Vin", "Duck with cherry sauce", "Salmon with Pinot Noir reduction", "Brie de Meaux"],
            "perfect_pairings_fr": ["Coq au Vin", "Canard sauce cerises", "Saumon à la réduction de Pinot Noir", "Brie de Meaux"],
            "main_regions": ["Burgund", "Oregon", "Neuseeland", "Deutschland"],
            "image_url": "https://images.unsplash.com/photo-1516594915697-87eb3b1c14ea?w=800"
        },
        {
            "slug": "cabernet-sauvignon",
            "name": "Cabernet Sauvignon",
            "type": "rot",
            "description": "Der König der roten Rebsorten – majestätisch, kraftvoll, unsterblich. Tiefes Rubinrot, fast undurchdringlich, wie das Versprechen auf etwas Großes. Schwarze Johannisbeere, Zedernholz, dunkle Schokolade und der unverwechselbare Duft von Bleistiftspitze. Am Gaumen strukturiert und muskulös, mit Tanninen wie Samt und Stahl zugleich. Cabernet braucht Zeit – wie alle großen Persönlichkeiten. Mit Reife offenbart er Tabak, Leder und eine fast meditative Tiefe.",
            "description_en": "The king of red grape varieties – majestic, powerful, immortal. Deep ruby red, almost impenetrable, like a promise of something great. Blackcurrant, cedarwood, dark chocolate, and the unmistakable scent of pencil shavings. On the palate: structured and muscular, with tannins like velvet and steel at once. Cabernet needs time – like all great personalities. With age, it reveals tobacco, leather, and an almost meditative depth.",
            "description_fr": "Le roi des cépages rouges – majestueux, puissant, immortel. Rouge rubis profond, presque impénétrable, comme la promesse de quelque chose de grand. Cassis, bois de cèdre, chocolat noir et le parfum incomparable de copeaux de crayon. En bouche: structuré et musclé, avec des tanins velours et acier à la fois.",
            "synonyms": ["Bouchet", "Petit Cabernet"],
            "body": "vollmundig",
            "acidity": "mittel bis hoch",
            "tannin": "hoch",
            "aging": "Holz (Barrique), trocken",
            "primary_aromas": ["Schwarze Johannisbeere", "Pflaume", "Kirsche", "Paprika"],
            "tertiary_aromas": ["Zedernholz", "Tabak", "Leder", "Schokolade", "Bleistift"],
            "perfect_pairings": ["T-Bone Steak vom Grill", "Lammkarree mit Rosmarin", "Entrecôte Café de Paris", "Gereifter Cheddar"],
            "perfect_pairings_en": ["Grilled T-bone steak", "Rack of lamb with rosemary", "Entrecôte Café de Paris", "Aged Cheddar"],
            "perfect_pairings_fr": ["T-bone steak grillé", "Carré d'agneau au romarin", "Entrecôte Café de Paris", "Cheddar affiné"],
            "main_regions": ["Bordeaux", "Napa Valley", "Chile", "Australien"],
            "image_url": "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=800"
        },
        {
            "slug": "merlot",
            "name": "Merlot",
            "type": "rot",
            "description": "Der sanfte Riese – zugänglich wie ein alter Freund, tiefgründig wie ein gutes Gespräch bei Kerzenlicht. Dunkle Pflaumen, reife Kirschen, Schokolade und ein Hauch von Kräutern malen ein Bild von Eleganz ohne Anstrengung. Am Gaumen geschmeidig und rund, mit weichen Tanninen, die wie eine warme Umarmung wirken. Merlot ist Balsam für die Seele – unkompliziert genug für jeden Tag, komplex genug für besondere Momente. Der Wein, der niemanden ausschließt.",
            "description_en": "The gentle giant – approachable like an old friend, profound like a good conversation by candlelight. Dark plums, ripe cherries, chocolate, and a hint of herbs paint a picture of effortless elegance. On the palate: supple and round, with soft tannins that feel like a warm embrace. Merlot is balm for the soul – uncomplicated enough for everyday, complex enough for special moments. The wine that excludes no one.",
            "description_fr": "Le gentil géant – accessible comme un vieil ami, profond comme une bonne conversation à la lueur des bougies. Prunes sombres, cerises mûres, chocolat et une touche d'herbes peignent une image d'élégance sans effort. En bouche: souple et rond, avec des tanins doux comme une étreinte chaleureuse.",
            "synonyms": ["Merlot Noir", "Vitraille"],
            "body": "mittel bis vollmundig",
            "acidity": "mittel",
            "tannin": "mittel",
            "aging": "Holz, trocken",
            "primary_aromas": ["Pflaume", "Kirsche", "Brombeere", "Veilchen"],
            "tertiary_aromas": ["Schokolade", "Kaffee", "Vanille", "Leder"],
            "perfect_pairings": ["Rinderbraten mit Rotweinjus", "Pilzrisotto mit Trüffel", "Hartkäse wie Pecorino", "Pasta Bolognese"],
            "perfect_pairings_en": ["Beef roast with red wine jus", "Mushroom risotto with truffle", "Hard cheese like Pecorino", "Pasta Bolognese"],
            "perfect_pairings_fr": ["Rôti de bœuf au jus de vin rouge", "Risotto aux champignons et truffe", "Fromage à pâte dure comme Pecorino", "Pâtes Bolognaise"],
            "main_regions": ["Bordeaux (Pomerol)", "Toskana", "Chile", "Kalifornien"],
            "image_url": "https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=800"
        },
        {
            "slug": "syrah",
            "name": "Syrah / Shiraz",
            "type": "rot",
            "description": "Der Rebell – dunkel, geheimnisvoll und mit einer Intensität, die unter die Haut geht. Brombeere, Veilchen, schwarzer Pfeffer und rauchige Speckwürze vereinen sich zu einem Wein von dramatischer Schönheit. In der Rhône elegant und würzig, in Australien als Shiraz kraftvoll und üppig. Am Gaumen konzentriert mit festen Tanninen und einem Finale, das nach Rauch und Wildheit schmeckt. Für alle, die Wein wollen, der Geschichten von fernen Ländern erzählt.",
            "description_en": "The rebel – dark, mysterious, and with an intensity that gets under your skin. Blackberry, violet, black pepper, and smoky bacon spice unite in a wine of dramatic beauty. In the Rhône elegant and spicy, in Australia as Shiraz powerful and opulent. On the palate: concentrated with firm tannins and a finish that tastes of smoke and wilderness. For those who want wine that tells stories of distant lands.",
            "description_fr": "Le rebelle – sombre, mystérieux et avec une intensité qui prend aux tripes. Mûre, violette, poivre noir et épices fumées de lard s'unissent dans un vin d'une beauté dramatique. Dans le Rhône élégant et épicé, en Australie comme Shiraz puissant et opulent.",
            "synonyms": ["Shiraz", "Hermitage", "Sérine"],
            "body": "vollmundig",
            "acidity": "mittel",
            "tannin": "mittel bis hoch",
            "aging": "Holz (Barrique), trocken",
            "primary_aromas": ["Brombeere", "Schwarze Kirsche", "Pflaume", "Veilchen"],
            "tertiary_aromas": ["Schwarzer Pfeffer", "Speck", "Rauch", "Leder", "Schokolade"],
            "perfect_pairings": ["Gegrilltes Lamm mit Kräuterkruste", "Wild mit Brombeersauce", "BBQ Ribs", "Roquefort"],
            "perfect_pairings_en": ["Grilled lamb with herb crust", "Game with blackberry sauce", "BBQ ribs", "Roquefort"],
            "perfect_pairings_fr": ["Agneau grillé en croûte d'herbes", "Gibier sauce aux mûres", "Côtes de porc BBQ", "Roquefort"],
            "main_regions": ["Rhône", "Australien (Barossa)", "Kalifornien", "Chile"],
            "image_url": "https://images.unsplash.com/photo-1568213816046-0ee1c42bd559?w=800"
        },
        {
            "slug": "tempranillo",
            "name": "Tempranillo",
            "type": "rot",
            "description": "Die Seele Spaniens – stolz wie ein Flamenco-Tänzer, warm wie die kastilische Sonne. Kirsche, Leder, Tabak und getrocknete Feigen vereinen sich mit einer erdigen Würze, die nach spanischer Erde schmeckt. Am Gaumen elegant und mittelschwer, mit geschliffenen Tanninen und einer Balance, die Jahrzehnte überdauert. Von Rioja bis Ribera del Duero – Tempranillo ist der rote Faden, der durch Spaniens große Weingeschichte webt.",
            "description_en": "The soul of Spain – proud as a flamenco dancer, warm as the Castilian sun. Cherry, leather, tobacco, and dried figs unite with an earthy spice that tastes of Spanish soil. On the palate: elegant and medium-bodied, with polished tannins and a balance that lasts decades. From Rioja to Ribera del Duero – Tempranillo is the red thread woven through Spain's great wine history.",
            "description_fr": "L'âme de l'Espagne – fière comme un danseur de flamenco, chaude comme le soleil castillan. Cerise, cuir, tabac et figues séchées s'unissent à une épice terreuse qui a le goût de la terre espagnole. En bouche: élégant et moyennement corsé, avec des tanins polis et un équilibre qui dure des décennies.",
            "synonyms": ["Tinto Fino", "Tinta de Toro", "Cencibel", "Aragonez"],
            "body": "mittel bis vollmundig",
            "acidity": "mittel",
            "tannin": "mittel",
            "aging": "Holz (amerikanisch oder französisch), trocken",
            "primary_aromas": ["Kirsche", "Pflaume", "Tomate", "Feige"],
            "tertiary_aromas": ["Leder", "Tabak", "Vanille", "Kokos", "Dill"],
            "perfect_pairings": ["Tapas mit Jamón Ibérico", "Lamm-Eintopf mit Chorizo", "Gegrilltes Spanferkel", "Manchego"],
            "perfect_pairings_en": ["Tapas with Jamón Ibérico", "Lamb stew with Chorizo", "Grilled suckling pig", "Manchego"],
            "perfect_pairings_fr": ["Tapas au Jambon Ibérique", "Ragoût d'agneau au Chorizo", "Cochon de lait grillé", "Manchego"],
            "main_regions": ["Rioja", "Ribera del Duero", "Toro", "Portugal (Alentejo)"],
            "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=800"
        },
        {
            "slug": "sangiovese",
            "name": "Sangiovese",
            "type": "rot",
            "description": "Das Herz der Toskana – lebhaft wie ein italienischer Sonntag, rustikal wie eine Trattoria in den Hügeln von Chianti. Sauerkirsche, getrocknete Tomaten, Oregano und ein Hauch von Veilchen malen ein Bild von dolce vita. Am Gaumen saftig mit präsenter Säure und körnigen Tanninen, die nach Essen schreien. Sangiovese ist gemacht für den Tisch – für Pasta, Pizza, und lange Abende mit Freunden. Salute!",
            "description_en": "The heart of Tuscany – lively as an Italian Sunday, rustic as a trattoria in the Chianti hills. Sour cherry, dried tomatoes, oregano, and a hint of violet paint a picture of dolce vita. On the palate: juicy with present acidity and grainy tannins that cry out for food. Sangiovese is made for the table – for pasta, pizza, and long evenings with friends. Salute!",
            "description_fr": "Le cœur de la Toscane – vif comme un dimanche italien, rustique comme une trattoria dans les collines du Chianti. Griotte, tomates séchées, origan et une touche de violette peignent une image de dolce vita. En bouche: juteux avec une acidité présente et des tanins granuleux qui crient pour de la nourriture.",
            "synonyms": ["Brunello", "Prugnolo Gentile", "Morellino"],
            "body": "mittel bis vollmundig",
            "acidity": "hoch",
            "tannin": "mittel bis hoch",
            "aging": "Holz (großes oder kleines Fass), trocken",
            "primary_aromas": ["Sauerkirsche", "Erdbeere", "Pflaume", "Veilchen"],
            "tertiary_aromas": ["Tomate", "Leder", "Tabak", "Espresso", "Kräuter"],
            "perfect_pairings": ["Bistecca alla Fiorentina", "Pasta al Ragù", "Pizza Margherita", "Pecorino Toscano"],
            "perfect_pairings_en": ["Bistecca alla Fiorentina", "Pasta al Ragù", "Pizza Margherita", "Pecorino Toscano"],
            "perfect_pairings_fr": ["Bistecca alla Fiorentina", "Pâtes au Ragù", "Pizza Margherita", "Pecorino Toscano"],
            "main_regions": ["Chianti", "Brunello di Montalcino", "Vino Nobile di Montepulciano", "Romagna"],
            "image_url": "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800"
        },
        {
            "slug": "nebbiolo",
            "name": "Nebbiolo",
            "type": "rot",
            "description": "Der Aristokrat des Piemonts – trügerisch hell, aber mit einer Kraft, die Könige und Päpste in die Knie zwang. Ziegelrot wie die Dächer Albas, mit betörenden Aromen von Rosen, Teer, Kirschen und Gewürzen. Am Gaumen eine Explosion aus Säure und Tanninen – herausfordernd, fordernd, belohnend. Barolo und Barbaresco sind seine Kronen. Nebbiolo braucht Geduld: Mit 20 Jahren Reife offenbart er Trüffel, Herbstlaub und transzendente Tiefe.",
            "description_en": "The aristocrat of Piedmont – deceptively pale, but with a power that brought kings and popes to their knees. Brick red like the roofs of Alba, with intoxicating aromas of roses, tar, cherries, and spices. On the palate: an explosion of acidity and tannins – challenging, demanding, rewarding. Barolo and Barbaresco are its crowns. Nebbiolo needs patience: at 20 years of age, it reveals truffle, autumn leaves, and transcendent depth.",
            "description_fr": "L'aristocrate du Piémont – trompeusement pâle, mais avec une puissance qui a mis rois et papes à genoux. Rouge brique comme les toits d'Alba, avec des arômes enivrants de roses, goudron, cerises et épices. En bouche: une explosion d'acidité et de tanins – exigeant, défiant, gratifiant.",
            "synonyms": ["Spanna", "Chiavennasca", "Picotener"],
            "body": "vollmundig",
            "acidity": "hoch",
            "tannin": "hoch",
            "aging": "Holz (große Fässer), trocken",
            "primary_aromas": ["Rose", "Kirsche", "Himbeere", "Veilchen"],
            "tertiary_aromas": ["Teer", "Trüffel", "Leder", "Tabak", "Herbstlaub"],
            "perfect_pairings": ["Brasato al Barolo", "Tajarin mit weißen Trüffeln", "Wild-Ragout", "Gereifter Parmigiano"],
            "perfect_pairings_en": ["Brasato al Barolo", "Tajarin with white truffles", "Game ragout", "Aged Parmigiano"],
            "perfect_pairings_fr": ["Brasato al Barolo", "Tajarin aux truffes blanches", "Ragoût de gibier", "Parmigiano affiné"],
            "main_regions": ["Barolo", "Barbaresco", "Langhe", "Valtellina"],
            "image_url": "https://images.unsplash.com/photo-1474722883778-792e7990302f?w=800"
        },
        {
            "slug": "malbec",
            "name": "Malbec",
            "type": "rot",
            "description": "Der argentinische Traum – einst in Frankreich verschmäht, in den Anden zur Weltklasse gereift. Tiefviolett wie der Nachthimmel über Mendoza, mit üppigen Aromen von Brombeere, schwarzer Pflaume, Veilchen und süßen Gewürzen. Am Gaumen samtig und vollmundig, mit weichen Tanninen und einer saftigen Frucht, die nach mehr verlangt. Malbec ist der Wein für Steakliebhaber – geboren fürs Grillen unter freiem Himmel.",
            "description_en": "The Argentine dream – once scorned in France, matured to world class in the Andes. Deep violet like the night sky over Mendoza, with opulent aromas of blackberry, dark plum, violet, and sweet spices. On the palate: velvety and full-bodied, with soft tannins and a juicy fruit that demands more. Malbec is the wine for steak lovers – born for grilling under the open sky.",
            "description_fr": "Le rêve argentin – autrefois dédaigné en France, mûri vers l'excellence mondiale dans les Andes. Violet profond comme le ciel nocturne au-dessus de Mendoza, avec des arômes opulents de mûre, prune noire, violette et épices douces. En bouche: velouté et corsé, avec des tanins souples.",
            "synonyms": ["Côt", "Auxerrois", "Pressac"],
            "body": "vollmundig",
            "acidity": "mittel",
            "tannin": "mittel",
            "aging": "Holz, trocken",
            "primary_aromas": ["Brombeere", "Schwarze Pflaume", "Kirsche", "Veilchen"],
            "tertiary_aromas": ["Vanille", "Kakao", "Tabak", "Mokka", "Leder"],
            "perfect_pairings": ["Argentinisches Asado", "Ribeye Steak", "Empanadas", "Blauschimmelkäse"],
            "perfect_pairings_en": ["Argentine Asado", "Ribeye steak", "Empanadas", "Blue cheese"],
            "perfect_pairings_fr": ["Asado argentin", "Steak Ribeye", "Empanadas", "Fromage bleu"],
            "main_regions": ["Mendoza", "Cahors", "Chile", "Kalifornien"],
            "image_url": "https://images.unsplash.com/photo-1516594915697-87eb3b1c14ea?w=800"
        }
    ]
    
    # Clear existing and insert new
    await db.grape_varieties.delete_many({})
    
    for grape_data in grapes:
        grape = GrapeVariety(**grape_data)
        doc = grape.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.grape_varieties.insert_one(doc)
    
    return {"message": f"{len(grapes)} Rebsorten wurden erstellt"}

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
