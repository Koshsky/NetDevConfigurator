from gui import BaseTab, apply_error_handler
from functools import wraps


def prepare_config_file(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.app._config is None:
            raise Exception("Config file is not loaded")
        if self.app._path is None:
            raise Exception("Path is not set")

        template = self._get_text_configuration()
        with open(self.app._path, 'w') as f:
            f.write(template)
        self.display_feedback(f'Template saved: {self.app._path}')

        return func(self, *args, **kwargs)
    return wrapper

@apply_error_handler
class ViewTab(BaseTab):
    def create_widgets(self):
        self.create_button_in_line(("SHOW TEMPLATE", self.show_template))

        protocols = [protocol['name'] for protocol in self.app.db_services['device'].get_info(self.app._device)['protocols']]
        if 'COM' in protocols:
            self.create_button_in_line(("LOAD BY COM", self.load_by_COM))
        if 'ssh' in protocols:
            self.create_button_in_line(("LOAD BY SSH", self.load_by_ssh))
        if 'http' in protocols:
            self.create_button_in_line(("LOAD BY HTTP", self.load_by_http))
        if 'SNMP' in protocols:
            self.create_button_in_line(("LOAD BY SNMP", self.load_by_snmp))
        self.create_button_in_line(("UPDATE FIRMWARES", self.update_firmwares))
        self.create_feedback_area()

    @prepare_config_file
    def load_by_ssh(self):
        pass

    @prepare_config_file
    def load_by_http(self):
        pass

    @prepare_config_file
    def load_by_COM(self):
        pass

    @prepare_config_file
    def load_by_snmp(self):
        pass

    def update_firmwares(self):
        firmwares = self.app.db_services['device'].get_info(self.app._device)['firmwares']
        for firmware in firmwares:
            path = firmware['full_path']
            if not os.path.exists(path):
                raise Exception(f"File {path} not found")
        # TODO: какая логика дальше?

    def show_template(self):
        template = self._get_text_configuration()
        self.display_feedback(template)

    def _get_text_configuration(self):
        template = ''
        for k, v in self.app._config.items():
            if v['text']:
                template += v['text'].replace('{INTERFACE_ID}', k) + '\n'  # TODO: возможно перенос строки '\r\n'
        template = template.replace('{CERT}', self.app.params['CERT'])
        template = template.replace('{OR}', self.app.params['OR'])
        template = template.replace('{MODEL}', self.app.params['MODEL'])
        template = template.replace('{ROLE}', self.app.params['ROLE'])
        return template + 'end\n'
