from sqlalchemy.orm import Session

from database.models import DeviceFirmwares, Devices, Firmwares
from .base_service import BaseService


class DeviceFirmwareService:
    def __init__(self, db: Session):
        self.db = db

    def reset_firmwares(self, device_id: int):
        self.db.query(DeviceFirmwares).filter(DeviceFirmwares.device_id == device_id).delete()
        self.db.commit()

    def get_firmwares_by_device_id(self, device_id: int):
        return [
            {
                    "name": firmware.name,
                    "full_path": firmware.full_path,
                    "type": firmware.type,
                    "id": firmware.id
            } for firmware in (
                self.db.query(Firmwares)
                .join(DeviceFirmwares, DeviceFirmwares.firmware_id == Firmwares.id,)
                .join(Devices, Devices.id == DeviceFirmwares.device_id)
                .filter(DeviceFirmwares.device_id == device_id)
                .all()
            )
        ]

    def add_firmware_by_id(self, device_id: int, firmware_id: int):
        if (
            self.db.query(DeviceFirmwares)
            .join(Firmwares, DeviceFirmwares.firmware_id == Firmwares.id)
            .filter(DeviceFirmwares.device_id == device_id)
            .all()
        ):
            raise ValueError("Firmware already exists for this device")
        self.db.add(DeviceFirmwares(device_id=device_id, firmware_id=firmware_id))
        self.db.commit()

    def remove_firmware_by_id(self, device_id: int, firmware_id: int):
        if not (
            self.db.query(DeviceFirmwares)
            .join(Firmwares, DeviceFirmwares.firmware_id == Firmwares.id)
            .filter(DeviceFirmwares.device_id == device_id)
            .all()
        ):
            raise ValueError("Firmware does not exist for this device")
        self.db.query(DeviceFirmwares).filter(
            DeviceFirmwares.device_id == device_id,
            DeviceFirmwares.firmware_id == firmware_id).delete()
        self.db.commit()
