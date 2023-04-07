from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=
    [
        [
            KeyboardButton(text="Ввод данных в БД"),
            KeyboardButton(text="Запросы")
        ],
        [
            KeyboardButton(text="Отмена")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)