from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ParseMode

from src.bot import bot

class VoteStates(StatesGroup):
    waiting_vote_question = State()
    waiting_vote_options = State()

VOTES_CHAT_ID = "-1001838610096"

cancel_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Отмена", callback_data='vote_cancel'))

async def wait_question(message: types.Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer("Перечислите через запятую варианты, которые будут в голосовании:")
    await VoteStates.waiting_vote_options.set()

async def wait_options(message: types.Message, state: FSMContext):
    options = (message.text).split(",")
    data = await state.get_data()
    await bot.send_poll(VOTES_CHAT_ID, question=data['question'],
                              options=options,
                              type='regular',
                              is_anonymous=True)
    await state.finish()


    
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.answer("Вы отменили обращение")
    await state.finish()

def setup(dp: Dispatcher):
    dp.register_message_handler(wait_question, state=VoteStates.waiting_vote_question)
    dp.register_message_handler(wait_options, state=VoteStates.waiting_vote_options)
    dp.register_callback_query_handler(cancel, lambda c: c.data == "vote_cancel", state=VoteStates.all_states)