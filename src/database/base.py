from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.config import config

DATABASE_URL = config.DATABASE_URL

engine = create_engine(DATABASE_URL)

# Создание базового класса для всех моделей
Base = declarative_base()

# Создание фабрики для создания сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


