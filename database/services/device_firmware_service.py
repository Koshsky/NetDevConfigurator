from sqlalchemy.orm import Session

from database.models import DeviceFirmwares, Devices, Firmwares


class DeviceFirmwareService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(DeviceFirmwares).all()

    def get_by_id(self, device_firmware_id: int):
        return self.db.query(DeviceFirmwares).filter(DeviceFirmwares.id == device_firmware_id).first()

    def get_firmwares_by_device_id(self, device_id: int):
        firmware_ids = (
            self.db.query(DeviceFirmwares.firmware_id)
            .filter(DeviceFirmwares.device_id == device_id)
            .all()
        )
        
        firmware_ids = [fid for (fid,) in firmware_ids]
        
        if firmware_ids:
            return self.db.query(Firmwares).filter(Firmwares.id.in_(firmware_ids)).all()
        else:
            return []

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
        existing_link = self.db.query(DeviceFirmwares).filter(
            DeviceFirmwares.device_id == device_id,
            DeviceFirmwares.firmware_id == firmware_id
        ).first()

        if existing_link:
            raise ValueError("Device firmware already linked")

        self.create({
            "device_id": device_id,
            "firmware_id": firmware_id
        })

    def unlink(self, device_id: int, firmware_id: int):
        existing_link = self.db.query(DeviceFirmwares).filter(
            DeviceFirmwares.device_id == device_id,
            DeviceFirmwares.firmware_id == firmware_id
        ).first()

        if not existing_link:
            raise ValueError("Device firmware not linked")

        self.delete(existing_link.id)
