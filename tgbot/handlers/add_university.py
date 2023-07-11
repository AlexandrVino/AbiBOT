from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards.keyboards import get_confirm_keyboards, get_university_keyboards
from tgbot.states.registration import AddingUniversity
from tgbot.storage.storage import STORAGE


async def add_university_handler(message: Message):
    await AddingUniversity.university.set()
    return await message.answer(
        "Please use choose university you'd like to add in you list",
        reply_markup=await get_university_keyboards()
    )


async def choose_university_handler(call: CallbackQuery, state: FSMContext):
    """
    :param call: CallbackQuery - сообщение с клавиатурой, на которое кликнул пользователь
    :param state: FSMContext - текущее состояние (чтобы сохранять в ОП данные, которые ввел пользователь)
    """

    await call.answer(cache_time=60)

    call_data = call.data.split(':')[1]
    STORAGE.add_university(call.from_user.id, call_data)

    async with state.proxy() as user_data:
        user_data['university'] = call_data

    await call.message.answer("Please send me program name")

    await AddingUniversity.add_name.set()
    return await call.message.delete()


async def send_program_name_handler(message: Message, state: FSMContext):
    async with state.proxy() as user_data:
        user_data['program_name'] = message.text

    await AddingUniversity.add_url.set()
    return await message.answer("Please send me url (link) of the program name")


async def send_program_url_handler(message: Message, state: FSMContext):
    url = message.text
    async with state.proxy() as user_data:
        user_data['url'] = url
        STORAGE.update_university_program(message.from_user.id, **user_data)

        del user_data['program_name']
        del user_data['url']

    await AddingUniversity.end.set()
    return await message.answer(
        "Successfully added, you can add next one",
        reply_markup=await get_confirm_keyboards()
    )


async def new_circle_handler(call: CallbackQuery, state: FSMContext):
    """
    :param call: CallbackQuery - сообщение с клавиатурой, на которое кликнул пользователь
    :param state: FSMContext - текущее состояние (чтобы сохранять в ОП данные, которые ввел пользователь)
    """

    await call.answer(cache_time=60)
    await call.message.delete()

    call_data = call.data.split(':')[1]
    if call_data == 'Yes':
        await AddingUniversity.add_name.set()
        return await call.message.answer("Please send me program name")
    else:
        await state.finish()
        return await call.message.answer(
            "You will be notified one time pir 120 minutes \n"
            "(to reset it use \reset_time command)"
        )


def register_add_university(dp: Dispatcher):
    dp.register_message_handler(add_university_handler, commands=["add_university"], state="*")
    dp.register_message_handler(send_program_name_handler, state=AddingUniversity.add_name)
    dp.register_message_handler(send_program_url_handler, state=AddingUniversity.add_url)

    dp.register_callback_query_handler(new_circle_handler, state=AddingUniversity.end)
    dp.register_callback_query_handler(choose_university_handler, state=AddingUniversity.university)
