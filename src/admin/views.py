from sqladmin import ModelView
from src.db.models import *


class ZapisAdmin(ModelView, model=Zapis):
    column_list = [column.key for column in Zapis.__table__.columns]
    column_sortable_list = [column.key for column in Zapis.__table__.columns]

    name_plural = "Zapis"
    can_create = False
    can_edit = True
    can_delete = True
    can_view_details = True


class StomatologyAdmin(ModelView, model=Stomatology):
    column_list = [column.key for column in Stomatology.__table__.columns]
    column_sortable_list = [column.key for column in Stomatology.__table__.columns]

    form_include_pk = True
    name_plural = "Stomatologies"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class LogAdmin(ModelView, model=Log):
    column_list = [column.key for column in Log.__table__.columns]
    column_sortable_list = [column.key for column in Log.__table__.columns]

    name_plural = "Logs"
    can_create = False
    can_edit = True
    can_delete = True
    can_view_details = True
