import os
import shutil
import io
import csv
import urllib.parse
from fastapi import FastAPI, HTTPException, Depends, status, Request, Form, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from bson import ObjectId
from typing import Optional

from database import user_collection, product_collection
from models import UserCreate, UserInDB, ProductInDB
from auth import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from generate_icon import create_icon

# Handle missing generate_icon module gracefully
try:
    from generate_icon import create_icon
except ImportError:
    def create_icon():
        print("⚠️ generate_icon module not found. Skipping icon generation.")

app = FastAPI(title="Local Shop")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sectors_data = [
  {
    "name": "secondhand-vehicles",
    "displayName": "Secondhand Vehicles",
    "image": "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?w=600&q=80",
    "description": "Pre-owned two, three and four wheelers and commercial vehicles",
    "subSectors": [
        {"name": "Two Wheelers", "image": "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?w=600&q=80"},
        {"name": "Four Wheelers", "image": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=600&q=80"},
        {"name": "Three Wheelers", "image": "https://images.unsplash.com/photo-1598084991519-c90900bf920c?w=600&q=80"},
        {"name": "Commercial Vehicles", "image": "https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?w=600&q=80"}
    ]
  },
  {
    "name": "fashion",
    "displayName": "Fashion",
    "image": "https://images.unsplash.com/photo-1537832816519-689ad163238b?w=600&q=80",
    "description": "Textiles, footwear, fancy stores and tailoring services",
    "subSectors": [
        {"name": "Textile", "image": "https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?w=600&q=80"},
        {"name": "Footwares", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80"},
        {"name": "Fancy Stores", "image": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=600&q=80"},
        {"name": "Tailoring", "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=600&q=80"}
    ]
  },
  {
    "name": "construction",
    "displayName": "Construction",
    "image": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=600&q=80",
    "description": "Materials and services for construction and interiors",
    "subSectors": [
        {"name": "Steels", "image": "https://images.unsplash.com/photo-1535813547-99c456a41d4a?w=600&q=80"},
        {"name": "Hardware", "image": "https://images.unsplash.com/photo-1581235720704-06d3acfcb36f?w=600&q=80"},
        {"name": "Home Decor", "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&q=80"},
        {"name": "Interiors", "image": "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=600&q=80"},
        {"name": "Paint", "image": "https://images.unsplash.com/photo-1562259949-e8e7689d7828?w=600&q=80"},
        {"name": "Electricals", "image": "https://images.unsplash.com/photo-1555732418-3f8e74739e81?w=600&q=80"}
    ]
  },
  {
    "name": "marts",
    "displayName": "Marts",
    "image": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=600&q=80",
    "description": "Retail marts and marketplaces",
    "subSectors": [
        {"name": "Supermarkets", "image": "https://images.unsplash.com/photo-1542838132-92c53300491e?w=600&q=80"},
        {"name": "Convenience Stores", "image": "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=600&q=80"},
        {"name": "Wholesale Markets", "image": "https://images.unsplash.com/photo-1533900298318-6b8da08a523e?w=600&q=80"},
        {"name": "Online Marts", "image": "https://images.unsplash.com/photo-1556742049-0cfed4f7a07d?w=600&q=80"}
    ]
  },
  {
    "name": "agriculture",
    "displayName": "Agriculture",
    "image": "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=600&q=80",
    "description": "Farming supplies and equipment",
    "subSectors": [
        {"name": "Seeds & Fertilizers", "image": "https://images.unsplash.com/photo-1628352081506-83c43123ed6d?w=600&q=80"},
        {"name": "Farm Equipment", "image": "https://images.unsplash.com/photo-1592982537447-6f2a6a0c7c18?w=600&q=80"},
        {"name": "Pesticides", "image": "https://images.unsplash.com/photo-1585314062340-f1a5a7c9328d?w=600&q=80"},
        {"name": "Irrigation Systems", "image": "https://images.unsplash.com/photo-1563514227147-6d2ff665a6a0?w=600&q=80"}
    ]
  },
  {
    "name": "traders",
    "displayName": "Traders",
    "image": "https://images.unsplash.com/photo-1488459716781-31db52582fe9?w=600&q=80",
    "description": "Specialised commodity and livestock traders",
    "subSectors": [
        {"name": "Maize Traders", "image": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=600&q=80"},
        {"name": "Silage Traders", "image": "https://images.unsplash.com/photo-1605000797499-95a51c5269ae?w=600&q=80"},
        {"name": "Sheep Traders", "image": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=600&q=80"},
        {"name": "Cow Traders", "image": "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=600&q=80"},
        {"name": "Dog Traders", "image": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=600&q=80"},
        {"name": "Coffee Traders", "image": "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=600&q=80"}
    ]
  },
  {
    "name": "electronic-appliances",
    "displayName": "Electronic Appliances",
    "image": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=600&q=80",
    "description": "Home and consumer electronic appliances",
    "subSectors": [
        {"name": "Home Appliances", "image": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=600&q=80"},
        {"name": "Audio & Video", "image": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=600&q=80"},
        {"name": "Kitchen Appliances", "image": "https://images.unsplash.com/photo-1556910103-1c02745a30bf?w=600&q=80"},
        {"name": "Cooling & Heating", "image": "https://images.unsplash.com/photo-1527613426441-4da17471b66d?w=600&q=80"}
    ]
  },
  {
    "name": "furnitures",
    "displayName": "Furnitures",
    "image": "https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=600&q=80",
    "description": "Home and office furniture",
    "subSectors": [
        {"name": "Sofas", "image": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&q=80"},
        {"name": "Beds", "image": "https://images.unsplash.com/photo-1505693416388-b034680950bf?w=600&q=80"},
        {"name": "Dining", "image": "https://images.unsplash.com/photo-1617806118233-18e1de247200?w=600&q=80"},
        {"name": "Office Furniture", "image": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=600&q=80"},
        {"name": "Outdoor Furniture", "image": "https://images.unsplash.com/photo-1595515106969-1ce29566ff1c?w=600&q=80"}
    ]
  },
  {
    "name": "event-management",
    "displayName": "Event Management",
    "image": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=600&q=80",
    "description": "Event services including catering and decoration",
    "subSectors": [
        {"name": "Catering", "image": "https://images.unsplash.com/photo-1555244162-803834f70033?w=600&q=80"},
        {"name": "Flower Decoration", "image": "https://images.unsplash.com/photo-1519225421980-715cb0202128?w=600&q=80"}
    ]
  },
  {
    "name": "others",
    "displayName": "Others",
    "image": "https://images.unsplash.com/photo-1513885535751-8b9238bd345a?w=600&q=80",
    "description": "Miscellaneous products and services",
    "subSectors": [
        {"name": "Books & Stationery", "image": "https://images.unsplash.com/photo-1524578271613-d550eacf6090?w=600&q=80"},
        {"name": "Sports & Fitness", "image": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&q=80"},
        {"name": "Pet Supplies", "image": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=600&q=80"},
        {"name": "Home & Garden", "image": "https://images.unsplash.com/photo-1416879115533-19602a04accd?w=600&q=80"},
        {"name": "Gifts & Novelties", "image": "https://images.unsplash.com/photo-1513885535751-8b9238bd345a?w=600&q=80"},
        {"name": "Miscellaneous", "image": "https://images.unsplash.com/photo-1513885535751-8b9238bd345a?w=600&q=80"}
    ]
  }
]

# Ensure directories exist
os.makedirs("static/css", exist_ok=True)
os.makedirs("templates", exist_ok=True)
os.makedirs("static/images", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    # Automatically generate icons if they don't exist
    if not os.path.exists("static/icon-512.png") or not os.path.exists("static/icon-192.png"):
        print("⚠️ Icons missing. Generating them now...")
        try:
            create_icon()
        except Exception as e:
            print(f"❌ Error generating icons: {e}")

@app.api_route("/favicon.ico", methods=["GET", "HEAD"], include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.svg")

@app.api_route("/manifest.json", methods=["GET", "HEAD"], include_in_schema=False)
async def manifest():
    return FileResponse("static/manifest.json", media_type="application/manifest+json")

@app.api_route("/sw.js", methods=["GET", "HEAD"], include_in_schema=False)
async def service_worker():
    return FileResponse("static/sw.js", media_type="application/javascript")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)

async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("userId")
        if user_id is None:
            return None
        user = await user_collection.find_one({"_id": ObjectId(user_id)})
        return user
    except JWTError:
        return None

@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def home(
    request: Request, 
    category: Optional[str] = None, 
    sub_category: Optional[str] = None, 
    search: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    taluk: Optional[str] = None,
    user: dict = Depends(get_current_user)
):
    query = {"isActive": True}
    if category:
        query["category"] = category
    if sub_category:
        query["sub_category"] = sub_category
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    if state and state != "All States":
        query["state"] = state
    if district and district != "All Districts":
        query["district"] = district
    if taluk and taluk != "All Taluks":
        query["taluk"] = taluk
        
    products = await product_collection.find(query).to_list(length=100)
    
    # Fetch seller details for products to get shop addresses
    seller_ids = set()
    for p in products:
        p["_id"] = str(p["_id"])
        if "seller" in p:
            try:
                seller_ids.add(ObjectId(p["seller"]))
            except:
                continue
    
    seller_map = {}
    if seller_ids:
        sellers = await user_collection.find({"_id": {"$in": list(seller_ids)}}).to_list(length=len(seller_ids))
        seller_map = {str(s["_id"]): s for s in sellers}

    for p in products:
        address_parts = []
        if "seller" in p and p["seller"] in seller_map:
            seller = seller_map[p["seller"]]
            p["shop_name"] = seller.get("shop_name")
            p["shop_image"] = seller.get("shop_image")
            p["pincode"] = seller.get("pincode")
            p["is_open"] = seller.get("is_open", True)
            
            if seller.get("shop_name"): address_parts.append(seller["shop_name"])
            if seller.get("shop_address"): address_parts.append(seller["shop_address"])
            
            if seller.get("latitude") and seller.get("longitude"):
                p["map_link"] = f"https://www.google.com/maps/dir/?api=1&destination={seller['latitude']},{seller['longitude']}"

        # Add product location context
        if p.get("taluk"): address_parts.append(p["taluk"])
        if p.get("district"): address_parts.append(p["district"])
        if p.get("state"): address_parts.append(p["state"])
        
        full_address = ", ".join([part for part in address_parts if part])
        p["encoded_address"] = urllib.parse.quote(full_address)

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "products": products, 
        "user": user, 
        "sectors": sectors_data,
        "selected_category": category,
        "selected_sub_category": sub_category,
        "search_query": search,
        "selected_state": state,
        "selected_district": district,
        "selected_taluk": taluk
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = await user_collection.find_one({"email": email})
    if not user or not verify_password(password, user["hashed_password"]):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    
    access_token = create_access_token(data={"userId": str(user["_id"])})
    redirect_url = "/seller/dashboard" if user.get("role") == "seller" else "/"
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/register/buyer", response_class=HTMLResponse)
async def register_buyer_page(request: Request):
    return templates.TemplateResponse("register_buyer.html", {"request": request})

@app.get("/register/seller", response_class=HTMLResponse)
async def register_seller_page(request: Request):
    return templates.TemplateResponse("register_seller.html", {"request": request})

@app.post("/register")
async def register(
    request: Request, 
    name: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...), 
    role: str = Form("user"),
    shop_name: Optional[str] = Form(None),
    shop_address: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    district: Optional[str] = Form(None),
    taluk: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    pincode: Optional[str] = Form(None),
    latitude: Optional[str] = Form(None),
    longitude: Optional[str] = Form(None),
    shop_image: Optional[UploadFile] = File(None)
):
    error_template = "register_seller.html" if role == "seller" else "register_buyer.html"
    
    existing_user = await user_collection.find_one({"email": email})
    if existing_user:
        return templates.TemplateResponse(error_template, {"request": request, "error": "Email already registered"})
    
    hashed_password = get_password_hash(password)
    new_user = {"name": name, "email": email, "hashed_password": hashed_password, "role": role}
    
    if role == "seller":
        if not all([shop_name, shop_address, state, district, taluk, phone, pincode]):
             return templates.TemplateResponse(error_template, {"request": request, "error": "All business details are required for sellers"})
        
        shop_image_url = None
        if shop_image and shop_image.filename:
            file_location = f"static/images/{ObjectId()}_{shop_image.filename}"
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(shop_image.file, buffer)
            shop_image_url = f"/{file_location}"

        new_user.update({
            "shop_name": shop_name,
            "shop_address": shop_address,
            "state": state,
            "district": district,
            "taluk": taluk,
            "phone": phone,
            "pincode": pincode,
            "latitude": latitude,
            "longitude": longitude,
            "shop_image": shop_image_url
        })
        
    await user_collection.insert_one(new_user)
    
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@app.get("/seller/dashboard", response_class=HTMLResponse)
async def seller_dashboard(request: Request, user: dict = Depends(get_current_user)):
    if not user or user.get("role") != "seller":
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    
    products = await product_collection.find({"seller": str(user["_id"])}).to_list(length=100)
    for p in products:
        p["_id"] = str(p["_id"])
        
    return templates.TemplateResponse("seller_dashboard.html", {
        "request": request, 
        "user": user, 
        "products": products
    })

@app.post("/seller/toggle-status")
async def toggle_status(request: Request, user: dict = Depends(get_current_user)):
    if not user or user.get("role") != "seller":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    current_status = user.get("is_open", True)
    new_status = not current_status
    
    await user_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"is_open": new_status}}
    )
    
    return {"status": "success", "is_open": new_status}

@app.get("/seller/export-csv")
async def export_seller_csv(user: dict = Depends(get_current_user)):
    if not user or user.get("role") != "seller":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    products = await product_collection.find({"seller": str(user["_id"])}).to_list(length=1000)
    
    output = io.StringIO()
    fieldnames = ["name", "category", "sub_category", "price", "description", "state", "district", "taluk"]
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for p in products:
        writer.writerow(p)
    
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()), 
        media_type="text/csv", 
        headers={"Content-Disposition": "attachment; filename=my_products.csv"}
    )

@app.post("/delete-product/{product_id}")
async def delete_product(product_id: str, request: Request, user: dict = Depends(get_current_user)):
    if not user or user.get("role") == "seller":
        await product_collection.delete_one({"_id": ObjectId(product_id), "seller": str(user["_id"])})
    return RedirectResponse(url="/seller/dashboard", status_code=status.HTTP_302_FOUND)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response

@app.get("/add-product", response_class=HTMLResponse)
async def add_product_page(request: Request, user: dict = Depends(get_current_user)):
    if not user or user.get("role") != "seller":
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("add_product.html", {"request": request, "user": user, "sectors": sectors_data})

@app.post("/add-product")
async def add_product(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    sub_category: str = Form(...),
    image: UploadFile = File(...),
    user: dict = Depends(get_current_user)
):
    if not user or user.get("role") != "seller":
        raise HTTPException(status_code=403, detail="Not authorized")

    # Save image
    file_location = f"static/images/{ObjectId()}_{image.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    image_url = f"/{file_location}"
    
    new_product = {
        "name": name,
        "description": description,
        "price": price,
        "category": category,
        "sub_category": sub_category,
        "state": user.get("state"),
        "district": user.get("district"),
        "taluk": user.get("taluk"),
        "images": [image_url],
        "seller": str(user["_id"]),
        "isActive": True
    }
    
    await product_collection.insert_one(new_product)
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

if __name__ == "__main__":
    import uvicorn
    import socket
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1"

    port = int(os.getenv("PORT", 5000))
    print("\n" + "="*50)
    print("LOCAL SHOP IS READY!")
    print(f"Access on this computer: http://localhost:{port}")
    print(f"Access on phone (same WiFi): http://{local_ip}:{port}")
    print("="*50 + "\n")

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)