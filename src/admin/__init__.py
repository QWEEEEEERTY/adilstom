from .views import *
from .auth import authentication_backend
from sqladmin import Admin

from fastapi import FastAPI
from src.db.postgres import get_engine


def create_admin(app: FastAPI):
    admin = Admin(app, get_engine(), authentication_backend=authentication_backend)
    admin.add_view(ZapisAdmin)
    admin.add_view(StomatologyAdmin)
    admin.add_view(LogAdmin)