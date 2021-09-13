from datetime import datetime

from .utils import sql_task, build_sql_update_request


@sql_task
async def post_user(connection, user_data: dict):
    await connection.fetchrow(
        "INSERT INTO users VALUES ($1, $2, $3, $4);",
        user_data["id"],
        user_data["username"],
        user_data["first_name"],
        user_data["last_name"],
    )


@sql_task
async def post_order(connection, order_data: dict):
    await connection.fetchrow(
        "INSERT INTO orders VALUES ($1, $2, $3, $4, $5);",
        order_data["id"],
        order_data["start_point"],
        order_data["work_type"],
        order_data["work_interval"],
        order_data["user_id"],
    )


@sql_task
async def update_user(connection, user_data: dict, user_id: int):
    request = build_sql_update_request(user_data, user_id)
    row = await connection.fetchrow(request)

    return row


@sql_task
async def get_user_data(connection, user_id: int):
    row = await connection.fetchrow(
        "SELECT id, username, first_name, last_name FROM users WHERE id = $1;", user_id
    )

    return row


@sql_task
async def check_user_orders_exists(connection, user_id: int):
    row = await connection.fetchrow(
        "SELECT EXISTS(SELECT 1 FROM orders WHERE user_id = $1 AND start_point > NOW());",
        user_id,
    )

    return row


@sql_task
async def get_day_work_period(connection, day: datetime):
    row = await connection.fetchrow(
        "SELECT start_point, end_point FROM workperiods WHERE work_date = $1 AND start_point > NOW();",
        day,
    )

    return row


@sql_task
async def get_orders_during_day(
    connection, start_point: datetime.timestamp, end_point: datetime.timestamp
):
    row = await connection.fetch(
        "SELECT start_point, work_interval FROM orders WHERE start_point > $1 AND start_point < $2;",
        start_point,
        end_point,
    )

    return row
