from pydantic import BaseModel

# 1. Жаңа папка құру үшін клиенттен келетін деректер
class FolderCreate(BaseModel):
    name: str
    user_id: int

# 2. Папкаға жаңа фото қосу үшін клиенттен келетін деректер
class PhotoCreate(BaseModel):
    file_url: str
    folder_id: int

# 3. Базадан папканы қайтарған кездегі формат (Response)
class FolderResponse(BaseModel):
    id: int
    name: str
    telegram_id: str

    class Config:
        from_attributes = True

# 4. Базадан фотоны қайтарған кездегі формат (Response)
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
    user_id: int
    new_folder_name: str

class TimezoneNew(BaseModel):
    new_time_zone: str


