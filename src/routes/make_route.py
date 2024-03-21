from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.fsm.context import FSMContext

from fsm.markups import AddMarkup, Markup
from repository import TravelRepository
from restrictions import *
from commands.markups import *
from keyboards.travel import kb_travel_menu
from keyboards.markups import kb_markup_actions_generate, kb_select_type, kb_go_back_generate, kb_show_markups_generate
from utils import safe_message_edit

router = Router()


@router.callback_query(F.data.startswith(Commands.LIST_MARKUPS.value))
async def list_markups_handler(message: CallbackQuery, state: FSMContext) -> None:
    user_id = message.from_user.id
    travel_id = int(message.data.split(':')[1])  # noqa #type: ignore
    full_id = message.data.split(':', 1)[1]  # noqa #type: ignore
    travel_data = await TravelRepository.select_by_id(travel_id)
    owner = travel_data['owner']
    if not travel_data['markups']:
        await safe_message_edit(message, Templates.NO_MARKUPS.value, kb_go_back_generate(full_id))  # noqa #type: ignore
        return
    if owner == user_id:
        await state.set_state(Markup.selecting)
        await safe_message_edit(message, Templates.SELECT_MARKUP.value, kb_show_markups_generate(travel_data['markups'], full_id))
        return

    else:
        visible_markups = [
            markup for markup in travel_data['markups'] if markup[2] == user_id or markup[1]]
        if not len(visible_markups):
            await safe_message_edit(message, Templates.NO_VISIBLE_MARKUPS.value, kb_go_back_generate(full_id))  # noqa #type: ignore
            return
        await state.set_state(Markup.selecting)
        await safe_message_edit(message, Templates.SELECT_MARKUP.value, kb_show_markups_generate(visible_markups, full_id))
