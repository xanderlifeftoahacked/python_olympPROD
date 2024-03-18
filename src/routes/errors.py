from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import ExceptionTypeFilter
from geopy.exc import GeocoderTimedOut

router = Router()


@router.error(ExceptionTypeFilter(GeocoderTimedOut))
async def handle_my_custom_exception(event: GeocoderTimedOut, message: Message):
    await message.answer("Oops, something went wrong!")

#
# @router.error()
# async def error_handler(event: ErrorEvent):
#     logger.critical("Critical error caused by %s",
#                     event.exception, exc_info=True)
#     # do something with error
#     ...
