import logging
from typing import List

from sqlalchemy.orm import Session

from database.models import DeviceProtocols, Devices, Protocols

from .base_service import JsonType
from .protocol_service import ProtocolService

logger = logging.getLogger("db")


class DeviceProtocolService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def update_protocols(self, device: Devices, protocols: List[Protocols]) -> None:
        self._reset_protocols(device)
        for protocol in protocols:
            self._add_protocol(device, protocol)
        logger.debug(
            'Successfully update protocols for device: {"name": "%s"}, bound %d protocols',
            device.name,
            len(protocols),
        )

    def _reset_protocols(self, device: Devices) -> None:
        deleted_count = (
            self.db.query(DeviceProtocols)
            .filter(DeviceProtocols.device_id == device.id)
            .delete()
        )
        self.db.commit()
        logger.debug(
            'Successfully reset protocols for device: {"name": "%s"}, deleted %d protocols',
            device.name,
            deleted_count,
        )

    def get_protocols(self, device: Devices) -> List[JsonType]:
        protocols = [
            ProtocolService(self.db).get_info(protocol)
            for protocol in (
                self.db.query(Protocols)
                .join(DeviceProtocols, DeviceProtocols.protocol_id == Protocols.id)
                .filter(DeviceProtocols.device_id == device.id)
                .all()
            )
        ]
        logger.debug(
            'Retrieved %d protocols for device {"name": "%s"}',
            len(protocols),
            device.name,
        )

    def _add_protocol(self, device: Devices, protocol: Protocols) -> None:
        device_protocol = DeviceProtocols(device_id=device.id, protocol_id=protocol.id)
        self.db.add(device_protocol)
        self.db.commit()
        logger.debug(
            'Successfully added protocol: {"name": "%s"} to device: {"name": "%s"}',
            protocol.name,
            device.name,
        )

        return device_protocol
