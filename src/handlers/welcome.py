from aiogram import Router
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from commands.common import CommonCommands
from templates.welcome import *
from commands.profile import *
from keyboards.common import kb_main

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(None)
    await message.answer("Добро пожаловать!", reply_markup=kb_main)


@router.message(F.text == CommonCommands.MAIN_MENU.value)
async def main_menu_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(None)
    await message.answer(text='Главное меню', reply_markup=kb_main)


@router.message(F.text == CommonCommands.INFO.value)
async def info_handler(message: Message) -> None:
    await message.answer('Мы над этим работаем...')