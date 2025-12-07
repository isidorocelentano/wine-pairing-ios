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
    import json
    import re
    
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
