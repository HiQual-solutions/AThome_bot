from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


from src.bot import bot
from src.keyboards import admin_keyboard

admins = [686796862]

class Master:
    def __init__(self, id: int, name: str, number: str, photo: None | str, type: int):
        self.id = id
        self.name = name
        self.number = number
        self.photo = photo 
        self.type = type
        
masters = [Master(0, "XLEB", "123123", None, 1)]

class AdminStates(StatesGroup):
    waiting_master_name = State()
    waiting_master_number = State()
    waiting_master_type = State()
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

async def ap_waiting_master_name(message: types.Message, state: FSMContext):
    await state.update_data(master_name=message.text)


    await AdminStates.waiting_master_number.set()
    await message.answer("Введите номер телефона мастера")

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


    await AdminStates.waiting_master_type.set()
    
    typesKeyboard = InlineKeyboardMarkup()

    for i in range(1, 10):
        typesKeyboard = typesKeyboard.add(InlineKeyboardButton(f"Тип {i}", callback_data=f"master_type_{i}"))

    await message.answer("Выберите тип работы мастера", reply_markup=typesKeyboard)

async def ap_waiting_master_type(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()

    user_data = await state.get_data()
    master_id = masters[-1].id + 1
    master_name = user_data["master_name"]
    master_number = user_data["master_number"]
    master_price = user_data["master_price"]
    master_photo = user_data["master_photo"]
    master_type = int(cb.data.split("_")[2])

    masters.append(Master(master_id, master_name, master_number, master_photo, master_type))

    await cb.message.answer(f"Вы добавили нового мастера:\n\nИмя: {master_name}\nНомер: {master_number}\nТип работы: {master_type}")
    await state.finish()

async def ap_remove_master(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()

    await AdminStates.waiting_masterID.set()

    inlineKeyboard = InlineKeyboardMarkup()
    
    for m in masters:
        inlineKeyboard.add(InlineKeyboardButton(f"{m.name} | Тип {m.type}", callback_data=f"remove_master_{m.id}"))

    await cb.message.answer("Выберите мастера, которого хотите удалить", reply_markup=inlineKeyboard)

async def ap_waiting_masterID(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()

    masterID = int(cb.data.split("_")[2])
    new_masters = masters
    master = [m for m in new_masters if m.id == masterID][0]

    #TODO: Здесь реализовать удаление мастера из бд
    
    await cb.message.delete()
    await cb.message.answer(f"Вы успешно удалили мастера: {master.name}, тип {master.type}")

    await state.finish()

async def ap_add_admin(cb: types.CallbackQuery):
    await cb.answer()

    await AdminStates.waiting_adminID_add.set()

    await cb.message.answer("Введите ID пользователя, которого хотите назначить администратором")

async def ap_waiting_adminID_add(msg: types.Message, state: FSMContext):
    if not (msg.text.isdigit()):
        await msg.answer("Введите ID пользователя, которого хотите назначить администратором")
        return

    adminID = msg.text.isdigit()
    await state.finish()

    await msg.answer("Вы успешно добавили администратора")

    #TODO: отправлять ид админа в бд


async def ap_remove_admin(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()

    inlineKb = InlineKeyboardMarkup()
    for a in admins:
        inlineKb.add(InlineKeyboardButton(f"{a}", callback_data=f"remove_admin_{a}"))

    await cb.message.answer("Выберите ID администратора, которому хотите обнулить доступ", reply_markup=inlineKb)
    await AdminStates.waiting_adminID_remove.set()


async def ap_waiting_adminID_remove(cb: types.CallbackQuery, state: FSMContext):
    adminID = cb.data.split("_")[2]
    await state.finish()

    await cb.message.answer(f"Вы успешно удалили администратора {adminID}")

    #TODO: удалить ид админа из бд

def setup(dp: Dispatcher):
    dp.register_callback_query_handler(open_admin_panel, lambda c: c.data == "open_admin_panel",  lambda c: c.from_user.id in admins)
    dp.register_callback_query_handler(ap_add_master, lambda c: c.data == "admin_panel_add_master")
    dp.register_callback_query_handler(ap_remove_master, lambda c: c.data == "admin_panel_remove_master")
    dp.register_callback_query_handler(ap_waiting_masterID, state=AdminStates.waiting_masterID)
    dp.register_message_handler(ap_waiting_master_name, lambda c: c.from_user.id in admins, state=AdminStates.waiting_master_name)
    dp.register_message_handler(ap_waiting_master_num, lambda c: c.from_user.id in admins, state=AdminStates.waiting_master_number)
    dp.register_message_handler(ap_waiting_master_price, lambda c: c.from_user.id in admins, state=AdminStates.waiting_master_price)
    dp.register_message_handler(ap_waiting_master_photo, lambda c: c.from_user.id in admins, state=AdminStates.waiting_master_photo, content_types=['document', 'text', 'photo'])
    dp.register_callback_query_handler(ap_waiting_master_type, lambda c: c.from_user.id in admins, state=AdminStates.waiting_master_type)
    dp.register_callback_query_handler(ap_add_admin, lambda c: c.data == "admin_panel_add_admin")
    dp.register_callback_query_handler(ap_remove_admin, lambda c: c.data == "admin_panel_remove_admin")
    dp.register_message_handler(ap_waiting_adminID_add, state=AdminStates.waiting_adminID_add)
    dp.register_callback_query_handler(ap_waiting_adminID_remove, state=AdminStates.waiting_adminID_remove)

