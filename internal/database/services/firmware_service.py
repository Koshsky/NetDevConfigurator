from sqlalchemy.orm import Session

from internal.database.models import Firmwares, DeviceFirmwares
from .base_service import BaseService
from .device_services.device_firmware_service import DeviceFirmwareService


class FirmwareService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Firmwares)
        self.device_service = DeviceFirmwareService(db)

    def get_info(self, firmware: Firmwares):
        associated_devices = self.device_service.get_devices_by_firmware_id(firmware.id)
        return {
            "id": firmware.id,
            "name": firmware.name,
            "full_path": firmware.full_path,
            "type": firmware.type,
            "associated_devices": [device.name for device in associated_devices]
        }

def determine_firmware_type(firmware_name: str) -> str:
    # первичная: .bl1
    # вторичная: .uboot .boot
    # сама прошивка: .firmware .iss .ros

    primary = "primary_bootloader"
    secondary = "secondary_bootloader"
    firmware = "firmware"

    firmware_types = {
        '.bl1': primary,
        '.uboot': secondary,
        '.boot': secondary,
        '.firmware': firmware,
        '.iss': firmware,
        '.ros': firmware,
    }

    return next(
        (
            description
            for extension, description in firmware_types.items()
            if firmware_name.endswith(extension)
        ),
        "UKNOWN",
    )
