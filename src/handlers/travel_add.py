from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from api.getlocation import get_location, get_location_from_raw
from api.gettime import (get_current_datetime, get_date_formatted,
                         get_date_obj, get_date_str_from_obj)
from commands.common import CommonCommands
from commands.travel import Commands
from fsm.travel import AddTravel
from keyboards.common import kb_input, kb_is_valid
from keyboards.profile import kb_reg
from keyboards.travel import (kb_travel_actions_generate,
                              kb_travel_friend_actions_generate,
                              kb_travel_menu)
from repository import TravelRepository, UserRepository
from restrictions import *
from templates.profile import Templates as TemplatesProfile
from templates.travel import Templates, TemplatesGen
from utils import safe_message_edit

router = Router()


@router.message(F.text == CommonCommands.MENU_TRAVELS.value)
async def menu_travel_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id  # noqa #type: ignore
    await message.bot.delete_message(chat_id=user_id, message_id=message.message_id)  # noqa #type: ignore
    if await UserRepository.id_exists(user_id):
        await message.answer(text=Templates.TRAVEL_MENU.value, reply_markup=kb_travel_menu)
    else:
        await message.answer(TemplatesProfile.ST_NOT_REGISTERED.value, reply_markup=kb_reg)


@router.message(F.text == Commands.LIST_TRAVELS.value)
async def list_travels_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id  # noqa #type: ignore
    user = await UserRepository.select_by_id(user_id)
    await message.bot.delete_message(chat_id=user_id, message_id=message.message_id)  # noqa #type: ignore
    if not user['travels']:  # noqa #type: ignore
        await message.answer(Templates.NO_TRAVELS.value, reply_markup=kb_travel_menu)
        return
    for (id, travel) in enumerate(user['travels'], start=1):  # noqa #type: ignore
        travel = await TravelRepository.select_by_id(travel)
        travel_id = f'{travel["id"]}:{id}'  # noqa #type: ignore
        if user_id == travel['owner']:
            await message.answer(text=TemplatesGen.travel(travel, id), reply_markup=kb_travel_actions_generate(travel_id))
        else:
            await message.answer(text=TemplatesGen.travel(travel, f'пользователя {travel["owner"]}'), reply_markup=kb_travel_friend_actions_generate(travel_id))


@router.message(F.text == Commands.ADD_TRAVEL.value)
async def add_travel_handler(message: Message, state: FSMContext) -> None:
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    await state.set_state(AddTravel.choosing_name)
    await message.answer(text=Templates.ADD_NAME.value)


@router.message(AddTravel.choosing_name, ~F.text.startswith('/'))
async def select_name_handler(message: Message, state: FSMContext) -> None:
    name = message.text
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    if len(name) > MAX_TRAVEL_LEN:  # noqa #type: ignore
        await message.answer(Templates.TOO_LONG_NAME.value)
        return
    if await TravelRepository.name_exists(name, message.from_user.id):  # noqa #type: ignore
        await message.answer(Templates.EXISTS_TRAVEL.value)
        return

    await state.update_data(name=name)
    await state.set_state(AddTravel.choosing_desc)
    await message.answer(text=Templates.ADD_DESCRIPTION.value)


@router.message(AddTravel.choosing_desc, ~F.text.startswith('/'))
async def select_desc_handler(message: Message, state: FSMContext) -> None:
    desc = message.text
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    if len(desc) > MAX_TRAVEL_LEN:  # noqa #type: ignore
        await message.answer(Templates.TOO_LONG_DESC.value)
        return
    await state.update_data(description=desc)
    await state.update_data(places=[])
    await state.set_state(AddTravel.choosing_places)
    await message.answer(text=Templates.ADD_PLACE.value)


@router.message(AddTravel.choosing_places, F.location)
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


@router.message(AddTravel.choosing_places, ~F.text.startswith('/'))
async def select_place_handler_str(message: Message, state: FSMContext) -> None:
    place = message.text
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    loc, lat, lon = await get_location_from_raw(place)  # noqa #type: ignore
    if not loc:  # noqa #type: ignore
        await message.answer(text=Templates.BAD_PLACE.value)
        return
    await state.update_data(cur_loc=[str(loc)], cur_coords=[lat, lon])
    await message.answer(text=TemplatesGen.is_location_good(loc), reply_markup=kb_is_valid)


@ router.message(AddTravel.choosing_date_start, ~F.text.startswith('/'))
@ router.message(AddTravel.choosing_date_end, ~F.text.startswith('/'))
async def select_date_handler(message: Message, state: FSMContext) -> None:
    date_str = message.text
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    date_obj = get_date_obj(date_str)  # noqa #type: ignore
    cur_state = await state.get_state()
    if not date_obj:  # noqa #type: ignore
        await message.answer(text=Templates.BAD_DATE.value)
        return
    if date_obj.date() < get_current_datetime().date():  # noqa #type: ignore
        await message.answer(text=Templates.OLD_DATE_START.value)
        return
    if cur_state == AddTravel.choosing_date_end:
        state_data = await state.get_data()
        date_start = state_data['cur_loc'][-1]
        if date_obj < get_date_obj(date_start):  # noqa #type: ignore
            await message.answer(text=Templates.OLD_DATE_END.value)
            return

    if cur_state == AddTravel.choosing_date_start:
        await state.update_data(start_time=get_date_formatted(date_obj))
    else:
        await state.update_data(end_time=get_date_formatted(date_obj))

    await message.answer(text=TemplatesGen.is_date_good(get_date_str_from_obj(date_obj)), reply_markup=kb_is_valid)


@ router.callback_query(AddTravel.choosing_date_start, F.data == CommonCommands.GOOD.value)
@ router.callback_query(AddTravel.choosing_date_end, F.data == CommonCommands.GOOD.value)
async def good_date_handler(message: CallbackQuery, state: FSMContext) -> None:
    state_data = await state.get_data()
    cur_loc = state_data['cur_loc']

    if await state.get_state() == AddTravel.choosing_date_start:
        cur_loc.append(state_data['start_time'])
        await state.update_data(cur_loc=cur_loc)
        await safe_message_edit(message, Templates.ADD_DATE_END.value)
        await state.set_state(AddTravel.choosing_date_end)
        return

    cur_loc.append(state_data['end_time'])
    await state.update_data(cur_loc=cur_loc)
    await state.set_state(AddTravel.choosing_places)
    await safe_message_edit(message, Templates.ADDED_PLACE.value, reply_markup=kb_input)


@ router.callback_query(AddTravel.choosing_date_start, F.data == CommonCommands.BAD.value)
@ router.callback_query(AddTravel.choosing_date_end, F.data == CommonCommands.BAD.value)
async def bad_date_handler(message: CallbackQuery, state: FSMContext) -> None:
    if await state.get_state() == AddTravel.choosing_date_start:
        await safe_message_edit(message, Templates.ADD_DATE_START.value)
        return
    await safe_message_edit(message, Templates.ADD_DATE_END.value)


@ router.callback_query(AddTravel.choosing_places, F.data == CommonCommands.GOOD.value)
async def good_place_handler(message: CallbackQuery, state: FSMContext) -> None:
    state_data = await state.get_data()
    places = state_data['places']

    state_data['cur_loc'].append(state_data['cur_coords'][0])
    state_data['cur_loc'].append(state_data['cur_coords'][1])

    places.append(state_data['cur_loc'])
    await state.update_data(places=places)
    await state.set_state(AddTravel.choosing_date_start)
    await safe_message_edit(message, Templates.LOC_SELECTED.value)
    await message.bot.send_message(chat_id=message.message.chat.id, reply_markup=kb_travel_menu, text=Templates.ADD_DATE_START.value)  # noqa #type: ignore


@ router.callback_query(AddTravel.choosing_places, F.data == CommonCommands.BAD.value)
async def bad_place_handler(message: CallbackQuery, state: FSMContext) -> None:
    await safe_message_edit(message, Templates.ADD_PLACE.value, reply_markup=kb_input)


@ router.callback_query(AddTravel.choosing_places, F.data == CommonCommands.END_INPUT.value)
async def end_input_handler(message: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    data.pop('cur_loc')
    data['owner'] = message.from_user.id
    await state.set_state(None)
    user = await UserRepository.select_by_id(message.from_user.id)
    travel_id = await TravelRepository.add_one(data)
    len_t = 0
    if user['travels']:  # noqa #type: ignore
        len_t = len(user['travels'])  # noqa #type: ignore
        user['travels'].append(travel_id)  # noqa #type: ignore
        await UserRepository.update_by_id(message.from_user.id, {'travels': user['travels']})  # noqa #type: ignore
    else:
        await UserRepository.update_by_id(message.from_user.id, {'travels': [travel_id]})  # noqa #type: ignore
    await safe_message_edit(message, TemplatesGen.travel(data, len_t + 1))  # noqa #type: ignore
