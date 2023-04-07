from aiogram import types, Dispatcher
from ..models.Mariadb import Database
from ..keabords.Choise import choise, cansel, keyboard
from ..models.Add_device import AddProduct
from aiogram.dispatcher import FSMContext
import mariadb

db = Database()


async def select_BD(message: types.Message):
    print(message.from_user.first_name)
    await message.answer(text="На выбор есть 3 БД\nЕсли вам никакая не нужна - нажмите кнопку отмена",
                         reply_markup=choise)


async def add_device(call: types.CallbackQuery):
    await call.message.answer("Для добавления товара введите следующие данные:")
    await call.message.answer("<i>Код прибора в ремонте: </i>", reply_markup=cansel)
    await AddProduct.Point_2.set()


async def add_name(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(id=answer)
    await message.answer("<i>Название прибора</i>", reply_markup=cansel)
    await AddProduct.next()


async def add_description(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(name=answer)
    await message.answer("<i>Тип прибора</i>", reply_markup=cansel)
    await AddProduct.next()


async def add_date(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(type=answer)
    await message.answer("<i>Дата производства\nв формате yyyy-mm-dd</i>", reply_markup=cansel)
    await AddProduct.next()


async def final(message: types.Message, state: FSMContext):
    data = await state.get_data()
    Id = data.get("id")
    Name = data.get("name")
    Type = data.get("type")
    Date = message.text
    await state.update_data(Date=Date)

    await message.answer(f"Данные прибора:\n\n"
                         f"<i> Код прибора в ремонте: </i>{Id}\n"
                         f"<i> Название прибора: </i>{Name}\n"
                         f"<i> Тип прибора: </i>{Type}\n"
                         f"<i> Дата производства: </i>{Date}\n",
                         reply_markup=keyboard)

    await AddProduct.next()


async def apload(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    Id = data.get("id")
    Name = data.get("name")
    Type = data.get("type")
    Date = data.get("Date")
    await db.create()
    try:
        db.add_device(Id=Id, Name=Name, Type=Type, Date=Date)
    except mariadb.Error as err:
        print(err)
    await call.message.answer("Добавлено в БД")
    await state.finish()


async def cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Отмена добавления")
    await state.finish()


def register_add_info(dp: Dispatcher):
    dp.register_message_handler(select_BD, text="Ввод данных в БД")
    dp.register_callback_query_handler(add_device, text="Device")
    dp.register_message_handler(add_name, state=AddProduct.Point_2)
    dp.register_message_handler(add_description, state=AddProduct.Point_3)
    dp.register_message_handler(add_date, state=AddProduct.Point_4)
    dp.register_message_handler(final, state=AddProduct.Point_5)
    dp.register_callback_query_handler(apload, state=AddProduct.Point_6, text="apload")
    dp.register_callback_query_handler(cancel, state=AddProduct.all_states, text="cancel")
