"""
Simple test to verify wine_database endpoint works correctly
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def test():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['wine_pairing_db']
    
    # Check wines in database
    count = await db.wine_database.count_documents({})
    print(f"Total wines in wine_database: {count}")
    
    # Get first wine
    wine = await db.wine_database.find_one({}, {"_id": 0})
    
    if wine:
        print(f"\nFirst wine:")
        print(f"  Name: {wine.get('name')}")
        print(f"  Has description: {('description' in wine)}")
        print(f"  Has description_de: {('description_de' in wine)}")
        print(f"  ID: {wine.get('id')}")
        
        # Check if it matches the error
        if wine.get('id') == '4f2a7e1e-cc7d-4ef3-848b-8dff3ba77e64':
            print("\n⚠️ This is the problematic wine from the error!")
    
    await client.close()

if __name__ == '__main__':
    asyncio.run(test())
