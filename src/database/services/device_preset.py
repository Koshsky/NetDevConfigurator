import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import func
from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from database.models import DevicePresets, Presets, Templates

from database.models import DevicePresets, Presets, Templates

from .decorators import transactional
from .device import DeviceService

logger = logging.getLogger(__name__)


def check_template(func):
    """Decorator to check template compatibility with a preset.

    This decorator ensures that a template can be added to a preset based on role and type.
    It raises ValueError if the template and preset have different roles or if an interface
    template is added when the preset already has the maximum number of interfaces.
    It raises TypeError if a non-interface template of the same type already exists in the preset.
    """

    def wrapper(
        self, preset: "Presets", template: "Templates", *args: Any, **kwargs: Any
    ) -> "DevicePresets":
        logger.debug(
            "Checking template compatibility: preset=%s, template=%s",
            preset.role,
            template.name,
        )
        if template.role not in ["common", preset.role]:
            logger.error("Template and preset have different roles")
            raise ValueError("Template and preset have different roles")
        if self.validate(preset) and template.type == "interface":
            logger.error(
                "Cannot insert interface template into preset: interface limit reached"
            )
            raise ValueError(
                "Cannot insert interface template into preset:\n"
                "the number of interface templates has reached the limit for the preset"
            )

        for _, t in self.get_info(preset)["configuration"].items():  # type: ignore[call-arg]
            if t["type"] != "interface" and t["type"] == template.type:
                logger.error(
                    "Cannot insert %s. Template with type=%s already in preset",
                    template.name,
                    template.type,
                )
                raise TypeError(
                    f"Cannot insert {template.name}. Template with type={template.type} already in preset"
                )
        logger.debug("Template compatibility check passed")
        return func(self, preset, template, *args, **kwargs)

    return wrapper


class DevicePresetService:
    """Manages the association between devices and presets in the database.

    This service provides methods to add, insert, remove, and validate template
    associations within a preset, ensuring consistency and data integrity.
    """

    def __init__(self, db: Session) -> None:
        """Initializes DevicePresetService with a database session.

        Args:
            db: The SQLAlchemy database session.
        """
        logger.debug("Initializing DevicePresetService")
        self.db = db

    @check_template
    @transactional
    def push_back(self, preset: "Presets", template: "Templates") -> "DevicePresets":
        """Adds a template to the end of a preset's configuration.

        Args:
            preset: The preset to add the template to.
            template: The template to add.

        Returns:
            The newly created DevicePresets instance.
        """
        logger.info("Adding template %s to preset %s", template.name, preset.role)
        max_ordered_number = self._get_max_ordered_number(preset.id)

        device_preset = DevicePresets(
            template_id=template.id,
            ordered_number=max_ordered_number + 1,
            preset_id=preset.id,
        )

        self.db.add(device_preset)
        logger.debug("Template %s added to preset %s", template.name, preset.role)
        return device_preset

    @check_template
    @transactional
    def insert(
        self, preset: "Presets", template: "Templates", ordered_number: int
    ) -> "DevicePresets":
        """Inserts a template into a preset's configuration at a specific position.

        Args:
            preset: The preset to insert the template into.
            template: The template to insert.
            ordered_number: The position to insert the template at.

        Returns:
            The newly created DevicePresets instance.

        Raises:
            ValueError: If the ordered_number exceeds the allowed limit.
        """
        logger.info(
            "Inserting template %s into preset %s at position %d",
            template.name,
            preset.role,
            ordered_number,
        )
        max_ordered_number = self._get_max_ordered_number(preset.id)
        if ordered_number > max_ordered_number + 1:
            logger.error(
                "The ordered_number=%d value exceeds the allowed limit for preset_id=%d",
                ordered_number,
                preset.id,
            )
            raise ValueError(
                f"The ordered_number={ordered_number} value exceeds the allowed limit for preset_id={preset.id}."
            )
        # Shift existing templates
        self.db.query(DevicePresets).filter(
            DevicePresets.preset_id == preset.id,
            DevicePresets.ordered_number >= ordered_number,
        ).update(
            {DevicePresets.ordered_number: DevicePresets.ordered_number + 1},
            synchronize_session=False,
        )

        new_device_preset = DevicePresets(
            template_id=template.id, ordered_number=ordered_number, preset_id=preset.id
        )

        self.db.add(new_device_preset)
        logger.debug("Template %s inserted into preset %s", template.name, preset.role)
        return new_device_preset

    @transactional
    def remove(self, preset_id: int, ordered_number: int) -> None:
        """Removes a template from a preset's configuration.

        Args:
            preset_id: The ID of the preset.
            ordered_number: The position of the template to remove.
        """
        logger.info(
            "Removing template at position %d from preset_id %d",
            ordered_number,
            preset_id,
        )
        self.db.query(DevicePresets).filter(
            DevicePresets.preset_id == preset_id,
            DevicePresets.ordered_number == ordered_number,
        ).delete(synchronize_session=False)
        # Shift existing templates
        self.db.query(DevicePresets).filter(
            DevicePresets.preset_id == preset_id,
            DevicePresets.ordered_number > ordered_number,
        ).update(
            {DevicePresets.ordered_number: DevicePresets.ordered_number - 1},
            synchronize_session=False,
        )
        logger.debug("Template removed from preset")

    def validate(self, preset: "Presets") -> bool:
        """Validates a preset by checking the number of interface templates.

        Args:
            preset: The preset to validate.

        Returns:
            True if the number of interface templates equals the number of device ports, False otherwise.

        Raises:
            ValueError: If more interfaces are described in the preset than in the device.
        """
        logger.debug("Validating preset: %s", preset.role)
        described_interfaces = len(
            self.db.query(DevicePresets)
            .join(Templates, DevicePresets.template_id == Templates.id)
            .filter(DevicePresets.preset_id == preset.id)
            .filter(Templates.type == "interface")
            .all()
        )
        device_ports = len(
            DeviceService(self.db).get_info_one(id=preset.device_id)["ports"]
        )
        if described_interfaces > device_ports:
            logger.error(
                "More interfaces are described in the preset than in the device: %d",
                described_interfaces,
            )
            raise ValueError(
                f"More interfaces are described in the preset than in the device: {described_interfaces}"
            )

        logger.debug(
            "Preset validation result: %s", described_interfaces == device_ports
        )
        return described_interfaces == device_ports

    def _get_max_ordered_number(self, preset_id: int) -> int:
        """Retrieves the maximum ordered number for a preset.

        Args:
            preset_id: The ID of the preset.

        Returns:
            The maximum ordered number, or 0 if no templates are associated with the preset.
        """
        logger.debug("Getting max ordered number for preset_id: %d", preset_id)
        max_ordered_number: int = (
            self.db.query(func.max(DevicePresets.ordered_number))
            .filter(DevicePresets.preset_id == preset_id)
            .scalar()
            or 0
        )
        logger.debug("Max ordered number: %d", max_ordered_number)
        return max_ordered_number
