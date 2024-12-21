from functools import wraps
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import delete, insert

from internal.database.models import DevicePresets, Templates
from ..decorators import transactional
from ..base_service import BaseService
from ..template_service import TemplateService

def check_template_role(func):
    def wrapper(self, template_id: int, preset_id: int, *args, **kwargs):
        template = self.template_service.get_by_id(template_id)
        preset = self.get_by_id(preset_id)
        if template.role not in ['common', preset.role]:
            raise ValueError("Template and preset have different roles")
        return func(self, *args, **kwargs)

    return wrapper


class DevicePresetService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, DevicePresets)
        self.template_service = TemplateService(db)

    def _get_max_ordered_number(self, preset_id: int) -> int:
        return self.db.query(func.max(DevicePresets.ordered_number)) \
            .filter(DevicePresets.preset_id == preset_id) \
            .scalar() or 0

    @check_template_role
    @transactional
    def push_back(self, preset_id: int, template_id: int):
        max_ordered_number = self._get_max_ordered_number(template_id)

        device_preset = DevicePresets(
            template_id=preset_id,
            ordered_number=max_ordered_number + 1,
            preset_id=template_id
        )

        self.db.add(device_preset)
        return device_preset

    @check_template_role
    @transactional
    def insert(self, preset_id: int, template_id: int, ordered_number: int):
        max_ordered_number = self._get_max_ordered_number(template_id)
        if ordered_number > max_ordered_number + 1:
            raise ValueError(f"The ordered_number={ordered_number} value exceeds the allowed limit for preset_id={template_id}.")
        # Shift existing templates
        self.db.query(DevicePresets) \
            .filter(DevicePresets.preset_id == template_id,
                    DevicePresets.ordered_number >= ordered_number) \
            .update({DevicePresets.ordered_number: DevicePresets.ordered_number + 1},
                    synchronize_session=False)

        new_device_preset = DevicePresets(
            template_id=preset_id,
            ordered_number=ordered_number,
            preset_id=template_id
        )

        self.db.add(new_device_preset)
        return new_device_preset

    @transactional
    def remove(self, preset_id: int, ordered_number: int):
        self.db.query(DevicePresets) \
            .filter(DevicePresets.preset_id == preset_id, DevicePresets.ordered_number == ordered_number) \
                .delete(synchronize_session=False)
        # Shift existing templates
        self.db.query(DevicePresets) \
            .filter(DevicePresets.preset_id == preset_id,
                    DevicePresets.ordered_number > ordered_number) \
            .update({DevicePresets.ordered_number: DevicePresets.ordered_number - 1},
                    synchronize_session=False)
