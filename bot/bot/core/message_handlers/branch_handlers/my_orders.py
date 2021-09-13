# from babel.dates import format_date, format_datetime, format_time

from ...dbs.requests import get_user_orders


async def show_orders(user_id: int) -> str:
    orders = list(await get_user_orders(user_id))
    orders = [dict(order) for order in orders]

    message = "Вы записаны:\n"
    for order in orders:
        message += (
            f"    {order['work_type']} - {order['start_point'].strftime('%d %B')}\n"
        )

    return message
