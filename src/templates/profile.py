from enum import Enum


class Templates(Enum):
    GET_AGE = 'Введите ваш возраст:'
    GET_BIO = 'Введите информацию о себе:'
    GET_CITY = 'Отправьте свое местоположение.\nЕсли вы с компьютера, напишите свой город в сообщении.'
    ST_LOOK_OR_EDIT = 'Просмотр или изменение профиля.'
    ST_NOT_REGISTERED = 'Вы еще не зарегестрированы!'
    ST_BAD_AGE = 'Неправильно указан возраст, попробуйте еще.'
    ST_BAD_BIO = 'Слишком длинный статус, попробуйте еще.'
    ST_BIO_CHANGED = 'Статус изменен.'
    ST_BAD_LOC = 'Не удалось определить локацию. Попробуйте еще'
    ST_CITY_CHANGED = 'Город изменен.'
    ST_REGISTERED = 'Регистрация завершена!'
    ST_AGE_CHANGED = 'Возраст изменен!'


class TemplatesGen:
    @classmethod
    def profile(cls, user_data):
        return f'''    <u>Ваш профиль</u>

        Уникальный ID: <b>{user_data['id']} </b>
        Возраст: <b>{user_data['age']}</b>
        Описание: <b>{user_data['bio']}</b>
        Местоположение: <b>{user_data['city']}</b>

            '''

    @classmethod
    def city_changed(cls, city):
        return f'Город изменен: {city}'

    @classmethod
    def location(cls, country, city):
        return f'{country}, {city}'

    @classmethod
    def is_location_good(cls, loc):
        return f'Правильно ли указан город:\n{loc}'
