from enum import Enum


class Templates(Enum):
    GET_LOCATION = 'Отправить локацию'
    TRAVEL_MENU = 'Меню путешествий:'
    NOT_NOW = 'В процессе работы'
    NO_TRAVELS = 'У вас нет путешествий'
    ADD_NAME = 'Напишите название путешествия:'
    ADDED_PLACE = 'Место добавлено. Можно продолжить ввод:'
    ADD_DESCRIPTION = 'Напишите описание путешествия:'
    ADD_PLACE = 'Отправьте локацию (с компьютера можете написать текстом)'
    ADD_USER = 'Введите ID пользователя, которого хотите добавить в путешествие:'
    TOO_LONG_NAME = 'Слишком длинное название! Попробуйте еще раз:'
    TOO_LONG_DESC = 'Слишком длинное описание! Попробуйте еще раз:'
    BAD_PLACE = 'Место не нашлось! Попробуйте еще раз:'


class TemplatesGen:
    @classmethod
    def travel(cls, travel_data, id):
        # if 'markups' in travel
        # markups = [markup for markup,
        #            visible in travel_data['markups'] if visible]

        return f'''    <u>Путешествие {id} </u>

        Название: <b>{travel_data['name']}</b>
        Описание: <b>{travel_data['description']}</b>
        Места: <b>{travel_data['places']}</b>

        '''

        # Совместно с: <b>{travel_data['friends']}</b>
        # Заметки: <b>{enumerate(markups)}</b>

    @classmethod
    def is_location_good(cls, loc):
        return f'Правильно ли указано место:\n{loc} ?'
