async def on_startup(dp):
  
  from loader import db
  from utils.db.db_api_gino import on_startup
  print('Connecting PostgreSQL')
  await on_startup(dp)
  
  print('Del Data Base')
  await db.gino.drop_all()
  
  print('Create tables')
  await db.gino.create_all()
  
  print('Done!')
  
  from utils.set_bot_commands import set_default_commands
  await set_default_commands(dp)
  
  print('Bot Goes')


if __name__ == '__main__':
  from aiogram import executor
  from handlers import dp
  
  executor.start_polling(dp, on_startup=on_startup)