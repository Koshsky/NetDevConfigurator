from internal.db_app.base_tab import BaseTab
from typing import Dict, List

from tkinter import ttk
# TODO: сделать просмотр содержимого template_pieces из базы данных по их имени
# TODO: сделать возможным просмотр СПИСКА template_pieces из базы данных

class ViewTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
    def create_widgets(self):
        if self.app.device is None:
            self.create_feedback_area()
            self.display_feedback("Please, choose a device in DeviceTab.")
            return
        self.create_block("template", {"name": self.app.header_templates}, button=("VIEW", self.show_by_name))
        self.create_button_in_line(("VIEW ALL", self.show_all))
        self.create_feedback_area()
        
    def show_by_name(self):
        pass
    
    def show_all(self):
        pass
    
