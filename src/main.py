import logging, os, json

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
from src.barrier import setup as barrier_setup, BarrierStates
from src.security import setup as security_setup, SecurityStates, cancel_keyboard
from src.masters import setup as masters_setup, MasterStates, cancel_keyboard
from src.vote import setup as votes_setup, VoteStates, cancel_keyboard
from src.send_advert_appart import setup as send_advert_apart_setup, AppartRentState
from src.bot import bot

from aiogram.types.poll import Poll

import src.func.info as get_weather_and_currency

from src.keyboards import webapp_keyboard, main_keyboard, rent_keyboard, buy_keyboard, master_keyboard

class InvoiceStates(StatesGroup):
    sendInvoice = State()
    moneybox = State()

from typer import Typer

from src.db.mongo import db_collection
from src.tasks import get_all_dramatiq

# TODO: сделать возможность отправки кнопки закончить после каждого фото
# TODO: реализовать отложенные задачи
# TODO: добавить все чаты в .env

User = db_collection("User")
Data_menu = db_collection("Data_menu")
mybot = Typer()
logging.basicConfig(level=logging.INFO)

# bot = Bot(token=os.getenv("TG_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    if message.from_user.id != message.chat.id:
        return

    data = Data_menu.find_by_sort([("period", -1)])
    await message.answer(f"Добрый день, {message.from_user.full_name}!", reply_markup=webapp_keyboard)
    await message.answer(
    f"\nПоследнее обновление: {data['date']}" + 
    f"\nТемпература: {data['temp']}°С | Влажность: {data['humidity']}%" +
    f"\nДавление: {data['pressure']} рт. ст." +
    f"\nКурс: ${data['currency'][0]}, €{data['currency'][1]}", reply_markup=main_keyboard)


    # data = get_info.get_weather_and_currency()
    # await message.answer(f"Добрый день, {message.from_user.full_name}!", reply_markup=webapp_keyboard)
    # await bot.send_message(message.chat.id, 
    # f"\n{data['date'][1]}.{data['date'][0]}" + 
    # f"\nТемпература: {data['temp']} | Влажность: {data['humidity']}%" +
    # f"\nДавление: {data['pressure']} рт. ст." +
    # f"\nКурс: ${data['currency'][0]}, €{data['currency'][1]}", reply_markup=main_keyboard)`
    # await bot.send_message(message.chat.id,"-",reply_markup=main_keyboard)
    # await message.answer_poll(question='Your answer?',
    #                           options=['A)', 'B)', 'C'],
    #                           type='quiz',
    #                           correct_option_id=1,
    #                           is_anonymous=False)




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

@dp.callback_query_handler(lambda c: c.data in ["appeal", "rent_appart", "rent_parking", "barrier"])
async def appeal_or_rent(cb: types.CallbackQuery):
    await cb.answer()
    if cb.data == "appeal":
        await AppealStates.waiting_appeal_text.set()
        await cb.message.answer("Введите текст обращения")
    elif cb.data == "rent_parking":
        await RentStates.waiting_rent_text.set()
        await cb.message.answer("Введите описание места")
    elif cb.data == "rent_appart":
        await AppartRentState.waiting_rent_text.set()
        await cb.message.answer("Введите описание")
    elif cb.data == "barrier":
        await BarrierStates.waiting_barrier_text.set()
        barrier_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Отмена", callback_data='barrier_cancel'))
        await cb.message.answer("Введите информацию, по которой охранник пропустит гостя (номер авто, название компании доставки и т.д):", reply_markup=barrier_keyboard)

# @dp.callback_query_handler(lambda c: c.data in ["buy_parking", "buy_appart"])
# async def buy(cb: types.CallbackQuery):
#     await cb.answer()
#     if cb.data == 'buy_parking':



@dp.callback_query_handler(lambda c: c.data == 'rent_menu')
async def set_rent(cb: types.CallbackQuery):
    await cb.message.edit_text(cb.message.text, reply_markup=rent_keyboard)

@dp.callback_query_handler(lambda c: c.data == 'buy_menu')
async def set_buy(cb: types.CallbackQuery):
    await cb.message.edit_text(cb.message.text, reply_markup=buy_keyboard)

@dp.callback_query_handler(lambda c: c.data == 'goback')
async def rent_goback(cb: types.CallbackQuery):
    await cb.message.edit_text(cb.message.text, reply_markup=main_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'order_master')
async def rent_goback(cb: types.CallbackQuery, state=FSMContext):
    await cb.message.edit_text("Выберите тип услуги:", reply_markup=master_keyboard)
    await state.set_state(MasterStates.waiting_order_type)

@dp.callback_query_handler(lambda c: c.data == 'create_vote')
async def rent_goback(cb: types.CallbackQuery, state=FSMContext):
    await cb.message.answer("Напишите вопрос, который будет решаться голосванием: ")
    await state.set_state(VoteStates.waiting_vote_question)

@dp.callback_query_handler(lambda c: c.data in ['order_cleaning', 'order_logistic', 'order_repair', 'order_painter', 'order_electrician', 'order_plumber'], state=MasterStates.waiting_order_type )
async def handle_master(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.answer("Опишите пробему, которую нужно решить:", reply_markup=cancel_keyboard)
    await state.set_state(MasterStates.waiting_order_text)
    if cb.data == 'order_cleaning':
        await state.update_data(type='Клининг')
    elif cb.data == 'order_logistic':
        await state.update_data(type='Логистика')
    elif cb.data == 'order_painter':
        await state.update_data(type='Маляры')
    elif cb.data == 'order_repair':
        await state.update_data(type='Ремонт')
    elif cb.data == 'order_logistic':
        await state.update_data(type='Логистика')
    elif cb.data == 'order_electrician':
        await state.update_data(type='Электрика')
    elif cb.data == 'order_plumber':
        await state.update_data(type='Сантехника')
    
@dp.callback_query_handler(lambda c: c.data == 'request_secr')
async def rent_goback(cb: types.CallbackQuery, state=FSMContext):
    await cb.message.answer("Напишите номер дома: ", reply_markup=cancel_keyboard)
    await state.set_state(SecurityStates.waiting_home_number)
        


@mybot.command()
def run() -> None:
    send_appeal_setup(dp)
    send_advert_setup(dp)
    send_advert_apart_setup(dp)
    barrier_setup(dp)
    masters_setup(dp)
    votes_setup(dp)
    security_setup(dp)

    logging.info("[RUN SERVICE]")
    
    get_all_dramatiq()
    executor.start_polling(dp, skip_updates=False)
