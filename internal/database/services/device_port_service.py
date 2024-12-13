from sqlalchemy.orm import Session

from internal.database.models import DevicePorts, Devices, Ports


class DevicePortService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(DevicePorts).order_by(DevicePorts.device_id).all()

    def get_device_ports(self, device_id: int):
        return (
            self.db.query(DevicePorts, Ports)
                .join(Ports, DevicePorts.port_id == Ports.id)
                .filter(DevicePorts.device_id == device_id)
                .order_by(DevicePorts.id)
                .all()
        )


    def get_by_id(self, device_port_id: int):
        return self.db.query(DevicePorts).filter(DevicePorts.id == device_port_id).first()

    def create(self, device_port: dict):
        device_port = DevicePorts(**device_port)
        self.db.add(device_port)
        self.db.commit()
        self.db.refresh(device_port)
        return device_port

    def delete(self, device_port: DevicePorts):
        if device_port:
            self.db.delete(device_port)
            self.db.commit()

    def delete_by_id(self, device_port_id: int):
        device_port = self.get_by_id(device_port_id)
        self.delete(device_port)
        