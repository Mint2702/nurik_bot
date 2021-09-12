import uuid
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext, Dispatcher, storage
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime, timedelta
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
from loguru import logger

from core.settings import settings
from core.utils import build_start_markup, post_update_user, get_available_times
from core.states import States
from core.markups import (
    generate_choice_markup,
    generate_free_times_markup,
    BUTTON_START_NAMES,
    generate_work_types_markup,
    WORK_TYPES,
)
from core.dbs.requests import post_order


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


@dp.message_handler(Text(equals="Обо мне", ignore_case=True), state="*")
async def about(message: types.Message, state: FSMContext):
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


@dp.message_handler(state=States.waiting_for_sign_up_or_decline)
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


@dp.message_handler(state=States.waiting_for_type)
async def type_input(message: types.Message, state: FSMContext):
    if message.text not in WORK_TYPES.keys():
        await message.answer("Пожалуйста, выберите предложенный нужную Вам стрижку:")
        return
    else:
        interval = timedelta(minutes=WORK_TYPES[message.text])
        await state.update_data(work_type=message.text, work_interval=interval)
        await message.answer(
            f"Вы выбрали - {message.text}", reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(
            "Выберите дату:", reply_markup=await SimpleCalendar().start_calendar()
        )
        await States.waiting_for_date.set()


@dp.callback_query_handler(simple_cal_callback.filter(), state=States.waiting_for_date)
async def process_simple_calendar(
    callback_query: CallbackQuery, callback_data: dict, state=States.waiting_for_date
):
    markup = generate_choice_markup()
    selected, date = await SimpleCalendar().process_selection(
        callback_query, callback_data
    )
    if selected:
        await state.update_data(date=date)

        times = await get_available_times(date)
        markup = generate_free_times_markup(times)
        await callback_query.message.answer(
            f"Выберите подходящее для вас время:", reply_markup=markup
        )
        await States.waiting_for_time.set()


@dp.message_handler(state=States.waiting_for_time)
async def time_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    times = await get_available_times(data["date"])
    if message.text not in times:
        await message.answer("Пожалуйста, выберите предложенное на клавиатуре время.")
        return
    else:
        order_id = str(uuid.uuid4().hex)
        start_point = datetime.strptime(
            data["date"].strftime("%Y-%m-%d ") + message.text, "%Y-%m-%d %H:%M"
        )
        await state.update_data(
            start_point=start_point, user_id=message.from_user.id, id=order_id
        )
        data = await state.get_data()
        await post_order(data)

        markup = await build_start_markup(message.from_user.id)
        await message.answer(
            f"Спасибо за запись, Вы записаны на {data['start_point']}, {data['work_type']}",
            reply_markup=markup,
        )
        await States.waiting_for_sign_up_or_decline.set()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, loop=loop)
