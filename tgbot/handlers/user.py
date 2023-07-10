from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards.keyboards import get_confirm_keyboards, get_university_keyboards
from tgbot.states.registration import BaseState
from tgbot.storage.storage import STORAGE


async def user_start_handler(message: Message):
    user = message.from_user
    STORAGE.create_user(
        user_id=user.id, first_name=user.first_name,
        last_name=user.last_name, username=user.username
    )
    await BaseState.university.set()
    return await message.answer(
        f"Hello, {message.from_user.username}!\n\n"
        "My name is AbiBOT and i can notify you about your current positions in incoming lists\n\n"
        "Please choose university you'd like to add in you list", reply_markup=await get_university_keyboards()
    )


async def choose_university_handler(call: CallbackQuery, state: FSMContext):
    """
    :param call: CallbackQuery - собщение с клавиатурой, на которое кликнул пользователь
    :param state: FSMContext - текущее состяние (чтобы сохранять в ОП данные, оторые ввел пользователь)
    Функция, которая сохраняет/ищет объявление
    """

    await call.answer(cache_time=60)

    call_data = call.data.split(':')[1]
    STORAGE.add_university(call.from_user.id, call_data)

    async with state.proxy() as user_data:
        user_data['university'] = call_data

    await call.message.answer("Please send me program name")

    await BaseState.add_name.set()
    return await call.message.delete()


async def send_program_name_handler(message: Message, state: FSMContext):
    async with state.proxy() as user_data:
        user_data['program_name'] = message.text

    await BaseState.add_url.set()
    return await message.answer("Please send me url (link) of the program name")


async def send_program_url_handler(message: Message, state: FSMContext):
    url = message.text
    async with state.proxy() as user_data:
        user_data['url'] = url
        STORAGE.update_university_program(message.from_user.id, **user_data)

        del user_data['program_name']
        del user_data['url']

    await BaseState.end.set()
    return await message.answer("Successfully added, you can add next one", reply_markup=await get_confirm_keyboards())


async def new_circle_handler(call: CallbackQuery, state: FSMContext):
    """
    :param call: CallbackQuery - собщение с клавиатурой, на которое кликнул пользователь
    :param state: FSMContext - текущее состяние (чтобы сохранять в ОП данные, оторые ввел пользователь)
    """

    await call.answer(cache_time=60)
    await call.message.delete()

    call_data = call.data.split(':')[1]
    if call_data == 'Yes':
        await BaseState.add_name.set()
        return await call.message.answer("Please send me program name")
    else:
        await state.finish()
        return await call.message.answer(
            "You will be notified one time pir 120 minutes \n(to reset it use \reset_time command)"
        )


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start_handler, commands=["start"], state="*")

    dp.register_message_handler(send_program_name_handler, state=BaseState.add_name)
    dp.register_message_handler(send_program_url_handler, state=BaseState.add_url)

    dp.register_callback_query_handler(new_circle_handler, state=BaseState.end)
    dp.register_callback_query_handler(choose_university_handler, state=BaseState.university)
