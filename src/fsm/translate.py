from aiogram.fsm.state import StatesGroup, State


class Translating(StatesGroup):
    choosing_type = State()
    choosing_language = State()
    sending_voice = State()
