from aiogram import Router
from io import BytesIO
from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, FSInputFile, Message
from aiogram.types.input_file import InputFile
from aiogram.fsm.context import FSMContext
from api.getlocation import get_coords_from_raw, get_location, get_location_from_raw

from api.make_route import try_to_build_route
from fsm.travel_help_route import MakingRoute
from keyboards.travel_helper import kb_go_back_generate, kb_select_route_type
from keyboards.location import kb_get_location
from repository import TravelRepository
from templates.travel_helper import *
from restrictions import *
from commands.travel_helper import *
# from keyboards.markups import kb_markup_actions_generate, kb_select_type, kb_go_back_generate, kb_show_markups_generate
from utils import safe_message_edit

router = Router()


@router.callback_query(F.data.startswith(Commands.MAKING_ROUTES.value))
async def make_route_choose_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    await safe_message_edit(message, Templates.SELECT_ROUTE.value, kb_select_route_type(full_id))


@router.callback_query(F.data.startswith(Commands.MAKE_ROUTE_OF_TRAVEL.value))
async def make_route_of_travel_handler(message: CallbackQuery, state: FSMContext) -> None:
    travel_id = int(message.data.split(':')[1])  # noqa #type: ignore
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_data = await TravelRepository.select_by_id(travel_id)
    locations = travel_data['places']
    if not locations or len(locations) < 2:
        await safe_message_edit(message, Templates.NO_PLACES.value, kb_go_back_generate(full_id))  # noqa #type: ignore
        return

    await safe_message_edit(message, Templates.WAIT_PLEASE.value, kb_go_back_generate(full_id))  # noqa #type: ignore
    (is_good, res, img) = await try_to_build_route(locations)

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

    await state.set_state(MakingRoute.choosing_place)
    await state.update_data(user_loc=location)
    await safe_message_edit(message, Templates.SEND_LOC.value, kb_go_back_generate(full_id))  # noqa #type: ignore


@ router.message(MakingRoute.choosing_place, F.location)
async def place_handler(message: Message, state: FSMContext) -> None:
    if not message.location:
        await message.answer(text=Templates.BAD_LOC.value)
        return
    lat = message.location.latitude
    lon = message.location.longitude
    await message.answer(text=Templates.WAIT_PLEASE.value)  # noqa #type: ignore
    state_data = await state.get_data()
    (is_good, res, img) = await try_to_build_route([['Userlocation', lat, lon], state_data['user_loc']], False)
    if not is_good:
        await message.answer(text=res)

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)

    await message.bot.send_photo(message.from_user.id, photo=BufferedInputFile(buffered.read(), filename='temp.png'))  # noqa #type: ignore

    await message.answer(text=res)

    await state.set_state(None)


@ router.message(MakingRoute.choosing_place, ~F.text.startswith('/'))
async def place_handler_str(message: Message, state: FSMContext) -> None:
    place = message.text
    loc, lat, lon = await get_location_from_raw(place)  # noqa #type: ignore
    if not loc:  # noqa #type: ignore
        await message.answer(text=Templates.BAD_LOC.value)
        return

    await message.answer(text=Templates.WAIT_PLEASE.value)  # noqa #type: ignore
    state_data = await state.get_data()

    (is_good, res, img) = await try_to_build_route([[loc, lat, lon], state_data['user_loc']], False)

    if not is_good:
        await message.answer(text=res)
        return

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)

    await message.bot.send_photo(message.from_user.id, photo=BufferedInputFile(buffered.read(), filename='temp.png'))  # noqa #type: ignore

    await message.answer(text=res)

    await state.set_state(None)
