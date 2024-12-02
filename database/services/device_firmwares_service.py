# services/device_firmware_service.py

from sqlalchemy.orm import Session
from database.models.models import DeviceFirmwares

class DeviceFirmwareService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(DeviceFirmwares).all()

    def get_by_id(self, device_firmware_id: int):
        return self.db.query(DeviceFirmwares).filter(DeviceFirmwares.id == device_firmware_id).first()

    def create(self, device_firmware: DeviceFirmwares):
        self.db.add(device_firmware)
        self.db.commit()
        self.db.refresh(device_firmware)
        return device_firmware

    def update(self, device_firmware_id: int, device_firmware_data: DeviceFirmwares):
        db_device_firmware = self.get_by_id(device_firmware_id)
        if not db_device_firmware:
            return None
        db_device_firmware.device_id = device_firmware_data.device_id
        db_device_firmware.firmware_id = device_firmware_data.firmware_id
        self.db.commit()
        return db_device_firmware

    def delete(self, device_firmware_id: int):
        db_device_firmware = self.get_by_id(device_firmware_id)