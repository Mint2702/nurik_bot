from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from ...logic.common import build_start_markup
from ...logic.decorators import basic_message_handler_wrapper
from ..markups import (
    BUTTON_START_NAMES,
    generate_work_types_markup,
    generate_orders_markup,
)
from ...logic.orders import show_my_orders
from ...logic.orders import get_orders_dict
from ..states import States


@basic_message_handler_wrapper
async def process_start_command(message: types.Message, state: FSMContext):
    await message.reply(
        "Привет!\nЯ Нурик, твой парикхмахер. Запишись ко мне на стрижку или покраску, или посмотри на мои работы)",
    )

    await state.finish()
    await chose_action(message)


@basic_message_handler_wrapper
async def home(message: types.Message, state: FSMContext):
    await message.answer("Оформление заказа отменено")

    await state.finish()
    await chose_action(message)


@basic_message_handler_wrapper
async def action_chosen(message: types.Message, state: FSMContext):
    if message.text not in BUTTON_START_NAMES.values():
        await message.answer(
            "Пожалуйста, выберите действие, используя клавиатуру ниже."
        )
    elif message.text == BUTTON_START_NAMES["sing up"]:
        markup = generate_work_types_markup()
        await message.answer("Выберите тип нужной Вам стрижки:", reply_markup=markup)
        await States.waiting_for_type.set()
    elif message.text == BUTTON_START_NAMES["orders"]:
        message_text = await show_my_orders(message.from_user.id)
        markup = await build_start_markup(message.from_user.id)
        await message.answer(message_text, reply_markup=markup)
    elif message.text == BUTTON_START_NAMES["decline"]:
        orders = await get_orders_dict(message.from_user.id)
        await state.update_data(orders=orders)
        markup = generate_orders_markup(orders.keys())
        await message.answer("Выберите нужную запись для отмены:", reply_markup=markup)
        await States.waiting_for_appointment_choise.set()
    else:
        markup = await build_start_markup(message.from_user.id)
        await message.answer("Я Нурик", reply_markup=markup)


async def chose_action(message: types.Message):
    markup = await build_start_markup(message.from_user.id)
    await message.answer("Выберите действие:", reply_markup=markup)

    await States.waiting_for_sign_up_or_decline.set()


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands="start", state="*")
    dp.register_message_handler(home, commands="home", state="*")
    dp.register_message_handler(
        home, Text(equals="главное меню", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        action_chosen, Text(equals="Записаться", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        action_chosen, Text(equals="Отменить запись", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        action_chosen, Text(equals="Обо мне", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        action_chosen, Text(equals="Мои записи", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        action_chosen, state=States.waiting_for_sign_up_or_decline
    )
