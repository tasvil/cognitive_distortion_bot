from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session
from src.database.models import User, UserActionLog
from src.database import SessionLocal
from datetime import datetime
from src.states.thought_analysis_states import ThoughtAnalysis  # Импортируем нужные состояния

import logging

logger = logging.getLogger('bot.middlewares.user_check_and_log')


class UserCheckAndBalanceMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        username = event.from_user.username
        first_name = event.from_user.first_name
        last_name = event.from_user.last_name

        session: Session = SessionLocal()
        state: FSMContext = data["state"]  # Получаем текущее состояние пользователя

        try:
            # Проверка и добавление пользователя
            user = session.query(User).filter(User.user_id == user_id).first()
            if not user:
                user = User(
                    user_id=user_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                )
                session.add(user)
                session.commit()
                data['is_new_user'] = True
            else:
                data['is_new_user'] = False

            # Проверка: если пользователь тестер, пропускаем списание баллов
            if user.is_tester:
                logger.debug(f'{username}:{user_id}:is_tester')
                return await handler(event, data)

            logger.debug(f'{username}:{user_id}:user_balance:{user.balance}')
            # Проверка состояния и списание баллов в нужных состояниях
            current_state = await state.get_state()
            
            # Если пользователь входит в начальное состояние анализа
            if current_state == ThoughtAnalysis.enter_thought.state:
                if user.balance < 0.5:
                    await event.answer("У вас недостаточно баллов для начала анализа.")
                    return  # Прерываем обработку, если баллов не хватает
                user.balance -= 0.5  # Списание 0.5 балла за начало анализа
                session.commit()

            # Если пользователь завершает цепочку
            elif current_state == ThoughtAnalysis.provide_rational_response.state:
                if user.balance < 0.5:
                    await event.answer("У вас недостаточно баллов для завершения анализа.")
                    return  # Прерываем обработку, если баллов не хватает
                user.balance -= 0.5  # Списание еще 0.5 балла за завершение анализа
                session.commit()

            # Логирование действия
            action_data = {
                "text": event.text,
                "timestamp": datetime.now().isoformat(),
                "state": current_state
            }
            new_log = UserActionLog(
                user_id=user_id,
                action_data=action_data,
            )
            session.add(new_log)
            session.commit()

        finally:
            session.close()

        # Передаем управление следующему обработчику
        return await handler(event, data)
