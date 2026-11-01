import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database_tools.database import Base, get_db, User, Folder
import asyncio
import random

engine = create_async_engine("sqlite+aiosqlite:///:memory:")
TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest.fixture(scope="session")
def db_session_factory():
    return TestingSessionLocal

@pytest.fixture(autouse=True)
async def setup_db():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    async with TestingSessionLocal() as session:
        random_id = random.randint(1000, 99999)
        user = User(user_id = 1, user_name = "new_user", is_admin = False, time_zone = "Asia/Almaty")
        session.add(user)
        await session.commit()

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c