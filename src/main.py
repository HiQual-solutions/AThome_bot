import logging, os, json

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from aiogram.types.reply_keyboard import KeyboardButton
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton


from typer import Typer

from src.db.mongo import db_collection
from src.tasks import get_all_dramatiq

# TODO: сделать возможность отправки кнопки закончить после каждого фото
# TODO: реализовать отложенные задачи

User = db_collection("User")
Data_menu = db_collection("Data_menu")
mybot = Typer()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("TG_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


web_app = WebAppInfo(url=os.getenv("WEBAPP_URL"))

main_keyboard = InlineKeyboardMarkup()

webapp_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Услуги', web_app=web_app)]
    ]
)

class AppealStates(StatesGroup):
    waiting_appeal_text = State()
    waiting_appeal_photo = State()
    sendInvoice = State()
    moneybox = State()



@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    if message.from_user.id != message.chat.id:
        return

    inlineKeyboard = main_keyboard.add(types.InlineKeyboardButton("Написать обращение", callback_data="appeal"))
    inlineKeyboard = main_keyboard.add(InlineKeyboardButton(text = "Отправить пожертвование в копилку: ", callback_data='payment'))


    data = Data_menu.find_by_sort([("period", -1)])

    await message.answer(f"Добрый день, {message.from_user.full_name}" + 
    f"\n{data['date'][1]}.{data['date'][0]}" + 
    f"\nТемпература: {data['temp']} | Влажность: {data['humidity']}%" +
    f"\nДавление: {data['pressure']} рт. ст." +
    f"\nКурс: ${data['currency'][0]}, €{data['currency'][1]}", reply_markup=inlineKeyboard)




@dp.callback_query_handler(lambda c: c.data == 'payment')
async def activate_payment(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, 'Отправьте сумму пожертвования: ')
    await AppealStates.sendInvoice.set()


@dp.message_handler(state=AppealStates.sendInvoice)
async def get_amout(message: types.Message, state: FSMContext):

    try:
        PRICE = types.LabeledPrice(label='Пожертвование', amount=int(message.text) * 100)
        await bot.send_invoice(message.chat.id, title='Working Time Machine',
                            description='Переведенные средства пойдут на благоустройство ЖК',
                            provider_token='381764678:TEST:50701',
                            currency='rub',
                            prices=[PRICE],
                            start_parameter='time-machine-example',
                            payload='HAPPY FRIDAYS COUPON')

        await state.finish()
    except: 
        await bot.send_message(message.chat.id, "Введено некоректное значение! Значение суммы должно быть целым числом большим 100. Попробуйте еще раз:")
    

@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Ошибка оплаты")



@dp.message_handler(state=AppealStates.waiting_appeal_text)
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


@dp.message_handler(state=AppealStates.waiting_appeal_photo, content_types=['document', 'text', 'photo'])
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


@dp.callback_query_handler(state=AppealStates.waiting_appeal_photo)
async def appeal_photo_ready(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    if callback.data == "appeal_photo_ready":
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
    elif callback.data == "appeal_cancel":
        await appeal_cancel(callback, state)


@dp.callback_query_handler(state=AppealStates.waiting_appeal_text)
async def appeal_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    if callback.data != "appeal_cancel":
        return

    await callback.message.answer("Вы отменили обращение")
    await state.finish()


@dp.callback_query_handler()
async def callback_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    if (callback.data == "appeal"):
        button = types.InlineKeyboardButton(
            "Отмена", callback_data="appeal_cancel")
        inlineKeyboard = types.InlineKeyboardMarkup().add(button)

        await callback.message.answer("Введите текст обращения", reply_markup=inlineKeyboard)
        await state.set_state(AppealStates.waiting_appeal_text)


@dp.message_handler(content_types='web_app_data')
async def get_data(message):
    data = json.loads(message.web_app_data.data)
    #await bot.send_message(message.chat.id, data, reply_markup=keyboard)
    await bot.send_contact(chat_id=message.chat.id,phone_number=data['tel'], first_name=data['first_name'])


@mybot.command()
def run() -> None:
    get_all_dramatiq()
    executor.start_polling(dp, skip_updates=False)
