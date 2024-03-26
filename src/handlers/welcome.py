from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from commands.common import CommonCommands
from keyboards.common import kb_main
from templates.welcome import Templates

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    await state.set_state(None)
    await message.answer(Templates.HELLO.value, reply_markup=kb_main)


@router.message(F.text == CommonCommands.MAIN_MENU.value)
async def main_menu_handler(message: Message, state: FSMContext) -> None:
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    await state.set_state(None)
    await message.answer(text=Templates.MAIN_MENU.value, reply_markup=kb_main)
