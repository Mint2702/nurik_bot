from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from ...logic.orders import get_orders
from ...logic.decorators import basic_message_handler_wrapper
from ..markups import generate_orders_markup
from ...dbs.requests import delete_order
from ..states import States


async def orders_markup(user_id: int):
    orders = await get_orders(user_id)
    orders_list_str = [
        f"{order['work_type']} - {order['start_point'].strftime('%d %B  -  %H:%M')}"
        for order in orders
    ]
    markup = generate_orders_markup(orders_list_str)

    return markup


@basic_message_handler_wrapper
async def remove_order(message: types.Message, state: FSMContext):
    await state.finish()

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
