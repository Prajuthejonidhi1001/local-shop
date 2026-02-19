import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from database import MONGO_DETAILS

async def clear_data():
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_DETAILS)
    db = client.localshop
    
    print("⚠️  WARNING: You are about to DELETE ALL DATA (Users, Products, Carts).")
    print("This action cannot be undone.")
    
    confirm = input("Type 'DELETE' to confirm: ")
    
    if confirm == "DELETE":
        # Delete all documents from collections
        print("Deleting users...")
        await db.users.delete_many({})
        print("✅ All Users deleted.")
        
        print("Deleting products...")
        await db.products.delete_many({})
        print("✅ All Products deleted.")
        
        print("Deleting carts...")
        await db.carts.delete_many({})
        print("✅ All Carts deleted.")
        
        print("\nDatabase has been completely cleared.")
    else:
        print("❌ Operation cancelled.")

if __name__ == "__main__":
    asyncio.run(clear_data())