from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    waiting_for_sign_up_or_decline = State()
    waiting_for_appointment_choise = State()

    waiting_for_date = State()
    waiting_for_time = State()
    waiting_for_type = State()
    waiting_for_confirm = State()
