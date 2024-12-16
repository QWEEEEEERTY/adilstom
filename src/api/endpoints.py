from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.services import create_zapis, get_schedule, delete_zapis
from src.services import CreateZapisForm, GetScheduleForm, DeleteZapisForm, TransferZapisForm
from src.db.postgres import get_session
from src.db.models import Zapis

from src.api.dependencies import token_dependency


router = APIRouter(tags=["Schedule"])


@router.get("/{stomatology}/get", summary="Получение свободных мест по дате")
async def get_entries(
        date: str = "30.11.2024",
        token: str = Depends(token_dependency)
):
    try:
        data = GetScheduleForm(start=date, end=date).model_dump()
        response = await get_schedule(token=token, params=data)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{stomatology}/create", summary="Сделать запись")
async def create_entry(
        form_data: CreateZapisForm,
        session: AsyncSession = Depends(get_session),
        token: str = Depends(token_dependency)
):
    try:
        form_dict = form_data.model_dump()
        response = await create_zapis(token=token, payload=form_dict)
        zapis = Zapis(phone=form_dict["phone"], date=form_dict["day"], zapis_id=response["status"])
        session.add(zapis)
        await session.commit()
        return {"message": f"Запись успешно создана. ID записи: {zapis.zapis_id}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{stomatology}/delete", summary="Отмена записи")
async def cancel_entry(
        form_data: DeleteZapisForm,
        session: AsyncSession = Depends(get_session),
        token: str = Depends(token_dependency)
):
    form_dict = form_data.model_dump()
    stmt = select(Zapis).where(
        Zapis.phone == form_dict["phone"],
        Zapis.date == form_dict["date"]
    )
    result = await session.execute(stmt)
    zapis = result.scalar_one_or_none()
    if zapis:
        response = await delete_zapis(token=token, zapis_id=zapis.zapis_id)
        return response
    raise HTTPException(
        status_code=400,
        detail=f"Нет записи с номером {form_dict["phone"]} на дату {form_dict["date"]}"
    )


@router.post("/{stomatology}/transfer", summary="Перенос записи")
async def transfer_entry(
        form_data: TransferZapisForm,
        session: AsyncSession = Depends(get_session),
        token: str = Depends(token_dependency)
):
    return token
