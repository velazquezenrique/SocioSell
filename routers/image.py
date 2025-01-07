from fastapi import APIRouter
from fastapi import File, UploadFile, Form
from typing import List, Optional
import logging
from schemas.image import (
    upload_image,
    search_products,
    get_product_listings,
    get_comparable_products,
    get_product_details,
    get_product_analytics,
    get_product_recommendations,
    get_categories,
    get_product_reviews
)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", 
    summary="Upload Product Image",
    description="Upload and analyze a product image for listing generation."
)
async def upload_image_route(
    files: List[UploadFile] = File(...),
    title: str = Form(...),
    caption: Optional[str] = Form(None)
):
    return await upload_image(files, title, caption)

@router.get("/search/{title}",
    summary="Search Products",
    description="Search for products by title across different categories."
)
async def search_products_route(title: str):
    return await search_products(title)

@router.get("/listings/{product_id}",
    summary="Get Product Listings",
    description="Get all listings for a specific product."
)
async def get_product_listings_route(product_id: str):
    return await get_product_listings(product_id)

@router.get("/compare/{product_id}",
    summary="Get Comparable Products",
    description="Get comparable products for comparison."
)
async def get_comparable_products_route(product_id: str, limit: int = 3):
    return await get_comparable_products(product_id, limit)

@router.get("/product/details/{product_id}",
    summary="Get Product Details",
    description="Get detailed information about a specific product."
)
async def get_product_details_route(product_id: str):
    return await get_product_details(product_id)

@router.get("/product/analytics/{product_id}",
    summary="Get Product Analytics",
    description="Get detailed analytics for a specific product"
)
async def get_product_analytics_route(product_id: str):
    return await get_product_analytics(product_id)
    
@router.get("/product/recommendations/{product_id}",
    summary="Get Product Recommendations",
    description="Get personalized product recommendations based on a product."
)
async def get_product_recommendations_route(product_id: str, limit: int = 5):
    return  await get_product_recommendations(product_id, limit)

@router.get("/categories",
    summary="Get All Categories",
    description="Get list of all available categories for both products and videos."
)
async def get_categories_route():
    return await get_categories()
    
@router.get("/product/reviews/{product_id}",
    summary="Get Product Reviews",
    description="Get customer reviews for a specific product.",
)
async def get_product_reviews_route(product_id: str, limit: int = 5):
    return await get_product_reviews(product_id, limit)
