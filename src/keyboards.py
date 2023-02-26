import os

from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo

# from src.admin_panel import admins

web_app = WebAppInfo(url=os.getenv("WEBAPP_URL"))

webapp_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Услуги', web_app=web_app)]
    ]
)



def set_main_keyboard(user, admins):
    main_keyboard = InlineKeyboardMarkup()
    main_keyboard = main_keyboard.add(InlineKeyboardButton("Написать обращение", callback_data="appeal"))
    main_keyboard = main_keyboard.add(InlineKeyboardButton("Сдать парковочное место", callback_data="parking_rent"))
    main_keyboard = main_keyboard.add(InlineKeyboardButton(text = "Отправить пожертвование в копилку: ", callback_data='payment'))

    if user in admins:
        main_keyboard.add(InlineKeyboardButton(text="Админ-панель", callback_data="open_admin_panel"))
        # print(main_keyboard)
        # return main_keyboard

    # print(kb)
    return main_keyboard

admin_keyboard = InlineKeyboardMarkup()
admin_keyboard = admin_keyboard.add(InlineKeyboardButton("Добавить мастера", callback_data="admin_panel_add_master"))
admin_keyboard = admin_keyboard.add(InlineKeyboardButton("Удалить мастера", callback_data="admin_panel_remove_master"))
admin_keyboard = admin_keyboard.add(InlineKeyboardButton("Добавить администратора", callback_data="admin_panel_add_admin"))
admin_keyboard = admin_keyboard.add(InlineKeyboardButton("Удалить администратора", callback_data="admin_panel_remove_admin"))