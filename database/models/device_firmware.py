from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .base import Base

class DeviceFirmware(Base):
    __tablename__ = 'device_firmwares'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    firmware_id = Column(Integer, ForeignKey('firmwares.id'), nullable=False)

    # Определение отношений
    device = relationship("Device", back_populates="firmwares")
    firmware = relationship("Firmware", back_populates="devices")

    def __repr__(self):
        return (f"<DeviceFirmware(id={self.id}, device_id={self.device_id}, "
                f"firmware_id={self.firmware_id})>")