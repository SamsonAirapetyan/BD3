from aiogram import types, Dispatcher
from ..models.Mariadb import Database
from ..keabords.Choise import choise, cansel, keyboard, requests
from ..models.Add_device import AddProduct
from aiogram.dispatcher import FSMContext
import mariadb

db = Database()


async def select_requests(message: types.Message):
    print(message.from_user.first_name)
    await message.answer(text="На выбор есть 2 запроса\nЕсли вам никакая не нужна - нажмите кнопку отмена",
                         reply_markup=requests)


async def count_device(call: types.CallbackQuery):
    await db.create()
    try:
        answer = db.count_of_device()
        await call.message.answer(f"Количество приборов в ремонтных работах: {answer[0]}")
    except Exception as err:
        print(err)


async def sum(call: types.CallbackQuery):
    await db.create()
    try:
        answer = db.sum_cost()
        await call.message.answer(f"Выручка со всех ремонтых работ: {answer[0]}$")
    except Exception as err:
        print(err)


def register_function(dp: Dispatcher):
    dp.register_message_handler(select_requests, text="Запросы")
    dp.register_callback_query_handler(count_device, text="count")
    dp.register_callback_query_handler(sum, text="sum")
