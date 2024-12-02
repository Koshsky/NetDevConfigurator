# services/firmware_service.py

from sqlalchemy.orm import Session
from database.models.models import Firmwares

class FirmwareService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Firmwares).all()

    def get_by_id(self, firmware_id: int):
        return self.db.query(Firmwares).filter(Firmwares.id == firmware_id).first()

    def create(self, firmware: Firmwares):
        self.db.add(firmware)
        self.db.commit()
        self.db.refresh(firmware)
        return firmware

    def update(self, firmware_id: int, firmware_data: Firmwares):
        db_firmware = self.get_by_id(firmware_id)
        if not db_firmware:
            return None
        db_firmware.name = firmware_data.name
        self.db.commit()
        return db_firmware

    def delete(self, firmware_id: int):
        db_firmware = self.get_by_id(firmware_id)
        if not db_firmware:
            return None
        self.db.delete(db_firmware)
        self.db.commit()
        return db_firmware