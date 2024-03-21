from enum import Enum

from api.gettime import get_date_formatted, get_date_obj, get_date_str_from_obj


class Templates(Enum):
    GET_LOCATION = 'Отправить локацию'
    TRAVEL_MENU = 'Меню путешествий:'
    EXISTS_TRAVEL = 'У вас уже есть путешествие с таким именем. Попробуйте еще раз:'
    NOT_NOW = 'В процессе работы'
    NO_TRAVELS = 'У вас нет путешествий'
    ADD_NAME = 'Напишите название путешествия:'
    ADDED_PLACE = 'Место добавлено. Можно продолжить ввод:'
    ADD_DESCRIPTION = 'Напишите описание путешествия:'
    ADD_PLACE = 'Отправьте локацию (с компьютера можете написать текстом)'
    ADD_USER = 'Введите ID (указан у него в профиле бота) пользователя, которого хотите добавить в путешествие:'
    TOO_LONG_NAME = 'Слишком длинное название! Попробуйте еще раз:'
    TOO_LONG_DESC = 'Слишком длинное описание! Попробуйте еще раз:'
    BAD_PLACE = 'Место не нашлось! Попробуйте еще раз:'
    ADD_DATE_START = 'Введите дату начала посещения (например: "завтра", "20-12-2025")'
    ADD_DATE_END = 'Введите дату конца посещения'
    OLD_DATE_START = 'К сожалению, путешествия в прошлое невозможны. Попробуйте еще раз:'
    OLD_DATE_END = 'К сожалению, закончить раньше, чем начать, нельзя. Попробуйте еще раз:'
    BAD_DATE = 'Не удалось распознать дату. Попробуйте еще раз:'
    SELECT_EDIT = 'Выберите, что хотите сделать'
    NO_FRIENDS = 'Пока это путешествие доступно только вам.\nСамое время добавить друзей!'
    FRIEND_ADDED_SUCCES = 'Друг добавлен! Можете добавить еще (снова напишите id) или выйти, нажав на кнопку'
    ST_BAD_FRIEND = 'Человек с указанным id не найден. Попробуйте еще или выйдите, нажав на кнопку'
    ST_ALREADY_FRIEND = 'Этот человек уже у вас в друзьях! Можете добавить еще или выйти, нажав на кнопку'
    DELETED_FRIEND = 'Друг удален!'
    ALREADY_DELETED_FRIEND = 'Этот друг уже удален'
    CHANGED_NAME = 'Имя путешествия успешно изменено!'
    CHANGED_DESC = 'Описание путешествия успешно изменено!'
    DELETE_PLACES = 'Выберете место, которое хотите удалить'
    DELETED_PLACE = 'Место успешно удалено!'
    ADDED_ONE_PLACE = 'Место успешно добавлено!'
    SURE_DELETING = 'Вы уверены, что хотите удалить это путешествие?'
    TRAVEL_DELETED = 'Путешествие удалено'
    SELECT_HELPER = 'Выберите, что хотите увидеть'


class TemplatesGen:
    @classmethod
    def travel(cls, travel_data, id):
        # if 'markups' in travel
        # markups = [markup for markup,
        #            visible in travel_data['markups'] if visible]
        places = "\n".join([f"    <b>{index + 1}.</b> {place[0]}. <i>\n({get_date_str_from_obj(get_date_obj(place[1]))} - {get_date_str_from_obj(get_date_obj(place[2]))})</i>" for index,
                           place in enumerate(travel_data['places'])])
        return f'''    <u>Путешествие {id} </u>

        Название: <b>{travel_data['name']}</b>
        Описание: <b>{travel_data['description']}</b>
        Места: 
    {places}

        '''

        # Совместно с: <b>{travel_data['friends']}</b>
        # Заметки: <b>{enumerate(markups)}</b>

    @classmethod
    def is_location_good(cls, loc):
        return f'Правильно ли указано место:\n{loc} ?'

    @classmethod
    def delete_place(cls, travel_data):
        return "\n".join([f"    <b>{index + 1}.</b> {place[0]}. <i>\n({place[1]} - {place[2]})</i>" for index,
                          place in enumerate(travel_data['places'])])

    @classmethod
    def friends(cls, friends):
        if friends:
            output = '\n'.join(
                [f'<b>{i+1}.</b> {friend}' for i, friend in enumerate(friends)])
        else:
            output = Templates.NO_FRIENDS.value
        return output

    @classmethod
    def added_friends(cls, count: int):
        return f'Вы успешно добавили {count} друзей к своему путешествию!'

    @classmethod
    def is_date_good(cls, date):
        return f'Правильно ли указана дата:\n{date} ?'

    @classmethod
    def new_friend(cls, date):
        return f'В путешествии новый участник: {date}'

    @classmethod
    def were_added_in_frineds(cls, id):
        return f'Пользователь <b>{id}</b> добавил вас в друзья! Теперь вам доступны его путешествия!'
