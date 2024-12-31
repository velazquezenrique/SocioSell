

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
from image_data import (
    PRODUCT_DATABASE,
    LISTINGS_DATABASE,
    COMPARABLE_DATABASE,
    SAMPLE_RESPONSES
)
from video_data import (
    VIDEO_DATABASE,
    VIDEO_LISTINGS_DATABASE,
    COMPARABLE_VIDEOS_DATABASE,
    VIDEO_ANALYTICS_DATABASE
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Social Media Product Listing Generator",
    description="""
    Product listing generator supporting both images and videos.
    
    Sample testing guide:
    
    1. Image Upload (/upload/):
       Categories:
       - Electronics: "Sony WH-1000XM4 Headphones"
       - Fashion: "Nike Air Max 270"
       - Home Decor: "Scandinavian Floor Lamp"
       
    2. Video Upload (/upload/video/):
       Categories:
       - Electronics: "iPhone 15 Review", "MacBook Pro Review"
       - Fashion: "Nike Collection", "Adidas Shoes"
       - Beauty: "Makeup Tutorial", "Skincare Routine"
    """
)

# MongoDB setup
MONGODB_URL = "add your mongodb url"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.social_media_products

# Static files and templates setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Image Processing Endpoints
@app.post("/upload/image", 
    summary="Upload Product Image",
    description="Upload and analyze a product image for listing generation."
)
async def upload_image(
    file: UploadFile = File(...),
    title: str = Form(...),
    caption: Optional[str] = Form(None)
):
    try:
        for key, response in SAMPLE_RESPONSES.items():
            if key in title.lower():
                return {
                    "status": "success",
                    "listing": response
                }

        return {
            "status": "success",
            "listing": {
                "product_id": "generic_123",
                "title": title,
                "category": "General",
                "description": caption or "Product description",
                "price": "$99.99",
                "features": ["Feature 1", "Feature 2", "Feature 3"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Add these image endpoints after your existing image upload endpoint

@app.get("/search/{title}", 
    summary="Search Products",
    description="Search for products by title across different categories."
)
async def search_products(title: str):
    results = []
    search_term = title.lower()
    
    for category in PRODUCT_DATABASE.values():
        for product in category:
            if search_term in product["title"].lower():
                results.append(product)
    
    return {
        "status": "success",
        "products": results
    }

@app.get("/listings/{product_id}", 
    summary="Get Product Listings",
    description="Get all listings for a specific product."
)
async def get_product_listings(product_id: str):
    if product_id in LISTINGS_DATABASE:
        return {
            "status": "success",
            "listings": [LISTINGS_DATABASE[product_id]]
        }
    
    # Generate default listing if not found
    return {
        "status": "success",
        "listings": [{
            "id": f"list_{abs(hash(product_id))}",
            "title": "Generic Product",
            "price": "$99.99",
            "description": "Standard product description",
            "features": [
                "Standard feature 1",
                "Standard feature 2",
                "Standard feature 3"
            ],
            "availability": "In Stock",
            "rating": 4.5,
            "seller_info": {
                "name": "General Store",
                "rating": 4.8,
                "reviews": 150
            },
            "shipping": {
                "free_shipping": True,
                "estimated_days": "3-5 business days"
            }
        }]
    }

@app.get("/compare/{product_id}", 
    summary="Get Comparable Products",
    description="Get comparable products for comparison."
)
async def get_comparable_products(product_id: str, limit: int = 3):
    if product_id in COMPARABLE_DATABASE:
        return {
            "status": "success",
            "comparable_products": COMPARABLE_DATABASE[product_id][:limit]
        }
    
    # Generate default comparisons if not found
    return {
        "status": "success",
        "comparable_products": [
            {
                "id": f"comp_1_{abs(hash(product_id))}",
                "name": "Similar Product",
                "price_range": "$89 - $199",
                "features": [
                    "Comparable feature 1",
                    "Similar quality",
                    "Alternative design"
                ]
            },
            {
                "id": f"comp_2_{abs(hash(product_id))}",
                "name": "Alternative Option",
                "price_range": "$79 - $189",
                "features": [
                    "Alternative feature",
                    "Different approach",
                    "Unique benefit"
                ]
            }
        ]
    }

@app.get("/product/details/{product_id}",
    summary="Get Product Details",
    description="Get detailed information about a specific product."
)
async def get_product_details(product_id: str):
    # Search through product database
    for category, products in PRODUCT_DATABASE.items():
        for product in products:
            if product["id"] == product_id:
                # Enrich with listings data if available
                listing_data = LISTINGS_DATABASE.get(product_id, {})
                return {
                    "status": "success",
                    "product": {
                        **product,
                        "description": listing_data.get("description", "Product description not available"),
                        "features": listing_data.get("features", ["Feature 1", "Feature 2", "Feature 3"]),
                        "specifications": {
                            "dimensions": "Standard size",
                            "weight": "Standard weight",
                            "material": "Standard material",
                            "warranty": "1 year limited warranty"
                        },
                        "availability": {
                            "status": "In Stock",
                            "quantity": 100,
                            "shipping_time": "3-5 business days"
                        },
                        "ratings": {
                            "average": 4.5,
                            "total_reviews": 150,
                            "breakdown": {
                                "5_star": "60%",
                                "4_star": "25%",
                                "3_star": "10%",
                                "2_star": "3%",
                                "1_star": "2%"
                            }
                        }
                    }
                }
    
    # Return default response if product not found
    return {
        "status": "success",
        "product": {
            "id": product_id,
            "title": "Generic Product",
            "category": "General",
            "price_range": "$99 - $199",
            "description": "Standard product description",
            "features": ["Feature 1", "Feature 2", "Feature 3"],
            "specifications": {
                "dimensions": "Standard size",
                "weight": "Standard weight",
                "material": "Standard material",
                "warranty": "1 year limited warranty"
            }
        }
    }

@app.get("/product/analytics/{product_id}",
    summary="Get Product Analytics",
    description="Get detailed analytics for a specific product."
)
async def get_product_analytics(product_id: str):
    return {
        "status": "success",
        "analytics": {
            "sales_performance": {
                "total_sales": "1.2K",
                "revenue": "$45,000",
                "average_price": "$99.99",
                "growth_rate": "15%"
            },
            "customer_behavior": {
                "view_to_purchase_rate": "8.5%",
                "cart_abandonment_rate": "25%",
                "repeat_purchase_rate": "35%",
                "average_rating": 4.5
            },
            "demographics": {
                "age_groups": {
                    "18-24": "20%",
                    "25-34": "35%",
                    "35-44": "25%",
                    "45+": "20%"
                },
                "top_locations": ["US", "UK", "Canada", "Australia"]
            },
            "marketing_metrics": {
                "click_through_rate": "3.2%",
                "conversion_rate": "2.8%",
                "return_on_ad_spend": "2.5x",
                "social_media_engagement": "High"
            }
        }
    }

@app.get("/product/recommendations/{product_id}",
    summary="Get Product Recommendations",
    description="Get personalized product recommendations based on a product."
)
async def get_product_recommendations(product_id: str, limit: int = 5):
    return {
        "status": "success",
        "recommendations": {
            "similar_products": [
                {
                    "id": f"rec_1_{product_id}",
                    "title": "Similar Product 1",
                    "price": "$89.99",
                    "rating": 4.6,
                    "match_score": "95%"
                },
                {
                    "id": f"rec_2_{product_id}",
                    "title": "Alternative Option",
                    "price": "$79.99",
                    "rating": 4.4,
                    "match_score": "90%"
                }
            ],
            "frequently_bought_together": [
                {
                    "id": f"bundle_1_{product_id}",
                    "title": "Complementary Product 1",
                    "price": "$29.99",
                    "bundle_discount": "10%"
                },
                {
                    "id": f"bundle_2_{product_id}",
                    "title": "Complementary Product 2",
                    "price": "$19.99",
                    "bundle_discount": "15%"
                }
            ],
            "trending_in_category": [
                {
                    "id": f"trend_1_{product_id}",
                    "title": "Trending Product 1",
                    "price": "$99.99",
                    "trend_score": "High"
                },
                {
                    "id": f"trend_2_{product_id}",
                    "title": "Trending Product 2",
                    "price": "$89.99",
                    "trend_score": "Medium"
                }
            ]
        }
    }

@app.get("/categories",
    summary="Get All Categories",
    description="Get list of all available categories for both products and videos."
)
async def get_categories():
    product_categories = set(PRODUCT_DATABASE.keys())
    video_categories = set(VIDEO_DATABASE.keys())
    
    return {
        "status": "success",
        "categories": {
            "products": list(product_categories),
            "videos": list(video_categories)
        }
    }

@app.get("/product/reviews/{product_id}",
    summary="Get Product Reviews",
    description="Get customer reviews for a specific product."
)
async def get_product_reviews(product_id: str, limit: int = 5):
    return {
        "status": "success",
        "reviews": {
            "average_rating": 4.5,
            "total_reviews": 150,
            "rating_distribution": {
                "5_star": "60%",
                "4_star": "25%",
                "3_star": "10%",
                "2_star": "3%",
                "1_star": "2%"
            },
            "recent_reviews": [
                {
                    "id": f"review_1_{product_id}",
                    "rating": 5,
                    "title": "Great product!",
                    "comment": "Exceeded my expectations. Would definitely recommend.",
                    "date": "2024-02-15",
                    "verified_purchase": True
                },
                {
                    "id": f"review_2_{product_id}",
                    "rating": 4,
                    "title": "Good value",
                    "comment": "Good quality for the price. Minor improvements could be made.",
                    "date": "2024-02-10",
                    "verified_purchase": True
                }
            ]
        }
    }

# Video Processing Endpoints
@app.post("/upload/video/", 
    summary="Upload Product Video",
    description="Upload and analyze a product video for listing generation."
)
async def upload_video(
    file: Optional[UploadFile] = File(None),  # Made file optional
    title: str = Form(...),
    description: Optional[str] = Form(None)
):
    try:
        # Common keywords for each category
        category_keywords = {
            "electronics": ["iphone", "macbook", "samsung", "laptop", "phone", "computer", "tech"],
            "fashion": ["nike", "adidas", "shoes", "clothing", "fashion", "wear", "style"],
            "beauty": ["makeup", "cosmetics", "skincare", "beauty", "tutorial"],
            "sports": ["fitness", "workout", "sports", "exercise", "training"]
        }

        # Determine category based on title
        video_category = "general"
        for category, keywords in category_keywords.items():
            if any(keyword in title.lower() for keyword in keywords):
                video_category = category
                break

        # Match with existing video data first
        for category, videos in VIDEO_DATABASE.items():
            for video_id, video_data in videos.items():
                if any(keyword.lower() in title.lower() for keyword in video_data["title"].split()):
                    return {
                        "status": "success",
                        "message": "Video processed successfully",
                        "product_info": {
                            "id": video_id,
                            **video_data
                        }
                    }

        # Generate unique video ID
        unique_id = f"video_{abs(hash(title))}"[:15]

        # Generate response based on category
        video_info = {
            "electronics": {
                "highlights": [
                    "Technical specifications",
                    "Performance benchmarks",
                    "Feature demonstration",
                    "Comparison with competitors"
                ],
                "key_features": [
                    "Technical performance",
                    "Build quality",
                    "User experience",
                    "Value for money"
                ]
            },
            "fashion": {
                "highlights": [
                    "Style overview",
                    "Material quality",
                    "Fit and sizing",
                    "Styling suggestions"
                ],
                "key_features": [
                    "Design elements",
                    "Material composition",
                    "Comfort factors",
                    "Versatility"
                ]
            },
            "beauty": {
                "highlights": [
                    "Product application",
                    "Results demonstration",
                    "Tips and tricks",
                    "Product comparison"
                ],
                "key_features": [
                    "Product effectiveness",
                    "Application method",
                    "Long-term benefits",
                    "Value proposition"
                ]
            },
            "sports": {
                "highlights": [
                    "Equipment review",
                    "Performance test",
                    "Durability check",
                    "Usage guidelines"
                ],
                "key_features": [
                    "Performance metrics",
                    "Durability factors",
                    "Comfort level",
                    "Professional features"
                ]
            }
        }

        # Get category-specific info or use general info
        category_info = video_info.get(video_category, {
            "highlights": [
                "Product overview",
                "Feature demonstration",
                "Performance review",
                "Final thoughts"
            ],
            "key_features": [
                "Main feature 1",
                "Main feature 2",
                "Main feature 3",
                "Main feature 4"
            ]
        })

        # Generate a comprehensive response
        return {
            "status": "success",
            "message": "Video analyzed successfully",
            "product_info": {
                "id": unique_id,
                "title": title,
                "category": video_category,
                "duration": "10:25",
                "highlights": category_info["highlights"],
                "transcript_summary": description or f"Detailed analysis of {title}",
                "key_features": category_info["key_features"],
                "price_range": "$99 - $999",
                "analytics": {
                    "views": "15K",
                    "likes": "1.2K",
                    "engagement_rate": "8.5%"
                },
                "platforms": [
                    {"name": "YouTube", "views": "10K", "rating": 4.8},
                    {"name": "TikTok", "views": "5K", "rating": 4.7}
                ],
                "recommendations": [
                    "Similar product 1",
                    "Alternative option 2",
                    "Related item 3"
                ]
            }
        }

    except Exception as e:
        logger.error(f"Error processing video request: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }
@app.get("/video/search/{title}",
    summary="Search Videos",
    description="Search for product videos by title."
)
async def search_videos(title: str):
    results = []
    search_term = title.lower()
    
    for category, videos in VIDEO_DATABASE.items():
        for video_id, video_data in videos.items():
            if search_term in video_data["title"].lower():
                results.append({
                    "id": video_id,
                    **video_data
                })
    
    return {
        "status": "success",
        "videos": results
    }

@app.get("/video/listings/{video_id}",
    summary="Get Video Listings",
    description="Get all listings and platforms for a specific video."
)
async def get_video_listings(video_id: str):
    if video_id in VIDEO_LISTINGS_DATABASE:
        return {
            "status": "success",
            "listings": VIDEO_LISTINGS_DATABASE[video_id]
        }
    
    # Generate default listing if not found
    return {
        "status": "success",
        "listings": [{
            "id": f"vlist_{abs(hash(video_id))}",
            "platform": "YouTube",
            "title": "Product Review",
            "views": "10K",
            "rating": 4.5,
            "key_timestamps": {
                "intro": "0:00",
                "features": "2:00",
                "demo": "5:00",
                "conclusion": "8:00"
            },
            "product_links": [
                {"store": "Online Store", "price": "$99.99"},
                {"store": "Marketplace", "price": "$89.99"}
            ]
        }]
    }

@app.get("/video/compare/{video_id}",
    summary="Get Comparable Videos",
    description="Get comparable videos for comparison."
)
async def get_comparable_videos(video_id: str, limit: int = 3):
    if video_id in COMPARABLE_VIDEOS_DATABASE:
        return {
            "status": "success",
            "comparable_videos": COMPARABLE_VIDEOS_DATABASE[video_id][:limit]
        }
    
    # Generate default comparisons if not found
    return {
        "status": "success",
        "comparable_videos": [
            {
                "id": f"comp_1_{abs(hash(video_id))}",
                "title": "Similar Product Review 1",
                "duration": "9:30",
                "views": "15K",
                "comparison_points": [
                    "Feature comparison",
                    "Price value",
                    "Performance",
                    "Quality"
                ],
                "price_range": "$89 - $199"
            },
            {
                "id": f"comp_2_{abs(hash(video_id))}",
                "title": "Alternative Product Review",
                "duration": "8:45",
                "views": "12K",
                "comparison_points": [
                    "Alternative features",
                    "Cost comparison",
                    "User experience",
                    "Durability"
                ],
                "price_range": "$79 - $189"
            }
        ]
    }

@app.get("/video/analytics/{video_id}",
    summary="Get Video Analytics",
    description="Get detailed analytics for a specific video."
)
async def get_video_analytics(video_id: str):
    if video_id in VIDEO_ANALYTICS_DATABASE:
        return {
            "status": "success",
            "analytics": VIDEO_ANALYTICS_DATABASE[video_id]
        }
    
    # Generate default analytics if not found
    return {
        "status": "success",
        "analytics": {
            "engagement": {
                "views": "5K",
                "likes": "500",
                "comments": "50",
                "average_watch_time": "5:30"
            },
            "audience": {
                "demographics": {
                    "18-24": "25%",
                    "25-34": "40%",
                    "35-44": "20%",
                    "45+": "15%"
                },
                "top_regions": ["US", "UK", "Canada", "Australia"]
            },
            "performance": {
                "retention_rate": "65%",
                "click_through_rate": "3.5%",
                "conversion_rate": "2.1%"
            }
        }
    }

# Combined Search
@app.get("/search/all/{query}",
    summary="Search All Content",
    description="Search both products and videos across all categories."
)
async def search_all_content(query: str):
    # Search products
    product_results = []
    search_term = query.lower()
    
    for category in PRODUCT_DATABASE.values():
        for product in category:
            if search_term in product["title"].lower():
                product_results.append(product)
    
    # Search videos
    video_results = []
    for category, videos in VIDEO_DATABASE.items():
        for video_id, video_data in videos.items():
            if search_term in video_data["title"].lower():
                video_results.append({
                    "id": video_id,
                    **video_data
                })
    
    return {
        "status": "success",
        "results": {
            "products": product_results,
            "videos": video_results
        }
    }

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.2", port=8002, reload=True)
