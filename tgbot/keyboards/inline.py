from typing import Dict, List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

inline_callback = CallbackData("tag", "value")
inline_callback_admin = CallbackData("tag", "value", 'admin')


async def get_inline_keyboard(keyboard_data: List[List[Dict]], method=inline_callback, **kwargs) -> InlineKeyboardMarkup:
    """
    :param keyboard_data: list with json objects
    :param method: callback method
    :returns: inline keyboard
    Функция, которая возвращает инлайн клавиатуру
    """

    keyboard = InlineKeyboardMarkup()

    for buttons in keyboard_data:
        keyboard.row(
            *[
                InlineKeyboardButton(
                    button_data['text'],
                    url=button_data.get('url'),
                    callback_data=method.new(value=button_data.get('value')),
                    **kwargs
                ) for button_data in buttons
            ])

    return keyboard
