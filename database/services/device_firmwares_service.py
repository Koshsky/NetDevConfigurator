from sqlalchemy.orm import Session

from database.models.models import DeviceFirmwares, Devices, Firmwares


class DeviceFirmwaresService:
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
        if db_device_firmware:
            self.db.delete(db_device_firmware)
            self.db.commit()
            return db_device_firmware
        return None
        
    def link_device_firmware(self, device_id: int, firmware_id: int):
        device = self.db.query(Devices).filter(Devices.id == device_id).first()
        firmware = self.db.query(Firmwares).filter(Firmwares.id == firmware_id).first()

        if not device:
            return "Device not found."
        if not firmware:
            return "Firmware not found."

        existing_link = self.db.query(DeviceFirmwares).filter(
            DeviceFirmwares.device_id == device_id,
            DeviceFirmwares.firmware_id == firmware_id
        ).first()

        if existing_link:
            return "This device and firmware combination already exists."

        device_firmware = DeviceFirmwares(device_id=device.id, firmware_id=firmware.id)

        self.create(device_firmware)
        return "Successfully linked device and firmware."
