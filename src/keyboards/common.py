from aiogram import types
from utils import inline_button, button
from commands.common import CommonCommands

kb_skip_setting = types.InlineKeyboardMarkup(inline_keyboard=[[inline_button(
    CommonCommands.SKIP_SETTING.value)]])


kb_input = types.InlineKeyboardMarkup(inline_keyboard=[[inline_button(
    CommonCommands.END_INPUT.value)]])

kb_is_valid = types.InlineKeyboardMarkup(inline_keyboard=[[inline_button(
    CommonCommands.GOOD.value)], [inline_button(CommonCommands.BAD.value)]])

kb_main = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[button(CommonCommands.INFO.value)],
                                                                    [button(CommonCommands.MY_PROFILE.value)],  [button(CommonCommands.MENU_TRAVELS.value)]])
