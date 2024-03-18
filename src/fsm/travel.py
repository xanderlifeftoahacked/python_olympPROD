from aiogram.fsm.state import StatesGroup, State


class AddTravel(StatesGroup):
    choosing_name = State()
    choosing_desc = State()
    choosing_places = State()
    choosing_date_start = State()
    choosing_date_end = State()
    choosing_friends = State()
    choosing_markups = State()
    done = State()


class EditTravel(StatesGroup):
    changing_name = State()
    changing_desc = State()
    changing_places = State()
    changing_places = State()
    choosing_date_start = State()
    choosing_date_end = State()
    adding_friend = State()
