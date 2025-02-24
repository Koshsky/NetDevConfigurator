import logging
from typing import List

from sqlalchemy.orm import Session

from database.models import Companies, DevicePorts, Devices, Ports

from .base_service import JsonType

logger = logging.getLogger("db")


class DevicePortService:
    def __init__(self, db: Session):
        self.db = db

    def update_ports(self, device: Devices, ports: List[Ports] | None) -> Devices:
        self._reset_ports(device)
        if ports is not None:
            for port in ports:
                self._add_port(device, port)
        logger.debug(
            'Successfully update ports for device: {"name": "%s"}, bound %d ports',
            device.name,
            len(ports),
        )

    def _reset_ports(self, device: Devices) -> None:
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

    def get_ports(self, device: Devices) -> List[JsonType]:
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

    def _add_port(self, device: Devices, port: Ports) -> DevicePorts:
        company = (
            self.db.query(Companies)
            .join(Devices, Companies.id == Devices.company_id)
            .filter(Devices.id == device.id)
            .first()
        )
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
        port = self.db.query(Ports).filter(Ports.id == port_id).first()
        q = len(
            self.db.query(DevicePorts)
            .join(Ports, DevicePorts.port_id == Ports.id)
            .filter(Ports.speed == port.speed, DevicePorts.device_id == device_id)
            .all()
        )
        return f"{'ten' if port.speed == 10000 else ''}gigabitethernet 0/{q + 1}"

    def _get_next_Zyxel_interface(self, device_id: int, port_id: int) -> str:
        port = self.db.query(Ports).filter(Ports.id == port_id).first()
        q = len(
            self.db.query(DevicePorts)
            .join(Ports, DevicePorts.port_id == Ports.id)
            .filter(Ports.speed == port.speed, DevicePorts.device_id == device_id)
            .all()
        )
        return f"port-channel {q + 1}"

    def _default_get_next_interface(self, device_id: int, port_id: int) -> str:
        raise NotImplementedError(
            "There is no default method for getting next interface"
        )
