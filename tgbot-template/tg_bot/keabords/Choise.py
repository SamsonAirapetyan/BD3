from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

choise = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [
        InlineKeyboardButton(text="Worker", callback_data="Worker"),
        InlineKeyboardButton(text="Device", callback_data="Device"),
        InlineKeyboardButton(text="Work_Repair", callback_data="Work_Repair"),
    ],
    [
        InlineKeyboardButton(
            text="Отмена",
            callback_data="cancel"
        )
    ]
])

cansel = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Отмена",
            callback_data="cancel"
        )
    ]
])

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить", callback_data="apload"),
            InlineKeyboardButton(text="Отмена", callback_data="cancel")
        ]
    ]
)

requests = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Количество приборов", callback_data="count"),
            InlineKeyboardButton(text="общая выручка", callback_data="sum")
        ]
    ]
)

