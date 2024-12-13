from internal.db_app.base_tab import BaseTab

class TablesTab(BaseTab):
    def create_widgets(self):
        self.create_button_in_line(("Companies", lambda : self.load_table('company')))
        self.create_button_in_line(("Families", lambda : self.load_table('family')))
        self.create_button_in_line(("Devices", lambda : self.load_table('device')))
        self.create_button_in_line(("Firmwares", lambda : self.load_table('firmware')))
        self.create_button_in_line(("Protocols", lambda : self.load_table('protocol')))
        self.create_button_in_line(("Template pieces", lambda : self.load_table('template_piece')))
        self.create_feedback_area()

    def load_table(self, service_name: str):
        try:
            rows = self.app.entity_services[service_name].get_all()
            self.display_feedback(self.format_table(rows))
        except ValueError as e:  # TODO: НАПИСАТЬ ДЕКОРАТОРА В БАЗОВОМ КЛАССЕ И ИСПОЛЬЗОВАТЬ НА МЕТОДАХ РАБОТАЮЩИХ С БД!!!
            self.show_error("Retrieval Error", e)
        except IntegrityError as e:
            self.show_error("Integrity Error", e)
            self.app.session.rollback()

    def format_table(self, rows):
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
