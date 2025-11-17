from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fast_api.core.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)


async def create_session():
    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        yield session
