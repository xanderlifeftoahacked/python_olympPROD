import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message

import validation
from api.getlocation import get_location, get_location_from_raw
from api.gettime import (get_current_datetime, get_date_formatted,
                         get_date_obj, get_date_str_from_obj)
from commands.common import CommonCommands
from commands.travel import Commands
from fsm.travel import EditTravel
from keyboards.common import kb_input, kb_is_valid
from keyboards.travel import (kb_travel_actions_generate,
                              kb_travel_delete_generate,
                              kb_travel_edit_generate,
                              kb_travel_friend_actions_generate,
                              kb_travel_friends_generate, kb_travel_menu,
                              kb_travel_places_generate)
from keyboards.travel_helper import kb_select_help
from repository import TravelRepository, UserRepository
from restrictions import *
from templates.travel import Templates, TemplatesGen
from utils import safe_message_edit

router = Router()


@ router.callback_query(F.data.startswith(Commands.EDIT_TRAVEL.value))
async def edit_travel_menu_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    await safe_message_edit(message, Templates.SELECT_EDIT.value, reply_markup=kb_travel_edit_generate(full_id))


@ router.callback_query(F.data.startswith(Commands.DELETE_TRAVEL.value))
async def delete_travel_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    await safe_message_edit(message, Templates.SELECT_EDIT.value, reply_markup=kb_travel_delete_generate(full_id))


@ router.callback_query(F.data.startswith(Commands.CONFIRM_DELETE.value))
async def delete_confirmed_travel_handler(message: CallbackQuery, state: FSMContext) -> None:
    travel_id = int(message.data.split(':')[1])  # noqa #type: ignore
    travel_data = await TravelRepository.remove_by_id(travel_id)
    owner_data = await UserRepository.select_by_id(travel_data['owner'])
    owner_data['travels'].remove(travel_id)
    await UserRepository.update_by_id(travel_data['owner'], {'travels': owner_data['travels']})

    if travel_data['friends']:
        for friend in travel_data['friends']:
            friend_data = await UserRepository.select_by_id(friend)
            friend_data['travels'].remove(travel_id)
            await UserRepository.update_by_id(friend, {'travels': friend_data['travels']})

    await safe_message_edit(message, Templates.TRAVEL_DELETED.value)


@ router.callback_query(State(None), F.data.startswith(Commands.DELETE_PLACE.value))
async def delete_place_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_id = int(full_id.split(':')[0])  # noqa #type: ignore
    travel_data = await TravelRepository.select_by_id(travel_id)
    if len(travel_data['places']):
        await state.set_state(EditTravel.changing_places)
        await safe_message_edit(message, TemplatesGen.show_places(travel_data), reply_markup=kb_travel_places_generate(len(travel_data['places']), full_id))


@ router.callback_query(State(None), F.data.startswith(Commands.ADD_PLACE.value))
async def add_place_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_id = int(full_id.split(':')[0])  # noqa #type: ignore
    await state.update_data(travel_id=travel_id)
    await state.set_state(EditTravel.changing_places)
    await message.bot.send_message(chat_id=message.message.chat.id, reply_markup=kb_travel_menu, text=Templates.ADD_PLACE)  # noqa #type: ignore


@ router.callback_query(EditTravel.changing_places, F.data.startswith(Commands.DELETE_PLACE_BUTTON.value))
async def deleted_place_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_id = int(full_id.split(':')[0])  # noqa #type: ignore
    location_index = int(full_id.split(':')[2])
    travel_id_for_button = ':'.join(full_id.split(':')[0:2])
    travel_data = await TravelRepository.select_by_id(travel_id)
    places = sorted(travel_data['places'], key=lambda x: x[3])
    places.pop(location_index)

    await state.set_state(None)
    await TravelRepository.update_by_id(travel_id, {'places': places})
    await safe_message_edit(message, Templates.DELETED_PLACE.value, reply_markup=kb_travel_edit_generate(travel_id_for_button))


@ router.callback_query(F.data.startswith(Commands.EDIT_TRAVEL_NAME.value))
async def edit_name_handler(message: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(travel_id=int(message.data.split(':')[1]))  # noqa #type: ignore
    await state.set_state(EditTravel.changing_name)
    await message.bot.send_message(chat_id=message.message.chat.id, reply_markup=kb_travel_menu, text=Templates.ADD_NAME)  # noqa #type: ignore


@ router.callback_query(F.data.startswith(Commands.EDIT_TRAVEL_DESC.value))
async def edit_desc_handler(message: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(travel_id=int(message.data.split(':')[1]))  # noqa #type: ignore
    await state.set_state(EditTravel.changing_desc)
    await message.bot.send_message(chat_id=message.message.chat.id, reply_markup=kb_travel_menu, text=Templates.ADD_DESCRIPTION)  # noqa #type: ignore


@ router.message(EditTravel.changing_desc, ~F.text.startswith('/'))
async def edited_desc_handler(message: Message, state: FSMContext) -> None:
    desc = message.text
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    state_data = await state.get_data()
    if len(desc) > MAX_TRAVEL_LEN:  # noqa #type: ignore
        await message.answer(Templates.TOO_LONG_DESC.value)
        return
    await TravelRepository.update_by_id(state_data['travel_id'], {'description': desc})
    await state.set_state(None)
    await message.answer(text=Templates.CHANGED_DESC.value)


@ router.message(EditTravel.changing_name, ~F.text.startswith('/'))
async def edited_name_handler(message: Message, state: FSMContext) -> None:
    name = message.text
    state_data = await state.get_data()  # noqa #type: ignore
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    if len(name) > MAX_TRAVEL_LEN:  # noqa #type: ignore
        await message.answer(Templates.TOO_LONG_NAME.value)
        return
    if await TravelRepository.name_exists(name, message.from_user.id):  # noqa #type: ignore
        await message.answer(Templates.EXISTS_TRAVEL.value)
        return

    await TravelRepository.update_by_id(state_data['travel_id'], {'name': name})
    await state.set_state(None)
    await message.answer(text=Templates.CHANGED_NAME.value)


@ router.callback_query(F.data.startswith(CommonCommands.GO_BACK.value))
async def menu_go_back_handler(message: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(None)
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_id = int(full_id.split(':')[0])  # noqa #type: ignore
    shown_id = int(full_id.split(':')[1])  # noqa #type: ignore

    travel_data = await TravelRepository.select_by_id(travel_id)
    if message.from_user.id != travel_data['owner']:
        await safe_message_edit(message, TemplatesGen.travel(travel_data, f'пользователя {travel_data["owner"]}'), reply_markup=kb_travel_friend_actions_generate(full_id))
        return
    await safe_message_edit(message, TemplatesGen.travel(travel_data, shown_id), reply_markup=kb_travel_actions_generate(full_id))


@ router.callback_query(F.data.startswith(Commands.EDIT_TRAVEL_FRIENDS.value))
async def list_friends_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_id = int(full_id.split(':')[0])  # noqa #type: ignore

    travel_data = await TravelRepository.select_by_id(travel_id)

    friends = travel_data['friends']  # noqa #type: ignore
    await safe_message_edit(message, TemplatesGen.friends(friends), reply_markup=kb_travel_friends_generate(friends, full_id))  # noqa #type: ignore

    # await safe_message_edit(message, Templates.SELECT_EDIT.value, reply_markup=kb_travel_friends_generate(full_id))


@ router.callback_query(State(None), F.data.startswith(Commands.ADD_TRAVEL_FRIEND.value))
async def add_friend_handler(message: CallbackQuery, state: FSMContext):
    travel_id = int(message.data.split(':')[1])  # noqa #type: ignore
    await message.bot.send_message(chat_id=message.message.chat.id, reply_markup=kb_travel_menu, text=Templates.ADD_USER)  # noqa #type: ignore
    await state.update_data(travel_id=travel_id)
    await state.update_data(friends_count=0)
    await state.set_state(EditTravel.adding_friend)


@ router.callback_query(EditTravel.adding_friend, F.data == CommonCommands.END_INPUT.value)
async def end_adding_friends_handler(message: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    state_data = await state.get_data()
    await message.bot.send_message(chat_id=message.message.chat.id, text=TemplatesGen.added_friends(state_data['friends_count']))  # noqa #type: ignore


@ router.message(EditTravel.adding_friend, ~F.text.startswith('/'))
async def added_friend_handler(message: Message, state: FSMContext):
    friend_id = str(message.text).strip()
    state_data = await state.get_data()

    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    if not re.fullmatch(validation.id_regex, friend_id) or not await UserRepository.id_exists(int(friend_id)):
        await message.answer(text=Templates.ST_BAD_FRIEND.value,
                             reply_markup=kb_input)
        return

    travel_data = await TravelRepository.select_by_id(state_data['travel_id'])  # noqa #type: ignore
    if not travel_data['friends']:  # noqa #type: ignore
        travel_data['friends'] = []  # noqa #type: ignore

    friend_id = int(friend_id)
    if friend_id in travel_data['friends']:  # noqa #type: ignore
        await message.answer(text=Templates.ST_ALREADY_FRIEND.value, reply_markup=kb_input)
        return

    for member_id in travel_data['friends']:
        await message.bot.send_message(chat_id=member_id, text=TemplatesGen.new_friend(member_id))  # noqa #type: ignore

    travel_data['friends'].append(friend_id)  # noqa #type: ignore
    await TravelRepository.update_by_id(state_data['travel_id'], {'friends': travel_data['friends']})  # noqa #type: ignore
    user_data = await UserRepository.select_by_id(int(friend_id))
    if user_data['travels']:  # noqa #type: ignore
        user_data['travels'].append(state_data['travel_id'])  # noqa #type: ignore
    else:
        user_data['travels'] = [state_data['travel_id']]  # noqa #type: ignore

    await UserRepository.update_by_id(int(friend_id), {'travels': user_data['travels']})  # noqa #type: ignore
    await message.bot.send_message(chat_id=friend_id, text=TemplatesGen.were_added_in_frineds(travel_data['owner']))  # noqa #type: ignore

    await state.update_data(friends_count=state_data['friends_count'] + 1)
    await message.answer(text=Templates.FRIEND_ADDED_SUCCES.value, reply_markup=kb_input)


@ router.callback_query(F.data.startswith(Commands.DEL_FRIEND.value))
async def delete_friend_handler(message: CallbackQuery, state: FSMContext):
    travel_id = int(message.data.split(':')[1])  # noqa #type: ignore
    friend_id = int(message.data.split(':')[3])  # noqa #type: ignore

    friend_data = await UserRepository.select_by_id(friend_id)
    if travel_id not in friend_data['travels']:
        await message.bot.send_message(chat_id=message.message.chat.id, text=Templates.ALREADY_DELETED_FRIEND)  # noqa #type: ignore
        return

    friend_data['travels'].remove(travel_id)  # noqa #type: ignore
    await UserRepository.update_by_id(friend_id, {'travels': friend_data['travels']})

    travel_data = await TravelRepository.select_by_id(travel_id)
    if travel_data['friends']:  # noqa #type: ignore
        travel_data['friends'].remove(friend_id)  # noqa #type: ignore
    else:
        travel_data['friends'] = []  # noqa #type: ignore

    await TravelRepository.update_by_id(travel_id, {'friends': travel_data['friends']})  # noqa #type: ignore

    await message.bot.send_message(chat_id=message.message.chat.id, text=Templates.DELETED_FRIEND)  # noqa #type: ignore


@ router.message(EditTravel.changing_places, F.location)
async def select_place_handler(message: Message, state: FSMContext) -> None:
    if not message.location:
        await message.answer(text=Templates.BAD_PLACE.value)
        return
    lat = message.location.latitude
    lon = message.location.longitude
    loc = await get_location(lat, lon)
    if not loc:
        await message.answer(text=Templates.BAD_PLACE.value)
        return

    await state.update_data(cur_loc=[str(loc)], cur_coords=[lat, lon])
    await message.answer(text=TemplatesGen.is_location_good(loc), reply_markup=kb_is_valid)


@ router.message(EditTravel.changing_places, ~F.text.startswith('/'))
async def select_place_handler_str(message: Message, state: FSMContext) -> None:
    place = message.text
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    loc, lat, lon = await get_location_from_raw(place)  # noqa #type: ignore
    if not loc:  # noqa #type: ignore
        await message.answer(text=Templates.BAD_PLACE.value)
        return
    await state.update_data(cur_loc=[str(loc)], cur_coords=[lat, lon])
    await message.answer(text=TemplatesGen.is_location_good(loc), reply_markup=kb_is_valid)


@ router.message(EditTravel.choosing_date_start, ~F.text.startswith('/'))
@ router.message(EditTravel.choosing_date_end, ~F.text.startswith('/'))
async def select_date_handler(message: Message, state: FSMContext) -> None:
    date_str = message.text
    date_obj = get_date_obj(date_str)  # noqa #type: ignore
    cur_state = await state.get_state()
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    if not date_obj:  # noqa #type: ignore
        await message.answer(text=Templates.BAD_DATE.value)
        return
    if date_obj.date() < get_current_datetime().date():  # noqa #type: ignore
        await message.answer(text=Templates.OLD_DATE_START.value)
        return
    if cur_state == EditTravel.choosing_date_end:
        state_data = await state.get_data()
        date_start = state_data['cur_loc'][-1]
        if date_obj < get_date_obj(date_start):  # noqa #type: ignore
            await message.answer(text=Templates.OLD_DATE_END.value)
            return

    if cur_state == EditTravel.choosing_date_start:
        await state.update_data(start_time=get_date_formatted(date_obj))
    else:
        await state.update_data(end_time=get_date_formatted(date_obj))

    await message.answer(text=TemplatesGen.is_date_good(get_date_str_from_obj(date_obj)), reply_markup=kb_is_valid)


@ router.callback_query(EditTravel.choosing_date_start, F.data == CommonCommands.GOOD.value)
@ router.callback_query(EditTravel.choosing_date_end, F.data == CommonCommands.GOOD.value)
async def good_date_handler(message: CallbackQuery, state: FSMContext) -> None:
    state_data = await state.get_data()
    cur_loc = state_data['cur_loc']

    if await state.get_state() == EditTravel.choosing_date_start:
        cur_loc.append(state_data['cur_coords'][0])
        cur_loc.append(state_data['cur_coords'][1])
        cur_loc.append(state_data['start_time'])
        await state.update_data(cur_loc=cur_loc)
        await safe_message_edit(message, Templates.ADD_DATE_END.value)
        await state.set_state(EditTravel.choosing_date_end)
        return

    cur_loc.append(state_data['end_time'])
    travel_data = await TravelRepository.select_by_id(state_data['travel_id'])
    travel_data['places'].append(cur_loc)
    await TravelRepository.update_by_id(state_data['travel_id'], {'places': travel_data['places']})
    await state.set_state(None)
    await message.bot.send_message(chat_id=message.message.chat.id, text=Templates.ADDED_ONE_PLACE.value, reply_markup=kb_travel_menu)  # noqa #type: ignore


@ router.callback_query(EditTravel.choosing_date_start, F.data == CommonCommands.BAD.value)
@ router.callback_query(EditTravel.choosing_date_end, F.data == CommonCommands.BAD.value)
async def bad_date_handler(message: CallbackQuery, state: FSMContext) -> None:
    if await state.get_state() == EditTravel.choosing_date_start:
        await safe_message_edit(message, Templates.ADD_DATE_START.value)
        return
    await safe_message_edit(message, Templates.ADD_DATE_END.value)


@ router.callback_query(EditTravel.changing_places, F.data == CommonCommands.GOOD.value)
async def good_place_handler(message: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EditTravel.choosing_date_start)
    await safe_message_edit(message, Templates.LOC_SELECTED.value)
    await message.bot.send_message(chat_id=message.message.chat.id, reply_markup=kb_travel_menu, text=Templates.ADD_DATE_START.value)  # noqa #type: ignore


@ router.callback_query(EditTravel.changing_places, F.data == CommonCommands.BAD.value)
async def bad_place_handler(message: CallbackQuery, state: FSMContext) -> None:
    await safe_message_edit(message, Templates.ADD_PLACE.value)


@ router.callback_query(F.data.startswith(Commands.HELP_TRAVEL.value))
async def travel_helper_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    await safe_message_edit(message, Templates.SELECT_HELPER.value, reply_markup=kb_select_help(full_id))
