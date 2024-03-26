from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton)
from aiogram.types.callback_query import CallbackQuery


def inline_button(s: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=s, callback_data=s)


def inline_button_with_id(s: str, id) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=s, callback_data=f'{s}:{id}')


def button_loc(s: str) -> KeyboardButton:
    return KeyboardButton(text=s, callback_data=s, request_location=True)


def button(s: str) -> KeyboardButton:
    return KeyboardButton(text=s, callback_data=s)


async def safe_message_edit(
    callback: CallbackQuery,
    new_text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> None:
    if callback.message is None:
        return
    try:
        await callback.message.edit_text(new_text, reply_markup=reply_markup, disable_web_page_preview=True)  # noqa #type: ignore
    except TelegramBadRequest as e:
        print(e)
        await callback.answer(None)
