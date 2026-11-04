from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers.get_data import router as get_data_router
from app.routers.insert_data import router as insert_folder_router
from app.routers.registration_login import router as login_router
from app.routers.folders_manage import router as folder_manage_router
from app.routers.photos_manage import router as photo_manage_router
from app.routers.admin_routers.all_users import router as all_users_router
from app.routers.admin_routers.get_folders import router as get_folders_router
from app.routers.admin_routers.get_user import router as get_user_router
from app.routers.admin_routers.remove_admin import router as remove_admin_router
from app.routers.admin_routers.make_admin import router as make_admin_router
from app.routers.admin_routers.delete_folders import router as delete_folders_router
from app.routers.admin_routers.delete_photo import router as delete_photo_router
from app.routers.admin_routers.get_photos import router as get_photos_router
from app.routers.admin_routers.stats import router as stats_router
from app.routers.admin_routers.delete_user import router as delete_user_router
import cloudinary
from dotenv import load_dotenv
import os
load_dotenv()

cloudinary.config( 
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"), 
    api_key=os.getenv("CLOUDINARY_API_KEY"), 
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

router = APIRouter(prefix="/api", tags=["Photos"])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "FastAPI бэкенды сәтті жұмыс істеп тұр!"}
from app.database_tools.database import engine, Base

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(get_data_router)
app.include_router(insert_folder_router)
app.include_router(login_router)
app.include_router(folder_manage_router)
app.include_router(photo_manage_router)
app.include_router(all_users_router)
app.include_router(remove_admin_router)
app.include_router(make_admin_router)
app.include_router(delete_folders_router)
app.include_router(delete_photo_router)
app.include_router(get_photos_router)
app.include_router(get_user_router)
app.include_router(get_folders_router)
app.include_router(stats_router)
app.include_router(delete_user_router)