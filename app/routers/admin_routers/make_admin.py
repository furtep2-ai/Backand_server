from app.database_tools.database import Folder, get_db, commit_or_rollback
from app.database_tools.jwt_token import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database_tools.database import User
from typing import Any
from app.routers.admin_routers.all_users import get_current_admin_user

router = APIRouter(prefix="/api/admin",tags=["Admin"])

@router.patch("/users/{user_id}/make-admin")
async def make_admin(
    user_id: int,
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_admin = True

    await commit_or_rollback(db)
    await db.refresh(user)

    return {
        "status": "success",
        "message": "User became admin",
        "user_id": user.user_id,
        "is_admin": user.is_admin
    }