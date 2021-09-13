from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, callback_query
from aiogram_calendar import simple_cal_callback, SimpleCalendar

import uuid
from datetime import datetime, timedelta

from ..utils import build_start_markup, get_available_times
from ..markups import WORK_TYPES, generate_choice_markup, generate_free_times_markup
from ...dbs.requests import post_order


class States(StatesGroup):
    waiting_for_sign_up_or_decline = State()

    waiting_for_date = State()
    waiting_for_time = State()
    waiting_for_type = State()

    waiting_for_record = State()


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


async def process_simple_calendar(
    callback_query: CallbackQuery, callback_data: dict, state=States.waiting_for_date
):
    markup = generate_choice_markup()
    selected, date = await SimpleCalendar().process_selection(
        callback_query, callback_data
    )
    if selected and date >= datetime.now():
        await state.update_data(date=date)

        times = await get_available_times(date)
        markup = generate_free_times_markup(times)
        await callback_query.message.answer(
            f"Выберите подходящее для вас время:", reply_markup=markup
        )
        await States.waiting_for_time.set()
    else:
        await callback_query.message.answer(
            "Выбирать дату из прошлого нельзя:",
            reply_markup=await SimpleCalendar().start_calendar(),
        )
        await States.waiting_for_date.set()


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


def register_handlers_create_appointment(dp: Dispatcher):
    dp.register_message_handler(type_input, state=States.waiting_for_type)
    dp.register_callback_query_handler(
        process_simple_calendar,
        simple_cal_callback.filter(),
        state=States.waiting_for_date,
    )
    dp.register_message_handler(time_input, state=States.waiting_for_time)
