import os
import motor.motor_asyncio

# MongoDB Connection String
# Option 1: Local MongoDB (Default)
# MONGO_DETAILS = "mongodb://127.0.0.1:27017"

# Option 2: MongoDB Atlas (Cloud) - Uncomment and replace <password> with your real password
# MONGO_DETAILS = "mongodb+srv://<username>:<password>@cluster0.example.mongodb.net/?retryWrites=true&w=majority"

# Use environment variable if available (Live), otherwise use local (Dev)
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://127.0.0.1:27017")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.localshop

user_collection = database.get_collection("users")
product_collection = database.get_collection("products")
cart_collection = database.get_collection("carts")