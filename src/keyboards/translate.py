from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from commands.translate import Commands
from utils import inline_button

langs = {'Английский': 'en',
         'Испанский': 'es',
         'Французский': 'fr',
         'Немецкий': 'de',
         'Итальянский': 'it',
         'Португальский': 'pt',
         'Хинди': 'hi',
         'Японский': 'ja',
         'Китайский': 'zh',
         'Корейский': 'ko',
         'Польский': 'pl',
         'Турецкий': 'tr',
         }
builder = InlineKeyboardBuilder()

for key, value in langs.items():
    builder.button(text=key, callback_data=value)
builder.adjust(3, 3, 3, 3)

kb_select_lang = builder.as_markup()
kb_select_type = types.InlineKeyboardMarkup(
    inline_keyboard=[[inline_button(Commands.FROM_RU.value), inline_button(Commands.TO_RU.value)]])
