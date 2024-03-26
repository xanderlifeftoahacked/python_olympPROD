from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from api.gettime import get_current_datetime
from commands.markups import Commands
from fsm.markups import AddMarkup, Markup
from keyboards.markups import (kb_go_back_generate, kb_markup_actions_generate,
                               kb_select_type, kb_show_markups_generate)
from keyboards.travel import kb_travel_menu
from repository import TravelRepository
from restrictions import *
from storage import delete_file, get_file_path, transliterate, validate_path
from templates.markups import Templates
from utils import safe_message_edit

router = Router()


@router.callback_query(F.data.startswith(Commands.LIST_MARKUPS.value))
async def list_markups_handler(message: CallbackQuery, state: FSMContext) -> None:
    user_id = message.from_user.id
    travel_id = int(message.data.split(':')[1])  # noqa #type: ignore
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_data = await TravelRepository.select_by_id(travel_id)
    if not travel_data['markups']:
        await safe_message_edit(message, Templates.NO_MARKUPS.value, kb_go_back_generate(full_id))  # noqa #type: ignore
        return

    visible_markups = [
        markup for markup in travel_data['markups'] if markup[2] == user_id or markup[1]]
    if not len(visible_markups):
        await safe_message_edit(message, Templates.NO_VISIBLE_MARKUPS.value, kb_go_back_generate(full_id))  # noqa #type: ignore
        return
    await state.set_state(Markup.selecting)
    await safe_message_edit(message, Templates.SELECT_MARKUP.value, kb_show_markups_generate(visible_markups, full_id))


@router.callback_query(Markup.selecting)
async def pressed_markup_handler(message: CallbackQuery, state: FSMContext) -> None:
    markup_name = message.data.split(':')[0]  # noqa #type: ignore
    user_id = message.from_user.id
    owner_id = message.data.split(':')[1]  # noqa #type: ignore
    travel_id = message.data.split(':')[2]  # noqa #type: ignore
    full_travel_id = "".join(message.data.split(':', 2)[2:])  # noqa #type: ignore
    await state.set_state(None)
    await state.update_data(markup_name=markup_name)  # noqa #type: ignore
    await state.update_data(travel_id=travel_id)  # noqa #type: ignore
    await state.update_data(full_travel_id=full_travel_id)  # noqa #type: ignore
    await safe_message_edit(message, Templates.SELECT_ACT.value, kb_markup_actions_generate(full_travel_id, user_id, owner_id))


@router.callback_query(F.data.startswith(Commands.DELETE_MARKUP.value))
async def delete_markup_handler(message: CallbackQuery, state: FSMContext) -> None:
    state_data = await state.get_data()
    travel_id = state_data['travel_id']
    markup_name = state_data['markup_name']

    travel_data = await TravelRepository.select_by_id(int(travel_id))
    new_markups_data = [
        markup for markup in travel_data['markups'] if not markup[0] == markup_name]
    await TravelRepository.update_by_id(int(travel_id), {'markups': new_markups_data})
    delete_file(travel_id, markup_name)
    await safe_message_edit(message, Templates.DELETED.value, kb_go_back_generate(state_data['full_travel_id']))


@router.callback_query(F.data.startswith(Commands.GET_MARKUP.value))
async def send_markup_handler(message: CallbackQuery, state: FSMContext) -> None:
    state_data = await state.get_data()
    travel_id = state_data['travel_id']
    markup_name = state_data['markup_name']

    file = FSInputFile(get_file_path(travel_id, markup_name))

    await message.bot.send_document(chat_id=message.from_user.id, document=file)  # noqa #type: ignore
    await safe_message_edit(message, Templates.SENDED.value, kb_go_back_generate(state_data['full_travel_id']))


@ router.callback_query(F.data.startswith(Commands.ADD_MARKUP.value))
async def add_markup_handler(message: CallbackQuery, state: FSMContext) -> None:
    id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_id = id.split(':')[0]
    await state.update_data(travel_id=int(travel_id))
    await safe_message_edit(message, Templates.SELECT_TYPE.value, kb_select_type(id))


@ router.callback_query(F.data.startswith(Commands.PRIVATE.value))
async def add_private_markup_handler(message: CallbackQuery, state: FSMContext) -> None:
    id = message.data.split(':', 1)[1]  # noqa #type: ignore
    await state.set_state(AddMarkup.adding_private)
    await state.update_data(is_pulic=False)
    await safe_message_edit(message, Templates.SEND_FILE, reply_markup=kb_go_back_generate(id))  # noqa #type: ignore


@ router.callback_query(F.data.startswith(Commands.PUBLIC.value))
async def add_public_markup_handler(message: CallbackQuery, state: FSMContext) -> None:
    id = message.data.split(':', 1)[1]  # noqa #type: ignore
    await state.set_state(AddMarkup.adding_public)
    await state.update_data(is_pulic=True)
    await safe_message_edit(message, Templates.SEND_FILE, reply_markup=kb_go_back_generate(id))  # noqa #type: ignore


@ router.message(AddMarkup.adding_public, ~F.text.startswith('/'), F.document | F.photo)
@ router.message(AddMarkup.adding_private, ~F.text.startswith('/'), F.document | F.photo)
async def sent_markup(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    user_id = message.from_user.id  # noqa #type: ignore

    await message.bot.delete_message(chat_id=user_id, message_id=message.message_id)  # noqa #type: ignore
    path_to_save = validate_path(str(state_data['travel_id']))
    if message.document:
        file_id = message.document.file_id  # noqa #type: ignore
        filename = transliterate(message.document.file_name)  # noqa #type: ignore
        await message.bot.download(file=file_id, destination=f'{path_to_save}/{filename}')  # noqa #type: ignore
    else:
        filename = f'{str(get_current_datetime()).replace(":", "-")}.jpg'  # noqa #type: ignore
        await message.bot.download(file=message.photo[-1].file_id, destination=f'{path_to_save}/{filename}')  # noqa #type: ignore

    travel_data = await TravelRepository.select_by_id(state_data['travel_id'])

    if state_data['is_pulic']:
        visible = True
    else:
        visible = False
    if 'markups' not in travel_data or not travel_data['markups']:
        travel_data['markups'] = []
    travel_data['markups'].append((filename, visible, user_id))
    await TravelRepository.update_by_id(state_data['travel_id'], {'markups': travel_data['markups']})

    await state.set_state(None)
    await message.answer(text=Templates.FILE_SENDED.value, reply_markup=kb_travel_menu)
