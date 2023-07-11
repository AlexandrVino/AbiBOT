from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from tgbot.storage.storage import STORAGE


async def user_start_handler(message: Message):
    user = message.from_user
    STORAGE.create_user(
        user_id=user.id, first_name=user.first_name,
        last_name=user.last_name, username=user.username
    )
    return await message.answer(
        f"Hello, {message.from_user.username}!\n\n"
        "My name is AbiBOT and i can notify you about your current positions in incoming lists\n\n"
        "Please use /add_university command to add university you'd like to add in you list"
    )


async def user_help_handler(message: Message):
    return await message.answer(
        "Commands: \n\n"
        f"/start - start communication with bot\n"
        f"/help - see all commands of the bot\n"
        f"/cancel - cancel all actions\n"
        f"/add_university - add university to watch notifications\n"
    )


async def user_cancel_handler(message: Message, state: FSMContext):
    await state.reset_data()
    await state.finish()

    return await message.answer("Current action has been ended")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_help_handler, commands=["help"], state="*")
    dp.register_message_handler(user_start_handler, commands=["start"], state="*")
    dp.register_message_handler(user_cancel_handler, commands=["cancel"], state="*")
