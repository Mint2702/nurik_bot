from .utils import sql_task


@sql_task
async def post_user(connection, user_data: dict):
    row = await connection.fetchrow(
        "INSERT INTO users VALUES ($1, $2, $3, $4);",
        user_data["id"],
        user_data["username"],
        user_data["first_name"],
        user_data["last_name"],
    )

    return row


@sql_task
async def update_user(connection, user_data: dict, user_id: int):
    def build_sql_request(user_data: dict, user_id: int) -> str:
        request = "UPDATE users SET "
        for key, value in user_data.items():
            if type(value) is str:
                request += f"{str(key)} = '{str(value)}', "
            elif value is None:
                request += f"{str(key)} = null, "
            else:
                request += f"{str(key)} = {str(value)}, "

        request = request[:-2]
        request += f" WHERE id = {str(user_id)};"

        return request

    request = build_sql_request(user_data, user_id)
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
