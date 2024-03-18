from collections.abc import Awaitable, Callable
from typing import Any, Dict
from aiogram import BaseMiddleware, Bot
from aiogram.types import CallbackQuery, Message, User
from sqlalchemy.inspection import exc
from geopy import exc

from templates.errors import Errors


class ExcHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],  # noqa #type: ignore
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        try:
            return await handler(event, data)

        except exc.GeocoderServiceError:
            print('CHECK GEOCODER! TRY TO RESTART/TURN OFF VPN')
            return await event.answer(Errors.SERVICE_GEO.value, show_alert=True)

        except Exception as e:
            print(e)
            return await event.answer(Errors.WENT_WRONG.value, show_alert=True)
