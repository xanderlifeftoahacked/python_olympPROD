from aiogram import types
from utils import inline_button, button, inline_button_with_id
from commands.travel import *
from commands.markups import Commands as MarkupCommands
from commands.common import CommonCommands


def kb_select_type(id):
    return types.InlineKeyboardMarkup(inline_keyboard=[[inline_button_with_id(MarkupCommands.PRIVATE.value, id),
                                                        inline_button_with_id(MarkupCommands.PUBLIC.value, id)], [inline_button_with_id(CommonCommands.GO_BACK.value, id)]])


def kb_go_back_generate(id):
    return types.InlineKeyboardMarkup(inline_keyboard=[[inline_button_with_id(CommonCommands.GO_BACK.value, id)]])


def kb_show_markups_generate(markups, id, user_id):
    if markups:
        print(markups)
        keyboard = []
        for markup in markups:
            if markup[2] == user_id:
                keyboard.append([inline_button_with_id(markup[0], id), inline_button_with_id(
                    MarkupCommands.DELETE_MARKUP.value, id)])
            else:
                keyboard.append([inline_button_with_id(markup[0], id)])

        keyboard.append([inline_button_with_id(
            CommonCommands.GO_BACK.value, id)])
    else:
        keyboard = [[inline_button_with_id(CommonCommands.GO_BACK.value, id)]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)
