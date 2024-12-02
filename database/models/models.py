from sqlalchemy import CheckConstraint, Column, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, UniqueConstraint

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Companies(Base):
    __tablename__ = 'companies'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='companies_pkey'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    devices = relationship('Devices', back_populates='company')


class Firmwares(Base):
    __tablename__ = 'firmwares'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='firmwares_pkey'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    device_firmwares = relationship('DeviceFirmwares', back_populates='firmware')
    devices_firmwares = relationship('DevicesFirmwares', back_populates='firmware')


class Devices(Base):
    __tablename__ = 'devices'
    __table_args__ = (
        CheckConstraint('(primary_conf >= 1) AND (primary_conf <= 3)', name='devices_primary_conf_check'),
        CheckConstraint('dev_type = ANY (ARRAY[1, 2])', name='devices_dev_type_check'),
        ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE', name='devices_company_id_fkey'),
        PrimaryKeyConstraint('id', name='devices_pkey')
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    company_id = Column(Integer, nullable=False)
    dev_type = Column(Integer, nullable=False)
    primary_conf = Column(Integer, nullable=False)
    port_num = Column(Integer, nullable=False)
    model = Column(Integer)

    company = relationship('Companies', back_populates='devices')
    device_firmwares = relationship('DeviceFirmwares', back_populates='device')
    devices_firmwares = relationship('DevicesFirmwares', back_populates='device')


class DeviceFirmwares(Base):
    __tablename__ = 'device_firmwares'
    __table_args__ = (
        ForeignKeyConstraint(['device_id'], ['devices.id'], ondelete='CASCADE', name='device_firmwares_device_id_fkey'),
        ForeignKeyConstraint(['firmware_id'], ['firmwares.id'], ondelete='CASCADE', name='device_firmwares_firmware_id_fkey'),
        PrimaryKeyConstraint('id', name='device_firmwares_pkey'),
        UniqueConstraint('device_id', 'firmware_id', name='unique_device_firmware')
    )

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, nullable=False)
    firmware_id = Column(Integer, nullable=False)

    device = relationship('Devices', back_populates='device_firmwares')
    firmware = relationship('Firmwares', back_populates='device_firmwares')


class DevicesFirmwares(Base):
    __tablename__ = 'devices_firmwares'
    __table_args__ = (
        ForeignKeyConstraint(['device_id'], ['devices.id'], ondelete='CASCADE', name='devices_firmwares_device_id_fkey'),
        ForeignKeyConstraint(['firmware_id'], ['firmwares.id'], ondelete='CASCADE', name='devices_firmwares_firmware_id_fkey'),
        PrimaryKeyConstraint('id', name='devices_firmwares_pkey')
    )

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, nullable=False)
    firmware_id = Column(Integer, nullable=False)

    device = relationship('Devices', back_populates='devices_firmwares')
    firmware = relationship('Firmwares', back_populates='devices_firmwares')
