import os

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
        self._width = width
        self._allow_none = allow_none
        self._template_filter = template_filter

    def _create_widgets(self):
        filtered_templates = self._filter_templates(self.app.json_config)
        self._create_config_block(filtered_templates)
        self._actualize_values()

    def _create_config_block(self, filtered_templates):
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
        for k, v in self.app.json_config.items():
            if k in self.fields["config"]["templates"]:
                self.fields["config"]["templates"][k].set(v["name"])

    def update_config(self):
        for k, v in self.app.json_config.items():
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
                self.app.json_config[k] = template_info

    def _get_templates_by_type(self, t):
        templates = self.app.db_services["template"].get_all(
            family_id=self.app.device["family"]["id"],
            role=[os.environ["DEV_ROLE"], "common"],
        )
        tail = ("None",) if self._allow_none else tuple()
        return tuple(entity.name for entity in templates if entity.type == t) + tail

    def _filter_templates(self, templates):
        return {k: v for k, v in templates.items() if self._template_filter(v)}
