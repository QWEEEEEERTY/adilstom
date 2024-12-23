from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, insert, text, func
from fastapi import HTTPException
import datetime

from .models import Stomatology, Zapis
from src.services.forms import CreateZapisForm, TransferZapisForm


async def get_auth_token(stomatology: str, session: AsyncSession) -> str:
    stmt = select(Stomatology).where(Stomatology.name == stomatology)
    result = await session.execute(stmt)
    stomatology = result.scalar_one_or_none()
    if stomatology:
        return stomatology.token
    raise HTTPException(status_code=400, detail="Стоматология с таким именем не найдена!")


async def insert_zapis(session: AsyncSession, stomatology: str, zapis_id: int, zapis: CreateZapisForm) -> None:
    date = datetime.datetime.strptime(zapis.day, "%d.%m.%Y").date()
    time = datetime.time(zapis.startHour, zapis.startMinute)

    model = Zapis(
        stomatology=stomatology,
        zapis_id=zapis_id,
        phone=zapis.phone,
        date=date,
        time=time,
        doctor_id=zapis.doctor,
        patient_name=zapis.patientName,
        comment=zapis.comment,
        zhaloba=zapis.zhaloba
    )
    session.add(model)
    await session.commit()


async def get_last_zapis(session: AsyncSession, stomatology: str, phone: str) -> (str, CreateZapisForm):
    stmt = (
        select(Zapis)
        .where(Zapis.phone == phone, Zapis.stomatology == stomatology)
        .order_by(Zapis.created_at.desc()).limit(1)
    )
    result = await session.execute(stmt)
    zapis = result.scalar_one_or_none()
    if zapis:
        return zapis.zapis_id, CreateZapisForm(
            phone=phone,
            day=zapis.date.strftime("%d.%m.%Y"),
            startHour=zapis.time.hour,
            startMinute=zapis.time.minute,
            doctor=zapis.doctor_id,
            patientName=zapis.patient_name,
            comment=zapis.comment,
            zhaloba=zapis.zhaloba
        )
    raise HTTPException(status_code=400, detail="Не удалось найти запись с данным номером")


async def deactivate_zapis(session: AsyncSession, zapis_id: int):
    stmt = (
        update(Zapis)
        .where(Zapis.zapis_id == zapis_id)
        .values(is_active=False)
    )
    await session.execute(stmt)
    await session.commit()




