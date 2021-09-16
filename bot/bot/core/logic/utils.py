from aiogram.types import ReplyKeyboardMarkup
from loguru import logger
from datetime import datetime, timedelta
from pytz import timezone

from ..dbs.requests import (
    get_day_work_period,
    get_orders_during_day,
    check_user_orders_exists,
)
from ..message_handlers.markups import generate_main_markup


tz = timezone("Europe/Moscow")


async def build_start_markup(user_id: int) -> ReplyKeyboardMarkup:
    """ Builds markup depends if the user has active orders or nah """

    user_orders_exists = dict(await check_user_orders_exists(user_id))
    if user_orders_exists["exists"]:
        markup = generate_main_markup(full=True)
    else:
        markup = generate_main_markup(full=False)

    return markup


def get_15mins_periods(start_point: datetime, end_point: datetime) -> list:
    """ Creates a list of 15-mins ranges from start to end points of a working day """

    work_periods = []
    while start_point <= end_point:
        work_periods.append(start_point.strftime("%H:%M"))
        start_point += timedelta(minutes=15)

    return work_periods


def get_unavailable_periods(orders: list) -> list:
    """ Creates a list of intervals that are already taken by another user """

    unavailable_times = []
    for order in orders:
        periods = get_15mins_periods(
            order["start_point"].astimezone(tz),
            order["start_point"].astimezone(tz) + order["work_interval"],
        )
        for i in range(len(periods) - 1):
            unavailable_times.append(periods[i])

    return unavailable_times


async def get_available_times(date: datetime) -> list:
    """ Creates a list of available start times for a session """

    work_period = await get_day_work_period(date)
    if work_period is not None:
        start_point, end_point = (
            dict(work_period)["start_point"].astimezone(tz),
            dict(work_period)["end_point"].astimezone(tz),
        )

        all_work_periods = get_15mins_periods(start_point, end_point)

        orders = await get_orders_during_day(start_point, end_point)
        orders = [dict(order) for order in orders]

        unavailable_times = get_unavailable_periods(orders)

        return sorted(list(set(all_work_periods) - set(unavailable_times)))
    else:
        return None
