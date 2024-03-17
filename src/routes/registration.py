from aiogram import F, Router, types
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import re

from commands.profile import *
from templates.profile import *
from restrictions import *
from fsm.profile import *
from repository import UserRepository
from utils import safe_message_edit
from keyboards.profile import kb_edit_profile, kb_is_valid, kb_reg
from keyboards.common import kb_main
from keyboards.location import kb_get_location
from validation import age_regex
from maps_api.getlocation import get_country_city

router = Router()


@router.message(F.text == Commands.MY_PROFILE.value)
async def profile_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    if await UserRepository.id_exists(user_id):
        await message.answer(Templates.ST_LOOK_OR_EDIT.value, reply_markup=kb_edit_profile)
    else:
        await message.answer(Templates.ST_NOT_REGISTERED.value, reply_markup=kb_reg)


@router.callback_query(F.data == Commands.REGISTER.value)
async def start_reg(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(RegisterProfile.choosing_age)
    await safe_message_edit(query, Templates.GET_AGE.value)


@router.message(RegisterProfile.choosing_age)
async def age_handler(message: Message, state: FSMContext):
    age = str(message.text).strip()

    if not re.fullmatch(age_regex, age):
        await message.answer(text=Templates.ST_BAD_AGE.value)
        return

    await state.update_data(age=age)
    await message.answer(text=Templates.GET_BIO.value)
    await state.set_state(RegisterProfile.choosing_bio)


@router.message(RegisterProfile.choosing_bio)
async def bio_handler(message: Message, state: FSMContext) -> None:
    bio = str(message.text).strip()

    if len(bio) > MAX_BIO_LEN:
        await message.answer(text=Templates.ST_BAD_BIO.value)
        return

    await state.update_data(bio=message.text)
    await message.answer(text=Templates.GET_CITY.value, reply_markup=kb_get_location)
    await state.set_state(RegisterProfile.choosing_city)


@router.message(RegisterProfile.choosing_city, F.location)
async def city_handler(message: Message, state: FSMContext) -> None:
    if not message.location:
        await message.answer(text=Templates.ST_BAD_LOC.value)
        return

    lat = message.location.latitude
    lon = message.location.longitude
    (country, city) = get_country_city(lat, lon)
    loc = TemplatesGen.location(country, city)

    await state.update_data(city=loc)
    await message.answer(text=TemplatesGen.is_location_good(loc), reply_markup=kb_is_valid)


@router.callback_query(F.data == Commands.GOOD.value, RegisterProfile.choosing_city)
async def city_good(message: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    user_data['id'] = message.from_user.id
    await UserRepository.add_one(user_data)
    await message.bot.send_message(chat_id=message.message.chat.id, reply_markup=kb_main, text=Templates.ST_REGISTERED.value)
    await safe_message_edit(message, TemplatesGen.profile(user_data))
    await state.set_state(RegisterProfile.done)


@router.callback_query(F.data == Commands.BAD.value, RegisterProfile.choosing_city)
async def city_bad(message: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(RegisterProfile.choosing_city)
    await safe_message_edit(message, Templates.GET_CITY.value)
