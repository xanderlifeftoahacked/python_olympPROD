from aiogram.fsm.state import StatesGroup, State


class Helper(StatesGroup):
    choosing_place = State()
    choosing_cafe = State()
    choosing_hotel = State()
