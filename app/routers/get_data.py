from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database_tools.database import AsyncSessionLocal, Folder, get_db, commit_or_rollback, Photo
from typing import Any
from app.database_tools.schemas import FolderGet
from fastapi import HTTPException, Query

router = APIRouter(prefix="/api", tags=["Get Folders & Photos"])

@router.get("/user/{user_id}/folders")
async def get_folders(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Folder).filter(Folder.folder_user_id == user_id))
    folders = result.scalars().all()
    
    if not folders:
        return []
        
    return [
        {
            "id": f.folder_id,
            "name": f.folder_name,
            "user_id": f.folder_user_id
        }
        for f in folders
    ]

@router.get("/folders/{folder_id}/photos")
async def get_folder_photos(folder_id: int, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(Photo).filter(Photo.folder_id == folder_id))
    photos = result.scalars().all()

    if not photos:
        return []  

    return [
        {
            "id": p.photo_id,
            "name": p.file_path.split("/")[-1] if p.file_path else "unknown", 
            "url": p.file_path,            
            "created_at": p.created_at
        } 
        for p in photos
    ]

@router.get("/folder/{folder_id}")
async def get_folder(
    folder_id: int, 
    user_id: int = Query(..., description="Қолданушының ID-і"), 
    db: AsyncSession = Depends(get_db)
) -> Any:
    folder = await db.get(Folder, folder_id)
        
    if not folder:
        raise HTTPException(status_code=404, detail="Папка не найдена!")
            
    if folder.folder_user_id != user_id:
        raise HTTPException(status_code=403, detail="У вас нет прав на просмотр этой папки!")

    return {
        "status": "success",
        "folder_id": folder.folder_id,
        "folder_name": folder.folder_name,
        "folder_user_id": folder.folder_user_id
    }
    
