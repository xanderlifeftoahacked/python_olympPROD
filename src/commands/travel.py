from enum import Enum


class Commands(Enum):
    ADD_TRAVEL = 'Добавить путешествие'
    LIST_TRAVELS = 'Просмотреть путешествия'

    EDIT_TRAVEL = 'Настройки путешествия'
    MARKUPS_MENU = 'Заметки'
    DELETE_TRAVEL = 'Удалить путешествие'
    HELP_TRAVEL = 'Помощь по путешествию'

    EDIT_TRAVEL_FRIENDS = 'Список друзей'
    DEL_FRIEND = 'Удалить друга'
    ADD_TRAVEL_FRIEND = 'Добавить друга'
    EDIT_TRAVEL_NAME = 'Изменить название'
    EDIT_TRAVEL_DESC = 'Изменить описание'
    DELETE_PLACE = 'Удалить место'
    DELETE_PLACE_BUTTON = 'Удалить место №'
    ADD_PLACE = 'Добавить место'
    CONFIRM_DELETE = 'Да, хочу удалить его'
