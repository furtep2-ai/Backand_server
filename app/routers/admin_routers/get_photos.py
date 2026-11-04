from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database_tools.database import AsyncSessionLocal, User, Photo
from typing import Any
from app.database_tools.database import Folder, get_db, commit_or_rollback
from app.routers.admin_routers.all_users import get_current_admin_user

router = APIRouter(prefix="/api/admin",tags=["Admin"])

@router.get("/photos")
async def get_all_photos(
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Photo)
    )

    photos = result.scalars().all()

    return {
        "status": "success",
        "count": len(photos),
        "photos": [
            {
                "photo_id": photo.photo_id,
                "folder_id": photo.folder_id,
                "file_id": photo.file_id,
                "file_path": photo.file_path
            }
            for photo in photos
        ]
    }

@router.get("/photos/{photo_id}")
async def get_photo_by_id(
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

    return {
        "status": "success",
        "photo": {
            "photo_id": photo.photo_id,
            "folder_id": photo.folder_id,
            "file_id": photo.file_id,
            "file_path": photo.file_path,
            "created_at": photo.created_at
        }
    }

@router.get("/users/{user_id}/photos")
async def get_user_photos(
    user_id: int,
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден!"
        )

    result = await db.execute(
        select(Photo)
        .join(Folder, Folder.folder_id == Photo.folder_id)
        .where(Folder.folder_user_id == user_id)
    )

    photos = result.scalars().all()

    return {
        "status": "success",
        "user_id": user_id,
        "photos_count": len(photos),
        "photos": [
            {
                "photo_id": photo.photo_id,
                "folder_id": photo.folder_id,
                "file_path": photo.file_path,
                "created_at": photo.created_at
            }
            for photo in photos
        ]
    }
