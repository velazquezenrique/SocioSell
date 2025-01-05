from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductListing(BaseModel):
    product_id: str  # Refers to Product's ID
    id: str
    title: str
    price: str
    description: str
    features: List[str]
    created_at: Optional[str] = datetime.now().isoformat()
    updated_at: Optional[str] = datetime.now().isoformat()
    class Config:
        # Allow population of fields with alias names
        fields = {
            "id": "_id"  
        }