from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Integer
from sqlalchemy.future import select

DATABASE_URL = "sqlite+aiosqlite:///./zapis.db"
engine = create_async_engine(DATABASE_URL, echo=False)

LocalSession = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


class Zapis(Base):
    __tablename__ = "zapis"

    phone: Mapped[str] = mapped_column(String, primary_key=True)
    date: Mapped[str] = mapped_column(String, primary_key=True)
    zapis_id: Mapped[int] = mapped_column(Integer)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def insert_zapis(phone: str, date: str, zapis_id: int) -> None:
    async with LocalSession() as session:
        zapis = Zapis(phone=phone, date=date, zapis_id=zapis_id)
        session.add(zapis)
        await session.commit()


async def get_zapis(phone: str, date: str) -> Zapis:
    async with LocalSession() as session:
        stmt = select(Zapis).where(Zapis.phone == phone, Zapis.date == date)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def main():
    await init_db()

    zapis = await get_zapis("+7(777)777-77-77", "2024.12.06")
    if zapis:
        print(f"User ID: {zapis.zapis_id}")
    else:
        print("User not found.")

