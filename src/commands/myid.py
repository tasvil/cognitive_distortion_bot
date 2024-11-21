import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

logger = logging.getLogger('bot.commands.myid')

@router.message(Command("myid"))
async def send_user_id(message: Message):
    logger.debug(f'{message.from_user.username}:{message.from_user.id}:myid')
    user_id = message.from_user.id
    await message.answer(f"Ваш идентификатор: {user_id}")
