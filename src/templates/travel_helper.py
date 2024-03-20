from enum import Enum


class Templates(Enum):
    NO_ROUTE = 'Маршрут не найден'
    SELECT_ROUTE = 'Выберите маршрут, который хотите получить:'
    ROUTING_ERROR = 'Ошибка при обращении к сервису маршрутизации. Попробуйте позже.'
    GIST_ERROR = 'Ошибка при работе с сервисом для загрузки карт. Попробуйте позже.'
    NO_PLACES = 'Слишком мало мест для маршрута!'


class TemplatesGen:
    @classmethod
    def route_ref(cls, ref):
        return f'Ссылка на маршрут: <a href="{ref}">маршрут</a>'
