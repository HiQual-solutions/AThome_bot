import logging, os, json
import asyncio

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, ContentTypes
from aiogram.utils import executor
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from src.send_appeal import setup as send_appeal_setup, AppealStates
from src.send_advert import setup as send_advert_setup, RentStates
from src.admin_panel import setup as ap_setup, admins
from src.bot import bot

import src.func.info as get_info

from src.keyboards import webapp_keyboard, set_main_keyboard

class InvoiceStates(StatesGroup):
    sendInvoice = State()
    moneybox = State()

from typer import Typer

# from src.db.mongo import db_collection
# from src.tasks import get_all_dramatiq

# TODO: сделать возможность отправки кнопки закончить после каждого фото


# User = db_collection("User")
# Data_menu = db_collection("Data_menu")
mybot = Typer()
logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
    ])

async def check_cmd(message: types.Message, state: FSMContext):
    print(message.text)
    print(await state.get_state())


@dp.message_handler(commands=["start"], state="*")
async def welcome(message: types.Message, state: FSMContext):
    if message.from_user.id != message.chat.id:
        return

    cur_state = await state.get_state()
    print(cur_state, bool(cur_state))

    if bool(cur_state):
        await state.finish()
    # data = Data_menu.find_by _sort([("period", -1)])
    # await message.answer(f"Добрый день, {message.from_user.full_name}" + 
    # f"\n{data['date'][1]}.{data['date'][0]}" + 
    # f"\nТемпература: {data['temp']} | Влажность: {data['humidity']}%" +
    # f"\nДавление: {data['pressure']} рт. ст." +
    # '''f"\nКурс: ${data['currency'][0]}, €{data['currency'][1]}"''', reply_markup=inlineKeyboard)
   

    data = get_info.get_weather_and_currency()
    await message.answer(f"Добрый день, {message.from_user.full_name}" + 
    f"\n{data['date'][1]}.{data['date'][0]}" + 
    f"\nТемпература: {data['temp']} | Влажность: {data['humidity']}%" +
    f"\nДавление: {data['pressure']} рт. ст." +
    f"\nКурс: ${data['currency'][0]}, €{data['currency'][1]}", reply_markup=set_main_keyboard(message.from_id, admins))


@dp.message_handler(commands=["help"], state="*")
async def helper(message: types.message, state: FSMContext):
    if message.from_user.id != message.chat.id:
        return

    cur_state = await state.get_state()
    # print(cur_state, bool(cur_state))

    if bool(cur_state):
        await state.finish()

    await message.answer("Помощник")
    
    # my_cmds = await dp.bot.get_my_commands()
    # print(my_cmds)


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

@dp.callback_query_handler(lambda c: c.data in ["appeal", "parking_rent"])
async def appeal_or_rent(cb: types.CallbackQuery):
    await cb.answer()
    if cb.data == "appeal":
        await AppealStates.waiting_appeal_text.set()
        await cb.message.answer("Введите текст обращения")
    elif cb.data == "parking_rent":
        await RentStates.waiting_rent_text.set()
        await cb.message.answer("Введите описание места")


@mybot.command()
def run() -> None:
    send_appeal_setup(dp)
    send_advert_setup(dp)
    ap_setup(dp)
    
    logging.info("[RUN SERVICE]")
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(set_default_commands(dp)) # tasks to do
    loop.run_until_complete(future) # loop until done
    # get_all_dramatiq()
    # dp.register_message_handler(check_cmd, commands=["start", "help"], state="*")
    executor.start_polling(dp, skip_updates=False)

