# services/device_service.py

from sqlalchemy.orm import Session
from ..models.device import Device  # Предполагается, что модели находятся в папке models

class DeviceService:
    def __init__(self, session: Session):
        self.session = session

    def create_device(self, name: str, company_id: int) -> Device:
        new_device = Device(name=name, company_id=company_id)
        self.session.add(new_device)
        self.session.commit()
        return new_device

    def get_device(self, device_id: int) -> Device:
        return self.session.query(Device).filter_by(id=device_id).first()

    def get_all_devices(self):
        return self.session.query(Device).all()

    def update_device(self, device_id: int, name: str = None) -> Device:
        device = self.get_device(device_id)
        if device:
            if name:
                device.name = name
            self.session.commit()
        return device

    def delete_device(self, device_id: int) -> bool:
        device = self.get_device(device_id)
        if device:
            self.session.delete(device)
            self.session.commit()
            return True
        return False