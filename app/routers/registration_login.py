from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database_tools.jwt_token import create_access_token, get_current_user
from typing import Any
from app.database_tools.schemas import Registartion, TimezoneNew, LoginSchema
from app.database_tools.database import User, get_db, commit_or_rollback

router = APIRouter(prefix="/api", tags=["Registration & Login"])

@router.post("/login")
async def login(user_data: LoginSchema, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    access_token = await create_access_token(data={"sub": str(user.user_id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

    
@router.post("/user/{user_id}")
async def add_user(user_id: int, user_data: Registartion, db: AsyncSession = Depends(get_db)) -> Any:
    existing_user = await db.get(User, user_id)
    if existing_user:
        return {
            "status": "exists",
            "message": "Пользователь уже зарегистрирован!",
            "user_id": user_id
        }
    
    new_user = User(
        user_id=user_id,
        user_name=user_data.user_name,
        time_zone=user_data.time_zone,
        is_admin=user_data.is_admin  
    )
    
    db.add(new_user)
    await commit_or_rollback(db)
    await db.refresh(new_user)
    
    return {
        "status": "success",
        "message": "Пользователь успешно зарегистрирован!",
        "user_id": new_user.user_id
    }

@router.get("/users/me")
async def get_my_profile(
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
) -> Any:
    return {
        "status": "success",
        "user_id": current_user.user_id,
        "user_name": current_user.user_name,
        "time_zone": current_user.time_zone,
        "is_admin": current_user.is_admin
    }

@router.put("/users/timezone")
async def change_my_timezone(
    timezone_data: TimezoneNew, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
) -> Any:
    # Токен арқылы кірген қолданушының таймзонасын өзгертеміз
    current_user.time_zone = timezone_data.new_time_zone 
    
    await commit_or_rollback(db)
    await db.refresh(current_user)
    
    return {
        "status": "success",
        "message": "Успешно изменено!",
        "user_id": current_user.user_id,
        "time_zone": current_user.time_zone
    }

@router.delete("/users/me")
async def delete_my_account(
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
) -> Any:
    await db.delete(current_user)
    await commit_or_rollback(db)
    
    return {
        "status": "success",
        "message": f"Ваш аккаунт (ID: {current_user.user_id}) успешно удален!",
    }
    
