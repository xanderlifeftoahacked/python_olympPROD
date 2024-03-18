from aiogram import types
from utils import inline_button, button
from commands.travel import *
from commands.common import CommonCommands

kb_travel_menu = types.ReplyKeyboardMarkup(keyboard=[[button(Commands.ADD_TRAVEL.value)], [button(
    Commands.LIST_TRAVELS.value)], [button(CommonCommands.MAIN_MENU.value)]], resize_keyboard=True)
