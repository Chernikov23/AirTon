from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Баланс", callback_data="balance"),
            InlineKeyboardButton(text="Отправить", callback_data="send")
        ]
    ]
)
