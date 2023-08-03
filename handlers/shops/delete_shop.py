import logging
from aiogram import types
from loader import dp, bot
from utils.db.quick_commands import select_all_shops, delete_shop_by_id
from utils.keyboard_utils import generate_inline_menu

# Функция для отображения списка магазинов или сообщения "Список магазинів пустий"
async def show_shops_list(chat_id: int):
    shops = await select_all_shops()
    if shops:
        for shop in shops:
            markup = types.InlineKeyboardMarkup()
            delete_button = types.InlineKeyboardButton("Удалить", callback_data=f"delete_shop_{shop.id}")
            markup.add(delete_button)
            await bot.send_message(chat_id, f"Ім'я магазину: {shop.name}", reply_markup=markup)
    else:
        inline_menu = generate_inline_menu()
        await bot.send_message(chat_id, f'Список магазинів пустий!\n Ви повернулись у головне меню:', reply_markup=inline_menu)

# Функция для обработки коллбеков кнопок "Видалити"
async def delete_shop_handler(query: types.CallbackQuery):
    try:
        shop_id = int(query.data.split('_')[-1])
        await delete_shop_by_id(shop_id)
        inline_menu = generate_inline_menu()
        await bot.send_message(query.from_user.id, f'Магазин успішно видалено!\n Ви повернулись у головне меню:', reply_markup=inline_menu)
    except Exception as e:
        await bot.send_message(query.from_user.id,"Помилка видалення магазину!")
        logging.exception(f"Помилка видалення магазину: {e}")

# Функция для обработки кнопки меню "Видалити магазин"
async def delete_shop_command_handler(message: types.Message):
    await show_shops_list(message.from_user.id)

dp.register_callback_query_handler(delete_shop_command_handler, text="delete_shop")
dp.register_callback_query_handler(delete_shop_handler, lambda query: query.data.startswith("delete_shop_"))