import streamlit as st
import uvicorn
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
import threading
import requests
from PIL import Image
import io
import json
import time

# Import your databases
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

# FastAPI setup
app = FastAPI(
    title="Social Media Product Listing Generator",
    description="""
    Product listing generator supporting both images and videos.
    """
)

# MongoDB setup
MONGODB_URL = "mongodb+srv://varshadewangan1605:Varsha1605@cluster0.d5ant.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.social_media_products

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# FastAPI endpoint functions (copy all your existing endpoints here)
@app.post("/upload/")
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

# Continue from previous code...

@app.get("/search/{title}")
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

@app.get("/listings/{product_id}")
async def get_product_listings(product_id: str):
    if product_id in LISTINGS_DATABASE:
        return {
            "status": "success",
            "listings": [LISTINGS_DATABASE[product_id]]
        }
    
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

@app.get("/compare/{product_id}")
async def get_comparable_products(product_id: str, limit: int = 3):
    if product_id in COMPARABLE_DATABASE:
        return {
            "status": "success",
            "comparable_products": COMPARABLE_DATABASE[product_id][:limit]
        }
    
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

@app.post("/upload/video/")
async def upload_video(
    file: Optional[UploadFile] = File(None),
    title: str = Form(...),
    description: Optional[str] = Form(None)
):
    try:
        category_keywords = {
            "electronics": ["iphone", "macbook", "samsung", "laptop", "phone", "computer", "tech"],
            "fashion": ["nike", "adidas", "shoes", "clothing", "fashion", "wear", "style"],
            "beauty": ["makeup", "cosmetics", "skincare", "beauty", "tutorial"],
            "sports": ["fitness", "workout", "sports", "exercise", "training"]
        }

        video_category = "general"
        for category, keywords in category_keywords.items():
            if any(keyword in title.lower() for keyword in keywords):
                video_category = category
                break

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

        unique_id = f"video_{abs(hash(title))}"[:15]

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
            # ... [Other categories remain the same as in your main.py]
        }

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
# Continue from previous code...

def run_fastapi():
    uvicorn.run(app, host="127.0.0.2", port=8000)

# Streamlit UI
st.set_page_config(
    page_title="Social Media Product Listing Generator",
    page_icon="🛍️",
    layout="wide"
)

# Start FastAPI in a separate thread
if 'fastapi_thread' not in st.session_state:
    st.session_state.fastapi_thread = threading.Thread(target=run_fastapi)
    st.session_state.fastapi_thread.daemon = True
    st.session_state.fastapi_thread.start()
    time.sleep(1)  # Give FastAPI time to start

# Main UI
st.title("Social Media Product Listing Generator")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page", 
    ["Home", "Image Upload", "Video Upload", "Search & Compare", "Analytics"]
)

# Home Page
if page == "Home":
    st.header("Welcome to Product Listing Generator")
    st.write("""
    This tool helps you generate professional product listings for both images and videos.
    Use the sidebar to navigate between different features:
    
    - **Image Upload**: Generate listings for product images
    - **Video Upload**: Create video-based product listings
    - **Search & Compare**: Find and compare products
    - **Analytics**: View detailed product and video analytics
    """)
    
    # Show categories
    if st.button("View Available Categories"):
        try:
            response = requests.get("http://127.0.0.2:8000/categories")
            if response.status_code == 200:
                data = response.json()
                st.subheader("Available Categories")
                st.json(data)
        except Exception as e:
            st.error(f"Error fetching categories: {str(e)}")

# Image Upload Page
elif page == "Image Upload":
    st.header("Upload Product Image")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        uploaded_file = st.file_uploader("Choose a product image", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    with col2:
        title = st.text_input("Product Title")
        caption = st.text_area("Product Caption (Optional)")
        
        if st.button("Generate Listing", key="img_generate"):
            if uploaded_file and title:
                with st.spinner("Generating listing..."):
                    try:
                        files = {
                            'file': ('image.jpg', uploaded_file.getvalue()),
                            'title': (None, title),
                            'caption': (None, caption if caption else "")
                        }
                        response = requests.post("http://127.0.0.2:8000/upload/", files=files)
                        if response.status_code == 200:
                            st.success("Listing generated successfully!")
                            st.json(response.json())
                        else:
                            st.error("Error generating listing")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please upload an image and provide a title")

# Video Upload Page
elif page == "Video Upload":
    st.header("Upload Product Video")
    
    video_file = st.file_uploader("Choose a product video", type=['mp4', 'mov', 'avi'])
    video_title = st.text_input("Video Title")
    video_description = st.text_area("Video Description (Optional)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        categories = ["Electronics", "Fashion", "Beauty", "Sports", "General"]
        selected_category = st.selectbox("Select Category", categories)
    
    with col2:
        if st.button("Generate Video Listing"):
            if video_title:
                with st.spinner("Processing video..."):
                    try:
                        files = {
                            'title': (None, video_title),
                            'description': (None, video_description if video_description else "")
                        }
                        if video_file:
                            files['file'] = ('video.mp4', video_file.getvalue())
                        
                        response = requests.post("http://127.0.0.2:8000/upload/video/", files=files)
                        if response.status_code == 200:
                            st.success("Video listing generated successfully!")
                            st.json(response.json())
                        else:
                            st.error("Error generating video listing")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please provide a video title")

# Search & Compare Page
elif page == "Search & Compare":
    st.header("Search & Compare Products")
    
    search_query = st.text_input("Search Products")
    search_type = st.radio("Search Type", ["All", "Products Only", "Videos Only"])
    
    if st.button("Search"):
        if search_query:
            with st.spinner("Searching..."):
                try:
                    if search_type == "All":
                        endpoint = f"/search/all/{search_query}"
                    elif search_type == "Products Only":
                        endpoint = f"/search/{search_query}"
                    else:
                        endpoint = f"/video/search/{search_query}"
                    
                    response = requests.get(f"http://127.0.0.2:8000{endpoint}")
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Search completed!")
                        st.json(data)
                        
                        # Show compare option for products
                        if search_type != "Videos Only" and data.get("products"):
                            selected_product = st.selectbox(
                                "Select a product to compare",
                                [p["title"] for p in data["products"]]
                            )
                            if st.button("Compare"):
                                product_id = next(p["id"] for p in data["products"] if p["title"] == selected_product)
                                compare_response = requests.get(f"http://127.0.0.2:8000/compare/{product_id}")
                                if compare_response.status_code == 200:
                                    st.subheader("Comparable Products")
                                    st.json(compare_response.json())
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a search term")

# Analytics Page
elif page == "Analytics":
    st.header("Product & Video Analytics")
    
    analytics_type = st.radio("Select Type", ["Product Analytics", "Video Analytics"])
    item_id = st.text_input("Enter Product/Video ID")
    
    if st.button("Get Analytics"):
        if item_id:
            with st.spinner("Fetching analytics..."):
                try:
                    endpoint = "/product/analytics/" if analytics_type == "Product Analytics" else "/video/analytics/"
                    response = requests.get(f"http://127.0.0.2:8000{endpoint}{item_id}")
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Analytics retrieved successfully!")
                        
                        # Display analytics in a more organized way
                        if analytics_type == "Product Analytics":
                            col1, col2 = st.columns(2)
                            with col1:
                                st.subheader("Sales Performance")
                                st.write(data["analytics"]["sales_performance"])
                                st.subheader("Customer Behavior")
                                st.write(data["analytics"]["customer_behavior"])
                            with col2:
                                st.subheader("Demographics")
                                st.write(data["analytics"]["demographics"])
                                st.subheader("Marketing Metrics")
                                st.write(data["analytics"]["marketing_metrics"])
                        else:
                            col1, col2 = st.columns(2)
                            with col1:
                                st.subheader("Engagement")
                                st.write(data["analytics"]["engagement"])
                                st.subheader("Performance")
                                st.write(data["analytics"]["performance"])
                            with col2:
                                st.subheader("Audience")
                                st.write(data["analytics"]["audience"])
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter an ID")

# Sidebar Additional Features
with st.sidebar:
    st.header("Quick Actions")
    
    if st.button("View Recent Products"):
        try:
            response = requests.get("http://127.0.0.2:8000/search/latest")
            if response.status_code == 200:
                st.json(response.json())
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.header("Help & Support")
    if st.button("Show Documentation"):
        st.markdown("""
        ### Quick Guide
        1. Upload images or videos
        2. Fill in the required information
        3. Generate listings automatically
        4. Search and compare products
        5. View detailed analytics
        
        For more help, contact support.
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Made with ❤️ by Your Product Team</p>
</div>
""", unsafe_allow_html=True)
