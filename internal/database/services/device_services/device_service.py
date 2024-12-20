from sqlalchemy.orm import Session

from internal.database.models import Devices
from .device_firmware_service import DeviceFirmwareService
from .device_port_service import DevicePortService
from .device_protocol_service import DeviceProtocolService
from ..base_service import BaseService


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
        device_protocols = self.device_protocol_service.get_device_protocols(device.id)
        device_firmwares = self.device_firmware_service.get_device_firmwares(device.id)

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
                    "name": device_protocol.protocol.name,
                    "id": device_protocol.protocol.id
                } for device_protocol in device_protocols
            ],
            "firmwares": [
                {
                    "name": device_firmware.firmware.name,
                    "full_path": device_firmware.firmware.full_path,
                    "type": device_firmware.firmware.type,
                    "id": device_firmware.firmware.id
                } for device_firmware in device_firmwares
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
