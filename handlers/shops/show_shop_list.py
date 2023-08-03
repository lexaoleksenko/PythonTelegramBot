import logging
from aiogram import types
from loader import dp, bot
from utils.db.quick_commands import select_assorted_shops, delete_shop_by_id
from utils.keyboard_utils import generate_inline_menu

# Функция для отображения списка магазинов или сообщения "Список магазинів пустий"
async def assorted_shops_list(chat_id: int):
    shops = await select_assorted_shops()
    if shops:
        # Собираем все названия магазинов в одну строку с разделителем '\n'
        shops_names = "\n".join(shop.name for shop in shops)

        # Отправляем сообщение с названиями магазинов, каждое на новой строке
        await bot.send_message(chat_id, shops_names)
        inline_menu = generate_inline_menu()
        await bot.send_message(chat_id, f'Ви повернулись у головне меню:', reply_markup=inline_menu)
    else:
        inline_menu = generate_inline_menu()
        await bot.send_message(chat_id, f'Список магазинів пустий!\n Ви повернулись у головне меню:', reply_markup=inline_menu)



# Функция для обработки кнопки меню "Видалити магазин"
async def assorted_shops_list_handler(message: types.Message):
    await assorted_shops_list(message.from_user.id)


dp.register_callback_query_handler(assorted_shops_list_handler, text="list_shops")
