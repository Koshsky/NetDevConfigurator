from sqlalchemy.orm import Session

from internal.database.models import DeviceFirmwares, Devices, Firmwares
from ..base_service import BaseService


class DeviceFirmwareService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, DeviceFirmwares)

    def get_device_firmwares(self, device_id: int):
        return self.db.query(DeviceFirmwares).filter(DeviceFirmwares.device_id == device_id).all()

    def get_by_device_firmware_id(self, device_id: int, firmware_id: int):
        return (
            self.db.query(DeviceFirmwares)
                .filter(
                    DeviceFirmwares.device_id == device_id,
                    DeviceFirmwares.firmware_id == firmware_id,
                )
                .first()
        )

    def get_devices_by_firmware_id(self, firmware_id: int):
        return (
            self.db.query(Devices)
                .join(Devices.device_firmwares)  # Используем relationship из модели
                .filter(DeviceFirmwares.firmware_id == firmware_id)
                .all()
        )

    def get_firmwares_by_device_id(self, device_id: int):
        return (
            self.db.query(Firmwares)
                .join(Firmwares.device_firmwares)  # Используем relationship из модели
                .filter(DeviceFirmwares.device_id == device_id)
                .all()
        )

    def delete_by_device_firmware_id(self, device_id: int, firmware_id: int):
        db_device_firmware = self.get_by_device_firmware_id(device_id, firmware_id)
        self.__delete(db_device_firmware)
