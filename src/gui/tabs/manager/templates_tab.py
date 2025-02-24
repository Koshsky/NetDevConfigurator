import tkinter as tk
from pprint import pformat

from gui import BaseTab, apply_error_handler


@apply_error_handler
class TemplatesTab(BaseTab):
    def _create_widgets(self):
        self.create_block(
            "template",
            {
                "name": self.app.entity_collections["template"],
                "family": self.app.entity_collections["family"],
                "type": self.app.entity_collections["template_type"],
                "role": self.app.entity_collections["role"] + ("common",),
            },
        )
        self.create_large_input_field("text")
        self.create_button_in_line(("SHOW", self.show_template))
        self.create_button_in_line(("UPDATE", self.update_template))
        self.create_button_in_line(("CREATE", self.create_template))
        self.create_button_in_line(("DELETE", self.delete_template))
        self.create_feedback_area()

    @property
    def selected_template(self):
        # TODO: здесь можно добавить какой-нибудь валидации данных
        family = self.app.db_services["family"].get_one(
            name=self.fields["template"]["family"].get().strip()
        )
        return {
            "name": self.fields["template"]["name"].get().strip(),
            "family_id": family.id,
            "role": self.fields["template"]["role"].get().strip(),
        }

    def delete_template(self):
        self.app.db_services["template"].delete_one(**self.selected_template)
        self.display_feedback("Successfully deleted from the templates table.")

    def create_template(self):
        self.app.db_services["template"].create(
            **self.selected_template,
            type=self.fields["template"]["type"].get().strip(),
            text=self.fields["text"].get("1.0", tk.END).strip(),
        )
        self.show_template()

    def update_template(self):
        template = self.app.db_services["template"].get_one(**self.selected_template)

        template = self.app.db_services["template"].update(
            template,
            text=self.fields["text"].get("1.0", tk.END).strip(),
        )
        self.show_template()

    def show_template(self):
        template_info = self.app.db_services["template"].get_info_one(
            **self.selected_template,
        )

        self.display_feedback(pformat(template_info))
        self.fields["text"].delete(1.0, tk.END)
        self.fields["text"].insert(tk.END, template_info["text"])
