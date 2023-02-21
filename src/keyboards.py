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
main_keyboard = main_keyboard.add(InlineKeyboardButton(text = "Покупка/продажа", callback_data='rent_menu'))
main_keyboard = main_keyboard.add(InlineKeyboardButton(text = "Отправить пожертвование в копилку", callback_data='payment'))

rent_keyboard = InlineKeyboardMarkup()
rent_keyboard = main_keyboard.add(InlineKeyboardButton("Сдать/продать парковочное место", callback_data="parking_rent"))
rent_keyboard = main_keyboard.add(InlineKeyboardButton("Сдать/продать недвижимость", callback_data="appart_rent"))