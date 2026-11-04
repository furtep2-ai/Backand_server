from app.database_tools.database import Folder, get_db, commit_or_rollback
from app.database_tools.jwt_token import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database_tools.database import AsyncSessionLocal, User
from typing import Any
from app.routers.admin_routers.all_users import get_current_admin_user

router = APIRouter(prefix="/api/admin",tags=["Admin"])

@router.delete("/users/{user_id}")
async def delete_user(
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

    if user.user_id == admin.user_id:
        raise HTTPException(
            status_code=400,
            detail="Вы не можете удалить сами себя!"
        )

    await db.delete(user)

    await commit_or_rollback(db)

    return {
        "status": "success",
        "message": "Пользователь удален",
        "user_id": user_id
    }