import asyncio
import logging
import sys
from os import getenv

import httpx
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from geopy.exc import GeocoderServiceError

import db
from handlers.markups import router as markup_router
from handlers.profile_add import router as registration_router
from handlers.profile_edit import router as edit_profile_router
from handlers.translate import router as translate_router
from handlers.travel_add import router as travel_add_router
from handlers.travel_edit import router as travel_edit_router
from handlers.travel_help_common import router as travel_help_common_router
from handlers.travel_help_route import router as travel_help_route_router
from handlers.travel_help_weather import router as travel_help_weather_router
from handlers.welcome import router as welcome_router
from lib.openmeteo.exceptions import OpenMeteoError
from templates.errors import Errors

TOKEN = str(getenv("BOT_TOKEN"))

dp = Dispatcher()
dp.include_routers(registration_router, welcome_router,
                   edit_profile_router, travel_add_router,
                   travel_edit_router, markup_router,
                   travel_help_route_router, travel_help_weather_router,
                   travel_help_common_router, translate_router)


@dp.error(ExceptionTypeFilter(GeocoderServiceError))
async def catch_geocoder_exc(event: ErrorEvent):
    print('GEOCODER NOT WORKING')
    if event.update.message:
        await event.update.message.bot.send_message(  # noqa #type: ignore
            event.update.message.from_user.id, Errors.SERVICE_GEO.value)  # noqa #type: ignore
    else:
        await event.update.callback_query.message.bot.send_message(  # noqa #type: ignore
            event.update.callback_query.from_user.id, Errors.SERVICE_GEO.value)  # noqa #type: ignore


@dp.error(ExceptionTypeFilter(OpenMeteoError))
async def catch_meteo_exc(event: ErrorEvent):
    print('OPENMETEO NOT WORKING')
    if event.update.message:
        await event.update.message.bot.send_message(  # noqa #type: ignore
            event.update.message.from_user.id, Errors.SERVICE_METEO.value)  # noqa #type: ignore
    else:
        await event.update.callback_query.message.bot.send_message(  # noqa #type: ignore
            event.update.callback_query.from_user.id, Errors.SERVICE_METEO.value)  # noqf #type: ignore


@dp.error(ExceptionTypeFilter(httpx.ConnectTimeout))
@dp.error(ExceptionTypeFilter(httpx.ReadTimeout))
async def catch_timeout_exc(event: ErrorEvent):
    print('CONNECTION TIMEOUT')
    if event.update.message:
        await event.update.message.bot.send_message(  # noqa #type: ignore
            event.update.message.from_user.id, Errors.TIMEOUT.value)  # noqa #type: ignore
    else:
        await event.update.callback_query.message.bot.send_message(  # noqa #type: ignore
            event.update.callback_query.from_user.id, Errors.TIMEOUT.value)  # noqf #type: ignore


@dp.error()
async def catch_all_exc(event: ErrorEvent):
    if event.update.message:
        await event.update.message.bot.send_message(  # noqa #type: ignore
            event.update.message.from_user.id, Errors.WENT_WRONG.value)  # noqa #type: ignore
    else:
        await event.update.callback_query.message.bot.send_message(  # noqa #type: ignore
            event.update.callback_query.from_user.id, Errors.WENT_WRONG.value)  # noqf #type: ignore


async def main() -> None:
    await db.create_tables()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=["message", "edited_channel_post", "callback_query"])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
