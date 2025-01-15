from gui import BaseTab, apply_error_handler


@apply_error_handler
class TablesTab(BaseTab):
    def create_widgets(self):
        for entity in [
            "company",
            "family",
            "device",
            "port",
            "protocol",
            "template",
            "preset",
        ]:
            self.create_button_in_line((entity.capitalize(), self.load_table(entity)))
        self.create_feedback_area()

    def load_table(self, entity):
        def wrapper():
            rows = self.app.db_services[entity].get_all()
            self.display_feedback(self.format_table(rows))

        return wrapper

    def format_table(self, rows):
        if not rows:
            return "No data found."

        rows = sorted(rows, key=lambda x: x.name)

        column_names = [column.name for column in rows[0].__table__.columns]
        table = "\t".join(column_names[:2])
        for row in rows:
            table += "\n"
            id_ = str(getattr(row, "id"))
            name = str(getattr(row, "name"))
            table += id_ + "\t" + name
        return table
