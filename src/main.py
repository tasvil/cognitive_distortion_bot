import asyncio
# import logging
# import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.config import config
from src.database import init_db, update_tester_status
from src.middlewares import UserCheckAndBalanceMiddleware
from src.commands import start, analyze, cancel, buttons, inline_buttons, myid
from src.logger.logger import setup_logger

async def main():
    logger = setup_logger('bot')
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logger.info('Запускаем бота')

    # Инициализация базы данных
    init_db()

    update_tester_status()

    # Инициализация бота и диспетчера
    bot = Bot(
        token=config.TELEGRAM_BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Удаление вебхука и пропуск накопившихся обновлений
    await bot.delete_webhook(drop_pending_updates=True)

    # Регистрация middleware
    dp.message.middleware(UserCheckAndBalanceMiddleware())

    # Регистрация обработчиков команд
    dp.include_router(start.router)
    dp.include_router(analyze.router)
    dp.include_router(cancel.router)
    dp.include_router(buttons.router)
    dp.include_router(inline_buttons.router)
    dp.include_router(myid.router)

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

