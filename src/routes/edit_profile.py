from aiogram import F, Router, types
from aiogram.types import CallbackQuery, Message, message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
import re

from messages import *
from restrictions import *
from repository import UserRepository
from utils import safe_message_edit
from templates import profile
from keyboards import kb_edit_profile, kb_skip_setting, kb_is_valid
from fsm import SettingProfile
from maps_api.existance import check_city_existance
from validation import age_regex

router = Router()


@router.callback_query(F.data == q_profile)
async def check_profile(query: CallbackQuery, state: FSMContext) -> None:
    # await UserRepository.update_by_id(message.from_user.id, {'age': message.text})
    user_data = await UserRepository.select_by_id(query.from_user.id)
    if user_data:
        await safe_message_edit(query, profile(user_data))


@router.callback_query(F.data == m_age)
async def age_handler(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SettingProfile.choosing_age)
    await safe_message_edit(query, a_age)


@router.callback_query(F.data == m_bio)
async def bio_handler(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SettingProfile.choosing_bio)
    await safe_message_edit(query, a_bio)


@router.callback_query(F.data == m_age)
async def age_handler(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SettingProfile.choosing_age)
    await safe_message_edit(query, a_age)


@router.callback_query(F.data == m_location)
async def loc_handler(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SettingProfile.choosing_location)
    await safe_message_edit(query, 'Напишите страну и город, разделенные пробелом')


@router.message(SettingProfile.choosing_location)
async def loc_chosen(message: Message, state: FSMContext):
    await state.update_data(chooseen_age=message.text)
    data = str(message.text).strip().split(' ')

    if len(data) < 2:
        await message.answer(text='Введите данные в формате: "Россия Москва"')
        return

    city = check_city_existance(data[0], data[1])

    if not city:
        await message.answer(text='Город не найден, попробуйте еще')
        return

    await UserRepository.update_by_id(message.from_user.id, {'city': city})
    await message.answer(text='Город изменен')
    await state.set_state(None)


@router.message(SettingProfile.choosing_bio)
async def bio_chosen(message: Message, state: FSMContext):
    await state.update_data(chooseen_age=message.text)
    bio = str(message.text).strip()

    if len(bio) > MAX_BIO_LEN:
        await message.answer(text='Слишком длинный статус, попробуйте еще')
        return

    await UserRepository.update_by_id(message.from_user.id, {'bio': bio})
    await message.answer(text='Статус изменен')
    await state.set_state(None)


@router.message(SettingProfile.choosing_age)
async def age_chosen(message: Message, state: FSMContext):
    await state.update_data(chooseen_age=message.text)
    age = str(message.text).strip()
    if not re.fullmatch(age_regex, age):
        await message.answer(text='Неправильно указан возраст, попробуйте еще')
        return
    await UserRepository.update_by_id(message.from_user.id, {'age': age})
    await message.answer(text='Возраст изменен')
    await state.set_state(None)
