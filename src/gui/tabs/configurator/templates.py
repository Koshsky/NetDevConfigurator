import os

from gui import BaseTab, apply_error_handler


@apply_error_handler
class TemplateTab(BaseTab):
    """Manages configuration templates.

    This tab allows users to select and apply configuration templates
    for different device settings.
    """

    def __init__(
        self, parent, app, log_name="TemplateTab", *, allow_none=False, width=6
    ):
        """Initializes the TemplateTab.

        Args:
            parent: The parent widget.
            app: The main application instance.
            log_name: The name for the logger.
            allow_none: Whether to allow "None" as a template option.
            width: The width of the template selection widgets.
        """
        super().__init__(parent, app, log_name)
        self._width = width
        self._allow_none = allow_none
        self._template_filter = lambda x: x["type"] != "interface"

    def _create_widgets(self):
        """Creates the widgets for the TemplateTab."""
        filtered_templates = self._filter_templates(self.app.preset["configuration"])
        self._create_config_block(filtered_templates)
        self._actualize_values()

    def _create_config_block(self, filtered_templates):
        """Creates the configuration block with template selections.

        Args:
            filtered_templates: A dictionary of filtered templates.
        """
        self.create_block(
            "config",
            {
                "templates": {
                    k: self._get_templates_by_type(v["type"])
                    for k, v in filtered_templates.items()
                }
            },
            width=self._width,
        )

    def _actualize_values(self):
        """Sets the initial values of the template selection widgets."""
        for k, v in self.app.preset["configuration"].items():
            if k in self.fields["config"]["templates"]:
                self.fields["config"]["templates"][k].set(v["name"])

    def update_config(self):
        """Updates the configuration with the selected templates."""
        for k, v in self.app.preset["configuration"].items():
            if k in self.fields["config"]["templates"]:
                new_template_name = self.fields["config"]["templates"][k].get().strip()
                if new_template_name not in self._get_templates_by_type(v["type"]):
                    raise ValueError(f"Invalid template for {k}")
                if new_template_name == "None":
                    template_info = {
                        "name": "None",
                        "id": -1,
                        "family": "all",
                        "type": "all",
                        "role": "common",
                        "text": "",
                    }
                else:
                    template_info = self.app.db_services["template"].get_info_one(
                        name=new_template_name,
                        role=["common", v["role"]],
                        family_id=int(self.app.device["family"]["id"]),
                    )
                self.app.preset["configuration"][k] = template_info

    def _get_templates_by_type(self, t):
        """Retrieves templates of a specific type.

        Args:
            t: The template type.

        Returns:
            A tuple of template names.
        """
        templates = self.app.db_services["template"].get_all(
            family_id=self.app.device["family"]["id"],
            role=[os.environ["DEV_ROLE"], "common"],
        )
        tail = ("None",) if self._allow_none else ()
        return tuple(entity.name for entity in templates if entity.type == t) + tail

    def _filter_templates(self, templates):
        """Filters templates based on the defined criteria.

        Args:
            templates: A dictionary of templates.

        Returns:
            A dictionary of filtered templates.
        """
        return {k: v for k, v in templates.items() if self._template_filter(v)}
