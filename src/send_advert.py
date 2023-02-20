from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from main import bot

RENT_CHATID = "-829365974"

class RentStates(StatesGroup):
    waiting_rent_text = State()
    waiting_rent_price = State()
    waiting_rent_photo = State()

async def rent_text_entered(msg: types.Message, state: FSMContext):
    if len(msg.text) < 5:
        await msg.answer("����� �������� ������ �������� ������� �� 5 ��������")
        return 
    
    button = types.InlineKeyboardButton(
            "������", callback_data="rent_cancel")
    inlineKeyboard = types.InlineKeyboardMarkup().add(button)

    await msg.answer("������� ���� �����", reply_markup=inlineKeyboard)
    await state.set_state(RentStates.waiting_rent_price)
    await state.update_data(rent_text=msg.text)

async def rent_price_entered(msg: types.Message, state: FSMContext):
    price = int(msg.text)

    if (price < 0):
        await msg.answer("���� �� ����� ���� ������ 0")
        return

    button = types.InlineKeyboardButton(text="���������", callback_data="rent_photo_ready")
    inlineKeyboard = types.InlineKeyboardMarkup().add(button)
    button = types.InlineKeyboardButton(
            "������", callback_data="rent_cancel")
    inlineKeyboard = inlineKeyboard.add(button)

    await msg.answer("��������� ���� �����, ����� ���� ������� ������ \"���������\"", reply_markup=inlineKeyboard)
    await state.set_state(RentStates.waiting_rent_photo)
    await state.update_data(rent_price=price)
    
async def rent_photo_sended(msg: types.Message, state: FSMContext):
    if len(msg.photo) < 0:
        await msg.answer("���������� ���� �����")

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
        await cb.message.answer("���������� ���� �����")
        return 

    await cb.message.answer("���� ���������� ����������")
    await bot.send_message(RENT_CHATID, f"����� ����������\n\n{user_data['rent_text']}\n����: {user_data['rent_price']}")
    
    for photo in user_data['rent_photo']:
        await bot.send_photo(RENT_CHATID, photo)    

    await state.finish()

async def rent_cancel(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()

    await cb.message.answer("�� �������� �������� ����������")
    await state.finish()

def setup(dp: Dispatcher):
    dp.register_message_handler(rent_text_entered, state=RentStates.waiting_rent_text)
    dp.register_message_handler(rent_price_entered, state=RentStates.waiting_rent_price)
    dp.register_message_handler(rent_photo_sended, state=RentStates.waiting_rent_photo, content_types=['document', 'text', 'photo'])
    dp.callback_query_handler(rent_photo_ready, lambda c: c.data == "rent_photo_ready", state=RentStates.waiting_rent_photo)
    dp.callback_query_handler(rent_cancel, lambda c: c.data == "rent_cancel", state=RentStates.all_states)