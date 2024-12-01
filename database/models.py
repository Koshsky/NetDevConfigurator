from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    devices = relationship("Device", back_populates="company")

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>"

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    dev_type = Column(Integer, nullable=False)
    model = Column(Integer)
    prim_conf = Column(Integer, nullable=False)
    port_num = Column(Integer, nullable=False)

    company = relationship("Company", back_populates="devices")
    firmwares = relationship("DeviceFirmware", back_populates="device")

    def __repr__(self):
        return f"<Device(id={self.id}, name='{self.name}', company_id={self.company_id})>"

class Firmware(Base):
    __tablename__ = 'firmwares'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    device_firmwares = relationship("DeviceFirmware", back_populates="firmware")

    def __repr__(self):
        return f"<Firmware(id={self.id}, name='{self.name}')>"

class DeviceFirmware(Base):
    __tablename__ = 'devices_firmwares'

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    firmware_id = Column(Integer, ForeignKey('firmwares.id'), nullable=False)

    device = relationship("Device", back_populates="firmwares")
    firmware = relationship("Firmware", back_populates="device_firmwares")

    def __repr__(self):
        return f"<DeviceFirmware(id={self.id}, device_id={self.device_id}, firmware_id={self.firmware_id})>"

# Создание подключения к базе данных
DATABASE_URL = "postgresql://username:password@localhost:5432/device_registry"  # Замените на ваши данные
engine = create_engine(DATABASE_URL)

# Создание всех таблиц в базе данных (если они еще не существуют)
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()