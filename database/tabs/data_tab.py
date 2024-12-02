import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import Session

from database.services.company_service import CompanyService
from database.services.device_service import DeviceService
from database.services.firmware_service import FirmwareService
from .base_tab import BaseTab

class DataTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app, "")

    def create_widgets(self):
        cur_row = 0
        cur_row = self.create_button_in_line(cur_row, "Companies", self.load_companies)
        cur_row = self.create_button_in_line(cur_row, "Devices", self.load_devices)
        cur_row = self.create_button_in_line(cur_row, "Firmwares", self.load_firmwares)
        self.create_feedback_area(cur_row)

    def load_companies(self):
        if self.app.session is None:
            self.display_feedback("Error: No connection to the database.")
            return

        try:
            rows = self.app.company_service.get_all()
            self.display_feedback(self.format_table(rows))
        except Exception as e:
            self.display_feedback(f"Error loading data: {e}")

    def load_firmwares(self):
        if self.app.session is None:
            self.display_feedback("Error: No connection to the database.")
            return

        try:
            rows = self.app.firmware_service.get_all()
            self.display_feedback(self.format_table(rows))
        except Exception as e:
            self.display_feedback(f"Error loading data: {e}")

    def load_devices(self):
        if self.app.session is None:
            self.display_feedback("Error: No connection to the database.")
            return

        try:
            rows = self.app.device_service.get_all()
            self.display_feedback(self.format_table(rows))
        except Exception as e:
            self.display_feedback(f"Error loading data: {e}")

    def format_table(self, rows):
        if not rows:
            return "No data found."
        
        column_names = [column.name for column in rows[0].__table__.columns]
        table = "\t".join(column_names)  # headers
        for row in rows:
            row_data = [str(getattr(row, column)) for column in column_names]
            table += "\n" + "\t".join(row_data)
        return table
            