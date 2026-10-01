from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

engine = create_async_engine(url=settings.DB_URL)

class Base(DeclarativeBase):
    pass

sessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with sessionLocal() as db:
        yield db
