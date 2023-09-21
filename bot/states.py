from aiogram.fsm.state import StatesGroup, State


class InputOrderData(StatesGroup):
    get_platform = State()
    get_username = State()
    get_password = State()
    get_recovery_codes = State()
    process_payment = State()
