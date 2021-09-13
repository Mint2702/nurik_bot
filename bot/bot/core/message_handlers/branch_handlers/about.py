from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup

from ..utils import build_start_markup, post_update_user
from ..markups import BUTTON_START_NAMES, generate_work_types_markup


class States(StatesGroup):
    waiting_for_sign_up_or_decline = State()

    waiting_for_type = State()


async def process_start_command(message: types.Message, state: FSMContext):
    await message.reply(
        "Привет!\nЯ Нурик, твой парикхмахер. Запишись ко мне на стрижку или покраску, или посмотри мои работы)",
    )

    await state.finish()
    await post_update_user(message)

    await chose_action(message)


async def home(message: types.Message, state: FSMContext):
    await message.answer("Оформление заказа отменено")

    await post_update_user(message)

    await state.finish()
    await chose_action(message)


async def action_chosen(message: types.Message, state: FSMContext):
    if message.text not in BUTTON_START_NAMES.values():
        await message.answer(
            "Пожалуйста, выберите действие, используя клавиатуру ниже."
        )
        return
    elif message.text == BUTTON_START_NAMES["sing up"]:
        markup = generate_work_types_markup()
        await message.answer("Выберите тип нужной Вам стрижки:", reply_markup=markup)
        await States.waiting_for_type.set()
    else:
        markup = await build_start_markup(message.from_user.id)
        await message.answer("Я Нурик", reply_markup=markup)


async def chose_action(message: types.Message):
    markup = await build_start_markup(message.from_user.id)
    await message.answer("Выберите действие:", reply_markup=markup)

    await post_update_user(message)

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
        action_chosen, state=States.waiting_for_sign_up_or_decline
    )
