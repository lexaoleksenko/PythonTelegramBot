from aiogram.dispatcher.filters.state import State, StatesGroup

class AuthorizationState(StatesGroup):
    LOGIN = State()
    PASSWORD = State()