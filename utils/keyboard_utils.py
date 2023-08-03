
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

def generate_inline_menu():
    inline_menu = InlineKeyboardMarkup()
    inline_menu.add(InlineKeyboardButton('Додати магазин', callback_data='add_shop'))
    inline_menu.add(InlineKeyboardButton('Видалити магазин', callback_data='delete_shop'))
    inline_menu.add(InlineKeyboardButton('Список магазинів', callback_data='list_shops'))
    
    return inline_menu

def generate_confirm_keyboard():
    keyboard = InlineKeyboardMarkup()
    add_button = InlineKeyboardButton("Підтвердити", callback_data='confirm_create')
    cancel_button = InlineKeyboardButton("Скасувати", callback_data='cancel_create')
    keyboard.row(add_button, cancel_button)
    
    return keyboard