from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    waiting_for_start_button = State()
