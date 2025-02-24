from functools import wraps
from gui import BaseTab, apply_error_handler


def update_config(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        message = func(self, *args, **kwargs)
        self.preset_info = self.app.db_services["preset"].get_info(self.preset)
        self.display_feedback(
            f"{message or ''}\n{self.config_meta()}\n\n{self.config_template}"
        )
        return message

    return wrapper


def preset_is_not_none(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.preset is None:
            raise ValueError("No preset selected")
        return func(self, *args, **kwargs)

    return wrapper


@apply_error_handler
class CommonConfigTab(BaseTab):
    def __init__(self, app, parent, log_name="ConfigTab"):
        super().__init__(app, parent, log_name)
        self.preset_info = None

    def _create_widgets(self):
        self.create_block(
            "preset",
            {
                "device": self.app.entity_collections["device"],
                "role": self.app.entity_collections["role"],
            },
        )
        self.create_button_in_line(("CREATE", self.create_preset))
        self.create_button_in_line(("DELETE", self.delete_preset))
        self.create_button_in_line(("REFRESH TEMPLATES", self.refresh_templates))
        self.create_block(
            "template",
            {
                "name": ("1", "2"),
                "ordered_number": None,
            },
        )
        self.create_button_in_line(("PUSH BACK", self.push_back))
        self.create_button_in_line(("INSERT", self.insert))
        self.create_button_in_line(("REMOVE", self.remove))
        self.create_button_in_line(("PREVIEW", self.preview))
        self.create_feedback_area()

    def create_preset(self):
        self.app.db_services["preset"].create(
            role=self.fields["preset"]["role"].get().strip(),
            device_id=self.selected_device.id,
        )

    def delete_preset(self):
        self.app.db_services["preset"].delete(self.selected_preset)

    @property
    def selected_device(self):
        return self.app.db_services["device"].get_one(
            name=self.fields["preset"]["device"].get().strip(),
        )

    @property
    def selected_preset(self):
        return self.app.db_services["preset"].get_one(
            device_id=self.selected_device.id,
            role=self.fields["preset"]["role"].get().strip(),
        )

    @property
    def relevant_templates(self):
        return self.app.db_services["template"].get_all(
            family_id=self.selected_device.family_id,
            role=["common", self.selected_preset.role],
        )

    @update_config
    @preset_is_not_none
    def remove(self) -> str:
        ordered_number = self.fields["template"]["ordered_number"].get().strip()
        if ordered_number and ordered_number.isdigit():
            preset = self.app.db_services["preset"].get_one(self.selected_preset)
            self.app.db_services["preset"].remove(preset.id, int(ordered_number))
        else:
            raise ValueError("Invalid ordered number")

    @update_config
    @preset_is_not_none
    def push_back(self) -> str:
        template = self.get_relevant_template(self.fields["template"]["name"].get())
        self.app.db_services["preset"].push_back(self.selected_preset, template)
        return f"Template {template.name} successfully pushed back\n"

    @update_config
    @preset_is_not_none
    def insert(self) -> str:
        template = self.get_relevant_template(self.fields["template"]["name"].get())
        ordered_number = self.fields["template"]["ordered_number"].get().strip()
        if ordered_number and ordered_number.isdigit():
            self.app.db_services["preset"].insert(
                self.selected_preset, template, int(ordered_number)
            )
        else:
            raise ValueError("Invalid ordered number")
        return f"Template {template.name} successfully inserted at position {ordered_number}\n"

    @update_config
    def refresh_templates(self):
        template_names = [template.name for template in self.relevant_templates]
        if not template_names:
            raise ValueError("There are no suitable configuration templates")
        self.fields["template"]["name"]["values"] = template_names
        self.fields["template"]["name"].set(template_names[0])

    def get_relevant_template(self, template_name):
        return filter(
            lambda x: x.name == template_name, self.relevant_templates
        ).__next__()

    def preview(self):
        self.display_feedback(
            "\n".join(
                v["text"]
                for _, (_, v) in enumerate(
                    self.preset_info["configuration"].items(), start=1
                )
            )
        )

    def config_meta(self):
        interfaces = len(
            [
                i
                for _, i in self.preset_info["configuration"].items()
                if i["type"] == "interface"
            ]
        )
        device_ports = len(
            self.app.db_services["device"].get_info_one(
                name=self.preset_info["device"]
            )["ports"]
        )
        return (
            f"Role: {self.preset_info['role']}\n"
            f"Device: {self.preset_info['device']}\n"
            f"Description: {self.preset_info['description']}\n"
            f"Described interfaces/Physical ports: {interfaces}/{device_ports}\n"
        )

    @property
    def config_template(self):
        return "\n".join(
            f"{i}\t{v['name']}"
            for i, (k, v) in enumerate(
                self.preset_info["configuration"].items(), start=1
            )
        )
