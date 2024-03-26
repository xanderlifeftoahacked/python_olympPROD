from aiogram import types

from commands.common import CommonCommands
from templates.travel import Templates
from utils import button, button_loc

kb_get_location = types.ReplyKeyboardMarkup(keyboard=[[button_loc(
    Templates.GET_LOCATION.value)], [button(CommonCommands.MAIN_MENU.value)]],
    resize_keyboard=True, one_time_keyboard=True)
