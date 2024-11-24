from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import logging
from dotenv import load_dotenv
import os

# Import your processors
from image_processor import ImageProcessor
from video_processor import VideoProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
MONGODB_URL = "mongodb+srv://varshadewangan1605:Varsha1605@cluster0.d5ant.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize FastAPI
app = FastAPI(
    title="Social Media to Amazon Product Converter",
    description="Convert social media content into Amazon product listings",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request validation
class SocialMediaPost(BaseModel):
    platform: str
    content_type: str  # "image", "video", or "text"
    content_url: str
    caption: Optional[str] = None

class ProductListing(BaseModel):
    title: str
    category: str
    description: str
    price: str
    features: List[str]
    specifications: Dict[str, str]
    images: List[str]
    video_url: Optional[str] = None

# Database connection
async def get_database():
    client = AsyncIOMotorClient(MONGODB_URL)
    return client.social_media_products

# Initialize processors
image_processor = ImageProcessor()
video_processor = VideoProcessor(GOOGLE_API_KEY)

# API endpoints
@app.post("/upload/", response_model=dict)
async def upload_social_media_content(post: SocialMediaPost, background_tasks: BackgroundTasks):
    """Upload social media content for processing"""
    try:
        db = await get_database()
        
        # Store the post in database
        post_dict = post.dict()
        post_dict["processed"] = False
        post_dict["timestamp"] = datetime.utcnow()
        
        result = await db.social_posts.insert_one(post_dict)
        
        # Add to background processing queue
        background_tasks.add_task(process_content, str(result.inserted_id))
        
        return {
            "status": "success",
            "message": "Content uploaded successfully",
            "post_id": str(result.inserted_id)
        }
    except Exception as e:
        logger.error(f"Error uploading content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{post_id}")
async def check_processing_status(post_id: str):
    """Check the processing status of uploaded content"""
    try:
        db = await get_database()
        post = await db.social_posts.find_one({"_id": post_id})
        
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        return {
            "processed": post.get("processed", False),
            "status": "complete" if post.get("processed") else "processing"
        }
    except Exception as e:
        logger.error(f"Error checking status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/listings/")
async def get_product_listings(skip: int = 0, limit: int = 10):
    """Get processed product listings"""
    try:
        db = await get_database()
        listings = await db.product_listings.find().skip(skip).limit(limit).to_list(length=limit)
        return listings
    except Exception as e:
        logger.error(f"Error fetching listings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_content(post_id: str):
    """Process the uploaded content in background"""
    try:
        db = await get_database()
        post = await db.social_posts.find_one({"_id": post_id})
        
        if not post:
            logger.error(f"Post {post_id} not found")
            return
        
        # Process based on content type
        if post["content_type"] == "image":
            analysis = await image_processor.analyze_product(post["content_url"])
        elif post["content_type"] == "video":
            analysis = await video_processor.process_video(post["content_url"])
        else:  # text
            analysis = await image_processor.text_processor.analyze_text(post["caption"])
        
        if analysis["status"] == "success":
            # Create product listing
            listing = {
                "title": analysis.get("product_name", ""),
                "category": analysis.get("category", ""),
                "description": analysis.get("description", ""),
                "price": analysis.get("price", ""),
                "features": analysis.get("key_features", []),
                "specifications": analysis.get("specifications", {}),
                "images": [post["content_url"]] if post["content_type"] == "image" else [],
                "video_url": post["content_url"] if post["content_type"] == "video" else None,
                "source_post_id": post_id,
                "created_at": datetime.utcnow()
            }
            
            # Save listing
            await db.product_listings.insert_one(listing)
            
            # Update post as processed
            await db.social_posts.update_one(
                {"_id": post_id},
                {
                    "$set": {
                        "processed": True,
                        "analysis_result": analysis
                    }
                }
            )
            
            logger.info(f"Successfully processed post {post_id}")
        else:
            logger.error(f"Processing failed for post {post_id}: {analysis.get('message')}")
            
    except Exception as e:
        logger.error(f"Error processing content: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
