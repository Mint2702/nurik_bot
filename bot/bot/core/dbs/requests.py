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
        print(request)

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
async def check_exams_exists(connection, exam_id: int):
    row = await connection.fetchrow(
        "SELECT EXISTS (SELECT 1 FROM exams WHERE id = $1);",
        exam_id,
    )

    return row


@sql_task
async def get_queue_status(connection, exam_id: int):
    row = await connection.fetchrow(
        "SELECT EXISTS (SELECT 1 FROM exam_verdicts WHERE exam = $1);",
        exam_id,
    )

    return row


@sql_task
async def get_queue_result(connection, exam_id: int):
    row = await connection.fetchrow(
        "SELECT admittance, verdicts, verdict_comment FROM full_exams_history WHERE exam_id = $1;",
        exam_id,
    )

    return row


@sql_task
async def post_exam_record(connection, record_data: dict):
    row = await connection.fetchrow(
        "SELECT new_exam ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11);",
        record_data["terminal_id"],
        record_data["driver_id"],
        record_data["exam_datetime"],
        record_data["duration"],
        record_data["type"],
        record_data["pressure_upper"],
        record_data["pressure_lower"],
        record_data["heart_rate"],
        record_data["temperature"],
        record_data["alcohol"],
        str(record_data["complaints_json"]),
    )

    return row  # Returns all exam file(with id)


@sql_task
async def update_exam_record(connection, record_id: int, file_id: str, field: str):
    row = await connection.fetchrow(
        f"UPDATE Exams SET {field} = $1 WHERE id = $2;", file_id, record_id
    )

    return row  # Returns all exam file(with id)
