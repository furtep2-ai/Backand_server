from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tg_app.routers.get_data import router as get_data_router
from tg_app.routers.insert_data import router as insert_folder_router
from tg_app.routers.registration_login import router as login_router
from tg_app.routers.folders_manage import router as folder_manage_router
from tg_app.routers.photos_manage import router as photo_manage_router
from tg_app.database_tools.database import AsyncSession, AsyncSessionLocal

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
from tg_app.database_tools.database import engine, Base

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(get_data_router)
app.include_router(insert_folder_router)
app.include_router(login_router)
app.include_router(folder_manage_router)
app.include_router(photo_manage_router)