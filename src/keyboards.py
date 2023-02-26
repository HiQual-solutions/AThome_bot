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
    main_keyboard = InlineKeyboardMarkup(row_width=3)
    main_keyboard = main_keyboard.row(InlineKeyboardButton("Написать обращение", callback_data="appeal"), InlineKeyboardButton("Заказать мастера", callback_data="order_master"))
    main_keyboard = main_keyboard.row(InlineKeyboardButton("Открыть шлагбаум", callback_data="barrier"), InlineKeyboardButton(text = "Вызвать охрану", callback_data='request_secr'))
    main_keyboard = main_keyboard.row(InlineKeyboardButton(text = "Аренда/покупка", callback_data='buy_menu'), InlineKeyboardButton(text = "Сдача/продажа", callback_data='rent_menu'))
    main_keyboard = main_keyboard.row(InlineKeyboardButton(text = "Голосования ЖК", url="t.me/votes_athome"),InlineKeyboardButton("Создать голосование", callback_data="create_vote"))
    main_keyboard = main_keyboard.row(InlineKeyboardButton(text = "Отправить пожертвование в копилку", callback_data='payment'), InlineKeyboardButton(text = "Новости", callback_data='buy_menu', url='https://t.me/home_bot_news'))


    if user in admins:
        main_keyboard.add(InlineKeyboardButton(text="Админ-панель", callback_data="open_admin_panel"))
    return main_keyboard

admin_keyboard = InlineKeyboardMarkup()
admin_keyboard = admin_keyboard.add(InlineKeyboardButton("Добавить мастера", callback_data="admin_panel_add_master"))
# admin_keyboard = admin_keyboard.add(InlineKeyboardButton("Удалить мастера", callback_data="admin_panel_remove_master"))
admin_keyboard = admin_keyboard.add(InlineKeyboardButton("Добавить администратора", callback_data="admin_panel_add_admin"))
admin_keyboard = admin_keyboard.add(InlineKeyboardButton("Удалить администратора", callback_data="admin_panel_remove_admin"))


rent_keyboard = InlineKeyboardMarkup()
rent_keyboard = rent_keyboard.add(InlineKeyboardButton("Сдать/продать парковочное место", callback_data="rent_parking"))
rent_keyboard = rent_keyboard.add(InlineKeyboardButton("Сдать/продать недвижимость", callback_data="rent_appart"))
rent_keyboard = rent_keyboard.add(InlineKeyboardButton("Назад", callback_data="goback"))

buy_keyboard = InlineKeyboardMarkup()
buy_keyboard = buy_keyboard.add(InlineKeyboardButton("Канал ПАРКИНГ", callback_data="buy_parking", url='https://t.me/parking_text'))
buy_keyboard = buy_keyboard.add(InlineKeyboardButton("Канал НЕДВИЖИМОСТЬ", callback_data="buy_appart", url='https://t.me/apparts_test'))
buy_keyboard = buy_keyboard.add(InlineKeyboardButton("Назад", callback_data="goback"))

master_keyboard = InlineKeyboardMarkup(row_width=3)
master_keyboard = master_keyboard.add(InlineKeyboardButton("Клининг", callback_data="order_cleaning"))
master_keyboard = master_keyboard.add(InlineKeyboardButton("Перевозка грузов", callback_data="order_logistic"))
master_keyboard = master_keyboard.add(InlineKeyboardButton("Ремонт квартир", callback_data="order_repair"))
master_keyboard = master_keyboard.add(InlineKeyboardButton("Маляры и штукатуры", callback_data="order_painter"))
master_keyboard = master_keyboard.add(InlineKeyboardButton("Электрика", callback_data="order_electrician"))
master_keyboard = master_keyboard.add(InlineKeyboardButton("Сантехника", callback_data="order_plumber"))
master_keyboard = master_keyboard.add(InlineKeyboardButton("Назад", callback_data="goback"))

