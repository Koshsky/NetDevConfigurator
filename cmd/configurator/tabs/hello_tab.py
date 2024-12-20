from internal.db_app import BaseTab
from internal.db_app import error_handler

class HelloTab(BaseTab):
    def create_widgets(self):
        self.create_block("params", {
            "CERT": None,
            "DEVICE": list(self.app.entity_collections['devices']),
            "ROLE": list(self.app.entity_collections['roles']),
            "OR": None,
        })
        self.create_block('preset', {'name': ["common", "common2"]}, ("UPDATE", self.update_preset_list))
        self.create_button_in_line(("REGISTER DEVICE", self.register_device))
        self.create_feedback_area()

    def update_preset_list(self):
        DEVICE = self.fields['params']['DEVICE'].get().strip()
        device_id = self.app.entity_services['device'].get_info_by_name(DEVICE)['id']
        ROLE = self.fields['params']['ROLE'].get().strip()
        if ROLE not in self.app.entity_collections['roles']:
            raise ValueError("Unknown ROLE")
        self.app.presets = self.app.entity_services['device_template'].get_presets(
                device_id,
                self.app.ROLE,
        )
        self.fields['preset']['name']['values'] = self.app.presets
        self.fields['preset']['name'].set(self.app.presets[0])
    @error_handler  
    def register_device(self):
        OR = self.fields['params']['OR'].get().strip()
        CERT = self.fields['params']['CERT'].get().strip()
        DEVICE = self.fields['params']['DEVICE'].get().strip()
        ROLE = self.fields['params']['ROLE'].get().strip()
        if not CERT or not CERT.isalpha():
            raise ValueError("CERT name cannot be empty and must be .isalpha()")
        if not OR or not OR.isdigit() or not (0 < int(OR) < 256):
            raise ValueError("Operation room number must be between 1 and 255")
        if ROLE not in self.app.entity_collections['roles']:
            raise ValueError(f"Unknown role: {ROLE}")
        

        self.app.device_info = self.app.entity_services['device'].get_info_by_name(self.fields['params']['DEVICE'].get().strip())
        self.app.ROLE = ROLE
        self.app.OR = OR
        self.app.CERT = CERT
        self.app.templates = self.app.entity_services['template'].list_templates_by_role_and_family(
            self.fields['params']['ROLE'].get().strip(),
            self.app.device_info['family']['id']
        )
        self.app.interface_templates = self.app.entity_services['template'].list_interface_templates(
            self.fields['params']['ROLE'].get().strip(),
            self.app.device_info['family']['id']
        )

        self.app.presets = self.app.entity_services['device_template'].get_presets(
            self.app.device_info['id'],
            self.app.ROLE,
        )
        self.fields['preset']['name'].set(self.app.presets)
        self.fields['preset']['name'].refresh
        self.display_feedback(f'device {self.app.device_info['name']} registered.\nNOW SELECT PRESET')
        
    def get_preset_names(self):
        print("GET PRESET NAMES")
    @error_handler
    def update_tabs(self):
        if self.app.device_info is None:
            raise RuntimeError("choose CERT, DEVICE, ROLE, OR")
        self.app.common_configuration = self.app.entity_services['device_template'].get_device_configuration(
            self.app.device_info['id'],
            self.fields['preset']['name'].get().strip()
        )
        for tab in self.app.tabs[1:]:
            tab.clear_frame()
            tab.create_widgets()
        self.display_feedback(f'device {self.app.device_info['name']} registered.\nNOW SELECT PRESET')
