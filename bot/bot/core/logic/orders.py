from ..dbs.requests import get_user_orders
from .utils import tz


async def get_orders(user_id: int) -> list:
    orders = await get_user_orders(user_id)
    new_orders = []
    for order in orders:
        order = dict(order)
        order["start_point"] = order["start_point"].astimezone(tz)
        new_orders.append(order)

    return new_orders


async def show_my_orders(user_id: int) -> str:
    orders = await get_orders(user_id)

    message = "Вы записаны:\n"
    for order in orders:
        message += f"    {order['work_type']} - {order['start_point'].strftime('%d %B  -  %H:%M')}\n"

    return message
