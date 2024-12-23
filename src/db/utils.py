import csv
import io

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from .models import Zapis, Stomatology, Log

models = [Zapis, Stomatology, Log]
table_name_from_columns = {
    tuple(column.name for column in model.__table__.columns): model.__tablename__ for model in models
}


def get_table_name(columns: tuple[str, ...]) -> str:
    table_name = table_name_from_columns.get(columns)
    if not table_name:
        raise ValueError("Columns don't match any database table")
    return table_name


def get_columns(csv_content: io.BytesIO):
    reader = csv.reader(csv_content.read().decode("utf-8").splitlines())
    columns = tuple(next(reader))
    return columns


async def copy_csv_to_postgres(session: AsyncSession, file: UploadFile):
    csv_stream = io.BytesIO(file.file.read())
    columns = get_columns(csv_stream)
    table_name = get_table_name(columns)
    csv_stream.seek(0)

    connection = await session.connection()
    raw_connection = await connection.get_raw_connection()
    asyncpg_conn = raw_connection.driver_connection
    await asyncpg_conn.copy_to_table(
        table_name=table_name, format='csv', header=True, source=csv_stream, columns=columns
    )
    await session.commit()
