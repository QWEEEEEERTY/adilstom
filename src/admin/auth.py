from sqladmin.authentication import AuthenticationBackend
from fastapi import Request

from src.config import ADMIN_PASSWORD


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        request.session.update({"token": "..."})
        return username == "admin" and password == ADMIN_PASSWORD

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        return True


authentication_backend = AdminAuth(secret_key=ADMIN_PASSWORD)
