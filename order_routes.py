from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from ..models.order import OrderCreate, OrderResponse, OrderStatusUpdate
from ..services import order_service
from ..auth.auth import get_current_user, check_permissions

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    current_user=Depends(check_permissions(["customer"]))
):
    order_dict = await order_service.create_order(str(current_user["_id"]), order)
    if not order_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid menu items in order"
        )
    return order_dict

@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user=Depends(get_current_user)
):
    # Admin/staff can see all orders, customers only see their own
    user_id = None if current_user["role"] in ["admin", "staff"] else str(current_user["_id"])
    return await order_service.get_orders(user_id, skip, limit)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, current_user=Depends(get_current_user)):
    # Admin/staff can see any order, customers only see their own
    user_id = None if current_user["role"] in ["admin", "staff"] else str(current_user["_id"])
    order = await order_service.get_order_by_id(order_id, user_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order

@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: str,
    status_update: OrderStatusUpdate,
    _=Depends(check_permissions(["admin", "staff"]))
):
    order = await order_service.update_order_status(order_id, status_update.status)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order
