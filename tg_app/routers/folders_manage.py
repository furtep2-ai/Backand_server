from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database_tools.database import AsyncSessionLocal
from typing import Any
from app.database_tools.schemas import FolderGet, FolderUpdate
from app.database_tools.database import Folder, get_db, commit_or_rollback

router = APIRouter(prefix="/api", tags=["Folders Manage"])

@router.put("/folders/{folder_id}")
async def change_folder(folder_id: int, folder_data: FolderUpdate, db: AsyncSession = Depends(get_db)) -> Any:
    folder = await db.get(Folder, folder_id)
    
    if not folder:
        raise HTTPException(status_code=404, detail="Папка не найдена!")
        
    if folder.folder_user_id != folder_data.user_id:
        raise HTTPException(status_code=403, detail="У вас нет прав на изменение этой папки!")

    folder.folder_name = folder_data.new_folder_name
    
    await commit_or_rollback(db)
    await db.refresh(folder)
    
    return {
        "status": "success",
        "message": "Название папки успешно изменено!",
        "folder_id": folder.folder_id,
        "new_folder_name": folder.folder_name
    }

@router.delete("/folders/{folder_id}")
async def delete_folder(folder_id: int, folder_data: FolderGet, db: AsyncSession = Depends(get_db)) -> Any:
    folder = await db.get(Folder, folder_id)
        
    if not folder:
        raise HTTPException(status_code=404, detail="Папка не найдена!")
            
    if folder.folder_user_id != folder_data.user_id:
        raise HTTPException(status_code=403, detail="У вас нет прав на изменение этой папки!")

    await db.delete(folder)
    await commit_or_rollback(db)
        
    return {
        "status": "success",
        "message": f"Папка успешно удалена!",
    }
