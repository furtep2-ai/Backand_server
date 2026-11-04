from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database_tools.database import AsyncSessionLocal, User
from typing import Any
from app.database_tools.database import Folder, get_db, commit_or_rollback
from app.database_tools.jwt_token import get_current_user
from app.database_tools.schemas import UserResponse, UsersResponse

router = APIRouter(prefix="/api/admin",tags=["Admin"])

async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Бұл әрекетті тек администратор ғана жасай алады!"
        )
    return current_user



@router.get("/users", response_model=UsersResponse)
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user) 
) -> UsersResponse:
    result = await db.execute(select(User))
    users = result.scalars().all()
    
    return {
        "status": "success",
        "users": users
    }
