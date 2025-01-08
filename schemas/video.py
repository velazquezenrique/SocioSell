from fastapi import APIRouter, HTTPException
from models.video import Video
from models.videoListing import VideoListing, ProductLink
from models.analyticsVideo import VideoAnalytics, VideoAudience, VideoEngagement, VideoPerformance  
from bson import ObjectId
from typing import Optional
from fastapi import File, UploadFile, Form
from video_data import VIDEO_DATABASE
from datetime import datetime
    
router = APIRouter()

# Upload and analyze a product video for listing generation.
async def upload_video(
    file: Optional[UploadFile] = File(None),  # Made file optional
    title: str = Form(...),
    description: Optional[str] = Form(None)
):
    from main import logger
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

# Search for product videos by title.
async def search_videos(title: str):
    from main import db
    results = []
    search_term = title.lower()
    
    # Fetching videos from the database
    video_cursor = db["videos"].find({"title": {"$regex": search_term, "$options": "i"}})
    
    async for video in video_cursor:
        video["id"] = str(video["_id"])  # Convert ObjectId to string

        try:
            results.append(Video(**video))  # Construct the Video object
        except Exception as e:
            print(f"Error while processing video: {e}")
            continue
    
    if not results:
        # Default response if no videos found
        results = [Video(
                id=f"comp_1_{abs(hash('677a67241f305bdd8827f546'))}",
                title="Similar Product Review 1",
                category="Electronics",
                subcategory="Headphone",
                duration="9:30",
                views="15K",
                highlights=["Feature comparison", "Price value"],
                transcript_summary="A review highlighting key features and pricing.",
                key_features=["Wireless", "Noise-cancelling"],
                price_range="$89 - $199",
            ),]
        
    return {
        "status": "success",
        "videos": results
    }

# Get all listings and platforms for a specific video.
async def get_video_listings(video_id: str):
    from main import db

    try:
        # Validate and convert the video_id to ObjectId
        object_id = ObjectId(video_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid video ID format")

    try:
        # Query for video listings with matching or similar video ID
        video_listings_cursor = db["video_listings"].find({"video_id": str(object_id)})
        video_listings = await video_listings_cursor.to_list(length=None)

        if video_listings:
            # Process each listing to match the expected structure
            results = []
            for listing in video_listings:
                listing["id"] = str(listing["_id"])  # Convert ObjectId to string
                del listing["_id"]  # Remove original ObjectId
                results.append(VideoListing(**listing))  # Convert to Pydantic model
            
            return {
                "status": "success",
                "listings": results
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching video listings: {e}")

    # Default response if no listing is found
    default_listing = VideoListing(
        product_id=f"prod_{abs(hash(video_id))}",
        platform="YouTube",
        title="Product Review",
        views="10K",
        rating=4.5,
        key_timestamps={
            "intro": "0:00",
            "features": "2:00",
            "demo": "5:00",
            "conclusion": "8:00"
        },
        product_links=[  # Ensure this is included
            ProductLink(store="Online Store", price="$99.99"),
            ProductLink(store="Marketplace", price="$89.99")
        ],
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    return {
        "status": "success",
        "listings": [default_listing]
    }

# Get comparable videos for comparison.
async def get_comparable_videos(video_id: str, limit: int = 3):
    from main import db
    try:
        # Validate and convert the video_id to ObjectId
        object_id = ObjectId(video_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid video ID format")

    # Fetch the reference video from the database
    target_video = await db["videos"].find_one({"_id": object_id})

    if not target_video:
        raise HTTPException(status_code=404, detail="Reference video not found")

    # Build the query to find comparable videos
    query = {
        "$or": [
            {"title": {"$regex": target_video["title"], "$options": "i"}},
            {"category": target_video.get("category")},
            {"subcategory": target_video.get("subcategory")},
            {"duration": target_video.get("duration")},
            {"highlights": {"$in": target_video.get("highlights", [])}},
            {"price_range": target_video.get("price_range")},
            {"key_features": {"$in": target_video.get("key_features", [])}}
        ],
        "_id": {"$ne": video_id}  # Exclude the reference video
    }

    # Fetch comparable videos based on the query
    comparable_videos_cursor = db["videos"].find(query).limit(limit)
    comparable_videos = await comparable_videos_cursor.to_list(length=None)

    comparable_videos = [
        {**cv, "id": str(cv["_id"])} # Map _id to id
        for cv in comparable_videos
    ]
   
    # Return found comparable videos
    if comparable_videos:
        return {
            "status": "success",
            "comparable_videos": [Video(**cv) for cv in comparable_videos]
        }

    # Default comparable videos if no data found or query fails
    return {
        "status": "success",
        "comparable_videos": [
            Video(
                id=f"comp_1_{abs(hash(video_id))}",
                title="Similar Product Review 1",
                category=target_video.get("category", "Unknown"),
                subcategory=target_video.get("subcategory", "Unknown"),
                duration="9:30",
                views="15K",
                highlights=["Feature comparison", "Price value"],
                transcript_summary="A review highlighting key features and pricing.",
                key_features=["Wireless", "Noise-cancelling"],
                price_range="$89 - $199",
            ),
            Video(
                id=f"comp_2_{abs(hash(video_id))}",
                title="Alternative Product Review",
                category="Electronics",
                subcategory="Smartwatches",
                duration="8:45",
                views="12K",
                highlights=["Cost comparison", "Durability"],
                transcript_summary="A comprehensive review of alternative smartwatches.",
                key_features=["Durable", "Long battery life"],
                price_range="$79 - $189",
            )
        ]
    }

# Get detailed analytics for a specific video.
async def get_video_analytics(video_id: str):
    from main import db

    try:
        # Validate and convert the video_id to ObjectId
        object_id = ObjectId(video_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid video ID format")

    try:
        # Fetch video analytics from the database
        video_analytics_data = await db["video_analytics"].find_one({"_id": object_id})

        if video_analytics_data:
            # Prepare analytics data
            video_analytics_data["id"] = str(video_analytics_data["_id"])  # Convert ObjectId to string
            del video_analytics_data["_id"]  # Remove ObjectId field
            analytics = VideoAnalytics(**video_analytics_data)  # Convert to Pydantic model
            return {
                "status": "success",
                "analytics": analytics.dict()  # Return the model as a dictionary
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching analytics: {e}")

    # Default analytics response if no data is found
    default_analytics = VideoAnalytics(
        product_id=video_id,
        engagement=VideoEngagement(
            views="5K",
            likes="500",
            comments="50",
            average_watch_time="5:30"
        ),
        audience=VideoAudience(
            demographics={
                "18-24": "25%",
                "25-34": "40%",
                "35-44": "20%",
                "45+": "15%"
            },
            top_regions=["US", "UK", "Canada", "Australia"]
        ),
        performance=VideoPerformance(
            retention_rate="65%",
            click_through_rate="3.5%",
            conversion_rate="2.1%"
        ),
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )

    return {
        "status": "success",
        "analytics": default_analytics.dict()  # Return default data
    }