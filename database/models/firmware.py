from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship  # Импортируем relationship
from .base import Base

class Firmware(Base):
    __tablename__ = 'firmwares'

    id = Column(Integer, primary_key=True)
    version = Column(String, nullable=False)

    # Определяем связь с DeviceFirmware
    device_firmwares = relationship("DeviceFirmware", back_populates="firmware")

    def __repr__(self):
        return f"<Firmware(id={self.id}, version='{self.version}')>"