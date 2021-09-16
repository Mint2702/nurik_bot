from aiogram.types import ReplyKeyboardMarkup

from ..dbs.requests import check_user_orders_exists
from ..message_handlers.markups import generate_main_markup


async def build_start_markup(user_id: int) -> ReplyKeyboardMarkup:
    """ Builds markup depends if the user has active orders or nah """

    user_orders_exists = dict(await check_user_orders_exists(user_id))
    if user_orders_exists["exists"]:
        markup = generate_main_markup(full=True)
    else:
        markup = generate_main_markup(full=False)

    return markup
