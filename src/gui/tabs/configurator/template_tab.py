from internal.db_app import BaseTab
import pprint
from tkinter import ttk


class TemplateTab(BaseTab):
    def __init__(self, parent, app, templates, *, width=6):
        self.templates = templates
        self.width = width
        super().__init__( parent, app)

    def create_widgets(self):
        self.create_label(
            f"DEVICE:\t{self.app.params['DEVICE']}\n"
            f"CERT:\t{self.app.params['CERT']}\n"
            f"ROLE:\t{self.app.params['ROLE']}\n"
            f"OR:\t{self.app.params['OR']}"
        )
        self.create_block("config", {
            "templates": {k: self._get_templates_by_type(v['type']) for k, v in self.templates.items()}
        }, width=self.width)
        self.create_button_in_line(("UPDATE", self.update_config))
        self.create_button_in_line(("ACTUALIZE", self.actualize_values))
        self.create_feedback_area()

    def actualize_values(self):
        for k, v in self.templates.items():
            self.fields['config']['templates'][k].set(v['name'])

    def update_config(self):
        for k, v in self.templates.items():
            actual_name = self.fields['config']['templates'][k].get().strip()
            if actual_name not in self._get_templates_by_type(v['type']):
                raise ValueError(f"Invalid template for {k}")
            actual_template = self.app.db_services['template'].get_by_name_and_role(actual_name, v['role'])
            actual = self.app.db_services['template'].get_info(actual_template)
            self.app._config[k] = actual
            self.templates[k] = actual
        self.display_feedback(pprint.pformat(
            self.app._config, sort_dicts=False
        ))

    def _get_templates_by_type(self, t):
        entities = self.app.db_services['template'].get_by_family_id_and_role(self.app._device.family_id, self.app._preset.role)
        return tuple(entity.name for entity in entities if entity.type == t)
