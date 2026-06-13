import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database.engine import Base, get_db
from app import app

TEST_DB = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(TEST_DB, connect_args={"check_same_thread": False})
SessionTest = async_sessionmaker(engine_test, expire_on_commit=False, autoflush=False)


async def override_get_db():
    async with SessionTest() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest_asyncio.fixture
async def db_session():
    async with SessionTest() as session:
        yield session
