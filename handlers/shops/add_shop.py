from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
import phonenumbers
from loader import dp

from states.shop_create import ShopCreateState
from utils.db.quick_commands import create_shop
from utils.keyboard_utils import generate_confirm_keyboard, generate_inline_menu


# Функция для обработки команды /add_shop
async def add_shop_command(message: types.Message):
    await message.answer("Оберіть назву магазина:")
    await ShopCreateState.NAME.set()


async def process_shop_name(message: types.Message, state: FSMContext):
    shop_name = message.text
    await state.update_data(shop_name=shop_name)

    await message.answer("Оберіть регіон, де знаходиться магазин:")
    await ShopCreateState.REGION.set()


async def process_shop_region(message: types.Message, state: FSMContext):
    shop_region = message.text
    await state.update_data(shop_region=shop_region)

    # Запрос контакта администратора магазина
    await message.answer("Напишіть контактний номер Адміністратора у форматі +380*********:")
    # Ожидание ответа от пользователя
    await ShopCreateState.ADMIN_CONTACT.set()


async def process_admin_contact(message: types.Message, state: FSMContext):
    # Получение контакта администратора магазина из ответа пользователя
    admin_contact = message.text

    # Проверяем, существует ли контакт администратора
    if not admin_contact:
        await message.answer("Не введений контакт адміністратора.")
        return

    try:
        # Пытаемся преобразовать контактный номер в объект PhoneNumber
        admin_contact_obj = phonenumbers.parse(admin_contact, None)

        # Проверяем, является ли номер действительным
        if not phonenumbers.is_valid_number(admin_contact_obj):
            await message.answer("Введений контакт адміністратора не є діючим номером телефона. Спробуйте ще. Формат - +380*********.")
            return

        # Преобразуем номер в формат E.164 и сохраняем в состоянии
        admin_contact_e164 = phonenumbers.format_number(admin_contact_obj, phonenumbers.PhoneNumberFormat.E164)
        await state.update_data(admin_contact=admin_contact_e164)

        # Все в порядке, переходим к следующему этапу
        await message.answer("Перевірте введену інформацію та підтвердіть створенння магазину.")
        await show_shop_info(message, state)

    except phonenumbers.NumberParseException:
        await message.answer("Введений контакт адміністратора не є діючим номером телефона. Спробуйте ще. Формат - +380*********.")
        return


async def show_shop_info(message: types.Message, state: FSMContext):
    # Получение всех данных о магазине из состояния
    data = await state.get_data()
    shop_name = data.get("shop_name")
    shop_region = data.get("shop_region")
    admin_contact = data.get("admin_contact")

    # Формирование результата и отображение его пользователю
    result_text = f"Назва магазину: {shop_name}\nРегіон: {shop_region}\nКонтакт адміністратора: {admin_contact}"
    await message.answer(result_text)
    
    # Вывод кнопок "Підтвердити" и "Скасувати" вместе с результатом
    keyboard = generate_confirm_keyboard()
    await message.answer("Додати магазин з такими даними?", reply_markup=keyboard)
    
    
async def confirm_create_shop(message: types.Message, state: FSMContext):   
    # Получение всех данных о магазине из состояния
    data = await state.get_data()
    shop_name = data.get("shop_name")
    shop_region = data.get("shop_region")
    admin_contact = data.get("admin_contact")
    author_id = message.chat.id
    
    try:
        # Сохранение магазина в базу данных
        await create_shop(name=shop_name, region=shop_region, admin_contact=admin_contact, author_id=author_id)
        await message.answer("Магазин успішно створено!")
        inline_menu = generate_inline_menu()
        await message.answer("Ви повернулись у головне меню:", reply_markup=inline_menu)

    except:
        # Вывод сообщения об ошибке, если что-то пошло не так
        await message.answer("Помилка при створенні магазину!")
        inline_menu = generate_inline_menu()
        await message.answer("Ви повернулись у головне меню:", reply_markup=inline_menu)

    # Завершение разговорного потока
    await state.finish()
    
async def cancel_create_shop(message: types.Message, state: FSMContext):
    # Вывод сообщения об отмене
    await message.answer("Відміна створення магазину!")
    inline_menu = generate_inline_menu()
    await message.answer("Ви повернулись у головне меню:", reply_markup=inline_menu)

    # Завершение разговорного потока
    await state.finish()

# Функция для обработки коллбека кнопки "Додати магазин"
async def add_shop_callback_handler(query: types.CallbackQuery):
    await query.answer()
    await add_shop_command(query.message)

# Функция для обработки коллбека кнопки "Підтвердити"
async def confirm_create_shop_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    await confirm_create_shop(query.message, state)

# Функция для обработки коллбека кнопки "Скасувати"
async def cancel_create_shop_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    await cancel_create_shop(query.message, state)
    
    
dp.register_callback_query_handler(add_shop_callback_handler, text="add_shop")
dp.register_message_handler(process_shop_name, state=ShopCreateState.NAME)
dp.register_message_handler(process_shop_region, state=ShopCreateState.REGION)
dp.register_message_handler(process_admin_contact, state=ShopCreateState.ADMIN_CONTACT)
dp.register_message_handler(show_shop_info, state=ShopCreateState.ADMIN_CONTACT)

dp.register_callback_query_handler(confirm_create_shop_handler, text="confirm_create", state="*")
dp.register_callback_query_handler(cancel_create_shop_handler, text="cancel_create", state="*")