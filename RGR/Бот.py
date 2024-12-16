import telebot
from telebot import types
import logging

# Ваш токен от бота
TOKEN = '8132989341:AAEdUisiBw8302kxPt75v5TL0Qenavs9SpE'

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

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


