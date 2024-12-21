from sqlalchemy.orm import Session

from internal.database.models import DeviceProtocols, Devices, Protocols
from ..base_service import BaseService


class DeviceProtocolService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, DeviceProtocols)

    def get_protocols_by_device_id(self, device_id: int):
        return (
            self.db.query(DeviceProtocols, Protocols)
                .join(DeviceProtocols, DeviceProtocols.protocol_id == Protocols.id)
                .filter(DeviceProtocols.device_id == device_id)
                .all()
        )
