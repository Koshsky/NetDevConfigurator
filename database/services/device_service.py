from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.device import Device
import logging

logging.basicConfig(level=logging.INFO)

class DeviceService:
    def __init__(self, session: Session):
        self.session = session

    def create_device(self, name: str, company_id: int) -> Device:
        try:
            new_device = Device(name=name, company_id=company_id)
            self.session.add(new_device)
            self.session.commit()
            logging.info(f"Device created: {new_device}")
            return new_device
        except SQLAlchemyError as e:
            self.session.rollback()
            logging.error(f"Error creating device: {e}")
            raise

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
            logging.info(f"Device updated: {device}")
        return device

    def delete_device(self, device_id: int) -> bool:
        device = self.get_device(device_id)
        if device:
            self.session.delete(device)
            self.session.commit()
            logging.info(f"Device deleted: {device}")
            return True
        return False

    def get_devices_by_company(self, company_id: int):
        return self.session.query(Device).filter_by(company_id=company_id).all()

    def get_devices_by_type(self, dev_type: str):
        return self.session.query(Device).filter_by(dev_type=dev_type).all()