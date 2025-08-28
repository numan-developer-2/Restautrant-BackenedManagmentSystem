from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from ..db.mongo import MongoDB
from ..models.menu import MenuCreate, MenuUpdate

async def create_menu_item(menu_item: MenuCreate) -> dict:
    menu_dict = menu_item.model_dump()
    menu_dict["created_at"] = datetime.utcnow()
    menu_dict["updated_at"] = menu_dict["created_at"]
    
    result = await MongoDB.db.menu.insert_one(menu_dict)
    menu_dict["_id"] = str(result.inserted_id)
    return menu_dict

async def get_menu_items(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    available_only: bool = False
) -> List[dict]:
    query = {}
    if category:
        query["category"] = category
    if available_only:
        query["availability"] = True
    
    cursor = MongoDB.db.menu.find(query).skip(skip).limit(limit)
    menu_items = []
    async for item in cursor:
        item["_id"] = str(item["_id"])
        menu_items.append(item)
    return menu_items

async def get_menu_item_by_id(menu_id: str) -> Optional[dict]:
    try:
        menu_item = await MongoDB.db.menu.find_one({"_id": ObjectId(menu_id)})
        if menu_item:
            menu_item["_id"] = str(menu_item["_id"])
        return menu_item
    except:
        return None

async def update_menu_item(menu_id: str, menu_update: MenuUpdate) -> Optional[dict]:
    try:
        update_data = menu_update.model_dump(exclude_unset=True)
        if not update_data:
            return None
        
        update_data["updated_at"] = datetime.utcnow()
        
        result = await MongoDB.db.menu.find_one_and_update(
            {"_id": ObjectId(menu_id)},
            {"$set": update_data},
            return_document=True
        )
        
        if result:
            result["_id"] = str(result["_id"])
        return result
    except:
        return None

async def delete_menu_item(menu_id: str) -> bool:
    try:
        result = await MongoDB.db.menu.delete_one({"_id": ObjectId(menu_id)})
        return result.deleted_count > 0
    except:
        return False
