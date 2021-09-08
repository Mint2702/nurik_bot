from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from loguru import logger

from .dbs.requests import post_user, update_user, get_user_data


def generate_main_markup(full: bool = True) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_add = KeyboardButton("Записаться")

    if full:
        button_remove = KeyboardButton("Отменить запись")
        markup.add(button_add).add(button_remove)
    else:
        markup.add(button_add)

    return markup


async def post_update_user(message):
    user_current_data = dict(await get_user_data(message.from_user.id))
    user_old_data = {
        "id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
    }
    if user_current_data is None:
        await post_user(user_old_data)
    else:
        if user_current_data != user_old_data:
            update_values = {
                key: value
                for key, value in user_old_data.items()
                if user_current_data[key] != value
            }
            await update_user(update_values, message.from_user.id)