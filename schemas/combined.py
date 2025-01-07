from fastapi import APIRouter, HTTPException

router = APIRouter()

# Search both products and videos across all categories.
async def search_all_content(query: str):
    from main import product_collection, video_collection
    
    search_term = query.lower()

    try:
        # Search products in MongoDB
        product_cursor = product_collection.find({"title": {"$regex": search_term, "$options": "i"}})
        product_results = await product_cursor.to_list(length=None)  # Convert cursor to list
        for product in product_results:
            product["_id"] = str(product["_id"])  # Convert ObjectId to string

        # Search videos in MongoDB
        video_cursor = video_collection.find({"title": {"$regex": search_term, "$options": "i"}})
        video_results = await video_cursor.to_list(length=None)  # Convert cursor to list
        for video in video_results:
            video["_id"] = str(video["_id"])  # Convert ObjectId to string

        return {
            "status": "success",
            "results": {
                "products": product_results,
                "videos": video_results
            }
        }
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail="Error fetching data from database")