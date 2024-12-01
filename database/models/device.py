from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .base import Base


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)

    company = relationship("Company", back_populates="devices")
    firmware = relationship("DeviceFirmware", back_populates="device")

    def __repr__(self):
        return f"<Device(id={self.id}, name='{self.name}', company_id={self.company_id})>"