from sqlalchemy.orm import Session

from database.models import Firmwares, DeviceFirmwares


class FirmwareService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Firmwares).all()

    def get_by_id(self, firmware_id: int):
        return self.db.query(Firmwares).filter(Firmwares.id == firmware_id).first()

    def get_by_name(self, name: str):
        return self.db.query(Firmwares).filter(Firmwares.name == name).first()
    
    def create(self, firmware: dict):
        new_firmware = Firmwares(**firmware)
        self.db.add(new_firmware)
        self.db.commit()
        self.db.refresh(new_firmware)
        return new_firmware

    def delete(self, firmware):
        if firmware:
            self.db.delete(firmware)
            self.db.commit()

    def delete_by_name(self, name: str):
        db_firmware = self.get_by_name(name)
        self.delete(db_firmware)

    def delete_by_id(self, firmware_id: int):
        db_firmware = self.get_by_id(firmware_id)
        self.delete(db_firmware)



def determine_firmware_type(firmware_name: str) -> str:
    # первичная: .bl1
    # вторичная: .uboot .boot
    # сама прошивка: .firmware .iss .ros

    primary = "primary_bootloader"
    secondary = "secondary_bootloader"
    firmware = "firmware"

    firmware_types = {
        '.bl1': primary,
        '.uboot': secondary,
        '.boot': secondary,
        '.firmware': firmware,
        '.iss': firmware,
        '.ros': firmware,
    }

    for extension, description in firmware_types.items():
        if firmware_name.endswith(extension):
            return description

    return "UKNOWN"
