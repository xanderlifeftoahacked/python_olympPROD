from enum import Enum


class Commands(Enum):
    MY_PROFILE = 'Мой профиль'
    EDIT_PROFILE = 'Редактировать профиль'
    REGISTER = 'Регистрация'
    GOOD = 'Верно'
    BAD = 'Повторить попытку'
    AGE = 'Возраст'
    BIO = 'Статус'
    PROFILE_DATA = 'Посмотреть профиль'
    LOCATION = 'Страна и город'
    SKIP_SETTING = 'Оставить пустым'
    INFO = 'Информация'


# class Answers
# q_profile = 'Посмотреть профиль'
# m_info = 'Информация'
# m_age = 'Возраст'
# m_location = 'Страна и город'
# m_bio = 'Статус'
#
# q_ask_change_yes = 'Изменить другие параметры'
# q_skip_setting = 'Оставить пустым'
# q_home = 'Вернуться на главную'
#
# a_age = 'Введите ваш возраст:'
# a_bio = 'Введите ваш статус:'
# a_country = 'Введите страну:'
# a_city = 'Введите город:'
