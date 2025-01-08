from fastapi import APIRouter, HTTPException
from bson import ObjectId
from models.product import Product
from models.listing import ProductListing
from models.review import RecentReview
from models.analytics import Analytics, SalesPerformance, CustomerBehavior, MarketingMetrics, Demographics
from fastapi import File, UploadFile, Form
from image_data import SAMPLE_RESPONSES
from typing import List, Optional
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Upload and analyze a product image for listing generation.
async def upload_image(
    files: List[UploadFile] = File(...),
    title: str = Form(...),
    caption: Optional[str] = Form(None)
):
    try:
        # Log the incoming request
        logger.info(f"Received upload request - Files: {len(files)}, Title: {title}")

        # To check if over 5 files are uploaded
        if len(files) > 5:
            logger.warning(f"Upload rejected - Too many files: {len(files)}")
            raise HTTPException(
                status_code=400,
                detail="Max 5 images are allowed. Please remove extra files and try again."
            )
        
        # Process files for easier handling
        processed_files = []
        for file in files:
            processed_files.append(file.filename)
            logger.info(f"Processed file: {file.filename}")

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

# Search for products by title across different categories.
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
            results = [Product(
                id=f"comp_1_{abs(hash("677a672445605bdd8827f546"))}",
                title="Similar Product",
                category="Electronics",
                subcategory="Headphone",
                price_range="$89 - $199",
                features=[
                    "Comparable feature 1",
                    "Similar quality",
                    "Alternative design"
                ]
            )
            ]

        return {"status": "success", "products": results}

    except Exception as e:
        print(f"Error during search: {e}")
        raise HTTPException(status_code=500, detail=f"Error during search: {e}")

# Get all listings for a specific product.
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

# Get comparable products for comparison.
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

# Get detailed information about a specific product.
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

# Get detailed analytics for a specific product.
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

# Get personalized product recommendations based on a product.
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
            Product(
                id=f"comp_2_{abs(hash(product_id))}",
                title="Alternative Option",
                category="Electronics",
                subcategory="Headphones",
                price_range="$79 - $189",
                features=[
                    "Alternative feature",
                    "Different approach",
                    "Unique benefit"
                ]
            ),
            Product(
                id="elec_123",
                title="Sony WH-1000XM4",
                category="Electronics",
                subcategory="Headphones",
                price_range="$299 - $349",
                features=["Noise-cancelling", "Long battery life", "Touch controls"]
            ),
            Product(
                id="elec_124",
                title="Samsung Galaxy Watch 6",
                category="Electronics",
                subcategory="Smartwatch",
                price_range="$299 - $449",
                features=["Fitness tracking", "AMOLED display", "Health monitoring"]
            ),
            Product(
                id="elec_125",
                title="Apple iPad Air",
                category="Electronics",
                subcategory="Tablets",
                price_range="$599 - $749",
                features=["Lightweight", "Powerful chip", "Pencil support"]
            )
        ],
        "fashion": [
            Product(
                id="fash_123",
                title="Nike Air Max 270",
                category="Fashion",
                subcategory="Sneakers",
                price_range="$150 - $170",
                features=["Comfortable", "Stylish design", "Durable sole"]
            ),
            Product(
                id="fash_124",
                title="Zara Oversized Blazer",
                category="Fashion",
                subcategory="Clothing",
                price_range="$89 - $129",
                features=["Trendy style", "High-quality fabric", "Versatile"]
            ),
            Product(
                id="fash_125",
                title="Adidas Ultraboost",
                category="Fashion",
                subcategory="Running Shoes",
                price_range="$180 - $200",
                features=["Boost technology", "Supportive fit", "Lightweight"]
            )
        ],
        "home_decor": [
            Product(
                id="decor_123",
                title="Scandinavian Floor Lamp",
                category="Home Decor",
                subcategory="Lighting",
                price_range="$199 - $249",
                features=["Modern design", "Energy-efficient", "Adjustable height"]
            ),
            Product(
                id="decor_124",
                title="Persian Area Rug 5x8",
                category="Home Decor",
                subcategory="Rugs",
                price_range="$299 - $499",
                features=["Handcrafted", "Elegant patterns", "Durable material"]
            ),
            Product(
                id="decor_125",
                title="Modern Wall Mirror",
                category="Home Decor",
                subcategory="Mirrors",
                price_range="$149 - $199",
                features=["Minimalist frame", "High-quality glass", "Easy to hang"]
            )
        ]
    }
}

# Get list of all available categories for both products and videos.
async def get_categories():
    from main import db
    try:
        # Fetch distinct categories for products
        product_categories = await db["products"].distinct("category")

        # Fetch distinct categories for videos
        video_categories = await db["videos"].distinct("category")

        return {
            "product_categories": product_categories,
            "video_categories": video_categories
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")

# Get customer reviews for a specific product.
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
        RecentReview(
            product_id="product_123",
            user_id="user_1",
            rating=5.0,
            title="Great product!",
            comment="Exceeded my expectations. Would definitely recommend.",
            verified_purchase=True,
        ),
        RecentReview(
            product_id="product_123",
            user_id="user_2",
            rating=4.0,
            title="Good value",
            comment="Good quality for the price. Minor improvements could be made.",
            verified_purchase=True,
        )
    ]

    return {
        "status": "success",
        "reviews": fallback_reviews
    }
