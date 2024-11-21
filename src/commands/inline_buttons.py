from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

router = Router()

import logging

logger = logging.getLogger('bot.commands.inline_buttons')


def get_inline_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Кнопка 1", callback_data="button1")],
        [InlineKeyboardButton(text="Кнопка 2", callback_data="button2")],
    ])

@router.message(Command("inline_buttons"))
async def show_inline_buttons(message: Message):
    await message.answer("Выберите опцию:", reply_markup=get_inline_keyboard())

@router.callback_query(lambda c: c.data and c.data.startswith("button"))
async def process_callback(callback_query: CallbackQuery):
    code = callback_query.data
    response = "Вы нажали кнопку 1" if code == "button1" else "Вы нажали кнопку 2"
    await callback_query.message.answer(response)
    await callback_query.answer()
