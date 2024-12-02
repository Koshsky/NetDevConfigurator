from sqlalchemy.orm import Session
from database.models.models import DeviceFirmwares

from ..models.models import Devices, Firmwares

class DeviceService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Devices).all()

    def get_by_id(self, device_id: int):
        return self.db.query(Devices).filter(Devices.id == device_id).first()

    def create(self, device: Devices):
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        return device

    def update(self, device_id: int, device_data: Devices):
        db_device = self.get_by_id(device_id)
        if not db_device:
            return None
        db_device.name = device_data.name
        db_device.company_id = device_data.company_id
        db_device.dev_type = device_data.dev_type
        db_device.primary_conf = device_data.primary_conf
        db_device.port_num = device_data.port_num
        db_device.model = device_data.model
        self.db.commit()
        return db_device

    def delete(self, device_id: int):
        db_device = self.get_by_id(device_id)
        if not db_device:
            return None
        self.db.delete(db_device)
        self.db.commit()
        return db_device

    def get_by_name(self, name: str):
        return self.db.query(Devices).filter(Devices.name == name).first()

    def delete_by_name(self, name: str):
        db_device = self.get_by_name(name)  # Use the get_by_name method
        if not db_device:
            return None  # Return None if the device does not exist
        self.db.delete(db_device)  # Delete the device
        self.db.commit()  # Commit the changes to the database
        return db_device  # Return the deleted device object

    def get_firmwares_by_device_id(self, device_id: int):
        # Query the DeviceFirmwares table to get all firmware IDs associated with the given device ID
        firmware_ids = (
            self.db.query(DeviceFirmwares.firmware_id)
            .filter(DeviceFirmwares.device_id == device_id)
            .all()
        )
        
        # Extract the firmware IDs from the result
        firmware_ids = [fid for (fid,) in firmware_ids]  # Unpack the tuples
        
        # Query the Firmwares table to get the firmware records based on the IDs
        if firmware_ids:  # Check if there are any firmware IDs
            return self.db.query(Firmwares).filter(Firmwares.id.in_(firmware_ids)).all()
        else:
            return []  # Return an empty list if no firmwares are associated