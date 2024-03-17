from aiogram import Router, types
from aiogram import F
from aiogram.types import Message
from aiogram.filters import CommandStart

from templates.welcome import *
from commands.profile import *
from keyboards.common import kb_main

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Добро пожаловать!", reply_markup=kb_main)


@router.message(F.text == Commands.INFO.value)
async def info_handler(message: Message) -> None:
    await message.answer('Мы над этим работаем...')
