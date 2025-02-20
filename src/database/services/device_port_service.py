import logging
from typing import List

from sqlalchemy.orm import Session

from database.models import Companies, DevicePorts, Devices, Ports

from .base_service import JsonType

logger = logging.getLogger("db")


class DevicePortService:
    def __init__(self, db: Session):
        self.db = db

    def reset_ports(self, device_id: int) -> None:
        try:
            deleted_count = (
                self.db.query(DevicePorts)
                .filter(DevicePorts.device_id == device_id)
                .delete()
            )
            self.db.commit()
            logger.info(
                "Successfully reset ports for device_id: %d, deleted %d ports",
                device_id,
                deleted_count,
            )
        except Exception as e:
            logger.error(
                "Failed to reset ports for device_id: %d, error: %s", device_id, str(e)
            )
            self.db.rollback()

    def _get_ports_by_id(self, device_id: int) -> List[JsonType]:
        try:
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
                    .filter(DevicePorts.device_id == device_id)
                    .all()
                )
            ]
            logger.info(
                "Retrieved ports for device_id: %d, found %d ports",
                device_id,
                len(ports),
            )
            return ports
        except Exception as e:
            logger.error(
                "Failed to get ports for device_id: %d, error: %s", device_id, str(e)
            )
            return []  # Возвращаем пустой список в случае ошибки

    def add_port_by_id(self, device_id: int, port_id: int) -> DevicePorts:
        try:
            company = (
                self.db.query(Companies)
                .join(Devices, Companies.id == Devices.company_id)
                .filter(Devices.id == device_id)
                .first()
            )
            get_next_interface = getattr(
                self,
                f"_get_next_{company.name}_interface",
                self._default_get_next_interface,
            )
            new_device_port = DevicePorts(
                device_id=device_id,
                port_id=port_id,
                interface=get_next_interface(device_id, port_id),
            )
            self.db.add(new_device_port)
            self.db.commit()
            logger.info(
                "Successfully added port_id: %d to device_id: %d", port_id, device_id
            )
            return new_device_port
        except Exception as e:
            logger.error(
                "Failed to add port_id: %d to device_id: %d, error: %s",
                port_id,
                device_id,
                str(e),
            )
            self.db.rollback()  # Откат транзакции в случае ошибки

    def remove_port_by_id(self, device_id: int, port_id: int) -> None:
        try:
            deleted_count = (
                self.db.query(DevicePorts)
                .filter(
                    DevicePorts.device_id == device_id, DevicePorts.port_id == port_id
                )
                .delete()
            )
            self.db.commit()
            logger.info(
                "Successfully removed port_id: %d from device_id: %d, deleted %d ports",
                port_id,
                device_id,
                deleted_count,
            )
        except Exception as e:
            logger.error(
                "Failed to remove port_id: %d from device_id: %d, error: %s",
                port_id,
                device_id,
                str(e),
            )
            self.db.rollback()  # Откат транзакции в случае ошибки

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
