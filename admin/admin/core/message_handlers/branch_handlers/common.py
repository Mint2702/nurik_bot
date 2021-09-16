from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from ..states import States


async def process_start_command(message: types.Message, state: FSMContext):
    await message.reply(
        "Привет, Нурик. Выбери действие:",
    )

    await state.finish()


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands="start", state="*")
