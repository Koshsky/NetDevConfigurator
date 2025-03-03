import logging

from sqlalchemy.orm import Session

from database.models import Devices, Presets

from .base_service import BaseService, JsonType
from .device_port_service import DevicePortService
from .device_protocol_service import DeviceProtocolService

logger = logging.getLogger("db")


class DeviceService(BaseService, DevicePortService, DeviceProtocolService):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Devices)

    def update_masks(
        self, device: Devices, boot: str, uboot: str, firmware: str
    ) -> Devices:
        device.boot = boot
        device.uboot = uboot
        device.firmware = firmware

        self.db.commit()
        logger.debug(
            "Updated files for device {} (Name: {}): boot='{}', uboot='{}', firmware='{}'".format(
                device.id, device.name, boot, uboot, firmware
            )
        )
        return device

    def get_info(self, device: Devices) -> JsonType:
        presets = (
            self.db.query(Presets)
            .join(Devices, Presets.device_id == Devices.id)
            .filter(Devices.name == device.name)
            .all()
        )
        return {
            "id": device.id,
            "name": device.name,
            "dev_type": device.dev_type,
            "family": {
                "name": device.family.name,
                "id": device.family.id,
            },  # TODO: НЕВАЖНО replace with get_info
            "company": {
                "name": device.company.name,
                "id": device.company.id,
            },  # TODO: НЕВАЖНО replace with get_info
            "pattern": {
                "boot": device.boot,
                "uboot": device.uboot,
                "firmware": device.firmware,
            },
            "protocols": self.get_protocols(device),
            "ports": self.get_ports(device),
            "roles": tuple(preset.role for preset in presets),
        }
