from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from bot import bot

class AppealStates(StatesGroup):
    waiting_appeal_text = State()
    waiting_appeal_photo = State() 

async def appeal_text_entered(message: types.Message, state: FSMContext):
    if len(message.text) < 5:
        await message.answer("Текст обращения должен составлять минимум 5 символов")
        return

    button = types.InlineKeyboardButton(text="Закончить", callback_data="appeal_photo_ready")
    inlineKeyboard = types.InlineKeyboardMarkup().add(button)
    button = types.InlineKeyboardButton(text="Отмена", callback_data="appeal_cancel")
    inlineKeyboard = inlineKeyboard.add(button)


    await state.update_data(appeal_text=message.text)
    await message.answer("Прикрепите фото к обращению, после того как прикрепите все фото, нажмите на кнопку", reply_markup=inlineKeyboard)
    await state.set_state(AppealStates.waiting_appeal_photo)

async def appeal_photo_sended(message: types.Message, state: FSMContext):
    if len(message.photo) < 1:
        await message.answer("Прикрепите фото к обращению")
        return

    user_data = await state.get_data()
    cur_data = []

    if 'appeal_photo' in user_data:
        cur_data = user_data['appeal_photo']

    cur_data.append(message.photo[-1].file_id)
    await state.update_data(appeal_photo=cur_data)

async def appeal_photo_ready(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    user_data = await state.get_data()

    if 'appeal_photo' not in user_data:
        await callback.message.answer("Прикрепите фото к обращению")
        return

    user_data = await state.get_data()
    await callback.message.answer(f"Ваше обращение отправлено\nТекст обращения: {user_data['appeal_text']}")
    await bot.send_message(chat_id="-829365974", text=f"Поступило новое обращение от пользователя {callback.from_user.full_name}\n\n{user_data['appeal_text']}")

    for el in user_data['appeal_photo']:
        await bot.send_photo(chat_id="-829365974", photo=el)
    
    await state.finish()
    
async def appeal_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.answer("Вы отменили обращение")
    await state.finish()

def setup(dp: Dispatcher):
    dp.register_message_handler(appeal_text_entered, state=AppealStates.waiting_appeal_text)
    dp.register_message_handler(appeal_photo_sended, state=AppealStates.waiting_appeal_photo, content_types=['document', 'text', 'photo'])
    dp.register_callback_query_handler(appeal_photo_ready, lambda c: c.data == "appeal_photo_ready", state=AppealStates.waiting_appeal_photo)
    dp.register_callback_query_handler(appeal_cancel, lambda c: c.data == "appeal_cancel", state=AppealStates.all_states)