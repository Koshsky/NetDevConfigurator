from sqlalchemy.orm import Session

from database.models import DevicePresets, Devices, Presets, Templates

from .base_service import BaseService, JsonType
from .device_preset_service import DevicePresetService
from .device_service import DeviceService
from .family_service import FamilyService
from .template_service import TemplateService


class PresetService(BaseService, DevicePresetService):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Presets)
        self.device_service = DeviceService(db)
        self.template_service = TemplateService(db)
        self.family_service = FamilyService(db)

    def get_info(self, preset: Presets, check: bool = False) -> JsonType:
        if check and not self.validate(preset):
            device = self.device_service.get_one(id=preset.device_id)
            raise ValueError(
                f"Invalid preset configuration. device={device.name}, role={preset.role}"
            )
        rows = (
            self.db.query(Presets, DevicePresets, Templates)
            .join(DevicePresets, Presets.id == DevicePresets.preset_id)
            .join(Templates, DevicePresets.template_id == Templates.id)
            .join(Devices, Presets.device_id == Devices.id)
            .filter(Presets.id == preset.id)
            .order_by(DevicePresets.ordered_number)
            .all()
        )
        device = self.device_service.get_one(id=preset.device_id)
        interfaces = (
            port["interface"] for port in self.device_service.get_info(device)["ports"]
        )  # generator
        return {
            "id": preset.id,
            "target": device.name,
            "family": self.family_service.get_info_one(id=device.family_id),
            "role": preset.role,
            "description": preset.description,
            "configuration": {
                f"{template.type if template.type != 'interface' else next(interfaces, 'INVALID INTERFACE')}": self.template_service.get_info(
                    template
                )
                for preset, device_preset, template in rows
            },
        }
