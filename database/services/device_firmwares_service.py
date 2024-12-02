from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.devices_firmwares import DevicesFirmwares
import logging

logging.basicConfig(level=logging.INFO)

class DevicesFirmwareService:
    def __init__(self, session: Session):
        self.session = session

    def create_devices_firmware(self, device_id: int, firmware_id: int) -> DevicesFirmwares:
        try:
            new_entry = DevicesFirmwares(device_id=device_id, firmware_id=firmware_id)
            self.session.add(new_entry)
            self.session.commit()
            logging.info(f"Devices-Firmware entry created: {new_entry}")
            return new_entry
        except SQLAlchemyError as e:
            self.session.rollback()
            logging.error(f"Error creating Devices-Firmware entry: {e}")
            raise

    def get_devices_firmware(self, entry_id: int) -> DevicesFirmwares:
        return self.session.query(DevicesFirmwares).filter_by(id=entry_id).first()

    def get_all_devices_firmwares(self):
        return self.session.query(DevicesFirmwares).all()

    def update_devices_firmware(self, entry_id: int, device_id: int = None, firmware_id: int = None) -> DevicesFirmwares:
        entry = self.get_devices_firmware(entry_id)
        if entry:
            if device_id is not None:
                entry.device_id = device_id
            if firmware_id is not None:
                entry.firmware_id = firmware_id
            self.session.commit()
            logging.info(f"Devices-Firmware entry updated: {entry}")
        return entry

    def delete_devices_firmware(self, entry_id: int) -> bool:
        entry = self.get_devices_firmware(entry_id)
        if entry:
            self.session.delete(entry)
            self.session.commit()
            logging.info(f"Devices-Firmware entry deleted: {entry}")
            return True
        return False