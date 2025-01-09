from pymongo import MongoClient, ASCENDING
from pymongo.server_api import ServerApi
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_product_database():
    """Setup product reference database with sample data"""
    uri = "add your string"
    
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client.social_media_products
        
        # Create Image Collections
        product_collection = db["products"]
        listing_collection = db["listings"]
        analytics_collection = db["analytics"]
        review_collection = db["reviews"]

        # Video Collections
        video_collection = db["videos"]
        video_listings_collection = db["video_listings"]
        video_analytics_collection = db["video_analytics"]
        
        # Create indexes for products
        product_collection.create_index([("id", ASCENDING)], unique=True)
        product_collection.create_index([("title", ASCENDING)])
        product_collection.create_index([("category", ASCENDING)])
        product_collection.create_index([("subcategory", ASCENDING)])
        product_collection.create_index([("features", ASCENDING)])
        product_collection.create_index([("price_range", ASCENDING)])
        product_collection.create_index([("created_at", ASCENDING)])
        product_collection.create_index([("updated_at", ASCENDING)])
        # Create indexes for listings
        listing_collection.create_index([("id", ASCENDING), ("product_id", ASCENDING)])
        listing_collection.create_index([("product_id", ASCENDING), ("created_at", ASCENDING)])
        listing_collection.create_index([("price", ASCENDING), ("updated_at", ASCENDING)])
        listing_collection.create_index([("features", ASCENDING), ("title", ASCENDING)])
        listing_collection.create_index([("id", ASCENDING)], unique=True)
        listing_collection.create_index([("title", ASCENDING)])
        listing_collection.create_index([("price", ASCENDING)])
        listing_collection.create_index([("features", ASCENDING)], name="features_index")
        # Create indexes for analytics
        analytics_collection.create_index([("id", ASCENDING), ("product_id", ASCENDING)])
        analytics_collection.create_index([("product_id", ASCENDING), ("created_at", ASCENDING)])
        analytics_collection.create_index([("id", ASCENDING)], unique=True)
        analytics_collection.create_index([("product_id", ASCENDING)], unique=True)          
        analytics_collection.create_index([("created_at", ASCENDING)])          
        analytics_collection.create_index([("updated_at", ASCENDING)])         
        analytics_collection.create_index([("sales_performance.total_sales", ASCENDING)])     
        analytics_collection.create_index([("sales_performance.revenue", ASCENDING)])          
        analytics_collection.create_index([("sales_performance.average_price", ASCENDING)])    
        analytics_collection.create_index([("customer_behavior.view_to_purchase_rate", ASCENDING)])  
        analytics_collection.create_index([("customer_behavior.repeat_purchase_rate", ASCENDING)])   
        analytics_collection.create_index([("customer_behavior.average_rating", ASCENDING)])         
        analytics_collection.create_index([("marketing_metrics.click_through_rate", ASCENDING)])    
        analytics_collection.create_index([("marketing_metrics.social_media_engagement", ASCENDING)])
        # Create indexes for review
        review_collection.create_index([("product_id", ASCENDING), ("rating", ASCENDING)])
        review_collection.create_index([("user_id", ASCENDING), ("product_id", ASCENDING)])
        review_collection.create_index([("id", ASCENDING)], unique=True)      
        review_collection.create_index([("product_id", ASCENDING)])      
        review_collection.create_index([("user_id", ASCENDING)])         
        review_collection.create_index([("rating", ASCENDING)])          
        review_collection.create_index([("title", ASCENDING)])           
        review_collection.create_index([("verified_purchase", ASCENDING)])  
        review_collection.create_index([("created_at", ASCENDING)])   
        review_collection.create_index([("updated_at", ASCENDING)])

        # Create indexes for video
        video_collection.create_index([("title", ASCENDING), ("views", ASCENDING)])
        video_collection.create_index([("views", ASCENDING), ("rating", ASCENDING)])
        video_collection.create_index([("id", ASCENDING)], unique=True)               
        video_collection.create_index([("title", ASCENDING)])                 
        video_collection.create_index([("category", ASCENDING)])              
        video_collection.create_index([("subcategory", ASCENDING)])           
        video_collection.create_index([("duration", ASCENDING)])              
        video_collection.create_index([("views", ASCENDING)])                 
        video_collection.create_index([("transcript_summary", "text")])       
        video_collection.create_index([("price_range", ASCENDING)])           
        video_collection.create_index([("created_at", ASCENDING)])            
        video_collection.create_index([("updated_at", ASCENDING)])           
        video_collection.create_index([("key_features", ASCENDING)])
        video_collection.create_index([("highlights", ASCENDING)])        
        # Create indexes for video listing
        video_listings_collection.create_index([("product_id", ASCENDING), ("id", ASCENDING)])
        video_listings_collection.create_index([("id", ASCENDING)], unique=True)                  
        video_listings_collection.create_index([("product_id", ASCENDING)])                  
        video_listings_collection.create_index([("platform", ASCENDING)])                    
        video_listings_collection.create_index([("title", ASCENDING)])                       
        video_listings_collection.create_index([("views", ASCENDING)])                       
        video_listings_collection.create_index([("rating", ASCENDING)])                      
        video_listings_collection.create_index([("created_at", ASCENDING)])                  
        video_listings_collection.create_index([("updated_at", ASCENDING)])                  
        video_listings_collection.create_index([("product_links.price", ASCENDING)]) 
        # Create indexes for video analytics
        video_analytics_collection.create_index([("id", ASCENDING), ("product_id", ASCENDING)])
        video_analytics_collection.create_index([("engagement.views", ASCENDING), ("engagement.likes", ASCENDING)])
        video_analytics_collection.create_index([("performance.retention_rate", ASCENDING), ("performance.click_through_rate", ASCENDING)])
        video_analytics_collection.create_index([("id", ASCENDING)], unique=True)                
        video_analytics_collection.create_index([("product_id", ASCENDING)])                
        video_analytics_collection.create_index([("created_at", ASCENDING)])                
        video_analytics_collection.create_index([("updated_at", ASCENDING)])                
        video_analytics_collection.create_index([("engagement.views", ASCENDING)])          
        video_analytics_collection.create_index([("engagement.likes", ASCENDING)])          
        video_analytics_collection.create_index([("engagement.comments", ASCENDING)])       
        video_analytics_collection.create_index([("engagement.average_watch_time", ASCENDING)])  
        video_analytics_collection.create_index([("audience.demographics", ASCENDING)])    
        video_analytics_collection.create_index([("audience.top_regions", ASCENDING)])     
        video_analytics_collection.create_index([("performance.retention_rate", ASCENDING)])  
        video_analytics_collection.create_index([("performance.click_through_rate", ASCENDING)])  

        # Sample product reference data
        sample_products = [
            {
                "category": "Electronics",
                "subcategory": "Smartphones",
                "brand_options": ["Samsung Galaxy S24", "iPhone 15", "Google Pixel 8"],
                "price_ranges": {
                    "budget": {"min": 299, "max": 499},
                    "mid_range": {"min": 500, "max": 799},
                    "premium": {"min": 800, "max": 1299}
                },
                "common_features": [
                    "5G Connectivity",
                    "AI-Enhanced Camera",
                    "AMOLED Display",
                    "Fast Charging",
                    "Wireless Charging"
                ],
                "keywords": ["smartphone", "mobile phone", "cell phone", "android", "ios"]
            },
            {
                "category": "Electronics",
                "subcategory": "Wireless Earbuds",
                "brand_options": ["Apple AirPods Pro", "Samsung Galaxy Buds", "Google Pixel Buds"],
                "price_ranges": {
                    "budget": {"min": 49, "max": 99},
                    "mid_range": {"min": 100, "max": 199},
                    "premium": {"min": 200, "max": 299}
                },
                "common_features": [
                    "Active Noise Cancellation",
                    "Touch Controls",
                    "Wireless Charging Case",
                    "Water Resistance",
                    "Voice Assistant Support"
                ],
                "keywords": ["earbuds", "wireless earphones", "tws", "headphones"]
            },
            {
                "category": "Electronics",
                "subcategory": "Smartwatches",
                "brand_options": ["Apple Watch Series 9", "Samsung Galaxy Watch 6", "Google Pixel Watch"],
                "price_ranges": {
                    "budget": {"min": 149, "max": 249},
                    "mid_range": {"min": 250, "max": 399},
                    "premium": {"min": 400, "max": 799}
                },
                "common_features": [
                    "Health Monitoring",
                    "Fitness Tracking",
                    "GPS",
                    "Always-On Display",
                    "Water Resistance"
                ],
                "keywords": ["smartwatch", "fitness tracker", "smart watch", "wearable"]
            }
        ]
        
        # Clear existing data
        # product_references.delete_many({})
        # listings.delete_many({})
        
        # Insert sample data
        # product_references.insert_many(sample_products)
        logger.info("Sample product references inserted successfully")
        
        # Insert sample listings
        # sample_listings = [
        #     {
        #         "product_id": str(product_references.find_one({"brand_options": "iPhone 15"})["_id"]),
        #         "title": "iPhone 15 Pro Max",
        #         "category": "Electronics",
        #         "subcategory": "Smartphones",
        #         "description": "Latest iPhone with A17 Pro chip and titanium design",
        #         "price": "$999",
        #         "features": [
        #             "48MP Main Camera",
        #             "Titanium Design",
        #             "Action Button"
        #         ],
        #         "keywords": ["iphone", "smartphone", "apple"],
        #         "original_caption": "Just got the new iPhone 15 Pro! Amazing camera system!",
        #         "created_at": datetime.utcnow(),
        #         "status": "active"
        #     }
        # ]
        
        # listings.insert_many(sample_listings)
        # logger.info("Sample listings inserted successfully")
        
    except Exception as e:
        logger.error(f"Error setting up database: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    setup_product_database()
