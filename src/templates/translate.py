from enum import Enum


class Templates(Enum):
    SEND_VOICE = 'Запишите голосовое сообщение'
    SELECT_LANG = 'Выберите язык:'
    TRANSLATE_ERROR = 'К сожалению, текст с не удалось первести'
    WAIT = 'Ожидайте, перевод выполняется...'
    SELECT_TYPE = 'Выберите, что вы хотите:'
    TRANSLATED = '<b>Результат перевода:</b>\n'
