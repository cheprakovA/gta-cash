from aiogram.fsm.state import StatesGroup, State



class InputOrderData(StatesGroup):
    enter_platform = State()
    enter_username = State()
    enter_password = State()
    enter_recovery_codes = State()