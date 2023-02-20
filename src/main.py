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

import send_appeal
import send_advert
from bot import bot

class InvoiceStates(StatesGroup):
    sendInvoice = State()
    moneybox = State()

from typer import Typer

from src.db.mongo import db_collection

from src.func.info import get_weather_and_currency
# TODO: сделать возможность отправки кнопки закончить после каждого фото
# TODO: реализовать отложенные задачиы

User = db_collection("User")
mybot = Typer()
logging.basicConfig(level=logging.INFO)

# bot = Bot(token=os.getenv("TG_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


web_app = WebAppInfo(url=os.getenv("WEBAPP_URL"))

main_keyboard = InlineKeyboardMarkup()

webapp_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Услуги', web_app=web_app)]
    ]
)



@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    if message.from_user.id != message.chat.id:
        return

    inlineKeyboard = main_keyboard.add(types.InlineKeyboardButton("Написать обращение", callback_data="appeal"))
    inlineKeyboard = main_keyboard.add(InlineKeyboardButton(text = "Отправить пожертвование в копилку: ", callback_data='payment'))


    data = await get_weather_and_currency()

    await message.answer(f"Добрый день, {message.from_user.full_name}" + 
    f"\n{data['date'][1]}.{data['date'][0]}" + 
    f"\nТемпература: {data['temp']} | Влажность: {data['humidity']}%" +
    f"\nДавление: {data['pressure']} рт. ст." +
    f"\nКурс: ${data['currency'][0]}, €{data['currency'][1]}", reply_markup=inlineKeyboard)




@dp.callback_query_handler(lambda c: c.data == 'payment')
async def activate_payment(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, 'Отправьте сумму пожертвования: ')
    await InvoiceStates.sendInvoice.set()


@dp.message_handler(state=InvoiceStates.sendInvoice)
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

@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Спасибо!' )    

@dp.message_handler(content_types='web_app_data')
async def get_data(message):
    data = json.loads(message.web_app_data.data)
    #await bot.send_message(message.chat.id, data, reply_markup=keyboard)
    await bot.send_contact(chat_id=message.chat.id,phone_number=data['tel'], first_name=data['first_name'])


@mybot.command()
def run() -> None:
    send_appeal.setup(dp)
    send_advert.setup(dp)
    executor.start_polling(dp, skip_updates=False)