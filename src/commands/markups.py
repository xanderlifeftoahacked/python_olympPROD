from enum import Enum


class Commands(Enum):
    LIST_MARKUPS = 'Список заметок'
    ADD_MARKUP = 'Добавить заметку'
    PRIVATE = 'Приватную'
    PUBLIC = 'Публичную'
