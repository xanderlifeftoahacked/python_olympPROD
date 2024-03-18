from aiogram.fsm.state import StatesGroup, State


class AddTravel(StatesGroup):
    choosing_name = State()
    choosing_desc = State()
    choosing_places = State()
    choosing_friends = State()
    choosing_markups = State()
    done = State()
