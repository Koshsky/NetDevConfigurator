from internal.db_app.base_tab import BaseTab
from typing import Dict, List

from tkinter import ttk


class TemplateTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
    def create_widgets(self):
        self.create_block("header", {"type": ["header1", "header2", "header3"]})
        self.create_block("footer", {"type": ["footer1", "footer2", "footer3"]})
        self.create_grid_combobox(10, "PORTS", get_port_map(num_of_gigabit=16, num_of_10gigabit=4))
        self.create_button_in_line(("GENERATE", self.mock_method))
        self.create_feedback_area()
        
    def mock_method(self):
        pass

def get_port_map(num_of_gigabit: int, num_of_10gigabit: int) -> Dict[str, List[str]]:
    port_map = dict()
    for i in range(num_of_gigabit):
        port_map[f"gigabitethernet 0/{i}"] = ["role1", "role2", "role3"]
    for i in range(num_of_10gigabit):
        port_map[f"tengigabitethernet 0/{i}"] = ["role1", "role2", "role3"]
    return port_map
