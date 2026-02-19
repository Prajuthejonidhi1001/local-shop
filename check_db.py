import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from database import MONGO_DETAILS

async def check():
    uri = MONGO_DETAILS
    client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
    try:
        print(f"Attempting to connect to {uri}...")
        await client.admin.command('ping')
        print("✅ Success! MongoDB is running and accessible.")
    except Exception as e:
        print("❌ Connection failed.")
        print(f"Error: {e}")
        print("\nPossible causes:")
        print("1. MongoDB service is not running (Run 'Start-Service MongoDB' in Admin Terminal)")
        print(r"   OR Manual start: cd 'C:\Program Files\MongoDB\Server\8.2\bin' ; .\mongod.exe --dbpath='C:\data\db'")
        print("2. MongoDB is not installed")

if __name__ == "__main__":
    asyncio.run(check())