import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from api.getlocation import get_country_city, get_country_city_from_raw
from commands.common import CommonCommands
from commands.profile import Commands
from fsm.profile import RegisterProfile
from keyboards.common import kb_main
from keyboards.location import kb_get_location
from keyboards.profile import kb_edit_profile, kb_is_valid, kb_reg
from repository import UserRepository
from restrictions import *
from templates.profile import Templates, TemplatesGen
from utils import safe_message_edit
from validation import age_regex

router = Router()


@router.message(F.text == CommonCommands.MY_PROFILE.value)
async def profile_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id  # noqa #type: ignore
    await message.bot.delete_message(chat_id=user_id, message_id=message.message_id)  # noqa #type: ignore
    await state.set_state(None)
    if await UserRepository.id_exists(user_id):
        await message.answer(Templates.ST_LOOK_OR_EDIT.value, reply_markup=kb_edit_profile)
    else:
        await message.answer(Templates.ST_NOT_REGISTERED.value, reply_markup=kb_reg)


@router.callback_query(F.data == Commands.REGISTER.value)
async def start_reg(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(RegisterProfile.choosing_age)
    await safe_message_edit(query, Templates.GET_AGE.value)


@router.message(RegisterProfile.choosing_age, ~F.text.startswith('/'))
async def age_handler(message: Message, state: FSMContext):
    age = str(message.text).strip()

    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    if not re.fullmatch(age_regex, age):
        await message.answer(text=Templates.ST_BAD_AGE.value)
        return

    await state.update_data(age=age)
    await message.answer(text=Templates.GET_BIO.value)
    await state.set_state(RegisterProfile.choosing_bio)


@router.message(RegisterProfile.choosing_bio, ~F.text.startswith('/'))
async def bio_handler(message: Message, state: FSMContext) -> None:
    bio = str(message.text).strip()

    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
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
    (country, city, coords) = await get_country_city(lat, lon)
    if not country or not city:
        await message.answer(text=Templates.ST_BAD_LOC.value)
        return

    loc = TemplatesGen.location(country, city)

    await state.update_data(city=(country, city, coords))
    await message.answer(text=TemplatesGen.is_location_good(loc), reply_markup=kb_is_valid)


@router.message(RegisterProfile.choosing_city, ~F.text.startswith('/'), F.text != CommonCommands.MAIN_MENU.value)
async def city_handler_str(message: Message, state: FSMContext) -> None:
    (country, city, coords) = await get_country_city_from_raw(message.text)  # noqa #type: ignore
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)  # noqa #type: ignore
    if not country or not city:
        await message.answer(text=Templates.ST_BAD_LOC.value)
        return

    loc = TemplatesGen.location(country, city)

    await state.update_data(city=(country, city, coords))
    await message.answer(text=TemplatesGen.is_location_good(loc), reply_markup=kb_is_valid)


@router.callback_query(F.data == CommonCommands.GOOD.value, RegisterProfile.choosing_city)
async def city_good(message: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    user_data['id'] = message.from_user.id
    await UserRepository.add_one(user_data)

    user_data['city'] = user_data['city'][0] + ', ' + user_data['city'][1]
    await message.bot.send_message(chat_id=message.message.chat.id, reply_markup=kb_main, text=Templates.ST_REGISTERED.value)  # noqa #type: ignore
    await safe_message_edit(message, TemplatesGen.profile(user_data))
    await state.set_state(None)


@router.callback_query(F.data == CommonCommands.BAD.value, RegisterProfile.choosing_city)
async def city_bad(message: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(RegisterProfile.choosing_city)
    await safe_message_edit(message, Templates.GET_CITY.value)
