from internal.db_app import BaseTab, error_handler
import pprint
from functools import wraps

def update_config(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        message = func(self, *args, **kwargs)
        self._config = self.app.entity_services['preset'].get_info_by_name(self.preset.name)
        print(1)
        self.display_feedback(f'{message or ""}\n{self.config_meta}\n\n{self.config_template}')
        return message
    return wrapper

def preset_is_not_none(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.preset is None:
            raise ValueError('No preset selected')
        return func(self, *args, **kwargs)
    return wrapper

class CommonConfigTab(BaseTab):
    def __init__(self, app, parent):
        self._config = None
        self.preset = None
        self.family_id = None
        super().__init__(app, parent)

    @property
    def config_meta(self):
        return f"Device: {self._config['device']}\nPreset: {self._config['preset']}\nRole: {self._config['role']}"
    @property
    def config_template(self):
        return '\r\n'.join(entity['template']['text'] for entity in self._config['configuration']) + '\r\nend\n'

    def create_widgets(self):
        self.create_block("preset", {
            "name": list(self.app.entity_collections['presets']),
        })
        self.create_button_in_line(("REFRESH", self.refresh))
        self.create_block("template", {
                "name": ["1", "2'"],
                "ordered_number": None,

        })
        self.create_button_in_line(("PUSH BACK", self.push_back))
        self.create_button_in_line(("INSERT", self.insert))
        self.create_button_in_line(("REMOVE", self.remove))
        self.create_feedback_area()

    @error_handler
    @update_config
    @preset_is_not_none
    def remove(self) -> str:
        ordered_number = self.fields['template']['ordered_number'].get().strip()
        if ordered_number and ordered_number.isdigit():
            self.app.entity_services['device_preset'].remove(self.preset.id, int(ordered_number))
        else:
            raise ValueError("Invalid ordered number")

    @error_handler
    @update_config
    @preset_is_not_none
    def push_back(self) -> str:
        template = self.check_template_name(self.fields['template']['name'].get())
        self.app.entity_services['device_preset'].push_back(self.preset.id, template.id)
        return f'Template {template.name} successfully pushed back\n'

    @error_handler
    @update_config
    @preset_is_not_none
    def insert(self) -> str:
        template = self.check_template_name(self.fields['template']['name'].get())
        ordered_number = self.fields['template']['ordered_number'].get().strip()
        if ordered_number and ordered_number.isdigit():
            self.app.entity_services['device_preset'].insert(self.preset.id, template.id, int(ordered_number))
        else:
            raise ValueError("Invalid ordered number")
        return f'Template {template.name} successfully inserted at position {ordered_number}\n'

    @error_handler
    @update_config
    def refresh(self):
        self.preset = self.check_preset_name(self.fields['preset']['name'].get())
        self.family_id = self.app.entity_services['device'].get_by_id(self.preset.device_id).family_id

        template_names = self.app.entity_services['template'].get_templates_by_family_and_role(self.family_id, self.preset.role)
        if not template_names:
            raise ValueError(f"There is no templates for role: {role}")
        self.fields['template']['name']['values'] = template_names
        self.fields['template']['name'].set(template_names[0])
