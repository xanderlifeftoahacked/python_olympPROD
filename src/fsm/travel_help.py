
from aiogram.fsm.state import StatesGroup, State


class Helper(StatesGroup):
    choosing_place = State()
    choosing_hotel = State()
    choosing_place = State()
