from pydantic import BaseModel

class FolderCreate(BaseModel):
    name: str
    user_id: int

class PhotoCreate(BaseModel):
    file_url: str
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
    user_id: int
    new_folder_name: str

class TimezoneNew(BaseModel):
    new_time_zone: str


