from types import MappingProxyType
from .constants import base_cookies


def merge_dicts(base: MappingProxyType | dict, extra: dict) -> dict:
    merged_dict = base.copy()
    for key, value in extra.items():
        merged_dict[key] = value
    return merged_dict


def build_cookies(token: str) -> dict:
    cookies = base_cookies.copy()
    cookies["user_token"] = token
    return cookies
