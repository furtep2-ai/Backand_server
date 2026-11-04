from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database_tools.database import AsyncSessionLocal, User, Photo
from typing import Any
from app.database_tools.database import Folder, get_db, commit_or_rollback
from app.routers.admin_routers.all_users import get_current_admin_user

router = APIRouter(prefix="/api/admin",tags=["Admin"])

@router.delete("/photos/{photo_id}")
async def admin_delete_photo(
    photo_id: int,
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    photo = await db.get(Photo, photo_id)

    if not photo:
        raise HTTPException(
            status_code=404,
            detail="Фото не найдено!"
        )

    await db.delete(photo)

    await commit_or_rollback(db)

    return {
        "status": "success",
        "message": "Фото удалено администратором",
        "photo_id": photo_id
    }