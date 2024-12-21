from internal.db_app import BaseTab, error_handler
import pprint
from functools import wraps

def show_config(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        message =  func(self, *args, **kwargs)
        self._config = self.app.entity_services['device_template'].get_device_configuration(self.device.id, self.preset)
        self.display_feedback(f'{message}{self.information}\n{self.config}')
        return message
    return wrapper

class CommonConfigTab(BaseTab):
    def __init__(self, app, parent):
        self.role = "common"
        self.device = None
        self.preset = ''
        self._config = None

        super().__init__(app, parent)

    @property
    def config(self):
        return '\r\n'.join(entity['template']['text'] for entity in self._config) + '\r\nend\n'

    @property
    def information(self):
        return (
            f"device_name: {self.device.name}\n"
            f"role: {self.role}\n"
            f"preset: {self.preset}\n"
        )

    def create_widgets(self):
        self.create_block("setup", {
            "device_name": list(self.app.entity_collections['devices']),
            "device_role": list(self.app.entity_collections['roles']),
            "preset": None,
        })
        self.create_button_in_line(("REFRESH", self.refresh))
        self.create_block("config", {
                "template_name": ["1", "2'"],
                "ordered_number": None,

        }, width=12)
        self.create_button_in_line(("PUSH BACK", self.push_back))
        self.create_button_in_line(("INSERT", self.insert))
        self.create_button_in_line(("REMOVE", self.remove))
        self.create_feedback_area()

    @show_config
    @error_handler
    def remove(self) -> str:
        ordered_number = self.fields['config']['ordered_number'].get().strip()
        self.app.entity_services['device_template'].remove(self.preset, int(ordered_number))
        return ""

    @show_config
    @error_handler
    def push_back(self) -> str:
        template = self.check_template_name(self.fields['config']['template_name'].get())
        self.app.entity_services['device_template'].push_back(self.device.id, template.id, self.preset)
        return f'Template {template.name} succesfully pushed back\n'

    @show_config
    @error_handler
    def insert(self) -> str:
        template = self.check_template_name(self.fields['config']['template_name'].get())
        ordered_number = self.fields['config']['ordered_number'].get().strip()
        if not ordered_number.isdigit() or int(ordered_number) < 1:
            raise ValueError("ordered_number must be digit greater than 0")
        self.app.entity_services['device_template'].insert(self.device.id, template.id, int(ordered_number), self.preset)
        return f'Template {template.name} successfully inserted at position {ordered_number}\n'

    @show_config
    @error_handler
    def refresh(self):
        device = self.check_device_name(self.fields['setup']['device_name'].get())
        family_id = self.app.entity_services['device'].get_info_by_id(device.id)['family']['id']
        role = self.fields['setup']['device_role'].get().strip()
        if not role:
            raise ValueError("Device_role cannot be empty")
        elif role not in self.app.entity_collections['roles']:
            raise ValueError(f"Unknown role: {role}")

        template_names = self.app.entity_services['template'].list_templates_by_role_and_family(family_id, role)
        template_names.extend(self.app.entity_services['template'].list_interface_templates(family_id, role))
        if not template_names:
            raise ValueError(f"There is no templates for role: {role}")
        self.fields['config']['template_name']['values'] = template_names

        self.device = device
        self.role = role
        self.preset = self.fields['setup']['preset'].get().strip()
        self.fields['config']['template_name'].set(template_names[0])
        return ''
