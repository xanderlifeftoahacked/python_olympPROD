from enum import Enum


class Commands(Enum):
    MAKING_ROUTES = 'Построение маршрутов'
    MAKE_ROUTE_TO_START = 'Маршрут до первой точки'
    MAKE_ROUTE_OF_TRAVEL = 'Маршрут по точкам путешествия'

    WEATHER_INFO = 'Погода'
    HOTEL_INFO = 'Отели'
    ATTRACTIONS_INFO = 'Достопримечательности'
    CAFES_INFO = 'Кафе и рестораны'
    FRIEND_FIND = 'Найти друга'

    SELECTING_LOC = 'SelLoc'
    YANDEX_TILES = 'Yandex'
    OSM_TILES = 'OSM'
