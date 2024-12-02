from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .base import Base

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    dev_type = Column(Integer, nullable=False)
    model = Column(Integer)
    prim_conf = Column(Integer, nullable=False)
    port_num = Column(Integer, nullable=False)

    # Определение отношений
    company = relationship("Company", back_populates="devices")

    def __repr__(self):
        return (f"<Device(id={self.id}, name='{self.name}', company_id={self.company_id}, "
                f"dev_type={self.dev_type}, model={self.model}, "
                f"prim_conf={self.prim_conf}, port_num={self.port_num})>")