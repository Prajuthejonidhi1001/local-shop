import asyncio
import csv
from motor.motor_asyncio import AsyncIOMotorClient
from database import MONGO_DETAILS

async def export_data():
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_DETAILS)
    db = client.localshop
    
    print("Exporting database content to CSV files...")

    # 1. Users
    users = await db.users.find().to_list(length=1000)
    if users:
        # Collect all field names dynamically
        fieldnames = set()
        for user in users:
            user['_id'] = str(user['_id'])
            fieldnames.update(user.keys())
            
        with open('users.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(fieldnames))
            writer.writeheader()
            writer.writerows(users)
        print(f"✅ Exported {len(users)} users to 'users.csv'")
    else:
        print("No users found to export.")

    # 2. Products
    products = await db.products.find().to_list(length=1000)
    if products:
        fieldnames = set()
        for product in products:
            product['_id'] = str(product['_id'])
            fieldnames.update(product.keys())
            
        with open('products.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(fieldnames))
            writer.writeheader()
            writer.writerows(products)
        print(f"✅ Exported {len(products)} products to 'products.csv'")
    else:
        print("No products found to export.")

if __name__ == "__main__":
    asyncio.run(export_data())
