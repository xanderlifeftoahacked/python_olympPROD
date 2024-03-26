import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from api.getlocation import get_country_city, get_country_city_from_raw
from commands.common import CommonCommands
from commands.profile import *
from fsm.profile import SettingProfile
from keyboards.common import kb_main
from repository import UserRepository
from restrictions import *
from templates.profile import *
from utils import safe_message_edit
from validation import age_regex

router = Router()


@router.callback_query(F.data == Commands.PROFILE_DATA.value)
async def check_profile(query: CallbackQuery, state: FSMContext) -> None:
    user_data = await UserRepository.select_by_id(query.from_user.id)
    if user_data:
        copy = user_data
        copy['city'] = ', '.join(copy['city'][0:2])
        await safe_message_edit(query, TemplatesGen.profile(copy))


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
    (country, city, coords) = await get_country_city(lat, lon)

    if not country or not city:
        await message.answer(text=Templates.ST_BAD_LOC.value)
        return

    loc = TemplatesGen.location(country, city)
    await state.update_data(city=(country, city, coords))
    await UserRepository.update_by_id(message.from_user.id, {'city': (country, city, coords)})  # noqa #type: ignore
    await message.answer(text=TemplatesGen.city_changed(loc), reply_markup=kb_main)
    await state.set_state(None)


@router.message(SettingProfile.choosing_location, ~F.text.startswith('/'), F.text != CommonCommands.MAIN_MENU)
async def loc_chosen_str(message: Message, state: FSMContext) -> None:
    (country, city, coords) = await get_country_city_from_raw(message.text)  # noqa #type: ignore
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    if not country or not city:
        await message.answer(text=Templates.ST_BAD_LOC.value)
        return

    loc = TemplatesGen.location(country, city)

    await state.update_data(city=(country, city, coords))
    await UserRepository.update_by_id(message.from_user.id, {'city': (country, city, coords)})  # noqa #type: ignore
    await message.answer(text=TemplatesGen.city_changed(loc), reply_markup=kb_main)
    await state.set_state(None)


@router.message(SettingProfile.choosing_bio, ~F.text.startswith('/'))
async def bio_chosen(message: Message, state: FSMContext):
    await state.update_data(chooseen_age=message.text)
    bio = str(message.text).strip()
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    if len(bio) > MAX_BIO_LEN:
        await message.answer(text=Templates.ST_BAD_BIO.value)
        return

    await UserRepository.update_by_id(message.from_user.id, {'bio': bio})  # noqa #type: ignore
    await message.answer(text=Templates.ST_BIO_CHANGED.value)
    await state.set_state(None)


@router.message(SettingProfile.choosing_age, ~F.text.startswith('/'))
async def age_chosen(message: Message, state: FSMContext):
    await state.update_data(chooseen_age=message.text)
    age = str(message.text).strip()
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    if not re.fullmatch(age_regex, age):
        await message.answer(text=Templates.ST_BAD_AGE.value)
        return
    await UserRepository.update_by_id(message.from_user.id, {'age': age})  # noqa #type: ignore
    await message.answer(text=Templates.ST_AGE_CHANGED.value)
    await state.set_state(None)
