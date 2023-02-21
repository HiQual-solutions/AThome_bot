import os

from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo

web_app = WebAppInfo(url=os.getenv("WEBAPP_URL"))

webapp_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Услуги', web_app=web_app)]
    ]
)

main_keyboard = InlineKeyboardMarkup()
main_keyboard = main_keyboard.add(InlineKeyboardButton("Написать обращение", callback_data="appeal"))
main_keyboard = main_keyboard.add(InlineKeyboardButton(text = "Сдача/продажа", callback_data='rent_menu'))
main_keyboard = main_keyboard.add(InlineKeyboardButton(text = "Аренда/покупка", callback_data='buy_menu'))
main_keyboard = main_keyboard.add(InlineKeyboardButton(text = "Новости", callback_data='buy_menu', url='https://t.me/news_athome'))
main_keyboard = main_keyboard.add(InlineKeyboardButton(text = "Отправить пожертвование в копилку", callback_data='payment'))

rent_keyboard = InlineKeyboardMarkup()
rent_keyboard = rent_keyboard.add(InlineKeyboardButton("Сдать/продать парковочное место", callback_data="rent_parking"))
rent_keyboard = rent_keyboard.add(InlineKeyboardButton("Сдать/продать недвижимость", callback_data="rent_appart"))
rent_keyboard = rent_keyboard.add(InlineKeyboardButton("Назад", callback_data="goback"))

buy_keyboard = InlineKeyboardMarkup()
buy_keyboard = buy_keyboard.add(InlineKeyboardButton("Канал ПАРКИНГ", callback_data="buy_parking", url='https://t.me/parking_text'))
buy_keyboard = buy_keyboard.add(InlineKeyboardButton("Канал НЕДВИЖИМОСТЬ", callback_data="buy_appart", url='https://t.me/apparts_test'))
buy_keyboard = buy_keyboard.add(InlineKeyboardButton("Назад", callback_data="goback"))