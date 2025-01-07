from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime

class RecentReview(BaseModel):
    product_id: str
    user_id: str
    rating: float
    title: str
    comment: Optional[str]
    verified_purchase: bool
    created_at: Optional[str] = datetime.now().isoformat()
    updated_at: Optional[str] = datetime.now().isoformat()

    class Config:
        # Allow population of fields with alias names
        my_field: str = Field(alias="myField")
