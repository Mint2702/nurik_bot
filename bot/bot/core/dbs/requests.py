from .utils import sql_task


@sql_task
async def get_driver_data(connection, driver_number: str, terminal_number: str):
    row = await connection.fetchrow(
        """SELECT p.second_name, p.first_name, p.father_name
        , date_part('year', age(p.date_of_birth))::int AS age
        , o.name AS organization_name
        , p.photo
        FROM personnel AS p
        JOIN organizations AS o ON p.organization = o.id
        WHERE p.pers_number = $1
        AND o.id = (SELECT organization_id FROM current_term_org
        WHERE serial_number=$2)
        LIMIT 1;""",
        driver_number,
        terminal_number,
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
