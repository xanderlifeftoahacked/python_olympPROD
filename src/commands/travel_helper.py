from enum import Enum


class Commands(Enum):
    MAKING_ROUTES = 'Построение маршрутов'
    MAKE_ROUTE_TO_START = 'Маршрут до первой точки'
    MAKE_ROUTE_OF_TRAVEL = 'Маршрут по точкам путешествия'

    WEATHER_INFO = 'Информация о погоде'
    HOTEL_INFO = 'Отели'
    ATTRACTIONS_INFO = 'Достопримечательности'
    CAFES_INFO = 'Кафе и рестораны'
    SECRET_INFO = 'Секретная кнопка'
