from sqlalchemy import BigInteger, String, Boolean, Integer, ForeignKey, Text, DateTime
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import os
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column , relationship
from typing import List
from fastapi import HTTPException
import datetime
load_dotenv()

import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"ssl": ssl_context},
    pool_pre_ping=True,
    pool_recycle=3600,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def commit_or_rollback(db: AsyncSession):
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Деректер қорымен жұмыс кезінде қате орын алды: {str(e)}"
        )

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=0)
    time_zone: Mapped[str] = mapped_column(String(50), default="Asia/Almaty")

    folders: Mapped[list["Folder"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Folder(Base):
    __tablename__ = "folders"
    folder_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    folder_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    folder_name: Mapped[str] = mapped_column(String(255), nullable=False)

    user: Mapped["User"] = relationship(back_populates="folders")
    photos: Mapped[list["Photo"]] = relationship(back_populates="folder", cascade="all, delete-orphan")

class Photo(Base):
    __tablename__ = "photos"

    photo_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    folder_id: Mapped[int] = mapped_column(ForeignKey("folders.folder_id"))
    file_id: Mapped[str] = mapped_column(String(255), nullable=False)   
    file_path: Mapped[str] = mapped_column(String(255), unique=True, nullable=False) 
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    folder: Mapped["Folder"] = relationship(back_populates="photos")

