from functools import wraps

from gui import BaseTab, apply_error_handler


def update_config(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        message = func(self, *args, **kwargs)
        self._config = self.app.db_services["preset"].get_info(self.preset)
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
        self._config = None
        self.preset = None

    def render_widgets(self):
        self.create_block(
            "preset",
            {
                "device": self.app.entity_collections["device"],
                "role": self.app.entity_collections["role"],
            },
        )
        self.create_button_in_line(("REFRESH", self.refresh_templates))
        self.create_block(
            "template",
            {
                "name": ("1", "2"),  # TODO: исправить этот костыль.
                "ordered_number": None,
            },
        )
        self.create_button_in_line(("PUSH BACK", self.push_back))
        self.create_button_in_line(("INSERT", self.insert))
        self.create_button_in_line(("REMOVE", self.remove))
        self.create_button_in_line(("PREVIEW", self.preview))
        self.create_feedback_area()

    def preview(self):
        self.display_feedback(
            "\n".join(
                v["text"]
                for _, (_, v) in enumerate(
                    self._config["configuration"].items(), start=1
                )
            )
        )

    def config_meta(self):
        interfaces = len(
            [
                i
                for _, i in self._config["configuration"].items()
                if i["type"] == "interface"
            ]
        )
        device_ports = len(
            self.app.db_services["device"].get_info_by_name(self._config["target"])[
                "ports"
            ]
        )
        return (
            f"Role: {self._config['role']}\n"
            f"Device: {self._config['target']}\n"
            f"Description: {self._config['description']}\n"
            f"Described interfaces/Physical ports: {interfaces}/{device_ports}\n"
        )

    @property
    def config_template(self):
        return "\n".join(
            f"{i}\t{v['name']}"
            for i, (k, v) in enumerate(self._config["configuration"].items(), start=1)
        )

    @update_config
    @preset_is_not_none
    def remove(self) -> str:
        ordered_number = self.fields["template"]["ordered_number"].get().strip()
        if ordered_number and ordered_number.isdigit():
            self.app.db_services["preset"].remove(self.preset.id, int(ordered_number))
        else:
            raise ValueError("Invalid ordered number")

    @update_config
    @preset_is_not_none
    def push_back(self) -> str:
        template_name = self.fields["template"]["name"].get()
        template = self.app.db_services["template"].get_by_name_and_role(
            template_name, self.preset.role
        )
        self.app.db_services["preset"].push_back(self.preset, template)
        return f"Template {template.name} successfully pushed back\n"

    @update_config
    @preset_is_not_none
    def insert(self) -> str:
        template_name = self.fields["template"]["name"].get()
        template = self.app.db_services["template"].get_by_name_and_role(
            template_name, self.preset.role
        )
        ordered_number = self.fields["template"]["ordered_number"].get().strip()
        if ordered_number and ordered_number.isdigit():
            self.app.db_services["preset"].insert(
                self.preset, template, int(ordered_number)
            )
        else:
            raise ValueError("Invalid ordered number")
        return f"Template {template.name} successfully inserted at position {ordered_number}\n"

    @update_config
    def refresh_templates(self):
        device = self.check_device_name(self.fields["preset"]["device"].get())
        self.preset = self.app.db_services["preset"].get_by_device_and_role(
            device, self.fields["preset"]["role"].get()
        )
        templates = self.app.db_services["template"].get_by_family_id_and_role(
            device.family_id, self.preset.role
        )
        template_names = [template.name for template in templates]
        if not template_names:
            raise ValueError("There are no suitable configuration templates")
        self.fields["template"]["name"]["values"] = template_names
        self.fields["template"]["name"].set(template_names[0])
