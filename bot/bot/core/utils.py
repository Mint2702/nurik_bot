from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def generate_main_markup(full: bool = True) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_add = KeyboardButton("Записаться")

    if full:
        button_remove = KeyboardButton("Отменить запись")
        markup.add(button_add).add(button_remove)
    else:
        markup.add(button_add)

    return markup
