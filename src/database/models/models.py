from sqlalchemy import CheckConstraint, Column, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Sequence, String, Text, UniqueConstraint

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
    templates = relationship('Templates', back_populates='family')


class Ports(Base):
    __tablename__ = 'ports'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='ports_pkey'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    speed = Column(Integer, nullable=False)
    material = Column(String(255))

    device_ports = relationship('DevicePorts', back_populates='port')


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
    dev_type = Column(String, nullable=False)
    family_id = Column(Integer, nullable=False)
    boot = Column(String)
    uboot = Column(String)
    firmware = Column(String)

    company = relationship('Companies', back_populates='devices')
    family = relationship('Families', back_populates='devices')
    device_ports = relationship('DevicePorts', back_populates='device')
    device_protocols = relationship('DeviceProtocols', back_populates='device')
    presets = relationship('Presets', back_populates='device')


class Templates(Base):
    __tablename__ = 'templates'
    __table_args__ = (
        ForeignKeyConstraint(['family_id'], ['families.id'], name='template_pieces_family_id_fkey'),
        PrimaryKeyConstraint('id', name='template_pieces_pkey'),
        UniqueConstraint('family_id', 'role', 'name', name='unique_family_role_name')
    )

    id = Column(Integer, Sequence('template_pieces_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    role = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    family_id = Column(Integer)

    family = relationship('Families', back_populates='templates')
    device_presets = relationship('DevicePresets', back_populates='template')


class DevicePorts(Base):
    __tablename__ = 'device_ports'
    __table_args__ = (
        ForeignKeyConstraint(['device_id'], ['devices.id'], ondelete='CASCADE', name='device_ports_device_id_fkey'),
        ForeignKeyConstraint(['port_id'], ['ports.id'], ondelete='CASCADE', name='device_ports_port_id_fkey'),
        PrimaryKeyConstraint('id', name='device_ports_pkey')
    )

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, nullable=False)
    port_id = Column(Integer, nullable=False)
    interface = Column(String(255), nullable=False)

    device = relationship('Devices', back_populates='device_ports')
    port = relationship('Ports', back_populates='device_ports')


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


class Presets(Base):
    __tablename__ = 'presets'
    __table_args__ = (
        ForeignKeyConstraint(['device_id'], ['devices.id'], name='presets_device_id_fkey'),
        PrimaryKeyConstraint('id', name='presets_pkey'),
        UniqueConstraint('device_id', 'role', name='unique_device_role')
    )

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, nullable=False)
    role = Column(String(256), nullable=False)
    name = Column(String(256), nullable=False)
    description = Column(Text)

    device = relationship('Devices', back_populates='presets')
    device_presets = relationship('DevicePresets', back_populates='preset')


class DevicePresets(Base):
    __tablename__ = 'device_presets'
    __table_args__ = (
        ForeignKeyConstraint(['preset_id'], ['presets.id'], ondelete='CASCADE', name='device_templates_preset_id_fkey'),
        ForeignKeyConstraint(['template_id'], ['templates.id'], ondelete='CASCADE', name='device_templates_template_id_fkey'),
        PrimaryKeyConstraint('id', name='device_templates_pkey')
    )

    id = Column(Integer, Sequence('device_templates_id_seq'), primary_key=True)
    template_id = Column(Integer, nullable=False)
    ordered_number = Column(Integer, nullable=False)
    preset_id = Column(Integer, nullable=False)

    preset = relationship('Presets', back_populates='device_presets')
    template = relationship('Templates', back_populates='device_presets')
