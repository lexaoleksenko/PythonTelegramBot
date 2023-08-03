from aiogram import types
from loader import dp
from aiogram.dispatcher import FSMContext
from states.authorization import AuthorizationState
from utils.db import quick_commands as commands

import logging

from utils.keyboard_utils import generate_inline_menu


@dp.message_handler(commands=['start'])
async def cmd_login(message: types.Message):
    user = await commands.select_one_user(user_id=message.from_user.id)
    if user is not None and user.status == 'active':
        await message.answer("Ви вже зареєстровані!")
        inline_menu = generate_inline_menu()
        await message.answer("Оберіть потрібний розділ:", reply_markup=inline_menu)
    else:
        await message.answer("Привіт! Наразі ваш профіль не зареєстровано! Оберіть логін:")
        await AuthorizationState.LOGIN.set()

@dp.message_handler(state=AuthorizationState.LOGIN)
async def process_login(message: types.Message, state: FSMContext):
    try:
        login = message.text
        await state.update_data(login=login)
        await message.answer("Введіть пароль:")
        await AuthorizationState.PASSWORD.set()
    except Exception as e:
        await message.answer(f"An error occurred: {e}")

@dp.message_handler(state=AuthorizationState.PASSWORD)
async def process_password(message: types.Message, state: FSMContext):
    try:
        password = message.text
        data = await state.get_data()
        login = data.get('login')
        logging.info(f"Received login: {login}, password: {password}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

    await commands.add_user(
        user_id=message.from_user.id,
        name=message.from_user.first_name,
        username=message.from_user.username,
        status='active',
        login=login,
        password=password
    )

    await state.finish()
    await message.answer("Ви успішно зареєстровані!")
    
    inline_menu = generate_inline_menu()
    await message.answer("Оберіть потрібний розділ:", reply_markup=inline_menu)