from enum import Enum


class Templates(Enum):
    NO_MARKUPS = 'У путешествия нет заметок. Можно добавить!'
    NO_VISIBLE_MARKUPS = 'У путешествия нет общих заметок.'
    SELECT_TYPE = 'Укажите приватность заметки'
    SEND_FILE = 'Отправьте файл (не больше 20 МБ)'
