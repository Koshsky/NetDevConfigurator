from sqlalchemy.orm import Session

from internal.database.models import Presets, DevicePresets, Templates, Devices
from .base_service import BaseService
from .device_services.device_service import DeviceService


class PresetService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Presets)
        self.device_service = DeviceService(db)

    def get_all_by_device_id(self, device_id):
        presets = (
            self.db.query(Presets.name)
            .filter(
                Presets.device_id == device_id,
            )
            .all()
        )
        return [preset[0] for preset in presets]

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
        return {
            "device": self.device_service.get_by_id(rows[0][0].device_id).name,
            "preset": preset.name,
            "role": rows[0][0].role,
            "description": rows[0][0].description,
            "configuration": [
                {
                    'template': {
                        'id': template.id,
                        'type': template.type,
                        'text': template.text
                    },
                    'ordered_number': device_preset.ordered_number
                } for preset, device_preset, template in rows
            ]
        }
