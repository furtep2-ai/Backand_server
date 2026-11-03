from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database_tools.jwt_token import get_current_user
from typing import Any
from app.database_tools.database import Photo, get_db, commit_or_rollback, User, Folder

router = APIRouter(prefix="/api", tags=["Photos & Folders Manage"])

@router.delete("/photos/{photo_id}")
async def delete_photo(
    photo_id: int, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
) -> Any:
    photo = await db.get(Photo, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Фото не найдено!")
        
    folder = await db.get(Folder, photo.folder_id)
    if not folder or folder.folder_user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="У вас нет прав на удаление этого фото!")
        
    await db.delete(photo)
    await commit_or_rollback(db)
    
    return {
        "status": "success",
        "message": "Фото успешно удалено!",
        "photo_id": photo_id
    }

@router.get("/photos/{photo_id}")
async def get_photo(
    photo_id: int, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
) -> Any:
    photo = await db.get(Photo, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Фото не найдено!")
        
    folder = await db.get(Folder, photo.folder_id)
    if not folder or folder.folder_user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="У вас нет прав на просмотр этого фото!")

    return {
        "status": "success",
        "photo_id": photo.photo_id,
        "folder_id": photo.folder_id,
        "file_id": photo.file_id,
        "file_path": photo.file_path
    }

