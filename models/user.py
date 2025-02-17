from pydantic import BaseModel, EmailStr
from bson import ObjectId

class User(BaseModel):
    id: ObjectId
    username: str
    email: EmailStr
    password: str

