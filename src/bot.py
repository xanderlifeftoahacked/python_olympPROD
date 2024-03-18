import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

import db
from routes.registration import router as registration_router
from routes.welcome import router as welcome_router
from routes.edit_profile import router as edit_profile_router
from routes.errors import router as error_router
from routes.travel_add import router as travel_add_router

TOKEN = str(getenv("BOT_TOKEN"))
TOKEN = '7046888785:AAHA_DVDVz3ry93xMQVDlvImi21zXtotyLw'

dp = Dispatcher()
dp.include_routers(registration_router, welcome_router,
                   edit_profile_router, error_router, travel_add_router)


async def main() -> None:
    await db.create_tables()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=["message", "edited_channel_post", "callback_query"])
    await db.delete_tables()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
