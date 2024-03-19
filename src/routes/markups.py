from aiogram import Router
from aiogram import F
from aiogram.dispatcher.event.handler import CallbackType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, callback_query
from aiogram.fsm.context import FSMContext

from fsm.markups import AddMarkup
from storage import FILES_PATH, validate_path
from templates.markups import *
from repository import TravelRepository, UserRepository
from restrictions import *
from fsm.travel import AddTravel
from commands.markups import *
from commands.common import CommonCommands
from api.getlocation import get_location, get_location_from_raw
from api.gettime import get_date_obj, get_date_str_from_obj, get_current_date
from keyboards.profile import kb_reg
from keyboards.travel import kb_travel_actions_generate, kb_travel_menu
from keyboards.common import kb_main, kb_input, kb_is_valid
from keyboards.location import kb_get_location
from keyboards.markups import kb_select_type, kb_go_back_generate, kb_show_markups_generate
from templates.profile import Templates as TemplatesProfile
from utils import safe_message_edit
# from templates.profile import *

router = Router()


@router.callback_query(F.data.startswith(Commands.LIST_MARKUPS.value))
async def list_markups_handler(message: CallbackQuery, state: FSMContext) -> None:
    user_id = message.from_user.id
    travel_id = int(message.data.split(':')[1])  # noqa #type: ignore
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_data = await TravelRepository.select_by_id(travel_id)
    owner = travel_data['owner']
    if not travel_data['markups']:
        await safe_message_edit(message, Templates.NO_MARKUPS.value, kb_go_back_generate(full_id))  # noqa #type: ignore
        return
    if owner == user_id:
        await safe_message_edit(message, Templates.SELECT_MARKUP.value, kb_show_markups_generate(travel_data['markups'], full_id, user_id))
        return

    else:
        visible_markups = [
            markup for markup in travel_data['markups'] if markup[2] == user_id or markup[1]]
        if not len(visible_markups):
            await safe_message_edit(message, Templates.NO_VISIBLE_MARKUPS.value, kb_go_back_generate(full_id))  # noqa #type: ignore
            return
        await safe_message_edit(message, Templates.SELECT_MARKUP.value, kb_show_markups_generate(visible_markups, full_id, user_id))


@router.callback_query(F.data.startswith(Commands.ADD_MARKUP.value))
async def add_markup_handler(message: CallbackQuery, state: FSMContext) -> None:
    # user_id = message.from_user.id
    id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_id = id.split(':')[0]
    await state.update_data(travel_id=int(travel_id))
    await safe_message_edit(message, Templates.SELECT_TYPE.value, kb_select_type(id))
    # travel_data = await TravelRepository.select_by_id(travel_id)
    # owner = travel_data['owner']
    # if travel_data['markups']:
    #     if owner == user_id:
    #         pass


@router.callback_query(F.data.startswith(Commands.PRIVATE.value))
async def add_private_markup_handler(message: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AddMarkup.adding_private)
    await message.bot.send_message(chat_id=message.message.chat.id, reply_markup=kb_travel_menu, text=Templates.SEND_FILE)  # noqa #type: ignore


@router.callback_query(F.data.startswith(Commands.PUBLIC.value))
async def add_public_markup_handler(message: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AddMarkup.adding_public)
    await message.bot.send_message(chat_id=message.message.chat.id, reply_markup=kb_travel_menu, text=Templates.SEND_FILE)  # noqa #type: ignore


@router.message(AddMarkup.adding_public, ~F.text.startswith('/'), F.document)
@router.message(AddMarkup.adding_private, ~F.text.startswith('/'), F.document)
async def sent_markup(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    print(state_data)
    user_id = message.from_user.id  # noqa #type: ignore

    file_id = message.document.file_id  # noqa #type: ignore
    file = await message.bot.get_file(file_id)  # noqa #type: ignore
    name = message.document.file_name  # noqa #type: ignore
    file_path = file.file_path
    path_to_save = validate_path(str(state_data['travel_id']))

    travel_data = await TravelRepository.select_by_id(state_data['travel_id'])

    if await state.get_state() == AddMarkup.adding_public:
        visible = True
    else:
        visible = False

    if 'markups' not in travel_data or not travel_data['markups']:
        travel_data['markups'] = []
    travel_data['markups'].append((name, visible, user_id))
    await TravelRepository.update_by_id(state_data['travel_id'], {'markups': travel_data['markups']})

    await message.bot.download_file(file_path, path_to_save + f'/{name}')  # noqa #type: ignore
    await state.set_state(None)
    await message.answer(text=Templates.FILE_SENDED.value, reply_markup=kb_travel_menu)
