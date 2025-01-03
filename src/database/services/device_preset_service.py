from functools import wraps
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import delete, insert

from database.models import DevicePresets, Templates, Presets
from .decorators import transactional


def check_template_role(func):
    def wrapper(self, preset_id: int, template_id: int, *args, **kwargs):
        template = self.db.query(Templates).filter(Templates.id == template_id).first()
        preset = self.db.query(Presets).filter(Presets.id == preset_id).first()
        if template.role not in ['common', preset.role]:
            raise ValueError("Template and preset have different roles")
        return func(self, preset_id, template_id, *args, **kwargs)

    return wrapper


class DevicePresetService:
    def __init__(self, db: Session):
        self.db = db

    def _get_max_ordered_number(self, preset_id: int) -> int:
        return self.db.query(func.max(DevicePresets.ordered_number)) \
            .filter(DevicePresets.preset_id == preset_id) \
            .scalar() or 0

    def _clear(self, preset_id):
        self.db.query(DevicePresets).filter(DevicePresets.preset_id == preset_id).delete()
        self.db.commit()

    def copy(self, source_preset, destination_preset):
        if source_preset == destination_preset:
            raise ValueError("preset_from is preset_to!")
        if source_preset.role != destination_preset.role:
            raise ValueError("Preset roles are different!")
        dev1 = self.device_service.get_by_id(source_preset.device_id)
        dev2 = self.device_service.get_by_id(destination_preset.device_id)
        if dev1.family_id != dev2.family_id:
            raise ValueError("Devices are from different families!")

        self._clear(destination_preset.id)
        records = self.db.query(DevicePresets).filter_by(preset_id=source_preset.id).all()
        for record in records:
            new_record = record.__class__(
                preset_id=destination_preset.id,
                template_id=record.template_id,
                ordered_number=record.ordered_number,
            )
            self.db.add(new_record)

        self.db.commit()
    @check_template_role
    @transactional
    def push_back(self, preset_id: int, template_id: int):
        max_ordered_number = self._get_max_ordered_number(preset_id)

        device_preset = DevicePresets(
            template_id=template_id,
            ordered_number=max_ordered_number + 1,
            preset_id=preset_id
        )

        self.db.add(device_preset)
        return device_preset

    @check_template_role
    @transactional
    def insert(self, preset_id: int, template_id: int, ordered_number: int):
        max_ordered_number = self._get_max_ordered_number(preset_id)
        if ordered_number > max_ordered_number + 1:
            raise ValueError(f"The ordered_number={ordered_number} value exceeds the allowed limit for preset_id={preset_id}.")
        # Shift existing templates
        self.db.query(DevicePresets) \
            .filter(DevicePresets.preset_id == preset_id,
                    DevicePresets.ordered_number >= ordered_number) \
            .update({DevicePresets.ordered_number: DevicePresets.ordered_number + 1},
                    synchronize_session=False)

        new_device_preset = DevicePresets(
            template_id=template_id,
            ordered_number=ordered_number,
            preset_id=preset_id
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
