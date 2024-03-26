from io import BytesIO

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message

from api.getlocation import get_location_from_raw
from api.getmap import get_route_image
from commands.travel_helper import Commands
from fsm.travel_help import Helper
from keyboards.travel_helper import (kb_go_back_generate, kb_select_route_type,
                                     kb_select_source_generate)
from repository import TravelRepository
from restrictions import *
from templates.travel_helper import Templates, TemplatesGen
from utils import safe_message_edit

router = Router()


@router.callback_query(F.data.startswith(Commands.MAKING_ROUTES.value))
async def make_route_choose_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    await safe_message_edit(message, Templates.SELECT_TILE_SOURCE.value, kb_select_source_generate(full_id))


@router.callback_query(F.data.startswith(Commands.OSM_TILES.value))
async def osm_source_handler(message: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(yandex=False, osm=True)
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    await safe_message_edit(message, Templates.SELECT_ROUTE.value, kb_select_route_type(full_id))


@router.callback_query(F.data.startswith(Commands.YANDEX_TILES.value))
async def yandex_source_handler(message: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(osm=False, yandex=True)
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    await safe_message_edit(message, Templates.SELECT_ROUTE.value, kb_select_route_type(full_id))


@router.callback_query(F.data.startswith(Commands.MAKE_ROUTE_OF_TRAVEL.value))
async def make_route_of_travel_handler(message: CallbackQuery, state: FSMContext) -> None:
    travel_id = int(message.data.split(':')[1])  # noqa #type: ignore
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_data = await TravelRepository.select_by_id(travel_id)
    locations = travel_data['places']
    state_data = await state.get_data()
    if not locations or len(locations) < 2:
        await safe_message_edit(message, Templates.NO_PLACES.value, kb_go_back_generate(full_id))  # noqa #type: ignore
        return

    await safe_message_edit(message, Templates.WAIT_PLEASE.value, kb_go_back_generate(full_id))  # noqa #type: ignore

    if state_data['yandex']:
        (is_good, res, img) = await get_route_image(locations)
    else:
        (is_good, res, img) = await get_route_image(locations, yandex=False)

    if not is_good:
        await safe_message_edit(message, res, kb_go_back_generate(full_id))
        return

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)

    await message.bot.send_photo(message.from_user.id, photo=BufferedInputFile(buffered.read(), filename='temp.png'))  # noqa #type: ignore
    await safe_message_edit(message, res, kb_go_back_generate(full_id))


@ router.callback_query(F.data.startswith(Commands.MAKE_ROUTE_TO_START.value))
async def make_route_to_travel_handler(message: CallbackQuery, state: FSMContext) -> None:
    travel_id = int(message.data.split(':')[1])  # noqa #type: ignore
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_data = await TravelRepository.select_by_id(travel_id)
    location = min(travel_data['places'], key=lambda x: x[3])
    if not location:
        await safe_message_edit(message, Templates.NO_PLACES.value, kb_go_back_generate(full_id))  # noqa #type: ignore
        return

    await state.set_state(Helper.choosing_place)
    await state.update_data(user_loc=location)
    await safe_message_edit(message, Templates.SEND_LOC.value, kb_go_back_generate(full_id))  # noqa #type: ignore


@ router.message(Helper.choosing_place, F.location)
async def place_handler(message: Message, state: FSMContext) -> None:
    if not message.location:
        await message.answer(text=Templates.BAD_LOC.value)
        return
    lat = message.location.latitude
    lon = message.location.longitude
    await message.answer(text=Templates.WAIT_PLEASE.value)  # noqa #type: ignore
    state_data = await state.get_data()

    if state_data['yandex']:
        (is_good, res, img) = await get_route_image([['Userlocation', lat, lon], state_data['user_loc']], False)
    else:
        (is_good, res, img) = await get_route_image([['Userlocation', lat, lon], state_data['user_loc']], False, False)

    if not is_good:
        await message.answer(text=res)

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)

    await message.bot.send_photo(message.from_user.id, photo=BufferedInputFile(buffered.read(), filename='temp.png'))  # noqa #type: ignore

    await message.answer(text=res)

    await state.set_state(None)


@ router.message(Helper.choosing_place, ~F.text.startswith('/'))
async def place_handler_str(message: Message, state: FSMContext) -> None:
    place = message.text
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    loc, lat, lon = await get_location_from_raw(place)  # noqa #type: ignore
    if not loc:  # noqa #type: ignore
        await message.answer(text=Templates.BAD_LOC.value)
        return

    await message.answer(text=Templates.WAIT_PLEASE.value)  # noqa #type: ignore
    state_data = await state.get_data()

    if state_data['yandex']:
        (is_good, res, img) = await get_route_image([[loc, lat, lon], state_data['user_loc']], False)
    else:
        (is_good, res, img) = await get_route_image([[loc, lat, lon], state_data['user_loc']], False, False)

    if not is_good:
        await message.answer(text=res)
        return

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)

    await message.bot.send_photo(message.from_user.id, photo=BufferedInputFile(buffered.read(), filename='temp.png'))  # noqa #type: ignore

    await message.answer(text=res)

    await state.set_state(None)
