import logging
import tkinter as tk
from pprint import pformat
from typing import TYPE_CHECKING, Any, Dict

from database.services import allowed_roles, allowed_types
from gui import BaseTab, apply_error_handler

if TYPE_CHECKING:
    from database.models import Templates

logger = logging.getLogger(__name__)


@apply_error_handler
class TemplateTab(BaseTab):
    """Tab for managing templates, including creating, updating, displaying, and deleting."""

    def _create_widgets(self) -> None:
        """Creates the widgets for the tab."""
        logger.debug("Creating widgets for TemplateTab")
        self.create_block(
            "template",
            {
                "name": tuple(
                    t.name for t in self.app.db_services["template"].get_all()
                ),
                "family": tuple(
                    f.name for f in self.app.db_services["family"].get_all()
                ),
                "type": allowed_types,
                "role": allowed_roles + ("common",),
            },
        )
        self.create_large_input_field("text")
        self.create_button_in_line(("SHOW", self.show_template))
        self.create_button_in_line(("UPDATE", self.update_template))
        self.create_button_in_line(("CREATE", self.create_template))
        self.create_button_in_line(("DELETE", self.delete_template))
        self.create_feedback_area()

    @property
    def selected_template(self) -> Dict[str, Any]:
        """Returns a dictionary containing the selected template's attributes."""
        logger.debug("Getting selected template")
        family_name: str = self.fields["template"]["family"].get().strip()
        family = self.app.db_services["family"].get_one(name=family_name)
        template_data: Dict[str, Any] = {
            "name": self.fields["template"]["name"].get().strip(),
            "family_id": family.id,
            "role": self.fields["template"]["role"].get().strip(),
        }
        logger.debug("Selected template: %s", template_data)
        return template_data

    def delete_template(self) -> None:
        """Deletes the selected template from the database."""
        logger.info("Deleting template")
        self.app.db_services["template"].delete_one(**self.selected_template)
        logger.debug("Template deleted successfully")
        self.display_feedback("Successfully deleted from the templates table.")

    def create_template(self) -> None:
        """Creates a new template in the database."""
        logger.info("Creating template")
        template_type = self.fields["template"]["type"].get().strip()
        text = self.fields["text"].get("1.0", tk.END).strip()
        self.app.db_services["template"].create(
            **self.selected_template, type=template_type, text=text
        )
        logger.debug("Template created successfully")
        self.show_template()

    def update_template(self) -> None:
        """Updates an existing template in the database."""
        logger.info("Updating template")
        template: "Templates" = self.app.db_services["template"].get_one(
            **self.selected_template
        )
        text = self.fields["text"].get("1.0", tk.END).strip()
        self.app.db_services["template"].update(template, text=text)
        logger.debug("Template updated successfully")
        self.show_template()

    def show_template(self) -> None:
        """Displays the selected template's information in the feedback area."""
        logger.info("Showing template information")
        template_info: Dict[str, Any] = self.app.db_services["template"].get_info_one(
            **self.selected_template,
        )

        self.display_feedback(pformat(template_info))
        self.fields["text"].delete(1.0, tk.END)
        self.fields["text"].insert(tk.END, template_info["text"])
        logger.debug("Template information displayed successfully")
