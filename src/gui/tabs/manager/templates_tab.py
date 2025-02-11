import tkinter as tk
from pprint import pformat

from database.services.exceptions import EntityNotFoundError
from gui import BaseTab, apply_error_handler


@apply_error_handler
class TemplatesTab(BaseTab):
    def _render_widgets(self):
        self.create_block(
            "template",
            {
                "name": self.app.entity_collections["template"],
                "role": self.app.entity_collections["role"] + ("common",),
            },
        )
        self.create_large_input_field("text")
        self.create_button_in_line(("SHOW", self.show_template))
        self.create_button_in_line(("UPDATE", self.update_template))
        self.create_feedback_area()

    def show_template(self):
        name = self.fields["template"]["name"].get().strip()
        try:
            template = self.app.db_services["template"].get_by_name(name)
        except EntityNotFoundError:
            role = self.fields["template"]["role"].get().strip()
            template = self.app.db_services["template"].get_by_name_and_role(name, role)
        template_info = self.app.db_services["template"].get_info(template)

        self.display_feedback(pformat(template_info))
        self.fields["text"].delete(1.0, tk.END)
        self.fields["text"].insert(tk.END, template_info["text"])

    def update_template(self):
        name = self.fields["template"]["name"].get().strip()
        try:
            template = self.app.db_services["template"].get_by_name(name)
        except EntityNotFoundError:
            role = self.fields["template"]["role"].get().strip()
            template = self.app.db_services["template"].get_by_name_and_role(name, role)

        text = self.fields["text"].get("1.0", tk.END).strip()
        template = self.app.db_services["template"].update(template, {"text": text})
        self.display_feedback(
            pformat(self.app.db_services["template"].get_info(template))
        )
