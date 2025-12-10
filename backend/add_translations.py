"""
Add English and French translations for country intros and descriptions
"""
import asyncio
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# Country intro translations
COUNTRY_INTROS_EN = {
    "Italien": "🍝 Aperitivo all'italiana: The Passion on the Plate. Italy is more than pizza and pasta – it's the birthplace of regional cuisine, where every city, every village guards its own, often centuries-old specialty.",
    "Frankreich": "🥐 Cuisine Bourgeoise: The Elegance of Terroirs. France is the undisputed epicenter of classical cuisine and the wine world. Here, cultural monuments like a Bresse chicken meet the greatest wines on earth.",
    "Spanien": "💃 Fiesta del Sabor: Sun, Tapas and Intense Flavors. Spain is a feast for the senses, combining the heat of the sun and the diversity of regions on the plate.",
    "Österreich": "🏔️ Alpine Elegance: Crispy Breading and Vibrant Acidity. Austria offers a unique blend of alpine groundedness and imperial elegance.",
    "Schweiz": "🧀 Alpine Richesse: Mountain Cheese, Fondue and Hidden Treasures. Switzerland is a mosaic of culinary influences – shaped by the mountains, warmth and diversity of its cultures.",
    "Griechenland": "☀️ Ode to the Aegean: Saltiness, Olive Oil and Ancient Flavors. Greece is the cradle of the Mediterranean diet, a cuisine that lives on the saltiness of the sea, fragrant oregano and the rich olive oil of the sun.",
    "Türkei": "🍢 Anatolian Fire: Smoke, Spice and the Bridge of Cultures. Turkey is a culinary powerhouse that combines the rich flavors of the Orient with the freshness of the Aegean.",
    "Japan": "🥢 Umami Masters: Precision, Subtlety and the Art of Texture. Japan is a culinary universe of subtlety and perfection. The cuisine lives on the magic of umami.",
    "Deutschland": "🌲 From Riesling Slopes to the Inn: Spice, Texture and Clarity. German cuisine is a celebration of regional identities."
}

COUNTRY_INTROS_FR = {
    "Italien": "🍝 Aperitivo all'italiana : La Passion dans l'Assiette. L'Italie, c'est bien plus que pizza et pâtes – c'est le berceau de la cuisine régionale, où chaque ville, chaque village protège sa propre spécialité, souvent centenaire.",
    "Frankreich": "🥐 Cuisine Bourgeoise : L'Élégance des Terroirs. La France est l'épicentre incontesté de la cuisine classique et du monde du vin. Ici, des monuments culturels comme une poularde de Bresse rencontrent les plus grands vins de la terre.",
    "Spanien": "💃 Fiesta del Sabor : Soleil, Tapas et Arômes Intenses. L'Espagne est une fête pour les sens, qui réunit dans l'assiette la chaleur du soleil et la diversité des régions.",
    "Österreich": "🏔️ Élégance Alpine : Panure Croustillante et Acidité Vivante. L'Autriche offre un mélange unique d'authenticité alpine et d'élégance impériale.",
    "Schweiz": "🧀 Richesse Alpine : Fromage de Montagne, Fondue et Trésors Cachés. La Suisse est une mosaïque d'influences culinaires – façonnée par les montagnes, la chaleur et la diversité de ses cultures.",
    "Griechenland": "☀️ Ode à la Mer Égée : Salinité, Huile d'Olive et Saveurs Antiques. La Grèce est le berceau du régime méditerranéen, une cuisine qui vit de la salinité de la mer, de l'origan parfumé et de l'huile d'olive riche du soleil.",
    "Türkei": "🍢 Feu Anatolien : Fumée, Épices et le Pont des Cultures. La Turquie est une puissance culinaire qui combine les riches saveurs de l'Orient avec la fraîcheur de la mer Égée.",
    "Japan": "🥢 Maîtres de l'Umami : Précision, Subtilité et l'Art de la Texture. Le Japon est un univers culinaire de subtilité et de perfection. La cuisine vit de la magie de l'umami.",
    "Deutschland": "🌲 Des Pentes de Riesling à l'Auberge : Épice, Texture et Clarté. La cuisine allemande est une célébration des identités régionales."
}


async def update_translations():
    """Add English and French translations"""
    
    print("🌍 Adding Multilingual Translations\n")
    print("=" * 60)
    
    # Update country intros
    print("\n📍 Updating Country Intros (EN/FR)...")
    for country in COUNTRY_INTROS_EN.keys():
        result = await db.regional_pairings.update_many(
            {"country": country},
            {
                "$set": {
                    "country_intro_en": COUNTRY_INTROS_EN[country],
                    "country_intro_fr": COUNTRY_INTROS_FR[country]
                }
            }
        )
        if result.modified_count > 0:
            print(f"  ✓ {country}: Added EN/FR intros ({result.modified_count} docs)")
    
    print("\n" + "=" * 60)
    print("✅ Country Intros Updated!")


async def update_images():
    """Update new country images"""
    
    print("\n\n🖼️ Updating New Country Images...")
    print("=" * 60)
    
    COUNTRY_IMAGES = {
        "Italien": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/gzi6i1r1_WINE-PAIRING.ONLINE%20SOMMELIER%20CLAUDE%20%20IN%20ITALIEN.png",
        "Österreich": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/p9jyplfk_WINE-PAIRING.ONLINE%20SOMMELIER%20CLAUDE%20%20IN%20AUSTRIA.png",
        "Türkei": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/8fnlvn47_WINE-PAIRING.ONLINE%20SOMMELIER%20CLAUDE%20%20IN%20T%C3%9CRKEI.png",
        "Deutschland": "https://customer-assets.emergentagent.com/job_9f296b6c-6dd4-4ccd-a818-3f5ca61a4e15/artifacts/udlwr19h_WINE-PAIRING.ONLINE%20SOMMELIER%20CLAUDE%20%20IN%20DEUTSCHLAND.png"
    }
    
    for country, image_url in COUNTRY_IMAGES.items():
        result = await db.regional_pairings.update_many(
            {"country": country},
            {"$set": {"country_image_url": image_url}}
        )
        print(f"  ✓ {country}: Image added ({result.modified_count} docs)")


async def main():
    await update_translations()
    await update_images()
    
    # Sample check
    print("\n\n📊 Sample Check:")
    print("=" * 60)
    sample = await db.regional_pairings.find_one(
        {"country": "Italien"}, 
        {
            "_id": 0, 
            "country": 1, 
            "country_intro": 1,
            "country_intro_en": 1,
            "country_intro_fr": 1,
            "country_image_url": 1
        }
    )
    if sample:
        print(f"\n🇮🇹 Italien Sample:")
        print(f"  DE: {sample.get('country_intro', 'N/A')[:70]}...")
        print(f"  EN: {sample.get('country_intro_en', 'N/A')[:70]}...")
        print(f"  FR: {sample.get('country_intro_fr', 'N/A')[:70]}...")
        print(f"  Image: {'✅ Present' if sample.get('country_image_url') else '❌ Missing'}")
    
    print("\n" + "=" * 60)
    print("✅ All Updates Complete!")


if __name__ == '__main__':
    asyncio.run(main())
