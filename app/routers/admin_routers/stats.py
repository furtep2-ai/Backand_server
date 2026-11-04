from app.database_tools.database import Folder, get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database_tools.database import AsyncSessionLocal, User, Photo
from typing import Any
from app.routers.admin_routers.all_users import get_current_admin_user
from sqlalchemy import select, func

router = APIRouter(prefix="/api/admin",tags=["Admin"])


@router.get("/users/{user_id}/stats")
async def get_user_stats(
    user_id: int,
    #admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден!"
        )

    folders_count = await db.scalar(
        select(func.count(Folder.folder_id))
        .where(Folder.folder_user_id == user_id)
    )

    photos_count = await db.scalar(
        select(func.count(Photo.photo_id))
        .join(Folder, Folder.folder_id == Photo.folder_id)
        .where(Folder.folder_user_id == user_id)
    )

    return {
        "status": "success",
        "user_id": user.user_id,
        "user_name": user.user_name,
        "folders_count": folders_count,
        "photos_count": photos_count,
        "is_admin": user.is_admin
    }