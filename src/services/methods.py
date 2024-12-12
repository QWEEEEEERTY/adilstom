import aiohttp
import json

from .constants import BASE_URL, headers
from .defaults import get_schedule_params, create_zapis_payload, delete_payload
from .utils import parse_schedule, merge_dicts


async def get_schedule(params: dict) -> dict:
    params = merge_dicts(get_schedule_params, params)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=BASE_URL, params=params, headers=headers) as response:
            content = await response.read()
            content = json.loads(content.decode("utf-8"))
            schedule = parse_schedule(content, date=params.get("start"))
            return schedule if schedule else "Расписание на этот день еще не создано!"


async def create_zapis(payload: dict) -> dict:
    payload = merge_dicts(create_zapis_payload, payload)
    async with aiohttp.ClientSession() as session:
        async with session.post(url=BASE_URL, headers=headers, data=payload) as response:
            content = await response.read()
            return json.loads(content.decode("utf-8"))


async def delete_zapis(zapis_id: int):
    payload = delete_payload.copy()
    payload["id"] = zapis_id
    async with aiohttp.ClientSession() as session:
        async with session.post(url=BASE_URL, headers=headers, data=payload) as response:
            content = await response.read()
            return json.loads(content.decode("utf-8"))
