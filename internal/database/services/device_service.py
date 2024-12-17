from sqlalchemy.orm import Session

from internal.database.models import Devices
from .device_firmware_service import DeviceFirmwareService
from .device_port_service import DevicePortService
from .device_protocol_service import DeviceProtocolService


class DeviceService:
    def __init__(self, db: Session):
        self.db = db
        self.device_port = DevicePortService(db)
        self.device_protocol = DeviceProtocolService(db)
        self.device_firmware = DeviceFirmwareService(db)

    def get_all(self):
        return self.db.query(Devices).all()
    
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


    def get_by_id(self, device_id: int):
        return self.db.query(Devices).filter(Devices.id == device_id).first()

    def get_by_name(self, name: str):
        return self.db.query(Devices).filter(Devices.name == name).first()


    def create(self, device: dict):
        device = Devices(**device)
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        return device

    def delete(self, device):
        if device:
            self.db.delete(device)
            self.db.commit()

    def delete_by_id(self, device_id: int):
        db_device = self.get_by_id(device_id)
        self.delete(db_device)

    def delete_by_name(self, name: str):
        db_device = self.get_by_name(name)
        self.delete(db_device)
        
    
    def get_info(self, device):
        device_ports = self.device_port.get_device_ports(device.id)
        device_protocols = self.device_protocol.get_device_protocols(device.id)
        device_firmwares = self.device_firmware.get_device_firmwares(device.id)

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
            "ports": [
                {
                    "interface": device_port.interface,
                    "material": port.material,
                    "speed": port.speed,
                    "name": port.name
                } for device_port, port in device_ports
            ],
            "firmwares": [
                {
                    "name": device_firmware.firmware.name,
                    "full_path": device_firmware.firmware.full_path,
                    "type": device_firmware.firmware.type,
                    "id": device_firmware.firmware.id
                } for device_firmware in device_firmwares
            ],
            "protocols": [
                {
                    "name": device_protocol.protocol.name,
                    "id": device_protocol.protocol.id
                } for device_protocol in device_protocols
            ]
        }

    def get_info_by_name(self, device_name: str):
        device = self.get_by_name(device_name)
        return self.get_info(device)
    
    def get_info_by_id(self, device_id: int):
        device = self.get_by_id(device_id)
        return self.get_info(device)
