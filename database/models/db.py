# models/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .base import Base  # Предполагается, что у вас есть файл base.py с определением Base

def create_engine_and_session(user, password, host, port, database):
    """Создает движок и сессию для подключения к базе данных PostgreSQL."""
    DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = scoped_session(sessionmaker(bind=engine))
    return engine, Session

def get_session(Session):
    """Функция для получения текущей сессии."""
    return Session()

def close_session(Session):
    """Функция для закрытия текущей сессии."""
    Session.remove()