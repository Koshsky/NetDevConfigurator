from sqlalchemy.orm import Session

from database.models import DeviceProtocols, Protocols
from .base_service import BaseService


class DeviceProtocolService:
    def __init__(self, db: Session):
        self.db = db

    def reset_protocols(self, device_id: int):
        self.db.query(DeviceProtocols).filter(DeviceProtocols.device_id == device_id).delete()
        self.db.commit()

    def get_protocols_by_device_id(self, device_id: int):
        return [
            {
                "id": protocol.id,
                "name": protocol.name,
            } for protocol in (
            self.db.query(Protocols)
                .join(DeviceProtocols, DeviceProtocols.protocol_id == Protocols.id)
                .filter(DeviceProtocols.device_id == device_id)
                .all()
            )
        ]

    def add_protocol_by_id(self, device_id: int, protocol_id: int):
        self.db.add(DeviceProtocols(device_id=device_id, protocol_id=protocol_id))
        self.db.commit()

    def remove_protocol_by_id(self, device_id: int, protocol_id: int):
        self.db.query(DeviceProtocols).filter(
            DeviceProtocols.device_id == device_id,
            DeviceProtocols.protocol_id == protocol_id
            ).delete()
        self.db.commit()