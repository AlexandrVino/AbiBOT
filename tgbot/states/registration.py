from aiogram.dispatcher.filters.state import State, StatesGroup


class BaseState(StatesGroup):
    university = State()
    add_url = State()
    add_name = State()
    end = State()
