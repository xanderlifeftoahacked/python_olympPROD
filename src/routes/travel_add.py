from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, callback_query
from aiogram.fsm.context import FSMContext

from templates.travel import *
from repository import TravelRepository, UserRepository
from restrictions import *
from commands.travel import *
from fsm.travel import AddTravel
from commands.common import CommonCommands
from maps_api.getlocation import get_location, get_location_from_raw
from keyboards.profile import kb_reg
from keyboards.common import kb_main, kb_input, kb_is_valid
from keyboards.travel import kb_travel_menu
from templates.profile import Templates as TemplatesProfile
from utils import safe_message_edit
# from templates.profile import *

router = Router()


@router.message(F.text == CommonCommands.MENU_TRAVELS.value)
async def menu_travel_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id  # noqa #type: ignore
    if await UserRepository.id_exists(user_id):
        await message.answer(text=Templates.TRAVEL_MENU.value, reply_markup=kb_travel_menu)
    else:
        await message.answer(TemplatesProfile.ST_NOT_REGISTERED.value, reply_markup=kb_reg)


@router.message(F.text == Commands.LIST_TRAVELS.value)
async def list_travels_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id  # noqa #type: ignore
    user = await UserRepository.select_by_id(user_id)
    if not user['travels']:  # noqa #type: ignore
        await message.answer(Templates.NO_TRAVELS.value, reply_markup=kb_travel_menu)
    else:
        for (id, travel) in enumerate(user['travels']):  # noqa #type: ignore
            travel = await TravelRepository.select_by_id(travel)
            await message.answer(text=TemplatesGen.travel(travel, id + 1))


@router.message(F.text == Commands.ADD_TRAVEL.value)
async def add_travel_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(AddTravel.choosing_name)
    await message.answer(text=Templates.ADD_NAME.value)


@router.message(AddTravel.choosing_name, ~F.text.startswith('/'))
async def select_name_handler(message: Message, state: FSMContext) -> None:
    name = message.text
    if len(name) > MAX_TRAVEL_LEN:  # noqa #type: ignore
        await message.answer(Templates.TOO_LONG_NAME.value)
        return

    await state.update_data(name=name)
    await state.set_state(AddTravel.choosing_desc)
    await message.answer(text=Templates.ADD_DESCRIPTION.value)


@router.message(AddTravel.choosing_desc, ~F.text.startswith('/'))
async def select_desc_handler(message: Message, state: FSMContext) -> None:
    desc = message.text
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
    loc = get_location(lat, lon)
    if not loc:
        await message.answer(text=Templates.BAD_PLACE.value)
        return

    await state.update_data(cur_loc=loc)
    await message.answer(text=TemplatesGen.is_location_good(loc), reply_markup=kb_is_valid)


@router.message(AddTravel.choosing_places, ~F.text.startswith('/'))
async def select_place_handler_str(message: Message, state: FSMContext) -> None:
    place = message.text
    loc = get_location_from_raw(place)  # noqa #type: ignore
    if not loc:  # noqa #type: ignore
        await message.answer(text=Templates.BAD_PLACE.value)
        return
    await state.update_data(cur_loc=str(loc))
    await message.answer(text=TemplatesGen.is_location_good(loc), reply_markup=kb_is_valid)


@router.callback_query(AddTravel.choosing_places, F.data == CommonCommands.GOOD.value)
async def good_place_handler(message: CallbackQuery, state: FSMContext) -> None:
    state_data = await state.get_data()
    places = state_data['places']
    places.append(state_data['cur_loc'])
    await state.update_data(places=places)
    await safe_message_edit(message, Templates.ADDED_PLACE.value, reply_markup=kb_input)


@router.callback_query(AddTravel.choosing_places, F.data == CommonCommands.BAD.value)
async def bad_place_handler(message: CallbackQuery, state: FSMContext) -> None:
    await safe_message_edit(message, Templates.ADD_PLACE.value, reply_markup=kb_input)


@router.callback_query(AddTravel.choosing_places, F.data == CommonCommands.END_INPUT.value)
async def end_input_handler(message: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    data.pop('cur_loc')
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
