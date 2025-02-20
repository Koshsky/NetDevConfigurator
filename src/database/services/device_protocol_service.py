from typing import List

from sqlalchemy.orm import Session

from database.models import DeviceProtocols, Devices, Protocols

from .base_service import JsonType


class DeviceProtocolService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def reset_protocols(self, device: Devices) -> None:
        self.db.query(DeviceProtocols).filter(
            DeviceProtocols.device_id == device.id
        ).delete()
        self.db.commit()

    def get_protocols(self, device: Devices) -> List[JsonType]:
        return [
            {
                "id": protocol.id,
                "name": protocol.name,
            }
            for protocol in (
                self.db.query(Protocols)
                .join(DeviceProtocols, DeviceProtocols.protocol_id == Protocols.id)
                .filter(DeviceProtocols.device_id == device.id)
                .all()
            )
        ]

    def add_protocol_by_id(self, device_id: int, protocol_id: int) -> None:
        return self.create(device_id=device_id, protocol_id=protocol_id)
