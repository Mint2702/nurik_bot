import asyncpg
from loguru import logger
from functools import wraps

from ..settings import settings


async def connect() -> asyncpg.Connection or bool:
    try:
        connection = await asyncpg.connect(
            host=settings.psql_host,
            port=settings.psql_port,
            user=settings.psql_user,
            password=settings.psql_password,
            database=settings.psql_db_name,
            timeout=60,
        )

        return connection

    except Exception as err:
        logger.error("Connection with DB failed")
        logger.warning(err)

        return False


def sql_task(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        connection = await connect()

        try:
            result = await func(connection, *args, **kwargs)
        except Exception as err:
            logger.error("SQL task could not be executed")
            logger.warning(err)

            return False

        await connection.close()

        return result

    return wrapper


def build_sql_update_request(user_data: dict, user_id: int) -> str:
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
