from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ParseMode

from src.bot import bot

class SecurityStates(StatesGroup):
    waiting_home_number = State()
    waiting_appart_number = State()
    waiting_message = State()

SECURITY_CHAT_ID = "-1001791992980"

cancel_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Отмена", callback_data='security_cancel'))

async def wait_home(message: types.Message, state: FSMContext):
    await state.update_data(home=message.text)
    await SecurityStates.waiting_home_number.set()
    await bot.send_message(message.chat.id, "Введите номер квартиры: ", reply_markup=cancel_keyboard)
    await state.set_state(SecurityStates.waiting_appart_number)


async def wait_number(message: types.Message, state: FSMContext):
    await state.update_data(appart=message.text)
    await message.answer("Введите сообщение охране:")
    await state.set_state(SecurityStates.waiting_message)

async def wait_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(SECURITY_CHAT_ID, f"*ВЫЗОВ ОХРАНЫ* \n\n *Дом:* {data['home']} \n *Квартира:* \n \t {data['appart']} \n *Сообщение: *{message.text}", parse_mode=ParseMode.MARKDOWN)
    await message.answer("Информация была передана охране.")
    await state.finish()
   
    
async def security_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Вы отменили обращение")
    await state.finish()

def setup(dp: Dispatcher):
    dp.register_message_handler(wait_home, state=SecurityStates.waiting_home_number)
    dp.register_message_handler(wait_number, state=SecurityStates.waiting_appart_number)
    dp.register_message_handler(wait_message, state=SecurityStates.waiting_message)
    dp.register_callback_query_handler(security_cancel, lambda c: c.data == "security_cancel", state=SecurityStates.all_states)