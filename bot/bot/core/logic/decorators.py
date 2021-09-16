from loguru import logger

from ..dbs.requests import get_user_data, post_user, update_user


async def post_update_user(message):
    """
    Adds user to db if the user is new. Checks if current user info is the same as the data in the db.
    Updates user data if needed.
    """

    user_current_data = await get_user_data(message.from_user.id)
    user_old_data = {
        "id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
    }
    if user_current_data is None:
        await post_user(user_old_data)
    else:
        user_current_data = dict(user_current_data)
        if user_current_data != user_old_data:
            update_values = {
                key: value
                for key, value in user_old_data.items()
                if user_current_data[key] != value
            }
            await update_user(update_values, message.from_user.id)


def basic_message_handler_wrapper(func):
    async def wrapper(message, state):
        await post_update_user(message)

        try:
            await func(message, state)
        except Exception as err:
            logger.error("Some error ocured while trying to process message")
            logger.warning(err)

    return wrapper
