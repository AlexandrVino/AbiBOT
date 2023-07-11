from aiogram.dispatcher.filters.state import State, StatesGroup


class SetTimeout(StatesGroup):
    set_timeout = State()
