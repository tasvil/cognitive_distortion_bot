from src.database.base import engine, Base, SessionLocal
from src.database.models import User, UserActionLog
import logging
from src.config import config
from sqlalchemy import update

logger = logging.getLogger('bot.database')


def init_db():
    logger.info("Creating DB if not exists...")
    Base.metadata.create_all(bind=engine)
    logger.info("Creating DB if not exists - Done")


def update_tester_status():
    # Получение списка идентификаторов тестеров из конфигурации
    tester_ids = config.TESTER_IDS

    # Создание сессии
    session = SessionLocal()

    try:
        # Установка is_tester в False для всех пользователей
        stmt_false = update(User).values(is_tester=False)
        session.execute(stmt_false)

        # Если список TESTER_IDS не пуст, устанавливаем is_tester в True для указанных пользователей
        if tester_ids:
            stmt_true = (
                update(User)
                .where(User.user_id.in_(tester_ids))
                .values(is_tester=True)
            )
            session.execute(stmt_true)

        # Фиксация изменений в базе данных
        session.commit()
        logger.debug("Статусы тестеров успешно обновлены.")
    except Exception as error:
        session.rollback()
        logger.error(f"Ошибка при обновлении базы данных: {error}")
    finally:
        # Закрытие сессии
        session.close()
        # Закрытие сессии
        session.close()