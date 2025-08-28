from datetime import datetime
from typing import Optional
from bson import ObjectId
from ..db.mongo import MongoDB
from ..models.user import UserCreate
from ..auth.auth import get_password_hash

async def create_user(user: UserCreate) -> dict:
    # Check if user already exists
    if await MongoDB.db.users.find_one({"email": user.email}):
        return None
    
    # Create new user
    user_dict = user.model_dump()
    user_dict["password_hash"] = get_password_hash(user_dict.pop("password"))
    user_dict["created_at"] = datetime.utcnow()
    user_dict["updated_at"] = user_dict["created_at"]
    
    result = await MongoDB.db.users.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    return user_dict

async def get_user_by_email(email: str) -> Optional[dict]:
    user = await MongoDB.db.users.find_one({"email": email})
    if user:
        user["_id"] = str(user["_id"])
    return user

async def get_user_by_id(user_id: str) -> Optional[dict]:
    try:
        user = await MongoDB.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
        return user
    except:
        return None
