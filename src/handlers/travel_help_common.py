from io import BytesIO

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery

from api.gethotels import get_hotels
from api.getmap import make_markers_map
from api.getplaces import get_cafes, get_interesting_places
from commands.travel_helper import Commands
from fsm.travel_help import Helper
from keyboards.travel_helper import (kb_go_back_generate,
                                     kb_select_place_generate)
from repository import TravelRepository
from restrictions import *
from templates.travel import TemplatesGen as TravelTemplatesGen
from templates.travel_helper import Templates, TemplatesGen
from utils import safe_message_edit

router = Router()


@router.callback_query(F.data.startswith(Commands.ATTRACTIONS_INFO.value))
@router.callback_query(F.data.startswith(Commands.HOTEL_INFO.value))
@router.callback_query(F.data.startswith(Commands.CAFES_INFO.value))
async def get_places_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_id = int(full_id.split(':')[0])

    travel = await TravelRepository.select_by_id(travel_id)

    if message.data.startswith(Commands.ATTRACTIONS_INFO.value):  # noqa #type: ignore
        await state.set_state(Helper.choosing_place)
        s = Templates.SELECT_LOCATION.value
    elif message.data.startswith(Commands.HOTEL_INFO.value):  # noqa #type: ignore
        await state.set_state(Helper.choosing_hotel)
        s = Templates.SELECT_HOTELS.value
    else:
        await state.set_state(Helper.choosing_cafe)
        s = Templates.SELECT_CAFE.value

    await state.update_data(places=sorted(travel['places'], key=lambda x: x[3]))
    await safe_message_edit(message, f'{s}\n{TravelTemplatesGen.show_places(travel)}',
                            kb_select_place_generate(len(travel['places']), full_id))


@router.callback_query(Helper.choosing_place, F.data.startswith(Commands.SELECTING_LOC.value))
@router.callback_query(Helper.choosing_hotel, F.data.startswith(Commands.SELECTING_LOC.value))
@router.callback_query(Helper.choosing_cafe, F.data.startswith(Commands.SELECTING_LOC.value))
async def selected_place_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    location_index = int(full_id.split(':')[2])
    travel_id_for_button = ':'.join(full_id.split(':')[0:2])
    state_data = await state.get_data()

    location = state_data['places'][location_index]

    await safe_message_edit(message, f'{Templates.WAITING_INFO.value}', kb_go_back_generate(travel_id_for_button))

    cur_state = await state.get_state()
    if cur_state == Helper.choosing_place:
        rets, places = await get_interesting_places(location[1], location[2])
        s = Templates.PLACES_TOVISIT.value
    elif cur_state == Helper.choosing_hotel:
        rets, places = await get_hotels(location[1], location[2], location[3], location[4], 2)
        s = Templates.HOTELS_TOVISIT.value
    else:
        rets, places = await get_cafes(location[1], location[2])
        s = Templates.CAFE_TOVISIT.value

    if not places:
        await safe_message_edit(message, f'{Templates.NOTHING_FOUND.value}', kb_go_back_generate(travel_id_for_button))
        return

    await safe_message_edit(message, f'{s}\n{rets}', kb_go_back_generate(travel_id_for_button))
    (is_good, res, img) = await make_markers_map(places, location[1], location[2])
    if not is_good:
        await message.answer(text=res)
        return

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)

    await state.set_state(None)
    await message.bot.send_photo(message.from_user.id, photo=BufferedInputFile(buffered.read(), filename='temp.png'))  # noqa #type: ignore
