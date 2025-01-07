from fastapi import APIRouter
from typing import Optional
from fastapi import File, UploadFile, Form
from schemas.video import (
    upload_video,
    search_videos,
    get_video_listings,
    get_comparable_videos,
    get_video_analytics
)
    
router = APIRouter()

@router.post("/", 
    summary="Upload Product Video",
    description="Upload and analyze a product video for listing generation."
)
async def upload_video_route(
    file: Optional[UploadFile] = File(None),  # Made file optional
    title: str = Form(...),
    description: Optional[str] = Form(None)
):
    return await upload_video(file, title, description)

@router.get("/search/{title}",
    summary="Search Videos",
    description="Search for product videos by title."
)
async def search_videos_route(title: str):
    return await search_videos(title)

@router.get("/listings/{video_id}",
    summary="Get Video Listings",
    description="Get all listings and platforms for a specific video."
)
async def get_video_listings_route(video_id: str):
    return await get_video_listings(video_id)

@router.get("/compare/{video_id}",
    summary="Get Comparable Videos",
    description="Get comparable videos for comparison."
)
async def get_comparable_videos_route(video_id: str, limit: int = 3):
    return await get_comparable_videos(video_id, limit)

@router.get("/analytics/{video_id}",
    summary="Get Video Analytics",
    description="Get detailed analytics for a specific video."
)
async def get_video_analytics_route(video_id: str):
    return await get_video_analytics(video_id)