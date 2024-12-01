# services/firmware_service.py

from sqlalchemy.orm import Session
from ..models.firmware import Firmware  # Предполагается, что модели находятся в папке models

class FirmwareService:
    def __init__(self, session: Session):
        self.session = session

    def create_firmware(self, version: str) -> Firmware:
        new_firmware = Firmware(version=version)
        self.session.add(new_firmware)
        self.session.commit()
        return new_firmware

    def get_firmware(self, firmware_id: int) -> Firmware:
        return self.session.query(Firmware).filter_by(id=firmware_id).first()

    def get_all_firmwares(self):
        return self.session.query(Firmware).all()

    def update_firmware(self, firmware_id: int, version: str) -> Firmware:
        firmware = self.get_firmware(firmware_id)
        if firmware:
            firmware.version = version
            self.session.commit()
        return firmware

    def delete_firmware(self, firmware_id: int) -> bool:
        firmware = self.get_firmware(firmware_id)
        if firmware:
            self.session.delete(firmware)
            self.session.commit()
            return True
        return False