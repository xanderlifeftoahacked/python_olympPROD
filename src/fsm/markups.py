from aiogram.fsm.state import StatesGroup, State


class AddMarkup(StatesGroup):
    adding_private = State()
    adding_public = State()
    choosing_markup = State()
    choosing_markup = State()


class Markup(StatesGroup):
    selecting = State()
