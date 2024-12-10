from internal.db_app.base_tab import BaseTab

class TablesTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)

    def create_widgets(self):
        self.create_button_in_line(("Companies", self.load_companies))
        self.create_button_in_line(("Devices", self.load_devices))
        self.create_button_in_line(("Firmwares", self.load_firmwares))
        self.create_button_in_line(("Protocols", self.load_protocols))
        self.create_feedback_area()

    def load_protocols(self):
        try:
            rows = self.app.protocol_service.get_all()
            self.display_feedback(self.format_table(rows))
        except Exception as e:
            self.display_feedback(f"Error loading data: {e}")
            self.app.session.rollback()

    def load_companies(self):
        try:
            rows = self.app.company_service.get_all()
            self.display_feedback(self.format_table(rows))
        except Exception as e:
            self.display_feedback(f"Error loading data: {e}")
            self.app.session.rollback()

    def load_firmwares(self):
        try:
            rows = self.app.firmware_service.get_all()
            self.display_feedback(self.format_table(rows))
        except Exception as e:
            self.display_feedback(f"Error loading data: {e}")
            self.app.session.rollback()

    def load_devices(self):
        try:
            rows = self.app.device_service.get_all()
            
            self.display_feedback(self.format_table(rows))
        except Exception as e:
            self.display_feedback(f"Error loading data: {e}")
            self.app.session.rollback()

    def format_table(self, rows):  # TODO: таблица прошивок плохо отображается, придумать другой вид (полные пути слишком длинные)
        if not rows:
            return "No data found."

        rows = sorted(rows, key=lambda x: x.name)
        
        column_names = [column.name.ljust(5) for column in rows[0].__table__.columns]
        table = "".join(column_names[:2])  # id and name
        for row in rows:
            table += '\n'
            id_ = str(getattr(row, "id"))
            name = str(getattr(row, "name"))
            table += id_.ljust(5) + name
        return table
