from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from api.getplaces import get_interesting_places
from api.gettime import get_date_obj
from api.getweather import get_weather

from keyboards.travel_helper import kb_go_back_generate
from keyboards.travel_helper import kb_select_place_generate
from repository import TravelRepository
from templates.travel_helper import *
from templates.travel import TemplatesGen as TravelTemplatesGen
from restrictions import *
from commands.travel_helper import *
from utils import safe_message_edit

router = Router()


@router.callback_query(F.data.startswith(Commands.ATTRACTIONS_INFO.value))
async def get_places_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_id = int(full_id.split(':')[0])

    travel = await TravelRepository.select_by_id(travel_id)
    await state.update_data(places=travel['places'])
    await safe_message_edit(message, f'{Templates.SELECT_LOCATION.value}\n{TravelTemplatesGen.show_places(travel)}', kb_select_place_generate(len(travel['places']), full_id))


@router.callback_query(F.data.startswith(Commands.SELECTING_LOC.value))
async def selected_place_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    location_index = int(full_id.split(':')[2])
    state_data = await state.get_data()

    location = state_data['places'][location_index]
    print(await get_interesting_places(location[1], location[2]))
