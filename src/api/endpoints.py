from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.services import create_zapis, get_schedule, delete_zapis
from src.services import CreateZapisForm, GetScheduleForm, DeleteZapisForm
from src.db.postgres import get_session
from src.db.models import Zapis, Stomatology
from src.db.queries import get_auth_token

router = APIRouter(tags=["Schedule"])


@router.get(
    "/{stomatology}/get",
    summary="Получение свободных мест по дате"
)
async def get_entries(
        stomatology: str = Path(example="adilstom"),
        date: str = "30.11.2024",
        session: AsyncSession = Depends(get_session)
):
    token = await get_auth_token(stomatology, session)

    try:
        data = GetScheduleForm(start=date, end=date).model_dump()
        response = await get_schedule(token=token, params=data)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/{stomatology}/create",
    summary="Сделать запись"
)
async def create_entry(
        form_data: CreateZapisForm,
        stomatology: str = Path(example="adilstom"),
        session: AsyncSession = Depends(get_session)
):
    token = await get_auth_token(stomatology, session)
    try:
        form_dict = form_data.model_dump()
        response = await create_zapis(token=token, payload=form_dict)
        if error := response.get("error"):
            raise HTTPException(status_code=400, detail=error)
        zapis_id = response.get("status")
        zapis = Zapis(
            phone=form_dict["phone"],
            date=form_dict["day"],
            zapis_id=zapis_id
        )
        session.add(zapis)
        await session.commit()
        return {"message": f"Запись успешно создана. ID записи: {zapis_id}"}
    except ValueError as e:

        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/{stomatology}/delete",
    summary="Отмена записи"
)
async def cancel_entry(
        form_data: DeleteZapisForm,
        stomatology: str = Path(example="adilstom"),
        session: AsyncSession = Depends(get_session)
):
    token = await get_auth_token(stomatology, session)
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
