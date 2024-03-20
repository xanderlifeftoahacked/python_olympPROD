from enum import Enum


class Templates(Enum):
    NO_MARKUPS = 'У путешествия нет заметок. Можно добавить!'
    NO_VISIBLE_MARKUPS = 'У путешествия нет общих заметок.'
    SELECT_TYPE = 'Укажите приватность заметки'
    SELECT_ACT = 'Выберете, что хотите сделать с заметкой'
    SELECT_MARKUP = 'Список доступных вам заметок'
    SENDED = 'Заметка отправлена!'
    SEND_FILE = 'Отправьте файл (не больше 20 МБ)'
    FILE_SENDED = 'Заметка сохранена!'
    DELETED = 'Заметка удалена!'
