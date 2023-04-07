from aiogram import types, Dispatcher
from ..models.Mariadb import Database
from ..keabords.Choise import choise, cansel, keyboard
from ..models.Add_device import AddWork_repair
from aiogram.dispatcher import FSMContext
import mariadb

db = Database()


async def add_Work_Repair(call: types.CallbackQuery):
    print(call.from_user.first_name)
    await call.message.answer("Для добавления Ремонтных работ введите следующие данные\n"
                              "<b>Важно!</b> вводите существующие данные\n<i>(код прибора, код мастера)</i>:")
    await call.message.answer("<i>Код прибора: </i>", reply_markup=cansel)
    await AddWork_repair.Point_2.set()


async def add_cod_master(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(id=answer)
    await message.answer("<i>Код мастера:</i>", reply_markup=cansel)
    await AddWork_repair.next()


async def add_FIO(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(id_master=answer)
    await message.answer("<i>ФИО владельца прибора:</i>", reply_markup=cansel)
    await AddWork_repair.next()


async def add_Date(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(name=answer)
    await message.answer("<i>Дата приема в ремонт\nв формате yyyy-mm-dd:</i>", reply_markup=cansel)
    await AddWork_repair.next()


async def add_type(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(Date=answer)
    await message.answer("<i>Тип поломки:</i>", reply_markup=cansel)
    await AddWork_repair.next()


async def add_cost(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(Type=answer)
    await message.answer("<i>Стоимость поломки:</i>", reply_markup=cansel)
    await AddWork_repair.next()


async def add_Cod_repair(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(Cost=answer)
    await message.answer("<i>Код ремонта:</i>", reply_markup=cansel)
    await AddWork_repair.next()


async def final(message: types.Message, state: FSMContext):
    data = await state.get_data()
    Id = data.get("id")
    Id_master = data.get("id_master")
    Name = data.get("name")
    Date = data.get("Date")
    Type = data.get("Type")
    Cost = data.get("Cost")
    Cod_repair = message.text
    await state.update_data(Cod=Cod_repair)

    await message.answer(f"Данные прибора:\n\n"
                         f"<i> Код прибора: </i>{Id}\n"
                         f"<i> Код мастера: </i>{Id_master}\n"
                         f"<i> ФИО владельца: </i>{Name}\n"
                         f"<i> Дата приема в ремонт: </i>{Date}\n"
                         f"<i> Тип поломки: </i>{Type}\n"
                         f"<i> Стоимость ремонта: </i>{Cost}\n"
                         f"<i> Код ремонта: </i>{Cod_repair}\n",
                         reply_markup=keyboard)
    await AddWork_repair.next()


async def apload(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    Id = data.get("id")
    Id_master = data.get("id_master")
    Name = data.get("name")
    Date = data.get("Date")
    Type = data.get("Type")
    Cost = data.get("Cost")
    Cod_repair = data.get("Cod")
    await db.create()
    try:
        db.add_Work_Repair(Id=Id, Id_master=Id_master, Name=Name, Date=Date, Type=Type, Cost=Cost, Cod=Cod_repair)
    except mariadb.Error as err:
        print(err)
    await call.message.answer("Добавлено в БД")
    await state.finish()


async def cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Отмена добавления")
    await state.finish()


def register_add_repair_work(dp: Dispatcher):
    dp.register_callback_query_handler(add_Work_Repair, text="Work_Repair")
    dp.register_message_handler(add_cod_master, state=AddWork_repair.Point_2)
    dp.register_message_handler(add_FIO, state=AddWork_repair.Point_3)
    dp.register_message_handler(add_Date, state=AddWork_repair.Point_4)
    dp.register_message_handler(add_type, state=AddWork_repair.Point_5)
    dp.register_message_handler(add_cost, state=AddWork_repair.Point_6)
    dp.register_message_handler(add_Cod_repair, state=AddWork_repair.Point_7)
    dp.register_message_handler(final, state=AddWork_repair.Point_8)
    dp.register_callback_query_handler(apload, state=AddWork_repair.Point_9)
    dp.register_callback_query_handler(cancel, state=AddWork_repair.all_states, text="cancel")
