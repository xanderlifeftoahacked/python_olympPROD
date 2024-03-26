import os
from pathlib import Path

FILES_PATH = './media/'

symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
           u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
tr = {ord(a): ord(b) for a, b in zip(*symbols)}


def transliterate(string: str):
    return string.translate(tr)


def validate_path(path):
    Path(FILES_PATH + path).mkdir(parents=True, exist_ok=True)
    return FILES_PATH + path


def delete_file(travel_id, filename):
    fullpath = f'{FILES_PATH}{travel_id}/{filename}'
    if os.path.isfile(fullpath):
        os.remove(fullpath)


def get_file_path(travel_id, filename):
    return f'{FILES_PATH}{travel_id}/{filename}'
