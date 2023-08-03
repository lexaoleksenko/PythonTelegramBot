from aiogram.dispatcher.filters.state import State, StatesGroup

class ShopCreateState(StatesGroup):
    NAME = State()
    REGION = State()
    ADMIN_CONTACT = State()