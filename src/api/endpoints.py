from fastapi import APIRouter, HTTPException
from src.services import create_zapis, get_schedule, delete_zapis
from src.services import CreateZapisForm, GetScheduleForm, DeleteZapisForm
from src.db import insert_zapis, get_zapis


router = APIRouter(tags=["Schedule"])


@router.get(
    "/get",
    summary="Получение свободных мест по дате"
)
async def get_entries(date: str = "30.11.2024"):
    try:
        data = GetScheduleForm(start=date, end=date).model_dump()
        response = await get_schedule(params=data)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/create",
    summary="Сделать запись"
)
async def create_entry(form_data: CreateZapisForm):
    try:
        form_dict = form_data.model_dump()
        response = await create_zapis(form_dict)
        if error := response.get("error"):
            raise HTTPException(status_code=400, detail=error)
        zapis_id = response.get("status")
        await insert_zapis(phone=form_dict["phone"], date=form_dict["day"], zapis_id=zapis_id)
        return {"message": f"Запись успешно создана. ID записи: {zapis_id}"}
    except ValueError as e:

        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/delete",
    summary="Отмена записи"
)
async def cancel_entry(form_data: DeleteZapisForm):
    form_dict = form_data.model_dump()
    zapis = await get_zapis(phone=form_dict["phone"], date=form_dict["date"])
    if zapis:
        response = await delete_zapis(zapis.zapis_id)
        return response
    raise HTTPException(status_code=400, detail=f"Нет записи с номером {form_dict["phone"]} на дату {form_dict["date"]}")
