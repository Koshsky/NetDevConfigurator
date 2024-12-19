from sqlalchemy.orm import Session

from internal.database.models import DevicePorts, Devices, Ports
from ..base_service import BaseService


class DevicePortService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, DevicePorts)

    def get_device_ports(self, device_id: int):
        return (
            self.db.query(DevicePorts, Ports)
                .join(Ports, DevicePorts.port_id == Ports.id)
                .filter(DevicePorts.device_id == device_id)
                .all()
        )