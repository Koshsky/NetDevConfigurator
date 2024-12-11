from internal.db_app.base_tab import BaseTab
from typing import Dict, List


class DeviceTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
    def create_widgets(self):
        self.create_block("device", {"name": list(self.app.devices)})
        self.create_button_in_line(("UPDATE TABS", self.update_tabs))
        self.create_feedback_area()

    def update_tabs(self):
        try:
            self.app.device = self.check_device_name(self.fields["device"]["name"].get())
            for tab in self.app.tabs[1:]:
                tab.clear_frame()
                tab.create_widgets()
            self.display_feedback(f'device {self.app.device.name} registered.\n')
        except Exception as e:
            self.display_feedback(f"An error: {e}")
        
    def generate_template(self):
        self.app.num_of_gigabit = 1
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
