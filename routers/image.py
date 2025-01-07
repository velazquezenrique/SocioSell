from fastapi import APIRouter, HTTPException
from bson import ObjectId
from models.product import Product
from models.listing import ProductListing
from models.review import ReviewsResponse
from models.analytics import Analytics, SalesPerformance, CustomerBehavior, MarketingMetrics, Demographics
from fastapi import File, UploadFile, Form
from image_data import SAMPLE_RESPONSES
from typing import List, Optional
from datetime import datetime
import logging

# from schemas.image import (
#     search_products,
#     get_product_listings,
#     get_comparable_products,
#     get_product_details,
#     get_product_analytics,
#     get_product_recommendations,
#     get_categories,
#     get_product_reviews
# )

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", 
    summary="Upload Product Image",
    description="Upload and analyze a product image for listing generation."
)
async def upload_image(
    files: List[UploadFile] = File(...),  # Accepts multiple files
    title: str = Form(...),
    caption: Optional[str] = Form(None)
):
    try:
        logger.info(f"Received upload request - Files: {len(files)}, Title: {title}")

        if len(files) > 5:
            logger.warning(f"Upload rejected - Too many files: {len(files)}")
            raise HTTPException(
                status_code=400,
                detail="Max 5 images are allowed. Please remove extra files and try again."
            )
        
        processed_files = []
        for file in files:
            processed_files.append(file.filename)
            logger.info(f"Processed file: {file.filename}")

        # Your existing logic for generating listings...
        for key, response in SAMPLE_RESPONSES.items():
            if key in title.lower():
                logger.info(f"Generated listing for title: {title}")
                return {
                    "status": "success",
                    "message": f"Successfully processed {len(files)} image(s)",
                    "processed_files": processed_files,
                    "listing": response
                }

        return {
            "status": "success",
            "message": f"Successfully processed {len(files)} image(s)",
            "processed_files": processed_files,
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

@router.get("/search/{title}",
    summary="Search Products",
    description="Search for products by title across different categories."
)
async def search_products(title: str):
    from main import db
    search_term = title.lower()
    results = []

    try:
        products_cursor = db["products"].find({"title": {"$regex": search_term, "$options": "i"}})

        async for product in products_cursor:
            product["id"] = str(product["_id"])  # Convert _id to id

            try:
                results.append(Product(**product))  # Convert to Pydantic model
            except Exception as e:
                print(f"Error while processing product: {e}")
                continue
        
        if not results:
            # Default response if no products found
            results = [
                {"id": "elec_123", "title": "Sony WH-1000XM4", "category": "Headphones", "price_range": "$299 - $349"}
            ]

        return {"status": "success", "products": results}

    except Exception as e:
        print(f"Error during search: {e}")
        raise HTTPException(status_code=500, detail=f"Error during search: {e}")

@router.get("/listings/{product_id}",
    summary="Get Product Listings",
    description="Get all listings for a specific product."
)
async def get_product_listings(product_id: str):
    from main import db
    listings_cursor = db["listings"].find({"product_id": product_id})
    listings = await listings_cursor.to_list(length=None)

    if listings:
        # Convert ObjectId to string for JSON compatibility
        for listing in listings:
            listing["id"] = str(listing["_id"])  # Convert _id to id 

        return {
            "status": "success",
            "listings": [ProductListing(**listing) for listing in listings]  # Convert to Pydantic model
        }

    # Fallback generic listing
    default_listing = ProductListing(
        id=f"list_{abs(hash(product_id))}",
        product_id=product_id,
        title="Generic Product",
        description="Standard product description",
        price="$99.99",
        features=[
            "Standard feature 1",
            "Standard feature 2",
            "Standard feature 3"
        ]
    )

    return {
        "status": "success",
        "listings": [default_listing.model_dump()]  # Convert Pydantic model to dict
    }

@router.get("/compare/{product_id}",
    summary="Get Comparable Products",
    description="Get comparable products for comparison."
)
async def get_comparable_products(product_id: str, limit: int = 3):
    from main import db
    
    try:
        object_id = ObjectId(product_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product ID format")
    
    # Fetch the product details to compare against
    target_product = await db["products"].find_one({"_id": object_id})
    
    if not target_product:
        raise HTTPException(status_code=404, detail="Product not found.")
    
    # Construct the query for finding similar products
    query = {
        "$or": [
            {"title": {"$regex": target_product["title"], "$options": "i"}},
            {"subcategory": target_product.get("subcategory")},
            {"category": target_product.get("category")},
            {"features": {"$in": target_product.get("features", [])}},
            {"price_range": target_product.get("price_range")},
        ],
        "_id": {"$ne": product_id}  # Exclude the target product itself
    }

    # Fetch comparable products based on the query
    comparable_products_cursor = db["products"].find(query).limit(limit)
    comparable_products = await comparable_products_cursor.to_list(length=None)

    comparable_products = [
        {**cp, "id": str(cp["_id"])}  # Map _id to id
        for cp in comparable_products
    ]

    if comparable_products:
        return {
            "status": "success",
            "comparable_products": [Product(**cp) for cp in comparable_products]
        }

    # If no comparable products found, return default set of comparable products
    return {
        "status": "success",
        "comparable_products": [
            Product(
                id=f"comp_1_{abs(hash(product_id))}",
                title="Similar Product",
                category=target_product.get("category", "Unknown"),
                subcategory=target_product.get("subcategory", "Unknown"),
                price_range="$89 - $199",
                features=[
                    "Comparable feature 1",
                    "Similar quality",
                    "Alternative design"
                ]
            ),
            Product(
                id=f"comp_2_{abs(hash(product_id))}",
                title="Alternative Option",
                category=target_product.get("category", "Unknown"),
                subcategory=target_product.get("subcategory", "Unknown"),
                price_range="$79 - $189",
                features=[
                    "Alternative feature",
                    "Different approach",
                    "Unique benefit"
                ]
            )
        ]
    }

@router.get("/product/details/{product_id}",
    summary="Get Product Details",
    description="Get detailed information about a specific product."
)
async def get_product_details(product_id: str):
    from main import db
    try:
        object_id = ObjectId(product_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    product = await db["products"].find_one({"_id": object_id})
    print(product)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Convert ObjectId to string and map to id
    product["id"] = str(product["_id"])
    product.pop("_id", None)  # Remove the _id field if not needed

    return Product(**product)  # Convert to Pydantic model

@router.get("/product/analytics/{product_id}",
    summary="Get Product Analytics",
    description="Get detailed analytics for a specific product or similar products."
)
async def get_product_analytics(product_id: str):
    from main import db

    try:
        # Validate and convert the product_id to ObjectId
        object_id = ObjectId(product_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    try:
        # Query for analytics using the product ID
        analytics_data = await db["analytics"].find_one({"product_id": str(object_id)})

        if analytics_data:
            # Convert MongoDB document to Pydantic model and return
            analytics_data["id"] = str(analytics_data["_id"])  # Add id field
            analytics_data.pop("_id", None)  # Remove _id field
            analytics = Analytics(**analytics_data)  # Convert to Pydantic model

            return {
                "status": "success",
                "analytics": analytics
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching analytics: {e}")

    # Default response if no analytics are found
    return {
        "status": "success",
        "analytics": Analytics(
            product_id=product_id,
            sales_performance=SalesPerformance(
                total_sales="1.2K",
                revenue="$45,000",
                average_price="$99.99",
                growth_rate="15%"
            ),
            customer_behavior=CustomerBehavior(
                view_to_purchase_rate="8.5%",
                cart_abandonment_rate="25%",
                repeat_purchase_rate="35%",
                average_rating=4.5
            ),
            demographics=Demographics(
                age_groups={"18-24": "20%", "25-34": "35%", "35-44": "25%", "45+": "20%"},
                top_locations=["US", "UK", "Canada", "Australia"]
            ),
            marketing_metrics=MarketingMetrics(
                click_through_rate="3.2%",
                conversion_rate="2.8%",
                return_on_ad_spend="2.5x",
                social_media_engagement="High"
            ),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
    }

@router.get("/product/recommendations/{product_id}",
    summary="Get Product Recommendations",
    description="Get personalized product recommendations based on a product."
)
async def get_product_recommendations(product_id: str, limit: int = 5):
    from main import db
    recommendations_cursor = db["products"].find({"product_id": product_id}).limit(limit)
    recommendations = await recommendations_cursor.to_list(length=None)

    if recommendations:
        for rec in recommendations:
            rec["id"] = str(rec["_id"])  # Convert _id to id
            del rec["_id"]  # Remove _id field if not needed

        return {
            "status": "success",
            "recommendations": recommendations 
        }

    return {
        "status": "success",
        "recommendations": {
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
        ]}  # Fallback recommendations
    }

@router.get("/categories",
    summary="Get All Categories",
    description="Get list of all available categories for both products and videos."
)
async def get_categories():
    from main import db 
    try:
        # Fetch and convert _id to id for products and videos
        product_categories_cursor = db["products"].find()
        products = await product_categories_cursor.to_list(length=None)

        for product in products:
            product["id"] = str(product["_id"])
            del product["_id"]

        video_categories_cursor = db["videos"].find()
        videos = await video_categories_cursor.to_list(length=None)

        for video in videos:
            video["id"] = str(video["_id"])
            del video["_id"]

        return {
            "products": products,
            "videos": videos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")

@router.get("/product/reviews/{product_id}",
    summary="Get Product Reviews",
    description="Get customer reviews for a specific product.",
    response_model=ReviewsResponse
)
async def get_product_reviews(product_id: str, limit: int = 5):
    from main import db

    try:
        ObjectId(product_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    reviews_cursor = db["reviews"].find({"product_id": product_id}).limit(limit)
    reviews = await reviews_cursor.to_list(length=None)

    if reviews:
        for review in reviews:
            review["id"] = str(review["_id"])  # Convert _id to id
            del review["_id"]  # Remove _id field if not needed

        return {
            "status": "success",
            "reviews": reviews  
        }

    fallback_reviews = [
        {
            "product_id": product_id,
            "user_id": "user_1",
            "rating": 5.0,
            "title": "Great product!",
            "comment": "Exceeded my expectations. Would definitely recommend.",
            "date": "2024-02-15",
            "verified_purchase": True
        },
        {
            "product_id": product_id,
            "user_id": "user_2",
            "rating": 4.0,
            "title": "Good value",
            "comment": "Good quality for the price. Minor improvements could be made.",
            "date": "2024-02-10",
            "verified_purchase": True
        }
    ]

    return {
        "status": "success",
        "reviews": fallback_reviews
    }
