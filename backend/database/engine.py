import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import event
from config import get_settings

settings = get_settings()

def _resolve_database_url(url: str) -> str:
    if url.startswith("sqlite+aiosqlite:///./"):
        relative = url.replace("sqlite+aiosqlite:///./", "")
        # base_dir = pasta backend/ (pai de database/)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        absolute = os.path.join(base_dir, relative)
        return f"sqlite+aiosqlite:///{absolute}"
    return url

_database_url = _resolve_database_url(settings.database_url)

connect_args = {"check_same_thread": False} if settings.is_sqlite else {}

engine = create_async_engine(
    _database_url,
    connect_args=connect_args,
    echo=settings.env == "development",
)

if settings.is_sqlite:
    @event.listens_for(engine.sync_engine, "connect")
    def set_sqlite_pragmas(dbapi_conn, _):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)