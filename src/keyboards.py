from aiogram import types
from utils import inline_button, button
from messages import *

kb_edit_profile = types.InlineKeyboardMarkup(inline_keyboard=[[inline_button(q_profile)], [inline_button(
    m_age), inline_button(m_bio)], [inline_button(m_location)]])

kb_skip_setting = types.InlineKeyboardMarkup(inline_keyboard=[[inline_button(
    q_skip_setting)]])

kb_is_valid = types.InlineKeyboardMarkup(inline_keyboard=[[inline_button(
    q_good)], [inline_button(q_bad)]])


kb_reg = types.InlineKeyboardMarkup(inline_keyboard=[[inline_button(
    q_reg)]])
