from datetime import datetime
from enum import Enum

from api.gettime import get_date_str_from_obj


class Templates(Enum):
    NO_ROUTE = 'Маршрут не найден. Вероятнее всего, на машине он невозможен.'
    SELECT_ROUTE = 'Выберите маршрут, который хотите получить:'
    ROUTING_ERROR = 'Ошибка при обращении к сервису маршрутизации. Попробуйте позже.'
    OSM_ERROR = 'Ошибка при работе с сервисом для работы с картами. Попробуйте позже.'
    NO_PLACES = 'Слишком мало мест для маршрута!'
    WAIT_PLEASE = 'Подождите, маршрут загружается...'
    SEND_LOC = 'Отправьте свое местоположение! С компьютера можно написать текстом.'
    SELECT_TYPE = 'Выберите, как хотите получить маршрут:'
    ROUTE_READY = 'Маршрут готов!'
    BAD_LOC = 'Не можем найти вас! Попробуйте еще.'

    NO_WEATHER = 'Не можем узнать погоду!'
    DONT_KNOW = 'Такого прогноза еще нет!'


class TemplatesGen:
    @classmethod
    def weather(cls, sunrise: datetime, sunset: datetime, temp_min: float,
                temp_max: float, weather_condition: str, date: datetime) -> str:
        return f'''<u><i>{get_date_str_from_obj(date)}</i></u>:
  🌅 {sunrise.time()} - {sunset.time()}
  🌡️ {weather_condition},  от {temp_min}℃  до {temp_max}℃ '''
