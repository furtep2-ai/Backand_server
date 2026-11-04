from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database_tools.database import AsyncSessionLocal, User, Photo, Folder
from typing import Any
from app.database_tools.database import Folder, get_db, commit_or_rollback
from app.routers.admin_routers.all_users import get_current_admin_user

router = APIRouter(prefix="/api/admin",tags=["Admin"])

@router.delete("/folders/{folder_id}")
async def admin_delete_folder(
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

    await db.delete(folder)
    await commit_or_rollback(db)

    return {
        "status": "success",
        "message": "Папка удалена администратором",
        "folder_id": folder_id
    }