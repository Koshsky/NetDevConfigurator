from sqlalchemy.orm import Session

from database.models import Devices, Presets
from .device_port_service import DevicePortService
from .device_protocol_service import DeviceProtocolService
from .base_service import BaseService


class DeviceService(BaseService, DevicePortService, DeviceProtocolService):
    def __init__(self, db: Session):
        super().__init__(db, Devices)

    def get_roles_by_name(self, device_name: str):
        presets = (
            self.db.query(Presets)
            .join(Devices, Presets.device_id == Devices.id)
            .filter(Devices.name == device_name)
            .all()
        )
        return tuple(preset.role for preset in presets)

    def get_by_company_id(self, company_id: int):
        return self.db.query(Devices).filter(Devices.company_id == company_id).all()

    def get_by_family_id(self, family_id: int):
        return self.db.query(Devices).filter(Devices.family_id == family_id).all()

    def update_files(self, device: Devices, boot: str, uboot: str, firmware: str):
        device.boot = boot
        device.uboot = uboot
        device.firmware = firmware

        self.db.commit()

        return device

    def get_info(self, entity):
        return {
            "id": entity.id,
            "name": entity.name,
            "dev_type": entity.dev_type,
            "family": {"name": entity.family.name, "id": entity.family.id},
            "company": {"name": entity.company.name, "id": entity.company.id},
            "pattern": {
                "boot": entity.boot,
                "uboot": entity.uboot,
                "firmware": entity.firmware,
            },
            "protocols": self.get_protocols_by_id(entity.id),
            "ports": self.get_ports_by_id(entity.id),
        }
