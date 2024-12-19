from internal.db_app import BaseTab, error_handler
import pprint


class CommonConfigTab(BaseTab):
    def __init__(self, app, parent):
        self.template_names = ["1", "2"]
        self.role = "common"
        self.device = None
        self.preset = ''

        super().__init__(app, parent)

    @property
    def message_prefix(self):
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
                "template_name": self.template_names,
                "ordered_number": None,

        }, width=12)
        self.create_button_in_line(("PUSH BACK", self.push_back))
        self.create_button_in_line(("INSERT", self.insert))
        self.create_feedback_area()

    @error_handler
    def push_back(self):
        template = self.check_template_name(self.fields['config']['template_name'].get())
        self.app.entity_services['device_template'].push_back(self.device.id, template.id, self.preset)
        self.display_feedback(f'{self.message_prefix}\nTemplate {template.name} pushed back to device {self.device.name}')

    @error_handler
    def insert(self):
        template = self.check_template_name(self.fields['config']['template_name'].get())
        ordered_number = self.fields['config']['ordered_number'].get().strip()
        if not ordered_number.isdigit() or int(ordered_number) < 1:
            raise ValueError("ordered_number must be digit greater than 0")
        self.app.entity_services['device_template'].insert(self.device.id, template.id, int(ordered_number), self.preset)
        self.display_feedback(f'{self.message_prefix}\nTemplate {template.name} inserted to device {self.device.name} at position {ordered_number}')

    @error_handler
    def refresh(self):
        device = self.check_device_name(self.fields['setup']['device_name'].get())
        family_id = self.app.entity_services['device'].get_info(device.id)['family']['id']
        role = self.fields['setup']['device_role'].get().strip()
        if not role:
            raise ValueError("Device_role cannot be empty")
        elif role not in self.app.entity_collections['roles']:
            raise ValueError(f"Unknown role: {role}")

        template_names = [template.name for template in self.app.entity_services['template'].get_all_by_role_family_id(family_id, role)]
        if not template_names:
            raise ValueError(f"There is no templates for role: {role}")
        self.template_names = template_names
        self.fields['config']['template_name']['values'] = self.template_names

        self.device = device
        self.role = role
        self.preset = self.fields['setup']['preset'].get().strip()
        self.fields['config']['template_name'].set(self.template_names[0])
        self.display_feedback(f'{self.message_prefix}\nrefreshed')
