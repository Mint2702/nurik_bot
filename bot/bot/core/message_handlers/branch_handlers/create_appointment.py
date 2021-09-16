from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram_calendar import simple_cal_callback, SimpleCalendar

import uuid
from datetime import datetime, timedelta

from ...logic.common import build_start_markup
from ...logic.utils import get_available_times
from ...logic.decorators import basic_message_handler_wrapper
from ..markups import (
    WORK_TYPES,
    CONFIRM_BUTTONS,
    generate_choice_markup,
    generate_free_times_markup,
    generate_confirm_markup,
)
from ...dbs.requests import post_order
from ..states import States


@basic_message_handler_wrapper
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
        if times is None:
            markup = await build_start_markup(callback_query.message.from_user.id)
            await callback_query.message.answer(
                "К сожалению, Нурик не работает в этот день", reply_markup=markup
            )
            await States.waiting_for_sign_up_or_decline.set()
            return
        else:
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


@basic_message_handler_wrapper
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

        markup = generate_confirm_markup()
        await message.answer(
            f"Проверьте и подтвердите данные по Вашей записи:\nВы записаны на {start_point}, {data['work_type']}",
        )
        await message.answer("Подтвердить?", reply_markup=markup)
        await States.waiting_for_confirm.set()


@basic_message_handler_wrapper
async def confirm(message: types.Message, state: FSMContext):
    if message.text not in CONFIRM_BUTTONS.values():
        await message.answer("Пожалуйста, подтвердите или отмените вашу запись.")
        return
    elif message.text == CONFIRM_BUTTONS["yes"]:
        data = await state.get_data()
        await state.reset_data()
        await post_order(data)

        markup = await build_start_markup(message.from_user.id)
        await message.answer(
            "Спасибо за запись!",
            reply_markup=markup,
        )
        await States.waiting_for_sign_up_or_decline.set()
    else:
        await state.reset_data()

        markup = await build_start_markup(message.from_user.id)
        await message.answer(
            "Запись отменена.",
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
    dp.register_message_handler(confirm, state=States.waiting_for_confirm)
