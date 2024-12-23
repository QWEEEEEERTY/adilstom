from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.services import create_zapis, get_schedule, delete_zapis
from src.services import CreateZapisForm, GetScheduleForm, DeleteZapisForm, TransferZapisForm
from src.db.postgres import get_session
from src.db.utils import copy_csv_to_postgres
from src.db.queries import insert_zapis, get_last_zapis, deactivate_zapis
from src.api.dependencies import token_dependency
from src.services.utils import merge_dicts

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
        stomatology: str,
        session: AsyncSession = Depends(get_session),
        token: str = Depends(token_dependency)
):
    try:
        form_dict = form_data.model_dump()
        zapis_id = await create_zapis(token=token, payload=form_dict)
        await insert_zapis(session=session, zapis_id=zapis_id, stomatology=stomatology, zapis=form_data)
        return {"message": "Запись успешно создана!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{stomatology}/delete", summary="Отмена записи")
async def cancel_entry(
        form_data: DeleteZapisForm,
        stomatology: str,
        session: AsyncSession = Depends(get_session),
        token: str = Depends(token_dependency)
):
    prev_id, prev_form = await get_last_zapis(session, stomatology, form_data.phone)
    response = await delete_zapis(token=token, zapis_id=prev_id)
    response = {"response": 1}
    if response.get("response") != 1:
        return "Не удалось удалить запись!"

    await deactivate_zapis(session=session, zapis_id=prev_id)
    return "Запись успешно удалена!"


@router.post("/{stomatology}/transfer", summary="Перенос записи")
async def transfer_entry(
        form_data: TransferZapisForm,
        stomatology: str,
        session: AsyncSession = Depends(get_session),
        token: str = Depends(token_dependency)
):
    try:
        prev_id, prev_form = await get_last_zapis(session, stomatology, form_data.phone)
        edited_form = merge_dicts(prev_form.model_dump(), form_data.model_dump())

        # Create zapis
        response = await create_zapis(token=token, payload=edited_form)
        await insert_zapis(
            session=session, zapis_id=response, stomatology=stomatology,
            zapis=CreateZapisForm(**edited_form)
        )

        # Delete zapis
        response = await delete_zapis(token=token, zapis_id=prev_id)
        if response.get("response") != 1:
            return "Не удалось удалить запись!"
        await deactivate_zapis(session=session, zapis_id=prev_id)

        return {"message": "Запись успешно обновлена!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/load-from-csv", summary="Восстановление данных базы через csv файл")
async def upload_csv(file: UploadFile = File(...), session: AsyncSession = Depends(get_session)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are allowed!")
    try:
        await copy_csv_to_postgres(session, file)
        return {"message": "CSV data successfully inserted into the database"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
