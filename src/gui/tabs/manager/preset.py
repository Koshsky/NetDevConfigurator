import logging
from typing import Any, Dict, List

from database.services import ALLOWED_ROLES
from gui import BaseTab, apply_error_handler

logger = logging.getLogger(__name__)


@apply_error_handler
class PresetTab(BaseTab):
    """
    Tab for managing device presets.
    """

    def __init__(self, app: Any, parent: Any, log_name: str = "ConfigTab") -> None:
        super().__init__(app, parent, log_name)
        self.preset_info: Dict[str, Any] = None

    def _create_widgets(self) -> None:
        """Creates and arranges widgets within the tab."""
        self._create_preset_block()
        self._create_configuration_block()
        self.create_feedback_area()
        self.refresh_templates()

    def _create_preset_block(self) -> None:
        """Creates the preset management block."""
        devices = self.app.db_services["device"].get_all(dev_type="switch")
        self.create_block(
            "preset",
            {
                "device": tuple(d.name for d in devices),
                "role": ALLOWED_ROLES,
            },
        )
        self.create_button_in_line(("CREATE", self.create_preset))
        self.create_button_in_line(("DELETE", self.delete_preset))
        self.create_button_in_line(("REFRESH TEMPLATES", self.refresh_templates))

    def _create_configuration_block(self) -> None:
        """Creates the configuration template block."""
        self.create_block(
            "template",
            {
                "name": ("1", "2"),  # Placeholder initial values
                "ordered_number": tuple(map(str, range(1, 101))),
            },
        )
        self.create_button_in_line(("PUSH BACK", self.push_back))
        self.create_button_in_line(("INSERT", self.insert))
        self.create_button_in_line(("REMOVE", self.remove))
        self.create_button_in_line(("PREVIEW", self.preview))

    def create_preset(self) -> None:
        """Creates a new preset."""
        role = self.fields["preset"]["role"].get().strip()
        device_id = self.selected_device.id
        logger.info(f"Creating preset for device {device_id} with role {role}")
        self.app.db_services["preset"].create(role=role, device_id=device_id)

    def delete_preset(self) -> None:
        """Deletes the selected preset."""
        logger.info(f"Deleting preset: {self.selected_preset}")
        self.app.db_services["preset"].delete(self.selected_preset)

    @property
    def selected_device(self) -> Any:
        """Returns the currently selected device."""
        device_name = self.fields["preset"]["device"].get().strip()
        logger.debug(f"Fetching device with name: {device_name}")
        return self.app.db_services["device"].get_one(name=device_name)

    @property
    def selected_preset(self) -> Any:
        """Returns the currently selected preset."""
        device_id = self.selected_device.id
        role = self.fields["preset"]["role"].get().strip()
        logger.debug(f"Fetching preset for device {device_id} with role {role}")
        preset = self.app.db_services["preset"].get_one(device_id=device_id, role=role)
        self.preset_info = self.app.db_services["preset"].get_info(preset)
        return preset

    @property
    def selected_template(self) -> Any:
        """Returns the currently selected template."""
        name = self.fields["template"]["name"].get().strip()
        family_id = self.selected_device.family_id
        role = ["common", self.selected_preset.role]
        logger.debug(
            f"Fetching template with name {name}, family {family_id}, and roles {role}"
        )
        return self.app.db_services["template"].get_one(
            name=name, family_id=family_id, role=role
        )

    @property
    def relevant_templates(self) -> List[str]:
        """Returns a list of relevant template names."""
        family_id = self.selected_device.family_id
        role = ["common", self.selected_preset.role]
        logger.debug(
            f"Fetching relevant templates for family {family_id} and roles {role}"
        )
        return [
            template.name
            for template in self.app.db_services["template"].get_all(
                family_id=family_id, role=role
            )
        ]

    def remove(self) -> None:
        """Removes a template from the preset."""
        ordered_number = int(self.fields["template"]["ordered_number"].get().strip())
        logger.info(
            f"Removing template at position {ordered_number} from preset {self.selected_preset.id}"
        )
        self.app.db_services["preset"].remove(self.selected_preset.id, ordered_number)
        self._display_configuration_status(
            f"Template at position {ordered_number} successfully removed\n"
        )

    def push_back(self) -> None:
        """Pushes a template to the back of the preset."""
        logger.info(
            f"Pushing back template {self.selected_template.name} to preset {self.selected_preset}"
        )
        self.app.db_services["preset"].push_back(
            self.selected_preset, self.selected_template
        )
        self._display_configuration_status(
            f"Template {self.selected_template.name} successfully pushed back\n"
        )

    def insert(self) -> None:
        """Inserts a template at a specific position in the preset."""
        ordered_number = int(self.fields["template"]["ordered_number"].get().strip())
        logger.info(
            f"Inserting template {self.selected_template.name} at position {ordered_number} in preset {self.selected_preset}"
        )
        self.app.db_services["preset"].insert(
            self.selected_preset, self.selected_template, ordered_number
        )
        self._display_configuration_status(
            f"Template {self.selected_template.name} successfully inserted at position {ordered_number}\n"
        )

    def refresh_templates(self) -> None:
        """Refreshes the list of available templates."""
        if not self.relevant_templates:
            logger.error("No suitable configuration templates found")
            raise ValueError("There are no suitable configuration templates")
        self.fields["template"]["name"].set_values(self.relevant_templates)
        self.fields["template"]["name"].set_text(
            self.relevant_templates[0] if self.relevant_templates else None
        )

    def preview(self) -> None:
        """Displays a preview of the preset configuration."""
        if self.preset_info:
            preview_text = "\n".join(
                v["text"]
                for _, (_, v) in enumerate(
                    self.preset_info["configuration"].items(), start=1
                )
            )
            self.display_feedback(preview_text)
        else:
            logger.warning("No preset selected for preview")
            self.display_feedback("No preset selected for preview")

    def _display_configuration_status(self, message: str) -> None:
        """Displays the configuration status."""
        status_message = (
            f"{message or ''}\n{self._config_meta()}\n\n{self._config_template()}"
        )
        self.display_feedback(status_message)

    def _config_meta(self) -> str:
        """Returns a formatted string of configuration metadata."""
        if not self.preset_info:
            return "No preset selected"

        interfaces = len(
            [
                i
                for _, i in self.preset_info["configuration"].items()
                if i["type"] == "interface"
            ]
        )
        device_ports = len(
            self.app.db_services["device"].get_info_one(
                name=self.preset_info["device"]
            )["ports"]
        )
        return (
            f"Role: {self.preset_info['role']}\n"
            f"Device: {self.preset_info['device']}\n"
            f"Description: {self.preset_info.get('description', 'N/A')}\n"  # Handle missing description
            f"Described interfaces/Physical ports: {interfaces}/{device_ports}\n"
        )

    def _config_template(self) -> str:
        """Returns a formatted string of the configuration template."""
        if not self.preset_info:
            return "No preset selected"
        return "\n".join(
            f"{i}\t{v['name']}"
            for i, (k, v) in enumerate(
                self.preset_info["configuration"].items(), start=1
            )
        )
