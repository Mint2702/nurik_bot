from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from loguru import logger

from .dbs.requests import post_user, update_user, get_user_data
from core.dbs.requests import check_user_orders_exists


BUTTON_START_NAMES = {
    "sing up": "Записаться",
    "about": "Обо мне",
    "decline": "Отменить запись",
}
BUTTON_CHOICE_NAMES = {"home": "Главное меню"}


async def build_start_markup(user_id: int) -> ReplyKeyboardMarkup:
    """ Builds markup depends if the user has active orders or nah """

    user_orders_exists = dict(await check_user_orders_exists(user_id))
    if user_orders_exists["exists"]:
        markup = generate_main_markup(full=True)
    else:
        markup = generate_main_markup(full=False)

    return markup


def generate_main_markup(full: bool = True) -> ReplyKeyboardMarkup:
    """ Generates ReplyKeyboardMarkup with one or two buttons depends on the 'full' arguement """

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_add = KeyboardButton(BUTTON_START_NAMES["sing up"])
    button_about = KeyboardButton(BUTTON_START_NAMES["about"])

    if full:
        button_remove = KeyboardButton(BUTTON_START_NAMES["decline"])
        markup.add(button_add).add(button_remove).add(button_about)
    else:
        markup.add(button_add).add(button_about)

    return markup


def generate_choice_markup() -> ReplyKeyboardMarkup:
    """ Generates ReplyKeyboardMarkup with 'back' and 'home' buttons """

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_home = KeyboardButton(BUTTON_CHOICE_NAMES["home"])

    markup.add(button_home)

    return markup


async def post_update_user(message):
    """
    Adds user to db if the user is new. Checks if current user info is the same as the data in the db.
    Updates user data if needed.
    """

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
