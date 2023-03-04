from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

import logging

from src.db.mongo import db_collection
from src.bot import bot
from src.keyboards import admin_keyboard

cleaning = db_collection("cleaning")
cargo = db_collection("cargo")
ren_apartment = db_collection("ren_apartment")
electricity = db_collection("electricity")
painter = db_collection("painter")
security = db_collection("security")
water = db_collection("water")
plumbing = db_collection("plumbing")

admins = db_collection("admins")

spec_names = {
    "1": "Клининг",
    "2": "Перевозка грузов",
    "3": "Ремонт квартир",
    "4": "Электрика",
    "5": "Маляры и штукатуры",
    "6": "Охрана",
    "7": "Доставка воды",
    "8": "Сантехника"
}

class AdminStates(StatesGroup):
    waiting_master_name = State()
    waiting_master_type = State()
    waiting_master_link = State()
    waiting_master_number = State()
    waiting_master_spec = State()
    waiting_master_price = State()
    waiting_master_photo = State()
    waiting_masterID = State()
    waiting_adminID_add = State()
    waiting_adminID_remove = State()

async def open_admin_panel(cb: types.CallbackQuery):
    await cb.answer()

    await cb.message.answer("Админ-панель", reply_markup=admin_keyboard)

async def ap_add_master(cb: types.CallbackQuery):
    await cb.answer()

    await AdminStates.waiting_master_name.set()
    await cb.message.answer("Введите имя мастера")
    
async def ap_waiting_master_type(cb: types.CallbackQuery):
        await cb.answer()

        if cb.data == "num":
            await AdminStates.waiting_master_number.set()
            await cb.message.answer("Введите номер телефона мастера")
            return

        await AdminStates.waiting_master_link.set()
        await cb.message.answer("Отправьте ссылку на профиль мастера")


async def ap_waiting_master_link(msg: types.Message, state: FSMContext):
    user_data = await state.get_data()
    master_name = user_data["master_name"]
    master_spec = user_data["master_spec"]
    master_link = msg.text

    match master_spec:
        case 1:
            cleaning.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : "",
                "photo" : "",
                "tel" : "",
                "link" : master_link
            })
        case 2:
            cargo.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : "",
                "photo" : "",
                "tel" : "",
                "link" : master_link
            })
        case 3:
            ren_apartment.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : "",
                "photo" : "",
                "tel" : "",
                "link" : master_link
            })
        case 4:
            electricity.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : "",
                "photo" : "",
                "tel" : "",
                "link" : master_link
            })
        case 5:
            painter.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : "",
                "photo" : "",
                "tel" : "",
                "link" : master_link
            })
        case 6:
            security.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : "",
                "photo" : "",
                "tel" : "",
                "link" : master_link
            })
        case 7:
            water.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : "",
                "photo" : "",
                "tel" : "",
                "link" : master_link
            })
        case 8:
            plumbing.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : "",
                "photo" : "",
                "tel" : "",
                "link" : master_link
            })


    await msg.answer(f"Вы добавили нового мастера:\n\nИмя: {master_name}\nСсылка: {master_link}\nТип работы: {spec_names[master_spec]}")
    await state.finish()


async def ap_waiting_master_name(message: types.Message, state: FSMContext):
    await state.update_data(master_name=message.text)


    # await AdminStates.waiting_master_number.set()
    # await message.answer("Введите номер телефона мастера")
    await AdminStates.waiting_master_spec.set()
    
    master_keyboard = InlineKeyboardMarkup(row_width=3)
    master_keyboard = master_keyboard.add(InlineKeyboardButton("Клининг", callback_data="1"))
    master_keyboard = master_keyboard.add(InlineKeyboardButton("Перевозка грузов", callback_data="2"))
    master_keyboard = master_keyboard.add(InlineKeyboardButton("Ремонт квартир", callback_data="3"))
    master_keyboard = master_keyboard.add(InlineKeyboardButton("Электрика", callback_data="4"))
    master_keyboard = master_keyboard.add(InlineKeyboardButton("Маляры и штукатуры", callback_data="5"))
    master_keyboard = master_keyboard.add(InlineKeyboardButton("Охрана", callback_data="6"))
    master_keyboard = master_keyboard.add(InlineKeyboardButton("Доставка воды", callback_data="7"))
    master_keyboard = master_keyboard.add(InlineKeyboardButton("Сантехника", callback_data="8"))
    master_keyboard = master_keyboard.add(InlineKeyboardButton("Назад", callback_data="9"))

    await message.answer("Выберите специальность мастера", reply_markup=master_keyboard)

    

async def ap_waiting_master_num(message: types.Message, state: FSMContext):
    await state.update_data(master_number=message.text)


    await AdminStates.waiting_master_price.set()
    await message.answer("Укажите цену мастера")

async def ap_waiting_master_price(message: types.Message, state:FSMContext):
    await state.update_data(master_price=message.text)


    await AdminStates.waiting_master_photo.set()
    await message.answer("Отправьте фото мастера")
    
async def ap_waiting_master_photo(message: types.Message, state: FSMContext):
    if len(message.photo) < 1:
        await message.answer("Отправьте фото мастера")
        return 

    # print(await message.photo[-1].get_url())
    await state.update_data(master_photo=(await message.photo[-1].get_url()))

    user_data = await state.get_data()

    master_name = user_data["master_name"]
    master_number = user_data["master_number"]
    master_price = user_data["master_price"]
    master_photo = user_data["master_photo"]
    master_spec = user_data["master_spec"]

    match master_spec:
        case 1:
            cleaning.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : master_price,
                "photo" : master_photo,
                "tel" : master_number,
            })
        case 2:
            cargo.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : master_price,
                "photo" : master_photo,
                "tel" : master_number,
            })
        case 3:
            ren_apartment.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : master_price,
                "photo" : master_photo,
                "tel" : master_number,
            })
        case 4:
            electricity.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : master_price,
                "photo" : master_photo,
                "tel" : master_number,
            })
        case 5:
            painter.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : master_price,
                "photo" : master_photo,
                "tel" : master_number,
            })
        case 6:
            security.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : master_price,
                "photo" : master_photo,
                "tel" : master_number,
            })
        case 7:
            water.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : master_price,
                "photo" : master_photo,
                "tel" : master_number,
            })
        case 8:
            plumbing.add_row({
                "status" : "active",
                "title" : master_name,
                "subtitle" : master_price,
                "photo" : master_photo,
                "tel" : master_number,
            })
        
    await message.answer(f"Вы добавили нового мастера:\n\nИмя: {master_name}\nНомер: {master_number}\nТип работы: {spec_names[master_spec]}")
    await state.finish()
    # await AdminStates.waiting_master_spec.set()
    
    # master_keyboard = InlineKeyboardMarkup(row_width=3)
    # master_keyboard = master_keyboard.add(InlineKeyboardButton("Клининг", callback_data="1"))
    # master_keyboard = master_keyboard.add(InlineKeyboardButton("Перевозка грузов", callback_data="2"))
    # master_keyboard = master_keyboard.add(InlineKeyboardButton("Ремонт квартир", callback_data="3"))
    # master_keyboard = master_keyboard.add(InlineKeyboardButton("Электрика", callback_data="4"))
    # master_keyboard = master_keyboard.add(InlineKeyboardButton("Маляры и штукатуры", callback_data="5"))
    # master_keyboard = master_keyboard.add(InlineKeyboardButton("Охрана", callback_data="6"))
    # master_keyboard = master_keyboard.add(InlineKeyboardButton("Доставка воды", callback_data="7"))
    # master_keyboard = master_keyboard.add(InlineKeyboardButton("Сантехника", callback_data="8"))
    # master_keyboard = master_keyboard.add(InlineKeyboardButton("Назад", callback_data="9"))

    # await message.answer("Выберите тип работы мастера", reply_markup=master_keyboard)

async def ap_waiting_master_spec(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.update_data(master_spec=int(cb.data))
    

    inlineKeyboad = InlineKeyboardMarkup()
    inlineKeyboad.add(InlineKeyboardButton("По номеру", callback_data="num"))
    inlineKeyboad.add(InlineKeyboardButton("По ссылке", callback_data="link"))

    await AdminStates.waiting_master_type.set()
    await cb.message.answer("Выберите тип вызова мастера", reply_markup=inlineKeyboad)


async def ap_remove_master(cb: types.CallbackQuery, state: FSMContext):
    # await cb.answer()

    # await AdminStates.waiting_masterID.set()

    # inlineKeyboard = InlineKeyboardMarkup()
    

    # for m in masters:
    #     inlineKeyboard.add(InlineKeyboardButton(f"{m.name} | Тип {m.type}", callback_data=f"remove_master_{m.id}"))

    # await cb.message.answer("Выберите мастера, которого хотите удалить", reply_markup=inlineKeyboard)
    pass

async def ap_waiting_masterID(cb: types.CallbackQuery, state: FSMContext):
    # await cb.answer()
    # masterID = int(cb.data.split("_")[2])

    # #TODO: Здесь реализовать удаление мастера из бд
    
    # await cb.message.delete()
    # await cb.message.answer(f"Вы успешно удалили мастера: {master.name}, тип {master.type}")

    # await state.finish()
    pass

async def ap_add_admin(cb: types.CallbackQuery):
    await cb.answer()


    await AdminStates.waiting_adminID_add.set()

    await cb.message.answer("Введите ID пользователя, которого хотите назначить администратором")

async def ap_waiting_adminID_add(msg: types.Message, state: FSMContext):
    if not (msg.text.isdigit()):
        await msg.answer("Введите ID пользователя, которого хотите назначить администратором")
        return

    adminID = int(msg.text)
    admins.add_row({
        "adminID": adminID,
        "status": "active",
    })

    await state.finish()

    await msg.answer("Вы успешно добавили администратора")

async def ap_remove_admin(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()

    inlineKb = InlineKeyboardMarkup()

    for a in admins.get_all_admins({"status" : "active"}):

        inlineKb.add(InlineKeyboardButton(f"{a}", callback_data=f"remove_admin_{a}"))

    await cb.message.answer("Выберите ID администратора, которому хотите обнулить доступ", reply_markup=inlineKb)
    await AdminStates.waiting_adminID_remove.set()




async def ap_waiting_adminID_remove(cb: types.CallbackQuery, state: FSMContext):
    adminID = cb.data.split("_")[2]

    admins.change_data({
        "adminID": adminID,
    }, {
        "status" : "deactive",
    })

    await state.finish()
    await cb.message.answer(f"Вы успешно удалили администратора {adminID}")

def setup(dp: Dispatcher):

    admins_list = admins.get_all_admins({"status" : "active"})

    dp.register_callback_query_handler(open_admin_panel, lambda c: c.data == "open_admin_panel",  lambda c: c.from_user.id in admins_list)
    dp.register_callback_query_handler(ap_add_master, lambda c: c.data == "admin_panel_add_master", lambda c: c.from_user.id in admins_list)
    dp.register_callback_query_handler(ap_remove_master, lambda c: c.data == "admin_panel_remove_master", lambda c: c.from_user.id in admins_list)
    dp.register_callback_query_handler(ap_waiting_masterID, lambda c: c.from_user.id in admins_list, state=AdminStates.waiting_masterID)
    dp.register_message_handler(ap_waiting_master_name, lambda c: c.from_user.id in admins_list, state=AdminStates.waiting_master_name)
    dp.register_message_handler(ap_waiting_master_num, lambda c: c.from_user.id in admins_list, state=AdminStates.waiting_master_number)
    dp.register_message_handler(ap_waiting_master_price, lambda c: c.from_user.id in admins_list, state=AdminStates.waiting_master_price)
    dp.register_message_handler(ap_waiting_master_photo, lambda c: c.from_user.id in admins_list, state=AdminStates.waiting_master_photo, content_types=['document', 'text', 'photo'])
    dp.register_callback_query_handler(ap_waiting_master_spec, lambda c: c.from_user.id in admins_list, state=AdminStates.waiting_master_spec)
    dp.register_callback_query_handler(
        ap_waiting_master_type, 
        lambda c: c.from_user.id in admins_list, 
        lambda c: c.data in ["num", "link"], 
        state=AdminStates.waiting_master_type
    )
    dp.register_message_handler(
        ap_waiting_master_link, 
        lambda c: c.from_user.id in admins_list, 
        state=AdminStates.waiting_master_link
    )
    dp.register_callback_query_handler(ap_add_admin, lambda c: c.data == "admin_panel_add_admin")
    dp.register_callback_query_handler(ap_remove_admin, lambda c: c.data == "admin_panel_remove_admin")
    dp.register_message_handler(ap_waiting_adminID_add, state=AdminStates.waiting_adminID_add)
    dp.register_callback_query_handler(ap_waiting_adminID_remove, state=AdminStates.waiting_adminID_remove)

