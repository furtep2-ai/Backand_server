from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database_tools.database import AsyncSessionLocal, User, Photo, Folder
from typing import Any
from app.database_tools.database import Folder, get_db, commit_or_rollback
from app.routers.admin_routers.all_users import get_current_admin_user

router = APIRouter(prefix="/api/admin",tags=["Admin"])

@router.get("/folders")
async def get_all_folders(
    #admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Folder)
    )

    folders = result.scalars().all()

    return {
        "status": "success",
        "count": len(folders),
        "folders": [
            {
                "folder_id": folder.folder_id,
                "folder_name": folder.folder_name,
                "folder_user_id": folder.folder_user_id
            }
            for folder in folders
        ]
    }

@router.get("/folders/{folder_id}")
async def get_folder_by_id(
    folder_id: int,
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    folder = await db.get(Folder, folder_id)

    if not folder:
        raise HTTPException(
            status_code=404,
            detail="Папка не найдена!"
        )

    return {
        "status": "success",
        "folder": {
            "folder_id": folder.folder_id,
            "folder_name": folder.folder_name,
            "folder_user_id": folder.folder_user_id
        }
    }

@router.get("/folders/{folder_id}/photos")
async def get_folder_photos(
    folder_id: int,
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    folder = await db.get(Folder, folder_id)

    if not folder:
        raise HTTPException(
            status_code=404,
            detail="Папка не найдена!"
        )

    result = await db.execute(
        select(Photo).where(
            Photo.folder_id == folder_id
        )
    )

    photos = result.scalars().all()

    return {
        "status": "success",
        "folder_id": folder_id,
        "photos_count": len(photos),
        "photos": [
            {
                "photo_id": photo.photo_id,
                "file_path": photo.file_path,
                "file_id": photo.file_id,
                "created_at": photo.created_at
            }
            for photo in photos
        ]
    }