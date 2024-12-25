from gui import BaseTab, error_handler


class ViewTab(BaseTab):
    def create_widgets(self):
        self.create_button_in_line(("SHOW TEMPLATE", self.show_template))
        self.create_feedback_area()

    def show_template(self):
        template = self._get_template()
        self.display_feedback(template)

    def _get_template(self):
        template = ''
        for k, v in self.app._config.items():
            if v['text']:
                template += v['text'].replace('{INTERFACE_ID}', k) + '\n'  # TODO: возможно перенос строки '\r\n'
        template = template.replace('{CERT}', self.app.params['CERT'])
        template = template.replace('{OR}', self.app.params['OR'])
        template = template.replace('{MODEL}', self.app.params['MODEL'])
        template = template.replace('{ROLE}', self.app.params['ROLE'])
        return template + 'end'