import aiohttp
import json

from .constants import BASE_URL, base_headers
from .defaults import base_get_params, base_create_payload, base_delete_payload
from .utils import merge_dicts, build_cookies
from .parsers import parse_schedule


async def get_schedule(token: str, params: dict) -> dict:
    cookies = build_cookies(token)
    params = merge_dicts(base=base_get_params, extra=params)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=BASE_URL, headers=base_headers, cookies=cookies, params=params) as response:
            content = await response.read()
            content = json.loads(content.decode("utf-8"))
            schedule = parse_schedule(content, date=params.get("start"))
            return schedule if schedule else "Расписание на этот день еще не создано!"


async def create_zapis(token: str, payload: dict) -> int:
    cookies = build_cookies(token=token)
    payload = merge_dicts(base=base_create_payload, extra=payload)
    async with aiohttp.ClientSession() as session:
        async with session.post(url=BASE_URL, headers=base_headers, cookies=cookies, data=payload) as response:
            content = await response.read()
            response = json.loads(content)
            if error := response.get("error"):
                raise ValueError(error)
            return response["status"]


async def delete_zapis(token: str, zapis_id: int):
    cookies = build_cookies(token)
    payload = merge_dicts(base=base_delete_payload, extra={"id": zapis_id})
    async with aiohttp.ClientSession() as session:
        async with session.post(url=BASE_URL, headers=base_headers, data=payload, cookies=cookies) as response:
            return json.loads(await response.read())

