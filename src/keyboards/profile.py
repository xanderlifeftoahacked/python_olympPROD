from aiogram import types
from utils import inline_button, button
from commands.profile import *
from commands.common import CommonCommands

kb_edit_profile = types.InlineKeyboardMarkup(
    inline_keyboard=[[inline_button(Commands.PROFILE_DATA.value)],
                     [inline_button(Commands.AGE.value),
                      inline_button(Commands.BIO.value)],
                     [inline_button(Commands.LOCATION.value)]])

kb_skip_setting = types.InlineKeyboardMarkup(inline_keyboard=[[inline_button(
    CommonCommands.SKIP_SETTING.value)]])

kb_is_valid = types.InlineKeyboardMarkup(inline_keyboard=[[inline_button(
    CommonCommands.GOOD.value)], [inline_button(CommonCommands.BAD.value)]])

kb_reg = types.InlineKeyboardMarkup(inline_keyboard=[[inline_button(
    Commands.REGISTER.value)]])
