from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from src.bot import bot

RENT_CHATID = "-1001865322306"

class RentStates(StatesGroup):
    waiting_rent_text = State()
    waiting_rent_price = State()
    waiting_rent_photo = State()

async def rent_text_entered(msg: types.Message, state: FSMContext):
    if len(msg.text) < 5:
        await msg.answer("Текст описания должен состоять минимум из 5 символов")
        return 
    
    button = types.InlineKeyboardButton(
            "Отмена", callback_data="rent_cancel")
    inlineKeyboard = types.InlineKeyboardMarkup().add(button)

    await msg.answer("Введите цену места", reply_markup=inlineKeyboard)
    await state.set_state(RentStates.waiting_rent_price)
    await state.update_data(rent_text=msg.text)

async def rent_price_entered(msg: types.Message, state: FSMContext):
    price = msg.text

    inlineKeyboard = types.InlineKeyboardMarkup()
    inlineKeyboard = inlineKeyboard.add(types.InlineKeyboardButton(text="Закончить", callback_data="rent_photo_ready"))
    inlineKeyboard = inlineKeyboard.add(types.InlineKeyboardButton(text="Отмена", callback_data="rent_cancel"))

    await msg.answer("Отправьте фото места, после чего нажмите кнопку \"закончить\"", reply_markup=inlineKeyboard)
    await state.set_state(RentStates.waiting_rent_photo)
    await state.update_data(rent_price=price)
    
async def rent_photo_sended(msg: types.Message, state: FSMContext):
    if len(msg.photo) < 1:
        await msg.answer("Прикрепите фото места")
        return 

    user_data = await state.get_data()
    cur_data = []

    if 'rent_photo' in user_data:
        cur_data = user_data['rent_photo']

    cur_data.append(msg.photo[-1].file_id)
    await state.update_data(rent_photo=cur_data)

async def rent_photo_ready(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()   

    user_data = await state.get_data()

    if 'rent_photo' not in user_data:
        await cb.message.answer("Прикрепите фото места")
        return 

    await cb.message.answer("Ваше объявление отправлено")
    await bot.send_message(RENT_CHATID, f"Новое объявление\n\n{user_data['rent_text']}\nЦена: {user_data['rent_price']}")
    
    for photo in user_data['rent_photo']:
        await bot.send_photo(RENT_CHATID, photo)    

    await state.finish()

async def rent_cancel(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()

    await cb.message.answer("Вы отменили создание объявления")
    await state.finish()

def setup(dp: Dispatcher):
    dp.register_message_handler(rent_text_entered, state=RentStates.waiting_rent_text)
    dp.register_message_handler(rent_price_entered, state=RentStates.waiting_rent_price)
    dp.register_message_handler(rent_photo_sended, state=RentStates.waiting_rent_photo, content_types=['document', 'text', 'photo'])
    dp.register_callback_query_handler(rent_photo_ready, lambda c: c.data == "rent_photo_ready", state=RentStates.waiting_rent_photo)
    dp.register_callback_query_handler(rent_cancel, lambda c: c.data == "rent_cancel", state=RentStates.all_states)