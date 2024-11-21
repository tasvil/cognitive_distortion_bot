from sqlalchemy import Column, Integer, JSON, String, DateTime, Boolean
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    balance = Column(Integer, default=3)  # Стартовый баланс в 3 балла
    is_tester = Column(Boolean, default=False)  # Поле для тестеров с неограниченным доступом
    created_at = Column(DateTime, default=datetime.now)

class UserActionLog(Base):
    __tablename__ = "user_action_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    action_data = Column(JSON, nullable=False)  
    created_at = Column(DateTime, default=datetime.now) 
