from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .company import Company
from .device import Device
from .firmware import Firmware
from .device_firmware import DeviceFirmware
from .base import Base  # Предполагается, что у вас есть файл base.py с определением Base

# Настройки подключения к базе данных
DATABASE_URL = 'sqlite:///example.db'  # Замените на вашу строку подключения

# Создание движка
engine = create_engine(DATABASE_URL)

# Создание базы данных (если она еще не существует)
Base.metadata.create_all(engine)

# Создание сессии
Session = scoped_session(sessionmaker(bind=engine))

def get_session():
    """Функция для получения текущей сессии."""
    return Session()

def close_session():
    """Функция для закрытия текущей сессии."""
    Session.remove()