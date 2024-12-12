from sqlalchemy.orm import Session

from internal.database.models import DeviceProtocols, Devices, Protocols


class DeviceProtocolService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(DeviceProtocols).all()
    
    def get_protocols_by_device_id(self, device_id: int):
        return self.db.query(Protocols).join(DeviceProtocols).filter(DeviceProtocols.device_id == device_id).all()

    def get_device_protocols(self, device_id: int):
        return self.db.query(DeviceProtocols).filter(DeviceProtocols.device_id == device_id).all()

    def get_by_id(self, device_protocol_id: int):
        return self.db.query(DeviceProtocols).filter(DeviceProtocols.id == device_protocol_id).first()

    def create(self, device_protocol: dict):
        device_protocol = DeviceProtocols(**device_protocol)
        self.db.add(device_protocol)
        self.db.commit()
        self.db.refresh(device_protocol)
        return device_protocol

    def delete(self, device_protocol: DeviceProtocols):
        if device_protocol:
            self.db.delete(device_protocol)
            self.db.commit()

    def delete_by_id(self, device_protocol_id: int):
        device_protocol = self.get_by_id(device_protocol_id)
        self.delete(device_protocol)
        