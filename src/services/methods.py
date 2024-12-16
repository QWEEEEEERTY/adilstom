import aiohttp
import json
from sqlalchemy.ext.asyncio import AsyncSession

from .constants import BASE_URL, headers, cookies
from .defaults import get_schedule_params, create_zapis_payload, delete_payload
from .utils import parse_schedule, merge_dicts


async def get_schedule(token: str, params: dict) -> dict:
    params = merge_dicts(get_schedule_params, params)
    temp_cookies = cookies.copy()
    temp_cookies["user_token"] = token
    async with aiohttp.ClientSession() as session:
        async with session.get(url=BASE_URL, params=params, headers=headers, cookies=temp_cookies) as response:
            content = await response.read()
            content = json.loads(content.decode("utf-8"))
            schedule = parse_schedule(content, date=params.get("start"))
            return schedule if schedule else "Расписание на этот день еще не создано!"


async def create_zapis(token: str, payload: dict) -> dict:
    payload = merge_dicts(create_zapis_payload, payload)
    async with aiohttp.ClientSession() as session:
        async with session.post(url=BASE_URL, headers=headers, data=payload, cookies=cookies) as response:
            content = await response.read()
            return json.loads(content.decode("utf-8"))


async def delete_zapis(token: str, zapis_id: int):
    payload = delete_payload.copy()
    payload["id"] = zapis_id
    async with aiohttp.ClientSession() as session:
        async with session.post(url=BASE_URL, headers=headers, data=payload, cookies=cookies) as response:
            if response.status >= 400:
                return "Не удалось удалить запись!"
            return "Успешно удалено!"



