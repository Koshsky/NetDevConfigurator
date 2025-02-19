from typing import Tuple

from sqlalchemy.orm import Session

from database.models import Devices, Presets

from .base_service import BaseService, JsonType
from .device_port_service import DevicePortService
from .device_protocol_service import DeviceProtocolService


class DeviceService(BaseService, DevicePortService, DeviceProtocolService):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Devices)

    def get_roles_by_name(self, device_name: str) -> Tuple[str]:  # TODO: rename
        presets = (
            self.db.query(Presets)
            .join(Devices, Presets.device_id == Devices.id)
            .filter(Devices.name == device_name)
            .all()
        )
        return tuple(preset.role for preset in presets)

    def update_files(
        self, device: Devices, boot: str, uboot: str, firmware: str
    ) -> Devices:
        device.boot = boot
        device.uboot = uboot
        device.firmware = firmware

        self.db.commit()

        return device

    def get_info(self, device: Devices) -> JsonType:
        return {
            "id": device.id,
            "name": device.name,
            "dev_type": device.dev_type,
            "family": {"name": device.family.name, "id": device.family.id},
            "company": {"name": device.company.name, "id": device.company.id},
            "pattern": {
                "boot": device.boot,
                "uboot": device.uboot,
                "firmware": device.firmware,
            },
            "protocols": self.get_protocols_by_id(device.id),
            "ports": self.get_ports_by_id(device.id),
        }
