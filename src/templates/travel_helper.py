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
    DONT_KNOW = 'Такого прогноза еще нет. Либо вы уже посетили это место!'

    SELECT_LOCATION = '<b>Выберите место, рядом с которым надо найти достоприечательности:</b>\n'
    SELECT_CAFE = '<b>Выберите, где хотите поискать еду:</b>\n'
    SELECT_HOTELS = '<b>Выберите место, рядом с которым будем искать номера:</b>\n'
    LOCATION_NUMBER = 'Локация №'
    OPENTRIP_ERROR = 'Ошибка при работе с сервисом для работы с отелями. Попробуйте позже'
    NO_INTERESTING = 'В радиусе 10 километров не найдено никаких интересных мест!'
    PLACES_TOVISIT = 'Вот 10 мест, которые вам точно стоит посетить!\n\n'
    CAFE_TOVISIT = 'Вот несколько кафе, куда можно зайти:\n\n'
    WAITING_INFO = 'Ждем информацию...'
    NO_HOTELS = 'Подходящих номеров поблизости не найдено!'
    NOTHING_FOUND = 'Ничего подоходящего поблизости не найдено!'
    HOTELS_TOVISIT = '<b>Вот доступные на ваши даты двухместные номера, в которых не стыдно поселиться с подружкой! Вам же не жалко денег?</b>\n'

    SELECT_TILE_SOURCE = ('<b>Выберите источник, из которого хотите получать изображение карты:</b>\n\n'
                          '<b>Yandex</b> - закрытый исходный код, очень высокая скорость получения изображения\n'
                          '<b>OpenStreetMap</b> - открытый исходный код, низкая скорость получения изображения')


class TemplatesGen:
    @classmethod
    def weather(cls, sunrise: datetime, sunset: datetime, temp_min: float,
                temp_max: float, weather_condition: str, date: datetime) -> str:
        return f'''<u><i>{get_date_str_from_obj(date)}</i></u>:
  🌅 {sunrise.strftime("%H:%M")} - {sunset.strftime("%H:%M")}
  🌡️ {weather_condition},  от {temp_min}℃  до {temp_max}℃ '''

    @classmethod
    def place(cls, name: str, description: str, distance: int, address: str, is_open: bool, index: int) -> str:
        last_str = '<u>\nТочно открыто сейчас!</u>' if is_open else ''
        prelast_str = f'\n    <b>Описание:</b> <i>{description}</i>    ' if description else ''

        return f'<b>{index}. {name}</b>\n    <b>Адрес:</b> {address} <i>({distance}м)</i>{prelast_str}{last_str}\n\n'

    @classmethod
    def hotel(cls, name: str, desc: str, price: str, index: int) -> str:
        return f'{index}. <b>{name}</b>\n    <b>Описание:</b> {desc}\n    <b>Цена:</b> {price}\n\n'

    @classmethod
    def cafe(cls, name: str, addr: str, url: str, hours: str, index: int) -> str:
        return f'{index}. <b><a href="{url}">{name}</a></b>\n    <b>Адрес:</b> {addr}\n    <b>Часы работы:</b> {hours}\n\n'
