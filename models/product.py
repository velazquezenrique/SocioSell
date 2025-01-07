from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Product(BaseModel):
    id: str
    title: str
    category: str
    subcategory: str
    features: List[str]
    price_range: str
    created_at: Optional[str] = datetime.now().isoformat()
    updated_at: Optional[str] = datetime.now().isoformat()

    class Config:
        # Allow population of fields with alias names
        my_field: str = Field(alias="myField")
