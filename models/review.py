from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RatingDistribution(BaseModel):
    five_star: str
    four_star: str
    three_star: str
    two_star: str
    one_star: str

class RecentReview(BaseModel):
    product_id: str
    user_id: str
    rating: float
    title: str
    comment: Optional[str]
    date: str
    verified_purchase: bool
    created_at: Optional[str] = datetime.now().isoformat()
    updated_at: Optional[str] = datetime.now().isoformat()

    class Config:
        # Allow population of fields with alias names
        fields = {
            "id": "_id"  
        }

class ReviewsResponse(BaseModel):
    status: str
    reviews: List[RecentReview]
