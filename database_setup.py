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
MAX_RETRIES = 5  # Maximum number of retries
INITIAL_RETRY_DELAY = 1  # Initial delay between retries in seconds
MAX_RETRY_DELAY = 30  # Maximum delay between retries in seconds
TIMEOUT_CONFIG = {
    "connectTimeoutMS": 5000,  # 5 seconds connection timeout
    "socketTimeoutMS": 10000  # 10 seconds socket timeout
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
    """Setup product reference database with sample data."""
    client = None
    try:
        client = connect_to_mongodb()
        db = client.social_media_products

        # Create collections
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
        # Additional indexes (kept as is from your original script)

        logger.info("Indexes created successfully")

        # Sample data insertion (disabled by default)
        # Uncomment the following to insert data into the collections
        # product_collection.insert_many(sample_products)
        # logger.info("Sample product references inserted successfully")

    except Exception as e:
        logger.error(f"Error setting up database: {e}")
    finally:
        if client:
            client.close()
            logger.info("MongoDB connection closed")


if __name__ == "__main__":
    setup_product_database()
