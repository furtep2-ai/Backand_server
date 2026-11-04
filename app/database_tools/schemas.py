from pydantic import BaseModel, config, ConfigDict
from typing import Literal


class FolderCreate(BaseModel):
    name: str

class PhotoCreate(BaseModel):
    folder_id: int

class FolderResponse(BaseModel):
    id: int
    name: str
    telegram_id: str

    class Config:
        from_attributes = True


class PhotoResponse(BaseModel):
    id: int
    file_url: str
    folder_id: int

    class Config:
        from_attributes = True

class Registartion(BaseModel):
    user_name: str
    is_admin: bool
    time_zone: str = "Asia/Almaty"

class VideoCreate(BaseModel):
    folder_id: int
    file_id: str      
    file_path: str

class FolderGet(BaseModel):
    folder_id: int
    user_id: int

class FolderUpdate(BaseModel):
    new_folder_name: str

class TimezoneNew(BaseModel):
    new_time_zone: str

class LoginSchema(BaseModel):
    user_id: int

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    user_name: str
    is_admin: bool
    time_zone: str

class UsersResponse(BaseModel):
    status: Literal["success"]
    users: list[UserResponse]



