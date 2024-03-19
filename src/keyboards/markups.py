from aiogram import types
from utils import inline_button, button, inline_button_with_id
from commands.travel import *
from commands.markups import Commands as MarkupCommands
from commands.common import CommonCommands

kb_travel_menu = types.ReplyKeyboardMarkup(keyboard=[[button(Commands.ADD_TRAVEL.value)], [button(
    Commands.LIST_TRAVELS.value)], [button(CommonCommands.MAIN_MENU.value)]], resize_keyboard=True)


def kb_select_type(id):
    return types.InlineKeyboardMarkup(inline_keyboard=[[inline_button_with_id(MarkupCommands.PRIVATE.value, id),
                                                        inline_button_with_id(MarkupCommands.PUBLIC.value, id)], [inline_button_with_id(CommonCommands.GO_BACK.value, id)]])
