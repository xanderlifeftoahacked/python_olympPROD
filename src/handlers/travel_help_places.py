from io import BytesIO
from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from api.getplaces import get_interesting_places

from api.getmap import make_markers_map
from keyboards.travel_helper import kb_go_back_generate
from keyboards.travel_helper import kb_select_place_generate
from repository import TravelRepository
from templates.travel_helper import *
from templates.travel import TemplatesGen as TravelTemplatesGen
from fsm.travel_help import Helper
from restrictions import *
from commands.travel_helper import *
from utils import safe_message_edit

router = Router()


@router.callback_query(F.data.startswith(Commands.ATTRACTIONS_INFO.value))
async def get_places_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_id = int(full_id.split(':')[0])

    travel = await TravelRepository.select_by_id(travel_id)
    await state.set_state(Helper.choosing_place)
    await state.update_data(places=travel['places'])
    await safe_message_edit(message, f'{Templates.SELECT_LOCATION.value}\n{TravelTemplatesGen.show_places(travel)}',
                            kb_select_place_generate(len(travel['places']), full_id))


@router.callback_query(Helper.choosing_place, F.data.startswith(Commands.SELECTING_LOC.value))
async def selected_place_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    location_index = int(full_id.split(':')[2])
    travel_id_for_button = ':'.join(full_id.split(':')[0:2])
    state_data = await state.get_data()
    location = state_data['places'][location_index]
    rets, places = await get_interesting_places(location[1], location[2])

    await safe_message_edit(message, f'{Templates.PLACES_TOVISIT.value}\n{rets}', kb_go_back_generate(travel_id_for_button))

    (is_good, res, img) = await make_markers_map(places, location[1], location[2])
    if not is_good:
        await message.answer(text=res)

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)

    await state.set_state(None)
    await message.bot.send_photo(message.from_user.id, photo=BufferedInputFile(buffered.read(), filename='temp.png'))  # noqa #type: ignore
