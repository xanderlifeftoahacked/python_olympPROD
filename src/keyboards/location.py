from aiogram import types
from utils import button, button_loc
from templates.travel import *
from commands.common import CommonCommands

kb_get_location = types.ReplyKeyboardMarkup(keyboard=[[button_loc(
    Templates.GET_LOCATION.value)], [button(CommonCommands.MAIN_MENU.value)]], resize_keyboard=True, one_time_keyboard=True)
