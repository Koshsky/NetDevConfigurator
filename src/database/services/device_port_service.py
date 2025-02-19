from typing import List

from sqlalchemy.orm import Session

from database.models import Companies, DevicePorts, Devices, Ports

from .base_service import JsonType


class DevicePortService:
    def __init__(self, db: Session):
        self.db = db

    def reset_ports(self, device_id: int) -> None:  # TODO: смущает
        self.db.query(DevicePorts).filter(DevicePorts.device_id == device_id).delete()
        self.db.commit()

    def get_ports_by_id(self, device_id: int) -> List[JsonType]:  # TODO: смущает
        # TODO: реализовать get_info у device_port
        return [
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

    def add_port_by_id(self, device_id: int, port_id: int) -> None:  # TODO: смущает
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
        self.db.add(
            DevicePorts(
                device_id=device_id,
                port_id=port_id,
                interface=get_next_interface(device_id, port_id),
            )
        )
        self.db.commit()

    def remove_port_by_id(self, device_id: int, port_id: int) -> None:  # TODO: смущает
        self.db.query(DevicePorts).filter(
            DevicePorts.device_id == device_id, DevicePorts.port_id == port_id
        ).delete()
        self.db.commit()

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
        return f"port-channel {q + 1}"  # TODO: МНЕ НУЖЕН ПРИМЕР КОНФИГУРАЦИИ ДЛЯ УТОЧНЕНИЯ.

    def _default_get_next_interface(self, device_id: int, port_id: int) -> str:
        raise NotImplementedError(
            "There is no default method for getting next interface"
        )
