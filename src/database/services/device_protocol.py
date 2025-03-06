import logging
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from database.models import DeviceProtocols, Devices, Protocols

from database.models import DeviceProtocols, Devices, Protocols

from .base_service import JsonType
from .protocol import ProtocolService

logger = logging.getLogger(__name__)


class DeviceProtocolService:
    """Manages device-protocol associations in the database.

    This service provides methods to update, reset, retrieve, and add protocol
    associations for devices.
    """

    def __init__(self, db: Session) -> None:
        """Initializes DeviceProtocolService with a database session.

        Args:
            db: The SQLAlchemy database session.
        """
        logger.debug("Initializing DeviceProtocolService")
        self.db = db

    def update_protocols(self, device: "Devices", protocols: List["Protocols"]) -> None:
        """Updates the protocols associated with a device.

        Args:
            device: The device to update protocols for.
            protocols: A list of protocols to associate with the device.
        """
        logger.info("Updating protocols for device: %s", device.name)
        self._reset_protocols(device)
        for protocol in protocols:
            self._add_protocol(device, protocol)
        logger.debug(
            'Successfully updated protocols for device: {"name": "%s"}, bound %d protocols',
            device.name,
            len(protocols),
        )

    def _reset_protocols(self, device: "Devices") -> None:
        """Resets the protocols associated with a device.

        This method deletes all existing protocol associations for the given device.

        Args:
            device: The device to reset protocols for.
        """
        logger.info("Resetting protocols for device: %s", device.name)
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

    def get_protocols(self, device: "Devices") -> List[JsonType]:
        """Retrieves the protocols associated with a device.

        Args:
            device: The device to retrieve protocols for.

        Returns:
            A list of protocol information dictionaries.
        """
        logger.info("Retrieving protocols for device: %s", device.name)
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
        return protocols

    def _add_protocol(
        self, device: "Devices", protocol: "Protocols"
    ) -> "DeviceProtocols":
        """Adds a protocol association to a device.

        Args:
            device: The device to add the protocol association to.
            protocol: The protocol to associate with the device.

        Returns:
            The newly created DeviceProtocols instance.
        """
        logger.info("Adding protocol %s to device: %s", protocol.name, device.name)
        device_protocol = DeviceProtocols(device_id=device.id, protocol_id=protocol.id)
        self.db.add(device_protocol)
        self.db.commit()
        logger.debug(
            'Successfully added protocol: {"name": "%s"} to device: {"name": "%s"}',
            protocol.name,
            device.name,
        )

        return device_protocol
