from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


BUTTON_START_NAMES = {
    "timetable": "Мое расписание",
    "set_dates": "Установить рабочие дни",
    "set works": "Установить список услуг",
    "orders": "Мои записи",
}
BUTTON_CHOICE_NAMES = {"home": "Главное меню"}
WORK_TYPES = {
    "Мужская стрижка": 15,
    "Мужская стрижка с покраской": 30,
    "Женская окраска": 120,
}
CONFIRM_BUTTONS = {"yes": "✔️ Подтвердить", "no": "⛔ Отменить"}


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