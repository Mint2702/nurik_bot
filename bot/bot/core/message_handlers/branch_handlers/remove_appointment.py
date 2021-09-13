from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup

from ..utils import build_start_markup, post_update_user
from ..markups import generate_orders_markup
from ...dbs.requests import get_user_orders, delete_order


class States(StatesGroup):
    waiting_for_appointment_choise = State()
    waiting_for_sign_up_or_decline = State()


async def orders_markup(user_id: int):
    orders = list(await get_user_orders(user_id))
    orders_list_dict = [dict(order) for order in orders]
    orders_list_str = [
        f"{order['work_type']} - {order['start_point'].strftime('%d %B  -  %H:%M')}"
        for order in orders_list_dict
    ]
    markup = generate_orders_markup(orders_list_str)

    return markup


async def remove_order(message: types.Message, state: FSMContext):
    await state.finish()
    await post_update_user(message)

    start_point = message.text
    print(start_point)
    await delete_order(message.from_user.id, start_point)

    await message.reply(
        "Запись отменена",
    )

    await States.waiting_for_sign_up_or_decline.set()


def register_handlers_remove_appointment(dp: Dispatcher):
    dp.register_message_handler(
        remove_order, state=States.waiting_for_appointment_choise
    )
