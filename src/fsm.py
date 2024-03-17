from aiogram.fsm.state import StatesGroup, State


class RegisterProfile(StatesGroup):
    choosing_age = State()
    choosing_bio = State()
    choosing_country = State()
    choosing_city = State()
    done = State()


class SettingProfile(RegisterProfile):
    choosing_age = State()
    choosing_bio = State()
    choosing_location = State()
    done = State()
