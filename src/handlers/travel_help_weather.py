from aiogram import Router
from io import BytesIO
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from api.getlocation import get_location_from_raw
from api.gettime import get_date_obj
from api.getweather import get_weather

from api.make_route import try_to_build_route
from fsm.travel_help_route import MakingRoute
from keyboards.travel_helper import kb_go_back_generate, kb_select_route_type
from repository import TravelRepository
from templates.travel_helper import *
from restrictions import *
from commands.travel_helper import *
from utils import safe_message_edit

router = Router()


@router.callback_query(F.data.startswith(Commands.WEATHER_INFO.value))
async def get_weather_handler(message: CallbackQuery, state: FSMContext) -> None:
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_id = int(full_id.split(':')[0])

    travel = await TravelRepository.select_by_id(travel_id)
    places = travel['places']
    rets = ''
    for id, place in enumerate(places, 1):
        s = await get_weather(place[1], place[2], get_date_obj(place[3]), get_date_obj(place[4]))
        rets += f'<b>{id}.</b>{s}'
    print(rets)
    await safe_message_edit(message, rets, kb_go_back_generate(full_id))
