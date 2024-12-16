import telebot
from telebot import types
import logging

# Ваш токен от бота
TOKEN = '8132989341:AAEdUisiBw8302kxPt75v5TL0Qenavs9SpE'

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# URL дашборда
DASHBOARD_URL = 'http://127.0.0.1:8050/'

# Кнопка для открытия дашборда
dashboard_button = types.InlineKeyboardButton(text="Открыть дашборд", url=DASHBOARD_URL)

# Список товаров для выбора
products = {
    'диван': ['Диван "Комфорт"', 25000],
    'кресло': ['Кресло "Релакс"', 15000],
    'стол': ['Стол "Элегантный"', 10000],
    'стул': ['Стул "Классический"', 5000]
}

# Каталог товаров
catalogue = types.InlineKeyboardMarkup()
for product_type, product_info in products.items():
    button = types.InlineKeyboardButton(product_info[0], callback_data=f'select_{product_type}')
    catalogue.add(button)

# Основная клавиатура
main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.row(types.KeyboardButton('🛍️Каталог'), types.KeyboardButton('🛒Корзина'),types.KeyboardButton('Очистить корзину'))
main_menu.row(types.KeyboardButton('📦Оформление заказа'), types.KeyboardButton('📊Статистика'))


# Переменная для хранения корзины покупок
cart = {}

# Команда /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Добро пожаловать в наш магазин мебели! чем можем помочь?", reply_markup=main_menu)

# Обработка основного меню
@bot.message_handler(func=lambda message: True)
def main_menu_handler(message):
    if message.text == '🛍️Каталог':
        bot.send_message(message.chat.id, "Пожалуйста, выберите товар:", reply_markup=catalogue)
    elif message.text == '🛒Корзина':
        show_cart(message)
    elif message.text == '📦Оформление заказа':
        checkout(message)
    if message.text == '📊Статистика':
        file = open('newplot.png','rb')
        bot.send_photo(message.chat.id, file)
        keyboard = types.InlineKeyboardMarkup().add(dashboard_button)
        bot.send_message(message.chat.id, "Нажмите на кнопку ниже, чтобы открыть дашборд:", reply_markup=keyboard)

    elif message.text == 'Очистить корзину':
        clear_cart(message)

# Показ корзины
# Показ корзины
def show_cart(message):
    total_price = 0
    cart_items = []
    for product_name, price in cart.items():
        cart_items.append(f"{product_name}: {price}")
        total_price += price
    if not cart:
        bot.send_message(message.chat.id, "Ваша корзина пуста.")
    else:
        bot.send_message(
            message.chat.id,
            f"Ваша корзина:\n{cart_items}\nОбщая стоимость: {total_price}",
            reply_markup=main_menu
        )

# Очистка корзины
def clear_cart(message):
    if not cart:
        bot.send_message(message.chat.id, "Ваша корзина уже пуста.", reply_markup=main_menu)
    else:
        cart.clear()
        bot.send_message(message.chat.id, "Корзина была успешно очищена.", reply_markup=main_menu)

# Оформление заказа
def checkout(message):
    if not cart:
        bot.send_message(message.chat.id, "Ваша корзина пуста. Добавьте товары в корзину.", reply_markup=main_menu)
    else:
        bot.send_message(message.chat.id, "Ваш заказ оформлен. Спасибо за покупку!", reply_markup=main_menu)

# Обработка выбора товара
@bot.callback_query_handler(func=lambda call: True)
def select_product(call):
    product_type = call.data.split('_')[1]
    product_name, price = products[product_type]
    if product_name in cart:
        cart[product_name] += price
    else:
        cart[product_name] = price
    bot.answer_callback_query(call.id, f"Товар '{product_name}' добавлен в корзину.")
    bot.send_message(call.message.chat.id, "Товар успешно добавлен в корзину.", reply_markup=main_menu)

bot.polling(none_stop = True)