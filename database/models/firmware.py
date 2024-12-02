from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from .base import Base

class Firmware(Base):
    __tablename__ = 'firmwares'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Firmware(id={self.id}, name='{self.name}')>"