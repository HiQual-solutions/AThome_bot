from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from src.bot import bot

class BarrierStates(StatesGroup):
    waiting_barrier_text = State()

BARRIER_CHATID = '-1001791992980'

async def barrier_wait(message: types.Message, state: FSMContext):
    await bot.send_message(BARRIER_CHATID, message.text)
    await message.answer("Информация была передана охраникам.")
    await state.finish()

    
async def barrier_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.answer("Вы отменили обращение к охранику")
    await state.finish()

def setup(dp: Dispatcher):
    dp.register_message_handler(barrier_wait, state=BarrierStates.waiting_barrier_text)
    dp.register_callback_query_handler(barrier_cancel, lambda c: c.data == "barrier_cancel", state=BarrierStates.all_states)