import datetime
import re


def validate_date(value: str):
    try:
        input_date = datetime.datetime.strptime(value, "%d.%m.%Y")
    except ValueError:
        raise ValueError("Даты должны быть в формате DD.MM.YYYY")

    today = datetime.datetime.today().date()
    # if input_date.date() < today:
    #     raise ValueError("Вы не можете выбрать прошедшую дату")
    return value


def validate_phone(value):
    pattern = r"^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$"
    if not re.match(pattern, value):
        raise ValueError("Номер должен быть в формате +7(777)777-77-77")
    value = f"{value[:2]} {value[2:7]} {value[7:]}"
    return value
