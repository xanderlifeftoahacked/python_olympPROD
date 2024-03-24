from enum import Enum


class Errors(Enum):
    WENT_WRONG = 'Что-то пошло не так. Попробуйте еще.'
    SERVICE_GEO = 'Сервис по работе с картами не отвечает, попробуйте еще.'
    SERVICE_METEO = 'Сервис по работе с метеоданными не отвечает, попробуйте еще.'
