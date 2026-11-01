from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database_tools.database import AsyncSessionLocal
from typing import Any
from app.database_tools.schemas import FolderCreate, PhotoCreate, VideoCreate
from app.database_tools.database import Photo, get_db, commit_or_rollback

router = APIRouter(prefix="/api", tags=["Photos & Folders Manage"])

@router.delete("/photos/{photo_id}")
async def delete_photo(photo_id: int, db: AsyncSession = Depends(get_db)) -> Any:
    photo = await db.get(Photo, photo_id)
    
    if not photo:
        raise HTTPException(status_code=404, detail="Фото не найдено!")
        
    await db.delete(photo)
    await commit_or_rollback(db)
    
    return {
        "status": "success",
        "message": "Фото успешно удалено!",
        "photo_id": photo_id
    }

@router.get("/photos/{photo_id}")
async def get_photo(photo_id: int, db: AsyncSession = Depends(get_db)) -> Any:
    photo = await db.get(Photo, photo_id)
        
    if not photo:
        raise HTTPException(status_code=404, detail="Фото не найдено!")

    return {
        "status": "success",
        "photo_id": photo.photo_id,
        "folder_id": photo.folder_id,
        "file_id": photo.file_id,
        "file_path": photo.file_path
    }

