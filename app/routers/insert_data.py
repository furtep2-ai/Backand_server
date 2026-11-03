from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database_tools.jwt_token import get_current_user
from typing import Any
from app.database_tools.schemas import FolderCreate
from app.database_tools.database import Photo, Folder, get_db, commit_or_rollback, User
import cloudinary.uploader
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from sqlalchemy import select

router = APIRouter(prefix="/api", tags=["Photos & Folders"])

@router.post("/folders")
async def create_folder(
    folder_data: FolderCreate, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
) -> Any:
    new_folder = Folder(
        folder_name=folder_data.name, 
        folder_user_id=current_user.user_id
    )
    db.add(new_folder)
    await commit_or_rollback(db)
    await db.refresh(new_folder)
    
    return {
        "message": "Папка успешно создана!", 
        "folder_id": new_folder.folder_id
    }



@router.post("/photos")
async def add_photo(
    folder_id: int = Form(...),
    file: UploadFile = File(...), 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
) -> Any:
    result = await db.execute(
        select(Folder).filter(
            Folder.folder_id == folder_id, 
            Folder.folder_user_id == current_user.user_id
        )
    )
    folder = result.scalars().first()
    if not folder:
        raise HTTPException(status_code=404, detail="Папка табылмады немесе сізде бұл папкаға құқық жоқ!")

    try:
        upload_result = cloudinary.uploader.upload(file.file)
        cloudinary_url = upload_result.get("secure_url") 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary жүктеу қатесі: {str(e)}")

    new_photo = Photo(
        file_id=cloudinary_url, 
        file_path=cloudinary_url, 
        folder_id=folder_id
    )
    db.add(new_photo)
    await commit_or_rollback(db)
    await db.refresh(new_photo)
    
    return {
        "message": "Фото успешно добавлено в Cloudinary!", 
        "photo_id": new_photo.photo_id,
        "image_url": cloudinary_url
    }







