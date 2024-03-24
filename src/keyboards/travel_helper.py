from aiogram import types
from utils import inline_button, button, inline_button_with_id
from commands.travel_helper import Commands
from templates.travel_helper import *
from commands.common import CommonCommands


def kb_select_help(id):
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[inline_button_with_id(Commands.MAKING_ROUTES.value, id)],
                         [inline_button_with_id(
                             Commands.HOTEL_INFO.value, id),
                          inline_button_with_id(
                             Commands.WEATHER_INFO.value, id)],
                         [inline_button_with_id(
                             Commands.CAFES_INFO.value, id),
                          inline_button_with_id(
                             Commands.ATTRACTIONS_INFO.value, id)],
                         [inline_button_with_id(
                             Commands.FRIEND_FIND.value, id)],
                         [inline_button_with_id(CommonCommands.GO_BACK.value, id)]])


def kb_select_route_type(id):
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[inline_button_with_id(Commands.MAKE_ROUTE_TO_START.value, id)],
                         [inline_button_with_id(
                             Commands.MAKE_ROUTE_OF_TRAVEL.value, id)],
                         [inline_button_with_id(CommonCommands.GO_BACK.value, id)]])


def kb_go_back_generate(id):
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[inline_button_with_id(CommonCommands.GO_BACK.value, id)]])


def kb_select_place_generate(places_count, id):
    if places_count:
        keyboard = [[types.InlineKeyboardButton(text=f'{Templates.LOCATION_NUMBER.value} {i}',
                                                callback_data=f'{Commands.SELECTING_LOC.value}:{id}:{i-1}')]
                    for i in range(1, places_count+1)]
        keyboard.append(
            [inline_button_with_id(CommonCommands.GO_BACK.value, id)])
    else:
        keyboard = [[inline_button_with_id(CommonCommands.GO_BACK.value, id)]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)
