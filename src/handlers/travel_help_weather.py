from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from api.gettime import get_date_obj
from api.getweather import get_weather
from commands.travel_helper import Commands
from keyboards.travel_helper import kb_go_back_generate
from repository import TravelRepository
from restrictions import *
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
    await safe_message_edit(message, rets, kb_go_back_generate(full_id))
