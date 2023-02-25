from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ParseMode

from src.bot import bot

class MasterStates(StatesGroup):
    waiting_order_type = State()
    waiting_order_text = State()
    waiting_order_number = State()

MASTERS_CHAT_ID = "-1001890534297"

cancel_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Отмена", callback_data='master_cancel'))

async def wait_text(message: types.Message, state: FSMContext):
    await state.update_data(order_text=message.text)
    await MasterStates.waiting_order_number.set()
    await bot.send_message(message.chat.id, "Укажите ваш номер телефона: ", reply_markup=cancel_keyboard)


async def wait_number(message: types.Message, state: FSMContext):
    await state.update_data(order_number=message.text)
    data = await state.get_data()
    await bot.send_message(MASTERS_CHAT_ID, f"*Новый заказ* \n\n *Тип услуги:* {data['type']} \n *Описание:* \n \t {data['order_text']} \n *Номер телефона заказчика: *{data['order_number']}", parse_mode=ParseMode.MARKDOWN)
    await message.answer("Информация была передана. Ожидайте звонка мастера.")
    await state.finish()

    
async def barrier_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.answer("Вы отменили обращение")
    await state.finish()

def setup(dp: Dispatcher):
    dp.register_message_handler(wait_text, state=MasterStates.waiting_order_text)
    dp.register_message_handler(wait_number, state=MasterStates.waiting_order_number)
    dp.register_callback_query_handler(barrier_cancel, lambda c: c.data == "master_cancel", state=MasterStates.all_states)