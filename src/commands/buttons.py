from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

router = Router()

import logging

logger = logging.getLogger('bot.commands.buttons')


@router.message(Command("buttons"))
async def show_buttons(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Кнопка 1"), KeyboardButton(text="Кнопка 2")],
            [KeyboardButton(text="Кнопка 3")],
        ],
        resize_keyboard=True,
    )
    await message.answer("Вот ваши кнопки:", reply_markup=keyboard)
