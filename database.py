import os
from motor.motor_asyncio import AsyncIOMotorClient

# Railway will provide this environment variable
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.localshop

user_collection = database.get_collection("users")
product_collection = database.get_collection("products")