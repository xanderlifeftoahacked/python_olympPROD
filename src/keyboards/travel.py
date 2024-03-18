from aiogram import types
from utils import inline_button, button, inline_button_with_id
from commands.travel import *
from commands.common import CommonCommands

kb_travel_menu = types.ReplyKeyboardMarkup(keyboard=[[button(Commands.ADD_TRAVEL.value)], [button(
    Commands.LIST_TRAVELS.value)], [button(CommonCommands.MAIN_MENU.value)]], resize_keyboard=True)

kb_travel_actions = types.InlineKeyboardMarkup(inline_keyboard=[[inline_button(
    Commands.HELP_TRAVEL.value)], [inline_button(Commands.EDIT_TRAVEL.value), inline_button(Commands.DELETE_TRAVEL.value)]])


def kb_travel_actions_generate(id):
    return types.InlineKeyboardMarkup(inline_keyboard=[[inline_button_with_id(
        Commands.HELP_TRAVEL.value, id)], [inline_button_with_id(Commands.EDIT_TRAVEL.value, id), inline_button_with_id(Commands.DELETE_TRAVEL.value, id)]])


def kb_travel_friends_generate(friends, id):
    if friends:
        keyboard = [[inline_button_with_id(
            f'{Commands.DEL_FRIEND.value} {i+1}', f'{id}:{friend}')] for i, friend in enumerate(friends)]
        keyboard.append(
            [inline_button_with_id(CommonCommands.GO_BACK.value, id)])
    else:
        keyboard = [[inline_button_with_id(CommonCommands.GO_BACK.value, id)]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)


def kb_travel_places_generate(places_count, id):
    if places_count:
        keyboard = [[inline_button_with_id(
            f'{Commands.DELETE_PLACE_BUTTON.value} {i}', f'{id}:{i-1}')] for i in range(1, places_count+1)]
        keyboard.append(
            [inline_button_with_id(CommonCommands.GO_BACK.value, id)])
    else:
        keyboard = [[inline_button_with_id(CommonCommands.GO_BACK.value, id)]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)


def kb_travel_edit_generate(id):
    return types.InlineKeyboardMarkup(inline_keyboard=[[inline_button_with_id(
        Commands.EDIT_TRAVEL_NAME.value, id), inline_button_with_id(Commands.EDIT_TRAVEL_DESC.value, id)],
        [inline_button_with_id(Commands.EDIT_TRAVEL_FRIENDS.value, id), inline_button_with_id(
            Commands.ADD_TRAVEL_FRIEND.value, id)],
        [inline_button_with_id(Commands.ADD_PLACE.value, id), inline_button_with_id(
            Commands.DELETE_PLACE.value, id)],
        [inline_button_with_id(CommonCommands.GO_BACK.value, id)]])


def kb_travel_delete_generate(id):
    return types.InlineKeyboardMarkup(inline_keyboard=[[inline_button_with_id(Commands.CONFIRM_DELETE.value, id)], [inline_button_with_id(CommonCommands.GO_BACK.value, id)]])


def kb_travel_friend_actions_generate(id):
    return types.InlineKeyboardMarkup(inline_keyboard=[[inline_button_with_id(
        Commands.HELP_TRAVEL.value, id)]])
