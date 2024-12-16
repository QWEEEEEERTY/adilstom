from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from .models import Stomatology


async def get_auth_token(stomatology: str, session: AsyncSession) -> str:
    stmt = select(Stomatology).where(Stomatology.name == stomatology)
    result = await session.execute(stmt)
    stomatology = result.scalar_one_or_none()
    if stomatology:
        return stomatology.token
    raise HTTPException(status_code=400, detail="Стоматология с таким именем не найдена!")
