from aiogram.fsm.state import StatesGroup, State

class OrderSteps(StatesGroup):
    choosing_category = State()
    choosing_flower = State()
    waiting_for_quantity = State()
    waiting_for_packaging = State()
    waiting_for_address = State()
    waiting_for_name = State()
    waiting_for_phone = State()
    confirm_order = State()