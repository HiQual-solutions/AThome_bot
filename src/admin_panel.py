from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


from src.bot import bot
from src.keyboards import admin_keyboard

admins = [6867968623]

class Master:
    def __init__(self, name: str, number: str, photo: None | str, type: int):
        self.name = name
        self.number = number
        self.photo = photo 
        self.type = type
 
masters = [Master("XLEB", "123123", None, 1)]

class AdminStates(StatesGroup):
    waiting_master_name = State()
    waiting_master_number = State()
    waiting_master_type = State()
    waiting_master_price = State()
    waiting_master_photo = State()
    waiting_adminID = State()

def is_user_admin(user):
    print(user in admins)
    if user in admins:
        return True

    return False

async def open_admin_panel(cb: types.CallbackQuery):
    await cb.answer()

    # if cb.from_user.id not in admins:
    #     return 

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


    await AdminStates.waiting_master_photo.set()
    await message.answer("Отправьте фото мастера")

async def ap_waiting_master_photo(message: types.Message, state: FSMContext):
    if len(message.photo) < 1:
        await message.answer("Отправьте фото мастера")
        return 

    await state.update_data(master_photo=message.photo[-1])


    await AdminStates.waiting_master_type.set()
    
    typesKeyboard = InlineKeyboardMarkup()

    for i in range(1, 10):
        typesKeyboard = typesKeyboard.add(InlineKeyboardButton(f"Тип {i}", callback_data=f"master_type_{i}"))

    await message.answer("Выберите тип работы мастера", reply_markup=typesKeyboard)

async def ap_waiting_master_type(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()

    user_data = await state.get_data()
    master_name = user_data["master_name"]
    master_number = user_data["master_number"]
    master_photo = user_data["master_photo"]
    master_type = int(cb.data.split("_")[2])

    masters.append(Master(master_name, master_number, master_photo, master_type))

    await cb.message.answer(f"Вы добавили нового мастера:\n\nИмя: {master_name}\nНомер: {master_number}\nТип работы: {master_type}")
    await state.finish()

async def ap_remove_master(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()

async def ap_add_admin(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()

async def ap_remove_admin(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()

def setup(dp: Dispatcher):
    # dp.register_message_handler(rent_text_entered, state=RentStates.waiting_rent_text)
    # dp.register_message_handler(rent_price_entered, state=RentStates.waiting_rent_price)
    # dp.register_message_handler(rent_photo_sended, state=RentStates.waiting_rent_photo, content_types=['document', 'text', 'photo'])
    # dp.register_callback_query_handler(rent_photo_ready, lambda c: c.data == "rent_photo_ready", state=RentStates.waiting_rent_photo)
    # dp.register_callback_query_handler(rent_cancel, lambda c: c.data == "rent_cancel", state=RentStates.all_states)
    dp.register_callback_query_handler(open_admin_panel, lambda c: c.data == "open_admin_panel",  lambda c: c.from_user.id in admins)
    dp.register_callback_query_handler(ap_add_master, lambda c: c.data == "admin_panel_add_master")
    dp.register_message_handler(ap_waiting_master_name, lambda c: c.from_user.id in admins, state=AdminStates.waiting_master_name)
    dp.register_message_handler(ap_waiting_master_num, lambda c: c.from_user.id in admins, state=AdminStates.waiting_master_number)
    dp.register_message_handler(ap_waiting_master_photo, lambda c: c.from_user.id in admins, state=AdminStates.waiting_master_photo, content_types=['document', 'text', 'photo'])
    dp.register_callback_query_handler(ap_waiting_master_type, lambda c: c.from_user.id in admins, state=AdminStates.waiting_master_type)