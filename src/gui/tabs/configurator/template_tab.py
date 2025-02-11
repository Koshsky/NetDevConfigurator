import os
from pprint import pformat

from gui import BaseTab, apply_error_handler


@apply_error_handler
class TemplateTab(BaseTab):
    def __init__(
        self,
        parent,
        app,
        log_name="TemplateTab",
        *,
        allow_none=False,
        width=6,
        template_filter=lambda x: True,
    ):
        super().__init__(parent, app, log_name)
        self.width = width
        self.allow_none = allow_none
        self.template_filter = template_filter

    def render_widgets(self):
        filtered_templates = {}
        for k, v in self.app.config_template.items():
            if self.template_filter(v):
                filtered_templates[k] = v
        self.create_block(
            "config",
            {
                "templates": {
                    k: self._get_templates_by_type(v["type"])
                    for k, v in filtered_templates.items()
                }
            },
            width=self.width,
        )
        self.actualize_values()
        self.create_button_in_line(("ACTUALIZE", self.actualize_values))
        self.create_button_in_line(("UPDATE", self.update_config))
        self.create_feedback_area()

    def actualize_values(self):
        for k, v in self.app.config_template.items():
            if k in self.fields["config"]["templates"]:
                self.fields["config"]["templates"][k].set(v["name"])

    def update_config(self):
        for k, v in self.app.config_template.items():
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
                    template = self.app.db_services["template"].get_by_name_and_role(
                        new_template_name, v["role"]
                    )
                    template_info = self.app.db_services["template"].get_info(template)
                self.app.config_template[k] = template_info
        self.display_feedback(pformat(self.app.config_template, sort_dicts=False))

    def _get_templates_by_type(self, t):
        entities = self.app.db_services["template"].get_by_family_id_and_role(
            self.app.device_info["family"]["id"],
            os.environ["DEV_ROLE"],
        )
        tail = ("None",) if self.allow_none else tuple()
        return tuple(entity.name for entity in entities if entity.type == t) + tail
