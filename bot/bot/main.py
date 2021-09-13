import uuid
from aiogram import Bot
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from loguru import logger
from aiogram.types import BotCommand

from core.message_handlers.branch_handlers.common import register_handlers_common
from core.message_handlers.branch_handlers.create_appointment import (
    register_handlers_create_appointment,
)
from core.message_handlers.branch_handlers.remove_appointment import (
    register_handlers_remove_appointment,
)
from core.settings import settings


def create_dispatcher() -> tuple:
    bot = Bot(token=settings.token)

    if settings.dev:
        storage = MemoryStorage()
    else:
        storage = RedisStorage2(
            settings.redis_host, settings.redis_port, password=settings.redis_password
        )

    dp = Dispatcher(bot, storage=storage)

    return dp, bot


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/home", description="Главное меню"),
    ]
    await bot.set_my_commands(commands)


async def main():
    dp, bot = create_dispatcher()

    register_handlers_common(dp)
    register_handlers_create_appointment(dp)
    register_handlers_remove_appointment(dp)

    await set_commands(bot)

    return dp


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    dp = loop.run_until_complete(main())
    executor.start_polling(dp, loop=loop)
