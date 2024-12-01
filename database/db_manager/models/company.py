from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .base import Base


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)

    devices = relationship("Device", back_populates="company")

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', address='{self.address}')>"