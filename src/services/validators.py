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


def validate_phone(phone):
    phone = re.sub(r"\D", "", phone)
    if phone[0] in "78":
        phone = f"7{phone[1:]}"

    phone = f"+{phone[:-10]} ({phone[-10:-7]}) {phone[-7:-4]}-{phone[-4:-2]}-{phone[-2:]}"
    return phone
