import logging
from typing import Any, Callable, Dict, Tuple

from gui import BaseTab, apply_error_handler
from utils.environ import get_env

logger = logging.getLogger(__name__)


@apply_error_handler
class TemplateTab(BaseTab):
    """Manages configuration templates."""

    def __init__(
        self,
        parent: Any,
        app: Any,
        log_name: str = "TemplateTab",
        *,
        allow_none: bool = False,
        width: int = 6,
    ) -> None:
        """Initializes the TemplateTab."""
        super().__init__(parent, app, log_name)
        self._width: int = width
        self._allow_none: bool = allow_none
        self._template_filter: Callable[[Dict[str, Any]], bool] = (
            lambda x: x["type"] != "interface"
        )

    def _create_widgets(self) -> None:
        """Creates the widgets for the TemplateTab."""
        filtered_templates = self._filter_templates(self.app.preset["configuration"])
        self._create_config_block(filtered_templates)
        self._actualize_values()

    def _create_config_block(self, filtered_templates: Dict[str, Any]) -> None:
        """Creates the configuration block with template selections."""
        self.create_block(
            "",
            {
                "templates": {
                    k: self._get_templates_by_type(v["type"])
                    for k, v in filtered_templates.items()
                }
            },
            width=self._width,
        )

    def _actualize_values(self) -> None:
        """Sets the initial values of the template selection widgets."""
        for k, v in self.app.preset["configuration"].items():
            if k in self.fields[""]["templates"]:
                self.fields[""]["templates"][k].set(v["name"])

    def update_config(self) -> None:
        """Updates the configuration with the selected templates."""
        for k, v in self.app.preset["configuration"].items():
            if k in self.fields[""]["templates"]:
                new_template_name = self.fields[""]["templates"][k].get().strip()
                valid_templates = self._get_templates_by_type(v["type"])
                if new_template_name not in valid_templates:
                    logger.error(f"Invalid template for {k}: {new_template_name}")
                    raise ValueError(f"Invalid template for {k}")

                template_info = (
                    {
                        "name": "None",
                        "id": -1,
                        "family": "all",
                        "type": "all",
                        "role": "common",
                        "text": "",
                    }
                    if new_template_name == "None"
                    else self.app.db_services["template"].get_info_one(
                        name=new_template_name,
                        role=["common", v["role"]],
                        family_id=int(self.app.device["family"]["id"]),
                    )
                )
                self.app.preset["configuration"][k] = template_info

    def _get_templates_by_type(self, template_type: str) -> Tuple[str, ...]:
        """Retrieves templates of a specific type."""
        templates = self.app.db_services["template"].get_all(
            family_id=self.app.device["family"]["id"],
            role=[get_env("DEV_ROLE"), "common"],
        )
        tail = ("None",) if self._allow_none else ()
        return (
            tuple(entity.name for entity in templates if entity.type == template_type)
            + tail
        )

    def _filter_templates(self, templates: Dict[str, Any]) -> Dict[str, Any]:
        """Filters templates based on the defined criteria."""
        return {k: v for k, v in templates.items() if self._template_filter(v)}
