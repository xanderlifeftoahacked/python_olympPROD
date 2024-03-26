from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from api.gettranslate import translate
from commands.common import CommonCommands
from commands.translate import Commands
from fsm.translate import *
from keyboards.common import kb_main
from keyboards.translate import kb_select_lang, kb_select_type
from templates.translate import *
from utils import safe_message_edit

router = Router()


@ router.message(F.text == CommonCommands.TRANSLATE.value)
async def translate_hadnler(message: Message, state: FSMContext) -> None:
    await state.set_state(Translating.choosing_type)
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    await message.bot.send_message(chat_id=message.from_user.id, text=Templates.SELECT_TYPE.value, reply_markup=kb_select_type)  # noqa #type: ignore


@ router.callback_query(Translating.choosing_type)
async def selected_type(message: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(lang=message.data)
    await state.set_state(Translating.choosing_language)

    callback_query = message.data

    if callback_query == Commands.TO_RU.value:
        await state.update_data(to_russian=True)
    else:
        await state.update_data(to_russian=False)

    await safe_message_edit(message, Templates.SELECT_LANG.value, reply_markup=kb_select_lang)  # noqa #type: ignore


@ router.callback_query(Translating.choosing_language)
async def selected_lang_handler(message: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(lang=message.data)
    await state.set_state(Translating.sending_voice)
    await safe_message_edit(message, Templates.SEND_VOICE.value)


@ router.message(Translating.sending_voice, F.voice)
async def sent_voice(message: Message, state: FSMContext) -> None:
    await state.set_state(None)
    state_data = await state.get_data()

    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    await message.answer(text=Templates.WAIT.value)

    if state_data['to_russian']:
        lang_from = state_data['lang']
        lang_to = 'ru'
    else:
        lang_to = state_data['lang']
        lang_from = 'ru'

    voice = await message.bot.download(file=message.voice.file_id)  # noqa #type: ignore
    s = await translate(voice, lang_from, lang_to)  # noqa #type: ignore
    await message.answer(text=f'{Templates.TRANSLATED.value}\n{s}', reply_markup=kb_main)
