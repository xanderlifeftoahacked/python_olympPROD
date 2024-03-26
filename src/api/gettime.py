from datetime import datetime
from typing import Any

import dateparser as dp


def get_current_datetime() -> datetime:
    return dp.parse(str(datetime.now()))  # noqa #type: ignore


def get_date_obj(date_str: str) -> Any:
    parsed_date = dp.parse(date_str)
    if parsed_date:
        return parsed_date
    return None


def get_date_str_from_obj(date: datetime) -> Any:
    if not date:
        return None

    month_names = {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря"
    }

    month = date.month
    month_name = month_names[month]

    formatted_date = f"{date.day} {month_name} {date.year}"

    return formatted_date


def get_date_formatted(date: datetime) -> Any:
    return date.strftime("%Y-%m-%d")
