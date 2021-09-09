from os import remove
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext, Dispatcher, storage
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from time import time
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
)

import asyncio
from aiogram_calendar import (
    simple_cal_callback,
    SimpleCalendar,
    dialog_cal_callback,
    DialogCalendar,
)

from core.settings import settings
from core.utils import (
    build_start_markup,
    generate_choice_markup,
    post_update_user,
    BUTTON_START_NAMES,
    BUTTON_CHOICE_NAMES,
)
from core.states import States


bot = Bot(token=settings.token)
# storage = RedisStorage2(settings.redis_host, settings.redis_port, password=settings.redis_password)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"], state="*")
async def process_start_command(message: types.Message, state: FSMContext):
    markup = await build_start_markup(message.from_user.id)
    await message.reply(
        "Привет!\nЯ Нурик, твой парикхмахер. Запишись ко мне на стрижку или покраску, или посмотри мои работы)",
        reply_markup=markup,
    )

    await state.finish()
    await post_update_user(message)

    await States.waiting_for_sign_up_or_decline.set()


@dp.message_handler(state=States.waiting_for_sign_up_or_decline)
async def action_chosen(message: types.Message, state: FSMContext):
    if message.text not in BUTTON_START_NAMES.values():
        await message.answer(
            "Пожалуйста, выберите действие, используя клавиатуру ниже."
        )
        return
    elif message.text == BUTTON_START_NAMES["sing up"]:
        await message.answer(
            "Выберите дату:", reply_markup=await SimpleCalendar().start_calendar()
        )
        await States.waiting_for_date.set()
    else:
        markup = await build_start_markup(message.from_user.id)
        await message.answer("Я Нурик", reply_markup=markup)


@dp.callback_query_handler(simple_cal_callback.filter(), state=States.waiting_for_date)
async def process_simple_calendar(
    callback_query: CallbackQuery, callback_data: dict, state=States.waiting_for_date
):
    markup = generate_choice_markup()
    selected, date = await SimpleCalendar().process_selection(
        callback_query, callback_data
    )
    if selected:
        await state.update_data(date=date.strftime("%Y-%m-%d"))
        await callback_query.message.answer(
            f"Выберите подходящее для вас время:", reply_markup=markup
        )
        await States.waiting_for_time.set()


@dp.message_handler(Text(equals="Обо мне", ignore_case=True), state="*")
async def home(message: types.Message, state: FSMContext):
    markup = await build_start_markup(message.from_user.id)
    await message.answer("Я Нурик", reply_markup=markup)

    await state.finish()
    await States.waiting_for_sign_up_or_decline.set()


@dp.message_handler(Text(equals="главное меню", ignore_case=True), state="*")
async def home(message: types.Message, state: FSMContext):
    markup = await build_start_markup(message.from_user.id)
    await message.answer("Оформление заказа отменено", reply_markup=markup)

    await post_update_user(message)

    await state.finish()
    await States.waiting_for_sign_up_or_decline.set()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, loop=loop)
