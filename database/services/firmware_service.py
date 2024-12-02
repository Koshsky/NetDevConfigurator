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

    def get_by_name(self, name: str):
        return self.db.query(Firmwares).filter(Firmwares.name == name).first()

    def delete_by_name(self, name: str):
        db_firmware = self.get_by_name(name)  # Use the get_by_name method
        if not db_firmware:
            return None  # Return None if the firmware does not exist
        self.db.delete(db_firmware)  # Delete the firmware
        self.db.commit()  # Commit the changes to the database
        return db_firmware  # Return the deleted firmware object