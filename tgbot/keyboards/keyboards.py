from tgbot.keyboards.inline import get_inline_keyboard


async def get_university_keyboards():
    return await get_inline_keyboard(keyboard_data=[
        [{'text': "СПбГУ", 'value': 'СПбГУ'}],
        [{'text': "ПГНИУ", 'value': 'ПГНИУ'}],
    ])


async def get_confirm_keyboards():
    return await get_inline_keyboard(keyboard_data=[
        [{'text': "Да", 'value': 'Yes'}],
        [{'text': "Нет", 'value': 'No'}],
    ])
