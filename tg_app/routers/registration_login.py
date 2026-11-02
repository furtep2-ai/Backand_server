from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database_tools.database import AsyncSessionLocal
from typing import Any
from app.database_tools.schemas import Registartion, TimezoneNew
from app.database_tools.database import User, get_db, commit_or_rollback

router = APIRouter(prefix="/api", tags=["Registration & Login"])

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

@router.get("/user/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> Any:
    user = await db.get(User, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
        
    return {
        "status": "success",
        "user_id": user.user_id,
        "user_name": user.user_name,
        "time_zone": user.time_zone,
        "is_admin": user.is_admin
    }

@router.put("/user/{user_id}/timezone")
async def change_timezone(user_id: int, timezone_data: TimezoneNew, db: AsyncSession = Depends(get_db)) -> Any:
    user = await db.get(User, user_id)
        
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")

    user.time_zone = timezone_data.new_time_zone 
    
    await commit_or_rollback(db)
    await db.refresh(user)
    
    return {
        "status": "success",
        "message": "Успешно изменено!",
        "user_id": user_id,
        "time_zone": user.time_zone
    }

@router.delete("/user/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> Any:
    user = await db.get(User, user_id)
        
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")

    await db.delete(user)
    await commit_or_rollback(db)
    
    return {
        "status": "success",
        "message": f"Пользователь с ID {user_id} успешно удален!",
        "user_id": user_id
    }
    
