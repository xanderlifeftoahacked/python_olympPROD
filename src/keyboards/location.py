from aiogram import types
from utils import button_loc
from templates.location import *

kb_get_location = types.ReplyKeyboardMarkup(keyboard=[[button_loc(
    Templates.GET_LOCATION.value)]], resize_keyboard=True, one_time_keyboard=True)
