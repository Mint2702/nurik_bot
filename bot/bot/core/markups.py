from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


BUTTON_START_NAMES = {
    "sing up": "Записаться",
    "about": "Обо мне",
    "decline": "Отменить запись",
}
BUTTON_CHOICE_NAMES = {"home": "Главное меню"}


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


def generate_free_times_markup(times: list):
    """ Generates ReplyKeyboardMarkup with available times for a client """

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    for time in times:
        button = KeyboardButton(time)
        markup.add(button)

    return markup
