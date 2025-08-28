from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    SERVED = "served"
    COMPLETED = "completed"

class OrderItem(BaseModel):
    menu_id: str
    name: str
    unit_price: float
    quantity: int

class OrderItemCreate(BaseModel):
    menu_id: str
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderInDB(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str
    items: List[OrderItem]
    total_price: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

class OrderResponse(OrderInDB):
    pass

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
