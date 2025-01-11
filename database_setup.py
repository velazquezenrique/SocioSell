from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from pymongo.server_api import ServerApi
import logging
import os
import time
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration for retry and timeouts
MAX_RETRIES = 5
INITIAL_RETRY_DELAY = 1
MAX_RETRY_DELAY = 30
TIMEOUT_CONFIG = {
    "connectTimeoutMS": 5000,
    "socketTimeoutMS": 10000
}

def exponential_backoff(attempt):
    """Calculate exponential backoff delay."""
    return min(INITIAL_RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)

def connect_to_mongodb():
    """Establish a MongoDB connection with retries and timeouts."""
    uri = os.getenv("MONGODB_URL")
    if not uri:
        logger.error("MONGODB_URL is not set in the environment.")
        raise ValueError("MONGODB_URL is missing")

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Attempting to connect to MongoDB (Attempt {attempt + 1}/{MAX_RETRIES})")
            client = MongoClient(uri, server_api=ServerApi('1'), **TIMEOUT_CONFIG)
            # Verify connection
            client.admin.command("ping")
            logger.info("Connected to MongoDB successfully")
            return client
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            delay = exponential_backoff(attempt)
            logger.warning(f"Connection failed (Attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.error("Maximum retry attempts reached. Exiting...")
                raise
        except Exception as e:
            logger.error(f"Unexpected error while connecting to MongoDB: {e}")
            raise

def setup_product_database():
    """Setup product reference database with sample data"""
    client = None
    try:
        client = connect_to_mongodb()
        db = client.social_media_products
        
        # Create Collections
        product_collection = db["products"]
        listing_collection = db["listings"]
        analytics_collection = db["analytics"]
        review_collection = db["reviews"]
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

        logger.info("All indexes created successfully")

        # Sample data insertion (commented out by default)
        # Uncomment and modify as needed
        # product_collection.insert_many(sample_products)
        # logger.info("Sample product references inserted successfully")

    except Exception as e:
        logger.error(f"Error setting up database: {e}")
        raise
    finally:
        if client:
            client.close()
            logger.info("MongoDB connection closed")

if __name__ == "__main__":
    setup_product_database()