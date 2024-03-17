from aiogram import types
from utils import inline_button, button
from commands.profile import *

kb_skip_setting = types.InlineKeyboardMarkup(inline_keyboard=[[inline_button(
    Commands.SKIP_SETTING.value)]])

kb_is_valid = types.InlineKeyboardMarkup(inline_keyboard=[[inline_button(
    Commands.GOOD.value)], [inline_button(Commands.BAD.value)]])

kb_main = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [button(Commands.MY_PROFILE.value)], [button(Commands.INFO.value)]])
