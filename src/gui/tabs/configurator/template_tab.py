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
        self.templates = {}
        for k, v in self.app.config_template.items():
            if self.template_filter(v):
                self.templates[k] = v
        self.create_block(
            "config",
            {
                "templates": {
                    k: self._get_templates_by_type(v["type"])
                    for k, v in self.templates.items()
                }
            },
            width=self.width,
        )
        self.actualize_values()
        self.create_button_in_line(("UPDATE", self.update_config))
        self.create_button_in_line(("ACTUALIZE", self.actualize_values))
        self.create_feedback_area()

    def actualize_values(self):  # TODO: refactor (can I remove self.templates???)
        for k, v in self.templates.items():
            self.fields["config"]["templates"][k].set(v["name"])

    def update_config(self):  # TODO: refactor (can I remove self.templates???)
        for k, v in self.templates.items():
            actual_name = self.fields["config"]["templates"][k].get().strip()
            if actual_name not in self._get_templates_by_type(v["type"]):
                raise ValueError(f"Invalid template for {k}")
            if actual_name == "None":
                actual = {
                    "name": "None",
                    "id": -1,
                    "family": "all",
                    "type": "all",
                    "role": "common",
                    "text": "",
                }
            else:
                actual_template = self.app.db_services["template"].get_by_name_and_role(
                    actual_name, v["role"]
                )
                actual = self.app.db_services["template"].get_info(actual_template)
            self.app.config_template[k] = actual
            self.templates[k] = actual
        self.display_feedback(pformat(self.app.config_template, sort_dicts=False))

    def _get_templates_by_type(self, t):
        entities = self.app.db_services["template"].get_by_family_id_and_role(
            self.app.device.family_id,
            self.app.preset.role,
        )
        tail = ("None",) if self.allow_none else tuple()
        return tuple(entity.name for entity in entities if entity.type == t) + tail
