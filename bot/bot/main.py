from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
import asyncio

from core.settings import settings
from core.utils import build_start_markup, post_update_user
from core.states import States


bot = Bot(token=settings.token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    await post_update_user(message)

    markup = await build_start_markup(message.from_user.id)
    await message.reply(
        "Привет!\nЯ Нурик, твой парикхмахер. Запишись ко мне, или посмотри мои работы)",
        reply_markup=markup,
    )
    await States.waiting_for_sign_up_or_decline.set()


@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    await post_update_user(message)

    markup = await build_start_markup(message.from_user.id)
    await message.reply(
        "Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!",
        reply_markup=markup,
    )


async def action_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_food_names:
        await message.answer("Пожалуйста, выберите блюдо, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_food=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_food_sizes:
        keyboard.add(size)
    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await OrderFood.next()
    await message.answer("Теперь выберите размер порции:", reply_markup=keyboard)


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, loop=loop)
