import logging
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from database.models import Companies, DevicePorts, Devices, Ports

from database.models import Companies, DevicePorts, Devices, Ports

from .base_service import JsonType

logger = logging.getLogger(__name__)


class DevicePortService:
    """Manages device ports in the database.

    This service provides methods to update, reset, retrieve, and add ports
    for devices, handling interface naming conventions for different companies.
    """

    def __init__(self, db: Session) -> None:
        """Initializes DevicePortService with a database session.

        Args:
            db: The SQLAlchemy database session.
        """
        logger.debug("Initializing DevicePortService")
        self.db = db

    def update_ports(self, device: "Devices", ports: List["Ports"] | None) -> "Devices":
        """Updates the ports associated with a device.

        This method resets the existing ports for the device and adds the new ports.

        Args:
            device: The device to update ports for.
            ports: A list of ports to associate with the device, or None to reset all ports.

        Returns:
            The device with updated ports.
        """
        logger.info("Updating ports for device: %s", device.name)
        self._reset_ports(device)
        if ports is not None:
            for port in ports:
                self._add_port(device, port)
        logger.debug(
            'Successfully updated ports for device: {"name": "%s"}, bound %d ports',
            device.name,
            len(ports) if ports else 0,  # Handle None case
        )
        return device

    def _reset_ports(self, device: "Devices") -> None:
        """Resets the ports associated with a device.

        This method deletes all existing port associations for the given device.

        Args:
            device: The device to reset ports for.
        """
        logger.info("Resetting ports for device: %s", device.name)
        deleted_count = (
            self.db.query(DevicePorts)
            .filter(DevicePorts.device_id == device.id)
            .delete()
        )
        self.db.commit()
        logger.debug(
            'Successfully reset ports for device: {"name": "%s"}, deleted %d ports',
            device.name,
            deleted_count,
        )

    def get_ports(self, device: "Devices") -> List[JsonType]:
        """Retrieves the ports associated with a device.

        This method returns a list of port information for the given device.

        Args:
            device: The device to retrieve ports for.

        Returns:
            A list of dictionaries, each containing information about a port.
        """
        logger.info("Retrieving ports for device: %s", device.name)
        ports = [
            {
                "interface": device_port.interface,
                "name": port.name,
                "material": port.material,
                "speed": port.speed,
            }
            for device_port, port in (
                self.db.query(DevicePorts, Ports)
                .join(Ports, DevicePorts.port_id == Ports.id)
                .filter(DevicePorts.device_id == device.id)
                .all()
            )
        ]
        logger.debug(
            'Retrieved %d ports for device {"name": "%s"}',
            len(ports),
            device.name,
        )
        return ports

    def _add_port(self, device: "Devices", port: "Ports") -> "DevicePorts":
        """Adds a port to a device.

        This method creates a new DevicePorts entry, associating the given port
        with the given device. It determines the next available interface name
        based on the company of the device.

        Args:
            device: The device to add the port to.
            port: The port to add.

        Returns:
            The newly created DevicePorts instance.

        Raises:
            NotImplementedError: If there's no method for getting the next interface for the company.
        """
        logger.info("Adding port %s to device: %s", port.name, device.name)
        company = (
            self.db.query(Companies)
            .join(Devices, Companies.id == Devices.company_id)
            .filter(Devices.id == device.id)
            .first()
        )
        if not company:
            logger.error("Company not found for device: %s", device.name)
            raise ValueError(f"Company not found for device: {device.name}")

        get_next_interface = getattr(
            self,
            f"_get_next_{company.name}_interface",
            self._default_get_next_interface,
        )
        device_port = DevicePorts(
            device_id=device.id,
            port_id=port.id,
            interface=get_next_interface(device.id, port.id),
        )
        self.db.add(device_port)
        self.db.commit()

        logger.debug(
            'Successfully added port: {"name": "%s"} to device: {"name": %s}',
            port.name,
            device.name,
        )
        return device_port

    def _get_next_Eltex_interface(self, device_id: int, port_id: int) -> str:
        """Generates the next available Eltex interface name.

        Args:
            device_id: The ID of the device.
            port_id: The ID of the port.

        Returns:
            The next available Eltex interface name.
        """
        logger.debug(
            "Getting next Eltex interface for device_id: %s, port_id: %s",
            device_id,
            port_id,
        )
        port = self.db.query(Ports).filter(Ports.id == port_id).first()
        if not port:
            logger.error("Port not found for port_id: %s", port_id)
            raise ValueError(f"Port not found for port_id: {port_id}")

        q = len(
            self.db.query(DevicePorts)
            .join(Ports, DevicePorts.port_id == Ports.id)
            .filter(Ports.speed == port.speed, DevicePorts.device_id == device_id)
            .all()
        )
        interface = f"{'ten' if port.speed == 10000 else ''}gigabitethernet 0/{q + 1}"
        logger.debug("Next Eltex interface: %s", interface)
        return interface

    def _get_next_Zyxel_interface(self, device_id: int, port_id: int) -> str:
        """Generates the next available Zyxel interface name.

        Args:
            device_id: The ID of the device.
            port_id: The ID of the port.

        Returns:
            The next available Zyxel interface name.
        """
        logger.debug(
            "Getting next Zyxel interface for device_id: %s, port_id: %s",
            device_id,
            port_id,
        )
        port = self.db.query(Ports).filter(Ports.id == port_id).first()
        if not port:
            logger.error("Port not found for port_id: %s", port_id)
            raise ValueError(f"Port not found for port_id: {port_id}")

        q = len(
            self.db.query(DevicePorts)
            .join(Ports, DevicePorts.port_id == Ports.id)
            .filter(Ports.speed == port.speed, DevicePorts.device_id == device_id)
            .all()
        )
        interface = f"port-channel {q + 1}"
        logger.debug("Next Zyxel interface: %s", interface)
        return interface

    def _default_get_next_interface(self, device_id: int, port_id: int) -> str:
        """Default method for getting the next interface name.

        Args:
            device_id: The ID of the device.
            port_id: The ID of the port.

        Raises:
            NotImplementedError: This method should be overridden by specific company methods.
        """
        logger.error("No method found for getting the next interface.")
        raise NotImplementedError(
            "There is no default method for getting next interface"
        )
