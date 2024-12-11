from sqlalchemy.orm import Session

from internal.database.models import DeviceFirmwares, Devices, Firmwares


class DeviceFirmwareService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(DeviceFirmwares).all()

    def get_by_id(self, device_firmware_id: int):
        return self.db.query(DeviceFirmwares).filter(DeviceFirmwares.id == device_firmware_id).first()
    
    def get_devices_by_firmware_id(self, firmware_id: int):
        return self.db.query(Devices).join(DeviceFirmwares).filter(DeviceFirmwares.firmware_id == firmware_id).all()

    def get_firmwares_by_device_id(self, device_id: int):
        return self.db.query(Firmwares).join(DeviceFirmwares).filter(DeviceFirmwares.device_id == device_id).all()

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
        
    def link(self, device_id: int, firmware_id: int):
        if (
            existing_link := self.db.query(DeviceFirmwares)
            .filter(
                DeviceFirmwares.device_id == device_id,
                DeviceFirmwares.firmware_id == firmware_id,
            )
            .first()
        ):
            raise ValueError("Device firmware already linked")

        self.create({
            "device_id": device_id,
            "firmware_id": firmware_id
        })

    def unlink(self, device_id: int, firmware_id: int):
        if (
            existing_link := self.db.query(DeviceFirmwares)
            .filter(
                DeviceFirmwares.device_id == device_id,
                DeviceFirmwares.firmware_id == firmware_id,
            )
            .first()
        ):
            self.delete(existing_link.id)
        else:
            raise ValueError("Device firmware not linked")
