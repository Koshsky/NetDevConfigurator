import logging
from typing import Dict

from sqlalchemy.orm import Session

from database.models import Devices, Presets

from .base_service import BaseService, JsonType
from .device_port import DevicePortService
from .device_protocol import DeviceProtocolService

logger = logging.getLogger(__name__)


class DeviceService(BaseService, DevicePortService, DeviceProtocolService):
    """Manages device-related database operations.

    This service provides methods to interact with device records, including
    updating file masks, retrieving device information, and managing associated
    ports and protocols.
    """

    def __init__(self, db: Session) -> None:
        """Initializes DeviceService with a database session and the Devices model.

        Args:
            db: The SQLAlchemy database session.
        """
        logger.debug("Initializing DeviceService")
        super().__init__(db, Devices)

    def update_masks(
        self, device: "Devices", boot: str, uboot: str, firmware: str
    ) -> "Devices":
        """Updates the boot, uboot, and firmware masks for a device.

        Args:
            device: The device to update.
            boot: The boot mask.
            uboot: The uboot mask.
            firmware: The firmware mask.

        Returns:
            The updated device.
        """
        logger.debug("Updating masks for device: %s", device.name)
        device.boot = boot
        device.uboot = uboot
        device.firmware = firmware

        self.db.commit()
        logger.debug(
            "Updated files for device %s (Name: %s): boot='%s', uboot='%s', firmware='%s'",
            device.id,
            device.name,
            boot,
            uboot,
            firmware,
        )
        return device

    def get_info(self, device: "Devices") -> JsonType:
        """Retrieves comprehensive information about a device.

        Args:
            device: The device to retrieve information for.

        Returns:
            A dictionary containing device details, including associated
            presets, protocols, and ports.
        """
        logger.debug("Retrieving information for device: %s", device.name)
        presets = (
            self.db.query(Presets)
            .join(Devices, Presets.device_id == Devices.id)
            .filter(Devices.name == device.name)
            .all()
        )

        device_info: Dict[str, JsonType] = {
            "id": device.id,
            "name": device.name,
            "dev_type": device.dev_type,
            "family": {
                "name": device.family.name,
                "id": device.family.id,
            },
            "company": {
                "name": device.company.name,
                "id": device.company.id,
            },
            "pattern": {
                "boot": device.boot,
                "uboot": device.uboot,
                "firmware": device.firmware,
            },
            "protocols": self.get_protocols(device),  # type: ignore[call-arg]
            "ports": self.get_ports(device),  # type: ignore[call-arg]
            "roles": tuple(preset.role for preset in presets),
        }
        return device_info
