from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database_tools.database import AsyncSessionLocal
from typing import Any
from app.database_tools.schemas import FolderCreate, PhotoCreate
from app.database_tools.database import Photo, Folder, get_db, commit_or_rollback

router = APIRouter(prefix="/api", tags=["Photos & Folders"])

@router.post("/folders")
async def create_folder(folder_data: FolderCreate, db: AsyncSession = Depends(get_db)) -> Any:
    new_folder = Folder(folder_name=folder_data.name, folder_user_id=folder_data.user_id)
    db.add(new_folder)
    await commit_or_rollback(db)
    await db.refresh(new_folder)
    return {"message": "Папка успешно создана!", "folder_id": new_folder.folder_id}

@router.post("/photos")
async def add_photo(photo_data: PhotoCreate, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(Folder).filter(Folder.folder_id == photo_data.folder_id))
    folder = result.scalars().first()
    if not folder:
        raise HTTPException(status_code=404, detail="Папка табылмады!")

    new_photo = Photo(
        file_id=photo_data.file_url, 
        file_path=photo_data.file_url,
        folder_id=photo_data.folder_id
    )
    db.add(new_photo)
    await commit_or_rollback(db)
    await db.refresh(new_photo)
    return {"message": "Фото успешно добавлено!", "photo_id": new_photo.photo_id}







