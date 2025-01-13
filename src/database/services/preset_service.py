from sqlalchemy.orm import Session

from database.models import Presets, DevicePresets, Templates, Devices
from .base_service import BaseService
from .device_service import DeviceService
from .device_preset_service import DevicePresetService
from .template_service import TemplateService


class PresetService(BaseService, DevicePresetService):
    def __init__(self, db: Session):
        super().__init__(db, Presets)
        self.device_service = DeviceService(db)
        self.template_service = TemplateService(db)

    def get_all_by_device_id(self, device_id):
        return [preset for preset in self.get_all() if preset.device_id == device_id]

    def get_info(self, preset):
        rows = (
            self.db.query(Presets, DevicePresets, Templates)
            .join(DevicePresets, Presets.id == DevicePresets.preset_id)
            .join(Templates, DevicePresets.template_id == Templates.id)
            .join(Devices, Presets.device_id == Devices.id)
            .filter(Presets.name == preset.name)
            .order_by(DevicePresets.ordered_number)
            .all()
        )
        interfaces = (
            port["interface"]
            for port in self.device_service.get_info_by_id(preset.device_id)["ports"]
        )  # generator
        return {
            "preset": preset.name,
            "id": preset.id,
            "target": self.device_service.get_by_id(preset.device_id).name,
            "role": preset.role,
            "description": preset.description,
            "configuration": {
                f"{template.type if template.type != 'interface' else next(interfaces)}": self.template_service.get_info(
                    template
                )
                for preset, device_preset, template in rows
            },
        }
