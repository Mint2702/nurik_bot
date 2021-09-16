from datetime import datetime

from .utils import sql_task, build_sql_update_request


@sql_task
async def post_admin(connection, user_data: dict):
    await connection.fetchrow(
        "INSERT INTO users VALUES ($1, $2, $3, $4, True);",
        user_data["id"],
        user_data["username"],
        user_data["first_name"],
        user_data["last_name"],
    )


@sql_task
async def update_user_to_admin(connection, user_id: int):
    await connection.fetchrow(
        "UPDATE users SET is_admin = True WHERE id = $1;", user_id
    )


@sql_task
async def check_user_is_admin(connection, user_id: int):
    row = await connection.fetchrow(
        "SELECT is_admin FROM users WHERE id = $1;",
        user_id,
    )

    return row


@sql_task
async def get_day_work_period(connection, day: datetime):
    row = await connection.fetchrow(
        "SELECT start_point, end_point FROM workperiods WHERE work_date = $1 AND start_point >= NOW();",
        day,
    )

    return row


@sql_task
async def get_orders_during_day(
    connection, start_point: datetime.timestamp, end_point: datetime.timestamp
):
    row = await connection.fetch(
        "SELECT start_point, work_interval FROM orders WHERE start_point >= $1 AND start_point <= $2;",
        start_point,
        end_point,
    )

    return row


@sql_task
async def get_user_orders(connection, user_id: int):
    row = await connection.fetch(
        "SELECT start_point, work_type, id FROM orders WHERE user_id = $1 AND start_point >= NOW();",
        user_id,
    )

    return row


@sql_task
async def delete_order(connection, id: str):
    row = await connection.fetch("DELETE FROM orders WHERE id = $1;", id)

    return row
