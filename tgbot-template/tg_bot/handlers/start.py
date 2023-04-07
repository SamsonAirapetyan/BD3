from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command, CommandStart, BoundFilter, Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ..filters.Admin import IsAdmin
from ..models.Mariadb import Database
from ..keabords.Menu import menu

db = Database()


async def start_admin(message: types.Message):
    await message.answer("Добро пожаловать!", reply_markup=menu)

    # await message.answer_photo(photo= 'https://arhivach.ng/storage/7/f8/7f867fbd0ad724b080e014d2c8999e80.png', caption='Пора топить и визуализировать')


async def start_users(message: types.Message):
    user = message.from_user.first_name
    await message.answer(f"Hello,{user},I'm ready to work", reply_markup=menu)


# async def select(message: types.Message):
#     await db.create()
#     try:
#         answer = db.select_code_delivery()
#         await message.answer(answer[0][0])
#     except Exception as err:
#         print(err)


async def motivation(message: types.Message):
    if message.text == "Отмена":
        await message.answer("Отменено")

async def cam(call: types.CallbackQuery):
    await call.message.answer("Отменено")

def register_start_admin(dp: Dispatcher):
    dp.register_message_handler(start_admin, CommandStart(), IsAdmin())
    dp.register_message_handler(start_users, CommandStart())
    # dp.register_message_handler(select, text="Maria")
    dp.register_message_handler(motivation, Text(equals=["Отмена"]))
    dp.register_callback_query_handler(cam, text = "cancel")