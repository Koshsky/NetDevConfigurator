from sqlalchemy import CheckConstraint, Column, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, UniqueConstraint

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Companies(Base):
    __tablename__ = 'companies'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='companies_pkey'),
        UniqueConstraint('name', name='unique_company_name')
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    devices = relationship('Devices', back_populates='company')


class Families(Base):
    __tablename__ = 'families'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='families_pkey'),
        UniqueConstraint('name', name='families_name_key')
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    devices = relationship('Devices', back_populates='family')


class Firmwares(Base):
    __tablename__ = 'firmwares'
    __table_args__ = (
        CheckConstraint("(type)::text = ANY (ARRAY[('primary_bootloader'::character varying)::text, ('secondary_bootloader'::character varying)::text, ('firmware'::character varying)::text])", name='firmwares_firmware_type_check'),
        PrimaryKeyConstraint('id', name='firmwares_pkey'),
        UniqueConstraint('full_path', name='firmwares_full_path_key'),
        UniqueConstraint('name', name='unique_firmware_name')
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    full_path = Column(String, nullable=False)
    type = Column(String, nullable=False)

    device_firmwares = relationship('DeviceFirmwares', back_populates='firmware')


class Protocols(Base):
    __tablename__ = 'protocols'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='protocols_pkey'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    device_protocols = relationship('DeviceProtocols', back_populates='protocol')


class Devices(Base):
    __tablename__ = 'devices'
    __table_args__ = (
        CheckConstraint("(dev_type)::text = ANY (ARRAY[('router'::character varying)::text, ('switch'::character varying)::text])", name='check_dev_type'),
        ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE', name='devices_company_id_fkey'),
        ForeignKeyConstraint(['family_id'], ['families.id'], name='fk_family'),
        PrimaryKeyConstraint('id', name='devices_pkey'),
        UniqueConstraint('name', name='unique_device_name')
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    company_id = Column(Integer, nullable=False)
    num_gigabit_ports = Column(Integer, nullable=False)
    dev_type = Column(String, nullable=False)
    num_10gigabit_ports = Column(Integer, nullable=False)
    family_id = Column(Integer, nullable=False)

    company = relationship('Companies', back_populates='devices')
    family = relationship('Families', back_populates='devices')
    device_firmwares = relationship('DeviceFirmwares', back_populates='device')
    device_protocols = relationship('DeviceProtocols', back_populates='device')


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


class DeviceProtocols(Base):
    __tablename__ = 'device_protocols'
    __table_args__ = (
        ForeignKeyConstraint(['device_id'], ['devices.id'], ondelete='CASCADE', name='device_protocols_device_id_fkey'),
        ForeignKeyConstraint(['protocol_id'], ['protocols.id'], ondelete='CASCADE', name='device_protocols_protocol_id_fkey'),
        PrimaryKeyConstraint('id', name='device_protocols_pkey')
    )

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, nullable=False)
    protocol_id = Column(Integer, nullable=False)

    device = relationship('Devices', back_populates='device_protocols')
    protocol = relationship('Protocols', back_populates='device_protocols')
