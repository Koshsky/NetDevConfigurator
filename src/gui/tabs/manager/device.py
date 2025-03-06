import logging
from typing import TYPE_CHECKING, List

from gui import BaseTab, apply_error_handler

if TYPE_CHECKING:
    from database.models import Devices, Ports, Protocols

logger = logging.getLogger(__name__)


@apply_error_handler
class UpdateTab(BaseTab):
    """Tab for updating device information, including masks, protocols, and ports."""

    def _create_widgets(self) -> None:
        """Creates the widgets for the tab."""
        logger.debug("Creating widgets for UpdateTab")
        self.create_block(
            "",
            {
                "device": self.app.entity_collections["device"],
                "mask": {"boot": ("",), "uboot": ("",), "firmware": ("",)},
                "protocols": list(self.app.entity_collections["protocol"]),
                "ports": {
                    f"{i}": (None,) + self.app.entity_collections["port"]
                    for i in range(1, 61)
                },
            },
            width=12,
        )
        self.create_button_in_line(("UPDATE MASKS", self.update_masks))
        self.create_button_in_line(("UPDATE PROTOCOLS", self.update_protocols))
        self.create_button_in_line(("UPDATE PORTS", self.update_ports))

    def update_masks(self) -> None:
        """Updates the boot, uboot, and firmware masks for the selected device."""
        logger.info("Updating device masks")
        device: "Devices" = self.selected_device
        boot: str = self.fields[""]["mask"]["boot"].get().strip()
        uboot: str = self.fields[""]["mask"]["uboot"].get().strip()
        firmware: str = self.fields[""]["mask"]["firmware"].get().strip()

        self.app.db_services["device"].update_masks(device, boot, uboot, firmware)
        logger.debug("Device masks updated successfully")

    def update_ports(self) -> None:
        """Updates the ports for the selected device."""
        logger.info("Updating device ports")
        self.app.db_services["device"].update_ports(
            self.selected_device, self.port_input
        )
        logger.debug("Device ports updated successfully")

    def update_protocols(self) -> None:
        """Updates the protocols for the selected device."""
        logger.info("Updating device protocols")
        self.app.db_services["device"].update_protocols(
            self.selected_device, self.protocol_input
        )
        logger.debug("Device protocols updated successfully")

    @property
    def selected_device(self) -> "Devices":
        """Returns the currently selected device."""
        device_name = self.fields[""]["device"].get().strip()
        logger.debug("Getting selected device: %s", device_name)
        return self.app.db_services["device"].get_one(name=device_name)

    @property
    def protocol_input(self) -> List["Protocols"]:
        """Returns a list of selected protocols."""
        logger.debug("Getting selected protocols")
        res: List["Protocols"] = []
        for protocol_name, checkbox in self.fields[""]["protocols"].items():
            if checkbox.get() == 1:
                protocol = self.app.db_services["protocol"].get_one(name=protocol_name)
                res.append(protocol)
        logger.debug("Selected protocols: %s", res)
        return res

    @property
    def port_input(self) -> List["Ports"]:
        """Returns a list of selected ports, handling mixed speeds and trailing None values."""
        logger.debug("Getting selected ports")
        raw_input: List[str] = list(
            map(lambda x: x[1].get(), self.fields[""]["ports"].items())
        )

        def strip_none(ports: List[str]) -> List[str]:
            """Removes trailing "None" values from the port list."""
            while ports and ports[-1] == "None":
                ports.pop()
            return ports

        def check_mixed_speeds(fields: List[str]) -> List["Ports"]:
            """Checks for mixed speeds in the port list and raises an error if found."""
            is1000mbps: bool = False
            res: List["Ports"] = []
            for port_name in fields[::-1]:
                if port_name == "None":
                    res.append(res[-1])
                    continue
                port: "Ports" = self.app.db_services["port"].get_one(name=port_name)
                if port.speed != 10000:
                    is1000mbps = True
                elif is1000mbps and port.speed == 10000:
                    logger.error("Mixed speeds detected in port enumeration")
                    raise ValueError("Mixed speeds in port enumeration")
                res.append(port)
            return res[::-1]

        ports = check_mixed_speeds(strip_none(raw_input))
        logger.debug("Selected ports: %s", ports)
        return ports
