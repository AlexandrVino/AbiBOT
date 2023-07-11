import asyncio
import json

from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards.keyboards import get_confirm_keyboards, get_university_keyboards
from tgbot.misc.parser import parse
from tgbot.states.notifier import SetTimeout
from tgbot.states.registration import AddingUniversity
from tgbot.storage.storage import STORAGE
from datetime import datetime

TASKS = {}


async def set_timeout_start_handler(message: Message):
    await SetTimeout.set_timeout.set()
    return await message.answer("Please send me time out time (in minutes)")


async def set_timeout_handler(message: Message, state: FSMContext):
    txt = message.text
    if not txt.isdigit():
        return await message.answer("Please send me time out time (in minutes) (must be digit!!!)")

    STORAGE.update_user(user_id=message.from_user.id, notify_time=int(txt) * 60)
    await state.finish()
    return await message.answer("Timeout successfully changed")


async def notifier(bot: Bot):
    cache = {}
    while True:
        curr_time = datetime.now().minute

        hours = f"{(curr_time // 60):02}"
        minutes = f"{(curr_time % 60):02}"

        for user_id, user in STORAGE.get_users():
            message_tmp = (
                "Hello {1}!\n\n"
                "This is mailing\n"
                f"Time: {hours}:{minutes}\n\n"
                "This is that i found:\n\n"
            )
            user_mess = {}
            close_user = False
            errors = []

            if not cache.get(user_id) or cache[user_id] > 1440 or cache[user_id] + user['notify_time'] >= curr_time:
                cache[user_id] = curr_time

                for university_name, university in user['universities'].items():
                    for program in university:

                        if not user_mess.get(university_name):
                            user_mess[university_name] = {}
                        try:
                            user_mess[university_name][program['program_name']] = parse(
                                url=program['url'], snils=user['snils'],
                                sum_points=user['sum_points'], university=university_name
                            )
                        except ValueError:
                            close_user = True
                            errors.append(program['program_name'])
                            break

                if close_user:
                    await bot.send_message(
                        user_id,
                        "I couldn't find you on some of your programs\n\n"
                        f"{json.dumps(errors, indent=4)}"
                    )

                await bot.send_message(user_id, message_tmp)
                await bot.send_message(user_id, f"```{json.dumps(user_mess, indent=4)}```")

        await asyncio.sleep(600)


def register_notifier(dp: Dispatcher):
    dp.register_message_handler(..., commands=["add_university"], state="*")
