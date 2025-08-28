from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str
    role: str = "customer"  # default role

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(UserBase):
    id: str = Field(..., alias="_id")
    role: str
    password_hash: str
    created_at: datetime
    updated_at: datetime

class UserResponse(UserBase):
    id: str = Field(..., alias="_id")
    role: str
    created_at: datetime
    updated_at: datetime
