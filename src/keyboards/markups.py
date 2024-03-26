from aiogram import types

from commands.common import CommonCommands
from commands.markups import Commands as MarkupCommands
from commands.travel import Commands
from utils import inline_button, inline_button_with_id


def kb_select_type(id):
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[inline_button_with_id(MarkupCommands.PRIVATE.value, id),
                          inline_button_with_id(MarkupCommands.PUBLIC.value, id)],
                         [inline_button_with_id(CommonCommands.GO_BACK.value, id)]])


def kb_go_back_generate(id):
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[inline_button_with_id(CommonCommands.GO_BACK.value, id)]])


def kb_show_markups_generate(markups, id):
    if markups:
        keyboard = []
        for markup in markups:
            show_button = types.InlineKeyboardButton(
                text=markup[0], callback_data=f'{markup[0]}:{markup[2]}:{id}')
            keyboard.append([show_button])

        keyboard.append([inline_button_with_id(
            CommonCommands.GO_BACK.value, id)])
    else:
        keyboard = [[inline_button_with_id(CommonCommands.GO_BACK.value, id)]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)


def kb_markup_actions_generate(full_travel_id, user_id, owner_id):
    if str(user_id) == str(owner_id):
        return types.InlineKeyboardMarkup(
            inline_keyboard=[[inline_button(MarkupCommands.GET_MARKUP.value),
                              inline_button(MarkupCommands.DELETE_MARKUP.value)],
                             [inline_button_with_id(CommonCommands.GO_BACK.value, full_travel_id)]])
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[inline_button(MarkupCommands.GET_MARKUP.value)],
                         [inline_button_with_id(CommonCommands.GO_BACK.value, full_travel_id)]])
