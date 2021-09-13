from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


BUTTON_START_NAMES = {
    "sing up": "Записаться",
    "about": "Обо мне",
    "decline": "Отменить запись",
    "orders": "Мои записи",
}
BUTTON_CHOICE_NAMES = {"home": "Главное меню"}
WORK_TYPES = {
    "Мужская стрижка": 15,
    "Мужская стрижка с покраской": 30,
    "Женская окраска": 120,
}


def generate_main_markup(full: bool = True) -> ReplyKeyboardMarkup:
    """ Generates ReplyKeyboardMarkup with one or two buttons depends on the 'full' arguement """

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_add = KeyboardButton(BUTTON_START_NAMES["sing up"])
    button_about = KeyboardButton(BUTTON_START_NAMES["about"])

    if full:
        button_remove = KeyboardButton(BUTTON_START_NAMES["decline"])
        button_orders = KeyboardButton(BUTTON_START_NAMES["orders"])
        markup.add(button_add, button_remove).add(button_about, button_orders)
    else:
        markup.add(button_add).add(button_about)

    return markup


def generate_choice_markup() -> ReplyKeyboardMarkup:
    """ Generates ReplyKeyboardMarkup with 'back' and 'home' buttons """

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_home = KeyboardButton(BUTTON_CHOICE_NAMES["home"])

    markup.add(button_home)

    return markup


def generate_free_times_markup(times: list) -> ReplyKeyboardMarkup:
    """ Generates ReplyKeyboardMarkup with available times for a client """

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    for time in times:
        button = KeyboardButton(time)
        markup.add(button)

    button_home = KeyboardButton(BUTTON_CHOICE_NAMES["home"])
    markup.add(button_home)

    return markup


def generate_work_types_markup() -> ReplyKeyboardMarkup:
    """ Generates ReplyKeyboardMarkup with work types """

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    for type in WORK_TYPES.keys():
        button = KeyboardButton(type)
        markup.add(button)

    button_home = KeyboardButton(BUTTON_CHOICE_NAMES["home"])
    markup.add(button_home)

    return markup


def generate_orders_markup(orders: list) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    for order in orders:
        button = KeyboardButton(order)
        markup.add(button)

    button_home = KeyboardButton(BUTTON_CHOICE_NAMES["home"])
    markup.add(button_home)

    return markup
