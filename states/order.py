from aiogram.fsm.state import State, StatesGroup


class OrderState(StatesGroup):
    full_name = State()
    phone = State()
    region = State()
    city = State()
    address = State()
    payment = State()