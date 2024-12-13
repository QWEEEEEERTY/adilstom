# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
# from sqlalchemy.future import select
# from sqlalchemy.orm import declarative_base
#
# from src.db.models import Zapis
# from src.config import SQLITE_URL
#
#
# engine = create_async_engine(SQLITE_URL, echo=False)
#
# LocalSession = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
# Base = declarative_base()
#
#
# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#
# async def insert_zapis(phone: str, date: str, zapis_id: int) -> None:
#     async with LocalSession() as session:
#         zapis = Zapis(phone=phone, date=date, zapis_id=zapis_id)
#         session.add(zapis)
#         await session.commit()
#
#
# async def get_zapis(phone: str, date: str) -> Zapis:
#     async with LocalSession() as session:
#         stmt = select(Zapis).where(Zapis.phone == phone, Zapis.date == date)
#         result = await session.execute(stmt)
#         return result.scalar_one_or_none()
