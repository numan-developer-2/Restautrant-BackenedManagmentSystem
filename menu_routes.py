from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from ..models.menu import MenuCreate, MenuUpdate, MenuResponse
from ..services import menu_service
from ..auth.auth import get_current_user, check_permissions

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.post("/", response_model=MenuResponse)
async def create_menu_item(
    menu_item: MenuCreate,
    _=Depends(check_permissions(["admin", "staff"]))
):
    return await menu_service.create_menu_item(menu_item)

@router.get("/", response_model=List[MenuResponse])
async def get_menu_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    available_only: bool = False
):
    return await menu_service.get_menu_items(skip, limit, category, available_only)

@router.get("/{menu_id}", response_model=MenuResponse)
async def get_menu_item(menu_id: str):
    menu_item = await menu_service.get_menu_item_by_id(menu_id)
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    return menu_item

@router.put("/{menu_id}", response_model=MenuResponse)
async def update_menu_item(
    menu_id: str,
    menu_update: MenuUpdate,
    _=Depends(check_permissions(["admin", "staff"]))
):
    menu_item = await menu_service.update_menu_item(menu_id, menu_update)
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    return menu_item

@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_item(
    menu_id: str,
    _=Depends(check_permissions(["admin", "staff"]))
):
    success = await menu_service.delete_menu_item(menu_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
