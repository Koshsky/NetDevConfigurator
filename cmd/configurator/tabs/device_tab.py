from internal.db_app.base_tab import BaseTab
from typing import Dict, List

from tkinter import ttk


class DeviceTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
    def create_widgets(self):
        self.create_block("Device", {"name": ["header1", "header2", "header3"]})
        self.create_grid_combobox(10, "PORTS", get_port_map(num_of_gigabit=16, num_of_10gigabit=4))  # откуда брать количество портов?
        self.create_button_in_line(("UPDATE TABS", self.generate_template))
        self.create_feedback_area()
        
    def generate_template(self):
        self.app.num_of_gigabit = 
        header_name = self.fields["header"]["name"].get().strip()  # TODO: обновить базу данных, а тут получать ее объект а не просто имя.
        footer_name = self.fields["header"]["name"].get().strip()  # если объекта не существует в базе данных, обрабатывать этот случай с выводом ошибки в дисплей
        for port_name, combobox in self.fields["PORTS"].items():
            port_template_name = combobox.get().strip()  # TODO: аналогично как с хедером и футером

        # TODO: реализовать сборку шаблона в байтовом или строковом виде
        # TODO: записать шаблон в файл в паппке /tmp/...
        # TODO: напечатать шаблон в feedback_area: self.display_feedback(template)


def get_port_map(num_of_gigabit: int, num_of_10gigabit: int) -> Dict[str, List[str]]:
    port_map = {        
        f"gigabitethernet 0/{i}": ["role1", "role2", "role3"]
        for i in range(num_of_gigabit)
    }
    for i in range(num_of_10gigabit):
        port_map[f"tengigabitethernet 0/{i}"] = ["role1", "role2", "role3"]
    return port_map
