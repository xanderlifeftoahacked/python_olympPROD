from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.fsm.context import FSMContext

from api.make_route import try_to_build_route
from keyboards.travel_helper import kb_go_back_generate, kb_select_route_type
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
    (is_good, res) = await try_to_build_route(locations)

    if not is_good:
        await safe_message_edit(message, res, kb_go_back_generate(full_id))

    await safe_message_edit(message, TemplatesGen.route_ref(res), kb_go_back_generate(full_id))
