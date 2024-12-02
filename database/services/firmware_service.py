from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.firmware import Firmware
import logging

logging.basicConfig(level=logging.INFO)

class FirmwareService:
    def __init__(self, session: Session):
        self.session = session

    def create_firmware(self, version: str) -> Firmware:
        try:
            new_firmware = Firmware(version=version)
            self.session.add(new_firmware)
            self.session.commit()
            logging.info(f"Firmware created: {new_firmware}")
            return new_firmware
        except SQLAlchemyError as e:
            self.session.rollback()
            logging.error(f"Error creating firmware: {e}")
            raise

    def get_firmware(self, firmware_id: int) -> Firmware:
        return self.session.query(Firmware).filter_by(id=firmware_id).first()

    def get_all_firmwares(self):
        return self.session.query(Firmware).all()

    def update_firmware(self, firmware_id: int, version: str) -> Firmware:
        firmware = self.get_firmware(firmware_id)
        if firmware:
            firmware.version = version
            self.session.commit()
            logging.info(f"Firmware updated: {firmware}")
        return firmware

    def delete_firmware(self, firmware_id: int) -> bool:
        firmware = self.get_firmware(firmware_id)
        if firmware:
            self.session.delete(firmware)
            self.session.commit()
            logging.info(f"Firmware deleted: {firmware}")
            return True
        return False