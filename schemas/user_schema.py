from pydantic import BaseModel, EmailStr, Field, validator
import re

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")

    @validator("password")
    def validate_password(cls, password):
        return password  # Temporarily disable validation for debugging


class UserLogin(BaseModel):
    username: str
    password: str


