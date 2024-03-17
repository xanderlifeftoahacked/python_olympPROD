from aiogram import F, Router, types
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import re

from commands.profile import *
from templates.profile import *
from restrictions import *
from repository import UserRepository
from utils import safe_message_edit
from keyboards.location import kb_get_location
from keyboards.common import kb_main
from fsm.profile import SettingProfile
from maps_api.getlocation import get_country_city
from validation import age_regex

router = Router()


@router.callback_query(F.data == Commands.PROFILE_DATA.value)
async def check_profile(query: CallbackQuery, state: FSMContext) -> None:
    user_data = await UserRepository.select_by_id(query.from_user.id)
    if user_data:
        await safe_message_edit(query, TemplatesGen.profile(user_data))


@router.callback_query(F.data == Commands.AGE.value)
async def age_handler(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SettingProfile.choosing_age)
    await safe_message_edit(query, Templates.GET_AGE.value)


@router.callback_query(F.data == Commands.BIO.value)
async def bio_handler(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SettingProfile.choosing_bio)
    await safe_message_edit(query, Templates.GET_BIO.value)


@router.callback_query(F.data == Commands.LOCATION.value)
async def loc_handler(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SettingProfile.choosing_location)
    await safe_message_edit(query, Templates.GET_CITY.value)


@router.message(SettingProfile.choosing_location, F.location)
async def loc_chosen(message: Message, state: FSMContext):
    if not message.location:
        await message.answer(text=Templates.ST_BAD_LOC.value)
        return

    lat = message.location.latitude
    lon = message.location.longitude
    (country, city) = get_country_city(lat, lon)
    loc = TemplatesGen.location(country, city)

    await state.update_data(city=loc)

    await UserRepository.update_by_id(message.from_user.id, {'city': city})  # noqa #type: ignore
    await message.answer(text=Templates.ST_CITY_CHANGED.value, reply_markup=kb_main)
    await state.set_state(None)


@router.message(SettingProfile.choosing_bio)
async def bio_chosen(message: Message, state: FSMContext):
    await state.update_data(chooseen_age=message.text)
    bio = str(message.text).strip()

    if len(bio) > MAX_BIO_LEN:
        await message.answer(text=Templates.ST_BAD_BIO.value)
        return

    await UserRepository.update_by_id(message.from_user.id, {'bio': bio})  # noqa #type: ignore
    await message.answer(text=Templates.ST_BIO_CHANGED.value)
    await state.set_state(None)


@router.message(SettingProfile.choosing_age)
async def age_chosen(message: Message, state: FSMContext):
    await state.update_data(chooseen_age=message.text)
    age = str(message.text).strip()
    if not re.fullmatch(age_regex, age):
        await message.answer(text=Templates.ST_BAD_AGE.value)
        return
    await UserRepository.update_by_id(message.from_user.id, {'age': age})  # noqa #type: ignore
    await message.answer(text='Возраст изменен')
    await state.set_state(None)
