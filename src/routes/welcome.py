from aiogram import Router, types
from aiogram import F
from aiogram.types import Message
from aiogram.filters import CommandStart


from messages import *
from utils import button

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
                                         [button(m_register)], [button(m_info)]])

    await message.answer("Добро пожаловать!", reply_markup=keyboard)


@router.message(F.text == m_info)
async def info_handler(message: Message) -> None:
    await message.answer('Мы над этим работаем...')
