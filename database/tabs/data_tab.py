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
        self.create_button_in_line("Companies", self.load_companies)
        self.create_button_in_line("Devices", self.load_devices)
        self.create_button_in_line("Firmwares", self.load_firmwares)
        self.create_feedback_area()

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
        
        column_names = [column.name.ljust(15) for column in rows[0].__table__.columns]
        table = "".join(column_names)  # headers
        for row in rows:
            table += '\n'
            for column in column_names:
                column = column.strip()
                if column == "dev_type":
                    val = "router" if getattr(row, column) == 1 else "switch"
                elif column == "primary_conf":
                    val = ['COM port + SSH', 'SSH', 'COM port + SNMP'][getattr(row, column) - 1]
                elif column == "company_id":
                    company = self.app.company_service.get_by_id(getattr(row, column))
                    val = company.name if company else "Unknown Company"
                else:
                    val = str(getattr(row, column))

                table += val.ljust(15)
        return table
