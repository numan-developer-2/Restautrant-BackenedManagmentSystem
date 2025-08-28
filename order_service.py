from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from ..db.mongo import MongoDB
from ..models.order import OrderCreate, OrderStatus, OrderItem

async def create_order(user_id: str, order: OrderCreate) -> Optional[dict]:
    # Validate and get menu items
    order_items = []
    total_price = 0.0
    
    for item in order.items:
        menu_item = await MongoDB.db.menu.find_one({"_id": ObjectId(item.menu_id)})
        if not menu_item or not menu_item.get("availability", False):
            return None
            
        order_item = OrderItem(
            menu_id=str(menu_item["_id"]),
            name=menu_item["name"],
            unit_price=menu_item["price"],
            quantity=item.quantity
        )
        order_items.append(order_item.model_dump())
        total_price += menu_item["price"] * item.quantity
    
    # Create order
    order_dict = {
        "user_id": user_id,
        "items": order_items,
        "total_price": total_price,
        "status": OrderStatus.PENDING,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await MongoDB.db.orders.insert_one(order_dict)
    order_dict["_id"] = str(result.inserted_id)
    return order_dict

async def get_orders(user_id: Optional[str] = None, skip: int = 0, limit: int = 10) -> List[dict]:
    query = {}
    if user_id:
        query["user_id"] = user_id
        
    cursor = MongoDB.db.orders.find(query).sort("created_at", -1).skip(skip).limit(limit)
    orders = []
    async for order in cursor:
        order["_id"] = str(order["_id"])
        orders.append(order)
    return orders

async def get_order_by_id(order_id: str, user_id: Optional[str] = None) -> Optional[dict]:
    try:
        query = {"_id": ObjectId(order_id)}
        if user_id:
            query["user_id"] = user_id
            
        order = await MongoDB.db.orders.find_one(query)
        if order:
            order["_id"] = str(order["_id"])
        return order
    except:
        return None

async def update_order_status(order_id: str, status: OrderStatus) -> Optional[dict]:
    try:
        order = await MongoDB.db.orders.find_one_and_update(
            {"_id": ObjectId(order_id)},
            {
                "$set": {
                    "status": status,
                    "updated_at": datetime.utcnow()
                }
            },
            return_document=True
        )
        if order:
            order["_id"] = str(order["_id"])
        return order
    except:
        return None
