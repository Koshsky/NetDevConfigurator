from sqlalchemy.orm import Session

from internal.database.models import DeviceFirmwares, Devices, Firmwares


class DeviceFirmwareService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(DeviceFirmwares).order_by(DeviceFirmwares.device_id).all()

    def get_by_id(self, device_firmware_id: int):
        return self.db.query(DeviceFirmwares).filter(DeviceFirmwares.id == device_firmware_id).first()
    
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
                .order_by(Devices.name)
                .all()
        )

    def get_firmwares_by_device_id(self, device_id: int):
        return (
            self.db.query(Firmwares)
                .join(Firmwares.device_firmwares)  # Используем relationship из модели
                .filter(DeviceFirmwares.device_id == device_id)
                .order_by(Firmwares.name)
                .all()
        )

    def create(self, device_firmware: dict):
        device_firmware = DeviceFirmwares(**device_firmware)
        self.db.add(device_firmware)
        self.db.commit()
        self.db.refresh(device_firmware)
        return device_firmware

    def delete(self, device_firmware: DeviceFirmwares):
        if device_firmware:
            self.db.delete(device_firmware)
            self.db.commit()

    def delete_by_id(self, device_firmware_id: int):
        db_device_firmware = self.get_by_id(device_firmware_id)
        self.delete(db_device_firmware)
        
    def delete_by_device_firmware_id(self, device_id: int, firmware_id: int):
        db_device_firmware = self.get_by_device_firmware_id(device_id, firmware_id)
        self.delete(db_device_firmware)
