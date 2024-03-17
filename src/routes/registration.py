from aiogram import F, Router, types
from aiogram.types import CallbackQuery, Message, message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
import re

from messages import *
from restrictions import *
from repository import UserRepository
from utils import safe_message_edit
from keyboards import kb_edit_profile, kb_skip_setting, kb_is_valid, kb_reg
from fsm import RegisterProfile
from validation import age_regex
from maps_api.existance import check_city_existance, check_country_existance
from templates import profile

router = Router()


@router.message(F.text == m_register)
async def registration_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    if await UserRepository.id_exists(user_id):
        await message.answer('Посмотреть или редактировать', reply_markup=kb_edit_profile)
    else:
        await message.answer('Вы еще не зарегестрированы', reply_markup=kb_reg)


@router.callback_query(F.data == q_reg)
async def start_reg(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(RegisterProfile.choosing_age)
    await safe_message_edit(query, a_age)


@router.message(RegisterProfile.choosing_age)
async def age_handler(message: Message, state: FSMContext):
    age = str(message.text).strip()

    if not re.fullmatch(age_regex, age):
        await message.answer(text='Неправильно указан возраст, попробуйте еще')
        return

    await state.update_data(age=age)
    await message.answer(text=a_bio)
    await state.set_state(RegisterProfile.choosing_bio)


@router.message(RegisterProfile.choosing_bio)
async def bio_handler(message: Message, state: FSMContext) -> None:
    bio = str(message.text).strip()

    if len(bio) > MAX_BIO_LEN:
        await message.answer(text='Слишком длинный статус, попробуйте еще')
        return

    await state.update_data(bio=message.text)
    await message.answer(text=a_country)
    await state.set_state(RegisterProfile.choosing_country)


@router.message(RegisterProfile.choosing_country)
async def country_handler(message: Message, state: FSMContext) -> None:
    country = check_country_existance(str(message.text).strip())
    if not country:
        await message.answer(text='Страна не найдена, попробуйте еще')
        return

    await state.update_data(country=country)
    await message.answer(text=f'Правильно ли указана страна:\n{country}', reply_markup=kb_is_valid)


@router.callback_query(F.data == q_good, RegisterProfile.choosing_country)
async def country_good(message: CallbackQuery, state: FSMContext) -> None:
    await safe_message_edit(message, a_city)
    await state.set_state(RegisterProfile.choosing_city)


@router.callback_query(F.data == q_bad, RegisterProfile.choosing_country)
async def country_bad(message: CallbackQuery, state: FSMContext) -> None:
    await safe_message_edit(message, a_country)


@router.message(RegisterProfile.choosing_city)
async def city_handler(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    city = check_city_existance(
        user_data['country'], str(message.text).strip())
    if not city:
        await message.answer(text='Город не найден, попробуйте еще')
        return

    await state.update_data(city=city)
    await message.answer(text=f'Правильно ли указан город:\n{city}', reply_markup=kb_is_valid)


@router.callback_query(F.data == q_good, RegisterProfile.choosing_city)
async def city_good(message: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    user_data['id'] = message.from_user.id
    await UserRepository.add_one(user_data)
    await safe_message_edit(message, profile(user_data))
    await state.set_state(RegisterProfile.done)


@router.callback_query(F.data == q_bad, RegisterProfile.choosing_city)
async def city_bad(message: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(RegisterProfile.choosing_country)
    await safe_message_edit(message, a_country)
