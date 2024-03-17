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

TOKEN = str(getenv("BOT_TOKEN"))

dp = Dispatcher()
dp.include_routers(registration_router, welcome_router, edit_profile_router)


async def main() -> None:
    await db.create_tables()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot, allowed_updates=["message", "edited_channel_post", "callback_query"])
    await db.delete_tables()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
