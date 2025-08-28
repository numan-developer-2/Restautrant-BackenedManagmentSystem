from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class MenuBase(BaseModel):
    name: str
    description: str
    price: float
    category: str
    availability: bool = True

class MenuCreate(MenuBase):
    pass

class MenuUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    availability: Optional[bool] = None

class MenuInDB(MenuBase):
    id: str = Field(..., alias="_id")
    created_at: datetime
    updated_at: datetime

class MenuResponse(MenuInDB):
    pass
