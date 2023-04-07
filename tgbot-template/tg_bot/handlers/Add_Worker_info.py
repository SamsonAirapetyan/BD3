from aiogram import types, Dispatcher
from ..models.Mariadb import Database
from ..keabords.Choise import choise, cansel, keyboard
from ..models.Add_device import AddWorker
from aiogram.dispatcher import FSMContext
import mariadb

db = Database()


async def add_worker(call: types.CallbackQuery):
    print(call.from_user.first_name)
    await call.message.answer("Для добавления товара введите следующие данные:")
    await call.message.answer("<i>Код мастера: </i>", reply_markup=cansel)
    await AddWorker.Point_2.set()


async def add_FIO(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(id=answer)
    await message.answer("<i>ФИО мастера:</i>", reply_markup=cansel)
    await AddWorker.next()


async def add_category(message: types.Message, state: FSMContext):
    answer = message.text
    fio = answer.split(' ')
    print(fio)
    await state.update_data(surname=fio[0])
    await state.update_data(name=fio[1])
    await state.update_data(patronymic=fio[2])
    await message.answer("<i>Категория мастера:</i>", reply_markup=cansel)
    await AddWorker.next()


async def add_Date_Reception(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(category=answer)
    await message.answer("<i>Дата приема на работу\nв формате yyyy-mm-dd:</i>", reply_markup=cansel)
    await AddWorker.next()


async def final(message: types.Message, state: FSMContext):
    data = await state.get_data()
    Id = data.get("id")
    Surname = data.get("surname")
    Name = data.get("name")
    Patronymic = data.get("patronymic")
    Category = data.get("category")
    Date = message.text
    await state.update_data(Date=Date)

    await message.answer(f"Данные прибора:\n\n"
                         f"<i> Код мастера: </i>{Id}\n"
                         f"<i> Фамилия мастера: </i>{Surname}\n"
                         f"<i> Имя мастера: </i>{Name}\n"
                         f"<i> Отчество мастера: </i>{Patronymic}\n"
                         f"<i> Разряд мастера: </i>{Category}\n"
                         f"<i> Дата приема на работу: </i>{Date}\n",
                         reply_markup=keyboard)
    await AddWorker.next()


async def apload(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    Id = data.get("id")
    Surname = data.get("surname")
    Name = data.get("name")
    Patronymic = data.get("patronymic")
    Category = data.get("category")
    Date = data.get("Date")
    await db.create()
    try:
        db.add_worker(Id=Id, Surname=Surname, Name=Name, Patronymic=Patronymic, Category=Category, Date=Date)
    except mariadb.Error as err:
        print(err)
    await call.message.answer("Добавлено в БД")
    await state.finish()


async def cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Отмена добавления")
    await state.finish()


def register_add_info_worker(dp: Dispatcher):
    dp.register_callback_query_handler(add_worker, text="Worker")
    dp.register_message_handler(add_FIO, state=AddWorker.Point_2)
    dp.register_message_handler(add_category, state=AddWorker.Point_3)
    dp.register_message_handler(add_Date_Reception, state=AddWorker.Point_4)
    dp.register_message_handler(final, state=AddWorker.Point_5)
    dp.register_callback_query_handler(apload, state=AddWorker.Point_6)
    dp.register_callback_query_handler(cancel, state=AddWorker.all_states, text="cancel")
