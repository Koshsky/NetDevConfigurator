from sqlalchemy.orm import Session

from database.models import DeviceFirmwares, Devices, Firmwares


class DeviceService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Devices).all()

    def get_by_id(self, device_id: int):
        return self.db.query(Devices).filter(Devices.id == device_id).first()

    def get_by_name(self, name: str):
        return self.db.query(Devices).filter(Devices.name == name).first()


    def create(self, device: dict):
        device = Devices(**device)
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        return device

    def delete(self, device):
        if db_device:
            self.db.delete(db_device)
            self.db.commit()

    def delete_by_id(self, device_id: int):
        db_device = self.get_by_id(device_id)
        self.delete(db_device)

    def delete_by_name(self, name: str):
        db_device = self.get_by_name(name)
        self.delete(db_device)