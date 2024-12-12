from internal.db_app.base_tab import BaseTab
from typing import Dict, List

from tkinter import ttk


class TemplateTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
    def create_widgets(self):
        if self.app.device is None:
            self.create_feedback_area()
            self.display_feedback("Please, choose a device in DeviceTab.")
            return
        self.create_block("template", {
                "header": ["header1", "header2", "header3"],
                "footer": ["footer1", "footer2", "footer3"],
                "interfaces": get_port_map()
        }, width=10)
        self.create_button_in_line(("GENERATE", self.generate_template))
        self.create_feedback_area()
        
    def generate_template(self):
        header_name = self.fields["header"]["name"].get().strip()  # TODO: обновить базу данных, а тут получать ее объект а не просто имя.
        footer_name = self.fields["header"]["name"].get().strip()  # если объекта не существует в базе данных, обрабатывать этот случай с выводом ошибки в дисплей
        for port_name, combobox in self.fields["PORTS"].items():
            port_template_name = combobox.get().strip()  # TODO: аналогично как с хедером и футером

        # TODO: реализовать сборку шаблона в байтовом или строковом виде
        # TODO: записать шаблон в файл в паппке /tmp/...
        # TODO: напечатать шаблон в feedback_area: self.display_feedback(template)


def get_port_map():
    return {        
        f"gigabitethernet 0/{i}": ["role1", "role2", "role3"]
        for i in range(25)
    }
