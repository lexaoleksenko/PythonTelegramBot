from aiogram import types
from loader import dp

@dp.message_handler(text='/my_id')
async def command_start(message: types.Message):
  await message.answer(f'Привіт!) {message.from_user.full_name}! \n'
                      f'Твій id - {message.from_user.id}')