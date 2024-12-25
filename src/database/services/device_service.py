from sqlalchemy.orm import Session

from database.models import Devices
from .device_firmware_service import DeviceFirmwareService
from .device_port_service import DevicePortService
from .device_protocol_service import DeviceProtocolService
from .base_service import BaseService


class DeviceService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Devices)
        self.device_port_service = DevicePortService(db)
        self.device_protocol_service = DeviceProtocolService(db)
        self.device_firmware_service = DeviceFirmwareService(db)

    def get_devices_by_company_id(self, company_id: int):
        return (
            self.db.query(Devices)
                .filter(Devices.company_id == company_id)
                .all()
        )

    def get_devices_by_family_id(self, family_id: int):
        return (
            self.db.query(Devices)
                .filter(Devices.family_id == family_id)
                .all()
        )

    def get_info(self, device):
        device_ports = self.device_port_service.get_device_ports(device.id)
        associated_protocols = self.device_protocol_service.get_protocols_by_device_id(device.id)
        associated_firmwares = self.device_firmware_service.get_firmwares_by_device_id(device.id)

        return {
            "id": device.id,
            "name": device.name,
            "dev_type": device.dev_type,
            "family": {
                "name": device.family.name,
                "id": device.family.id
            },
            "company": {
                "name": device.company.name,
                "id": device.company.id
            },
            "protocols": [
                {
                    "name": protocol.name,
                    "id": protocol.id
                } for _, protocol in associated_protocols
            ],
            "firmwares": [
                {
                    "name": firmware.name,
                    "full_path": firmware.full_path,
                    "type": firmware.type,
                    "id": firmware.id
                } for firmware in associated_firmwares
            ],
            "ports": [
                {
                    "interface": device_port.interface,
                    "material": port.material,
                    "speed": port.speed,
                    "name": port.name
                } for device_port, port in device_ports
            ],
        }
