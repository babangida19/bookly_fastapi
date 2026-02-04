from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
# async_engine = AsyncEngine(
#     create_engine(
#     url= Config.DATABASE_URL,
#     echo= True
# ))

async_engine = create_async_engine(
    Config.DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)
async def init_db():
    async with async_engine.begin() as conn:
        from src.books.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session

# async def get_session() -> AsyncSession:
#     Session = sessionmaker(
#         bind=async_engine,
#         class_= AsyncSession,
#         expire_on_commit=False
#     )

#     async with Session() as session:
#         yield session

# from sqlmodel import SQLModel
# from sqlmodel.ext.asyncio.session import AsyncSession
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.orm import sessionmaker
# from src.config import Config

# # ✅ Create async engine (THIS is the big fix)
# engine = create_async_engine(
#     Config.DATABASE_URL,
#     echo=True,
# )

# # ✅ Create tables
# async def init_db():
#     async with engine.begin() as conn:
#         from src.books.models import Book
#         await conn.run_sync(SQLModel.metadata.create_all)

# # ✅ Dependency to get DB session
# async_session = sessionmaker(
#     engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )

# async def get_session():
#     async with async_session() as session:
#         yield session
