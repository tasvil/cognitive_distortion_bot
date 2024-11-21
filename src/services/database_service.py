from sqlalchemy.orm import Session
from src.database.models import User
from src.database.base import SessionLocal

import logging

logger = logging.getLogger('bot.services.database')


class DatabaseService:
    def __init__(self):
        self.db_session = SessionLocal()

    def get_user(self, user_id: int):
        return self.db_session.query(User).filter(User.user_id == user_id).first()

    def add_user(self, user_id: int, username: str, first_name: str, last_name: str):
        db_user = User(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)
        return db_user

    def user_exists(self, user_id: int) -> bool:
        return self.get_user(user_id) is not None

    def close(self):
        self.db_session.close()
