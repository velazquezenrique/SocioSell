from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List
from pydantic import BaseModel
import logging
from pathlib import Path
import aiofiles
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse




app = FastAPI(
    title="Social Media Product Listing Generator",
    description="""
    Sample testing guide:
    
    1. Upload endpoint (/upload/):
       Examples for different categories:
       - Electronics: "Sony WH-1000XM4 Headphones"
       - Fashion: "Nike Air Max 270"
       - Home Decor: "Scandinavian Floor Lamp"
       - Beauty: "MAC Ruby Woo Lipstick"
       - Sports: "Wilson Evolution Basketball"
    
    2. Search endpoint (/search/{title}):
       Try searching these categories:
       - Electronics: sony, samsung, apple
       - Fashion: nike, adidas, zara
       - Home Decor: lamp, rug, mirror
       - Beauty: mac, loreal, maybelline
       - Sports: wilson, nike, adidas
    """
)

# MongoDB setup
MONGODB_URL = "mongodb+srv://varshadewangan1605:Varsha1605@cluster0.d5ant.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.social_media_products


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Add a route for the dashboard
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload/", 
    summary="Upload Product Image",
    description="Upload a product image with title and caption."
)
async def upload_file(
    file: UploadFile = File(..., description="Product image file"),
    title: str = Form(..., description="Product title"),
    caption: Optional[str] = Form(None, description="Social media caption (optional)")
):
    try:
        # Sample responses based on product category
        sample_responses = {
            "headphones": {
                "product_id": "audio_123",
                "title": "Sony WH-1000XM4",
                "category": "Electronics",
                "description": "Premium noise-cancelling headphones",
                "price": "$349",
                "features": ["Active Noise Cancellation", "30-hour Battery Life", "Touch Controls"]
            },
            "shoes": {
                "product_id": "shoe_123",
                "title": "Nike Air Max 270",
                "category": "Fashion",
                "description": "Modern lifestyle sneakers",
                "price": "$150",
                "features": ["Air Unit Cushioning", "Breathable Mesh", "Comfortable Fit"]
            },
            "lamp": {
                "product_id": "decor_123",
                "title": "Scandinavian Floor Lamp",
                "category": "Home Decor",
                "description": "Modern minimalist lighting",
                "price": "$199",
                "features": ["Adjustable Height", "Energy Efficient", "Natural Wood Base"]
            },
            "lipstick": {
                "product_id": "beauty_123",
                "title": "MAC Ruby Woo",
                "category": "Beauty",
                "description": "Classic matte red lipstick",
                "price": "$19",
                "features": ["Long-lasting", "Matte Finish", "Highly Pigmented"]
            },
            "basketball": {
                "product_id": "sports_123",
                "title": "Wilson Evolution",
                "category": "Sports",
                "description": "Official game basketball",
                "price": "$59.99",
                "features": ["Moisture-Wicking", "Superior Grip", "Indoor Use"]
            }
        }

        # Return a mock response based on the title
        for key, response in sample_responses.items():
            if key in title.lower():
                return {
                    "status": "success",
                    "listing": response
                }

        # Default response if no specific match
        return {
            "status": "success",
            "listing": {
                "product_id": "generic_123",
                "title": title,
                "category": "General",
                "description": "Product description",
                "price": "$99.99",
                "features": ["Feature 1", "Feature 2", "Feature 3"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/{title}", 
    summary="Search Products",
    description="Search for products by title across different categories."
)
async def search_products(title: str):
    # Expanded mock product database
    product_database = {
        "electronics": [
            {"id": "elec_123", "title": "Sony WH-1000XM4", "category": "Headphones", "price_range": "$299 - $349"},
            {"id": "elec_124", "title": "Samsung Galaxy Watch 6", "category": "Smartwatch", "price_range": "$299 - $449"},
            {"id": "elec_125", "title": "Apple iPad Air", "category": "Tablets", "price_range": "$599 - $749"}
        ],
        "fashion": [
            {"id": "fash_123", "title": "Nike Air Max 270", "category": "Sneakers", "price_range": "$150 - $170"},
            {"id": "fash_124", "title": "Zara Oversized Blazer", "category": "Clothing", "price_range": "$89 - $129"},
            {"id": "fash_125", "title": "Adidas Ultraboost", "category": "Running Shoes", "price_range": "$180 - $200"}
        ],
        "home_decor": [
            {"id": "decor_123", "title": "Scandinavian Floor Lamp", "category": "Lighting", "price_range": "$199 - $249"},
            {"id": "decor_124", "title": "Persian Area Rug 5x8", "category": "Rugs", "price_range": "$299 - $499"},
            {"id": "decor_125", "title": "Modern Wall Mirror", "category": "Mirrors", "price_range": "$149 - $199"}
        ],
        "beauty": [
            {"id": "beauty_123", "title": "MAC Ruby Woo Lipstick", "category": "Makeup", "price_range": "$19 - $22"},
            {"id": "beauty_124", "title": "L'Oreal Telescopic Mascara", "category": "Makeup", "price_range": "$11 - $13"},
            {"id": "beauty_125", "title": "Maybelline Fit Me Foundation", "category": "Makeup", "price_range": "$8 - $10"}
        ],
        "sports": [
            {"id": "sports_123", "title": "Wilson Evolution Basketball", "category": "Basketball", "price_range": "$59 - $69"},
            {"id": "sports_124", "title": "Nike Mercurial Soccer Cleats", "category": "Soccer", "price_range": "$89 - $129"},
            {"id": "sports_125", "title": "Adidas Tennis Racket", "category": "Tennis", "price_range": "$199 - $249"}
        ]
    }

    # Search across all categories
    results = []
    search_term = title.lower()
    for category in product_database.values():
        for product in category:
            if search_term in product["title"].lower():
                results.append(product)

    return {
        "status": "success",
        "products": results
    }

# Update these sections in your main.py:

@app.get("/listings/{product_id}", 
    summary="Get Product Listings",
    description="Get all listings for a specific product."
)
async def get_product_listings(product_id: str):
    # Mock listings database
    listings_database = {
        # Electronics
        "elec_123": {
            "id": "list_123",
            "title": "Sony WH-1000XM4",
            "price": "$349",
            "description": "Industry-leading noise cancelling headphones",
            "features": ["30-hour Battery Life", "Touch Controls", "Speak-to-chat"]
        },
        "elec_124": {
            "id": "list_124",
            "title": "Samsung Galaxy Watch 6",
            "price": "$399",
            "description": "Advanced smartwatch with comprehensive health tracking",
            "features": ["Sleep Tracking", "ECG Monitor", "Durable Design"]
        },
        "elec_125": {
            "id": "list_125",
            "title": "Apple iPad Air",
            "price": "$599",
            "description": "Powerful tablet for creativity and productivity",
            "features": ["M1 Chip", "10.9-inch Display", "Apple Pencil Support"]
        },
        
        # Fashion
        "fash_123": {
            "id": "list_126",
            "title": "Nike Air Max 270",
            "price": "$150",
            "description": "Iconic lifestyle sneakers with visible Air unit",
            "features": ["Air Cushioning", "Mesh Upper", "Rubber Outsole"]
        },
        "fash_124": {
            "id": "list_127",
            "title": "Zara Oversized Blazer",
            "price": "$99",
            "description": "Versatile oversized blazer for any occasion",
            "features": ["Premium Fabric", "Relaxed Fit", "Multiple Pockets"]
        },
        "fash_125": {
            "id": "list_128",
            "title": "Adidas Ultraboost",
            "price": "$180",
            "description": "Premium running shoes with responsive cushioning",
            "features": ["Boost Midsole", "Primeknit Upper", "Continental Rubber"]
        },
        
        # Home Decor
        "decor_123": {
            "id": "list_129",
            "title": "Scandinavian Floor Lamp",
            "price": "$199",
            "description": "Modern minimalist floor lamp with wooden accents",
            "features": ["LED Compatible", "Natural Wood", "Adjustable Height"]
        },
        "decor_124": {
            "id": "list_130",
            "title": "Persian Area Rug 5x8",
            "price": "$399",
            "description": "Traditional Persian rug with intricate patterns",
            "features": ["Hand-Knotted", "Wool Blend", "Fade Resistant"]
        },
        "decor_125": {
            "id": "list_131",
            "title": "Modern Wall Mirror",
            "price": "$179",
            "description": "Contemporary wall mirror with elegant frame",
            "features": ["Beveled Edge", "Easy Mounting", "Anti-Fog Coating"]
        },
        
        # Beauty
        "beauty_123": {
            "id": "list_132",
            "title": "MAC Ruby Woo Lipstick",
            "price": "$19",
            "description": "Iconic matte red lipstick",
            "features": ["Long-lasting", "Matte Finish", "Highly Pigmented"]
        },
        "beauty_124": {
            "id": "list_133",
            "title": "L'Oreal Telescopic Mascara",
            "price": "$11",
            "description": "Lengthening mascara for dramatic lashes",
            "features": ["Precision Brush", "Smudge-proof", "Easy Removal"]
        },
        "beauty_125": {
            "id": "list_134",
            "title": "Maybelline Fit Me Foundation",
            "price": "$8",
            "description": "Lightweight foundation for natural coverage",
            "features": ["Oil-Free", "SPF 18", "Natural Finish"]
        },
        
        # Sports
        "sports_123": {
            "id": "list_135",
            "title": "Wilson Evolution Basketball",
            "price": "$59.99",
            "description": "Premium indoor game basketball",
            "features": ["Composite Leather", "Cushion Core", "Maximum Grip"]
        },
        "sports_124": {
            "id": "list_136",
            "title": "Nike Mercurial Soccer Cleats",
            "price": "$89",
            "description": "Professional soccer cleats for speed",
            "features": ["Lightweight Design", "Studded Sole", "Dynamic Fit"]
        },
        "sports_125": {
            "id": "list_137",
            "title": "Adidas Tennis Racket",
            "price": "$199",
            "description": "Professional grade tennis racket",
            "features": ["Graphite Frame", "Perfect Balance", "Spin Friendly"]
        }
    }

    if product_id in listings_database:
        return {
            "status": "success",
            "listings": [listings_database[product_id]]
        }
    
    return {
        "status": "error",
        "message": "Listing not found"
    }

@app.get("/compare/{product_id}", 
    summary="Get Comparable Products",
    description="Get comparable products for comparison."
)
async def get_comparable_products(product_id: str, limit: int = 5):
    # Mock comparable products database
    comparable_database = {
        # Electronics Comparisons
        "elec_123": [
            {
                "id": "elec_126",
                "name": "Bose QuietComfort 45",
                "price_range": "$279 - $329",
                "features": ["Noise Cancellation", "24-hour Battery", "Bluetooth 5.1"]
            },
            {
                "id": "elec_127",
                "name": "Apple AirPods Max",
                "price_range": "$549 - $599",
                "features": ["Active Noise Cancellation", "Spatial Audio", "20-hour Battery"]
            },
            {
                "id": "elec_128",
                "name": "Sennheiser Momentum 4",
                "price_range": "$349 - $379",
                "features": ["60-hour Battery", "Adaptive Noise Cancellation", "Premium Sound"]
            }
        ],
        
        # Fashion Comparisons
        "fash_123": [
            {
                "id": "fash_126",
                "name": "Adidas NMD R1",
                "price_range": "$140 - $160",
                "features": ["Boost Cushioning", "Knit Upper", "Streetwear Style"]
            },
            {
                "id": "fash_127",
                "name": "Puma RS-X",
                "price_range": "$110 - $130",
                "features": ["Retro Design", "Running System Tech", "Mesh Construction"]
            },
            {
                "id": "fash_128",
                "name": "New Balance 327",
                "price_range": "$100 - $120",
                "features": ["Retro Inspired", "Suede Overlays", "EVA Midsole"]
            }
        ],
        
        # Home Decor Comparisons
        "decor_123": [
            {
                "id": "decor_126",
                "name": "Industrial Tripod Floor Lamp",
                "price_range": "$179 - $229",
                "features": ["Metal Construction", "Adjustable Height", "Vintage Style"]
            },
            {
                "id": "decor_127",
                "name": "Modern Arc Floor Lamp",
                "price_range": "$249 - $299",
                "features": ["Arched Design", "Marble Base", "Dimmable Light"]
            },
            {
                "id": "decor_128",
                "name": "Contemporary LED Floor Lamp",
                "price_range": "$159 - $199",
                "features": ["Touch Control", "Color Temperature Adjustment", "Energy Efficient"]
            }
        ],
        
        # Beauty Comparisons
        "beauty_123": [
            {
                "id": "beauty_126",
                "name": "NARS Red Square",
                "price_range": "$26 - $30",
                "features": ["Velvet Matte", "Long Wear", "Rich Pigment"]
            },
            {
                "id": "beauty_127",
                "name": "Charlotte Tilbury Red Carpet Red",
                "price_range": "$34 - $38",
                "features": ["Creamy Texture", "Moisturizing", "Celebrity Favorite"]
            },
            {
                "id": "beauty_128",
                "name": "Fenty Beauty Stunna Lip Paint",
                "price_range": "$24 - $28",
                "features": ["Liquid Formula", "12-Hour Wear", "Universal Red"]
            }
        ],
        
        # Sports Comparisons
        "sports_123": [
            {
                "id": "sports_126",
                "name": "Spalding NBA Official Game Ball",
                "price_range": "$49 - $59",
                "features": ["Full Grain Leather", "Official Size", "Indoor/Outdoor"]
            },
            {
                "id": "sports_127",
                "name": "Molten X-Series Basketball",
                "price_range": "$39 - $49",
                "features": ["FIBA Approved", "Premium Grip", "Consistent Bounce"]
            },
            {
                "id": "sports_128",
                "name": "Nike Elite Competition Ball",
                "price_range": "$59 - $69",
                "features": ["Nike Grip Technology", "Deep Channel Design", "Indoor Only"]
            }
        ]
    }

    if product_id in comparable_database:
        return {
            "status": "success",
            "comparable_products": comparable_database[product_id][:limit]
        }
    
    return {
        "status": "error",
        "message": "No comparable products found"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
