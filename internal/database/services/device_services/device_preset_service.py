from functools import wraps
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import delete, insert

from internal.database.models import DevicePresets, Templates
from ..decorators import transactional
from ..base_service import BaseService
from ..template_service import TemplateService
from ..preset_service import PresetService
from .device_service import DeviceService

def check_template_role(func):
    def wrapper(self, preset_id: int, template_id: int, *args, **kwargs):
        template = self.template_service.get_by_id(template_id)
        preset = self.preset_service.get_by_id(preset_id)
        if template.role not in ['common', preset.role]:
            raise ValueError("Template and preset have different roles")
        return func(self, preset_id, template_id, *args, **kwargs)

    return wrapper


class DevicePresetService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, DevicePresets)
        self.preset_service = PresetService(db)
        self.template_service = TemplateService(db)
        self.device_service = DeviceService(db)

    def _get_max_ordered_number(self, preset_id: int) -> int:
        return self.db.query(func.max(DevicePresets.ordered_number)) \
            .filter(DevicePresets.preset_id == preset_id) \
            .scalar() or 0

    def __clear(self, preset_id):
        self.db.query(DevicePresets).filter(DevicePresets.preset_id == preset_id).delete()
        self.db.commit()

    def copy(self, source, destination):
        if source == destination:
            raise ValueError("preset_from is preset_to!")
        dev1 = self.device_service.get_by_id(source.device_id)
        dev2 = self.device_service.get_by_id(destination.device_id)
        if dev1.family_id != dev2.family_id:
            raise ValueError("Devices are from different families!")

        self.__clear(destination.id)
        records = self.db.query(DevicePresets).filter_by(preset_id=source.id).all()
        for record in records:
            new_record = record.__class__(
                preset_id=destination.id,
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
