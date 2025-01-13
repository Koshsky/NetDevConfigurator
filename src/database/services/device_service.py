from sqlalchemy.orm import Session

from database.models import Devices
from .device_firmware_service import DeviceFirmwareService
from .device_port_service import DevicePortService
from .device_protocol_service import DeviceProtocolService
from .base_service import BaseService


class DeviceService(
    BaseService, DeviceFirmwareService, DevicePortService, DeviceProtocolService
):
    def __init__(self, db: Session):
        super().__init__(db, Devices)

    def get_all_by_company_id(self, company_id: int):
        return self.db.query(Devices).filter(Devices.company_id == company_id).all()

    def get_all_by_family_id(self, family_id: int):
        return self.db.query(Devices).filter(Devices.family_id == family_id).all()

    def get_info(self, entity):
        return {
            "id": entity.id,
            "name": entity.name,
            "dev_type": entity.dev_type,
            "family": {"name": entity.family.name, "id": entity.family.id},
            "company": {"name": entity.company.name, "id": entity.company.id},
            "protocols": self.get_protocols_by_device_id(entity.id),
            "firmwares": self.get_firmwares_by_device_id(entity.id),
            "ports": self.get_ports_by_device_id(entity.id),
        }
