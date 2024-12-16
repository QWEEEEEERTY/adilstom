from fastapi import Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.queries import get_auth_token
from src.db.postgres import get_session


async def token_dependency(
    stomatology: str = Path(example="adilstom"),
    session: AsyncSession = Depends(get_session)
):
    token = await get_auth_token(stomatology, session)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    return token
