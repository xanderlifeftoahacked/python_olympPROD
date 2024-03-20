
from aiogram.fsm.state import StatesGroup, State


class MakingRoute(StatesGroup):
    choosing_place = State()
