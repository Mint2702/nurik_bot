from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from ...logic.decorators import basic_message_handler_wrapper
from ...dbs.requests import delete_order
from ..states import States
from ...logic.common import build_start_markup


@basic_message_handler_wrapper
async def remove_order(message: types.Message, state: FSMContext):
    orders = dict(await state.get_data())["orders"]
    await state.finish()

    order_id = orders[message.text]
    await delete_order(order_id)

    markup = await build_start_markup(message.from_user.id)
    await message.reply("Запись отменена", reply_markup=markup)

    await States.waiting_for_sign_up_or_decline.set()


def register_handlers_remove_appointment(dp: Dispatcher):
    dp.register_message_handler(
        remove_order, state=States.waiting_for_appointment_choise
    )
