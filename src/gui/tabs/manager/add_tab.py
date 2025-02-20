from gui import BaseTab, apply_error_handler


@apply_error_handler
class AddTab(BaseTab):
    def _create_widgets(self):
        self.create_block("company", {"name": None}, ("SUBMIT", self.submit_company))
        self.create_block("family", {"name": None}, ("SUBMIT", self.submit_family))
        self.create_block("protocol", {"name": None}, ("SUBMIT", self.submit_protocol))
        self.create_block(
            "device",
            {
                "name": None,
                "company": self.app.entity_collections["company"],
                "family": self.app.entity_collections["family"],
                "dev_type": ("switch", "router"),
            },
            ("SUBMIT", self.submit_device),
        )
        self.create_block(
            "template",
            {
                "name": None,
                "family": self.app.entity_collections["family"],
                "type": self.app.entity_collections["template_type"],
                "role": self.app.entity_collections["role"] + ("common",),
                "text": None,
            },
            ("SUBMIT", self.submit_template),
        )
        self.create_block(
            "preset",
            {
                "device": self.app.entity_collections["device"],
                "role": self.app.entity_collections["role"],
            },
            ("SUBMIT", self.submit_preset),
        )
        self.create_feedback_area()

    def submit_preset(self):
        device = self.check_device_name(self.fields["preset"]["device"].get())
        role = self.fields["preset"]["role"].get().strip()
        if role not in self.app.entity_collections["role"] or role == "common":
            raise ValueError("Invalid role.")

        self.app.db_services["preset"].create(role=role, device_id=device.id)
        self.display_feedback("successfully")

    def submit_template(self):
        template_name = self.fields["template"]["name"].get().strip()
        template_type = self.fields["template"]["type"].get().strip()
        role = self.fields["template"]["role"].get().strip()
        text = self.fields["template"]["text"].get().strip()

        if not (template_name and template_type and role):
            raise ValueError("All parameters must be set")

        family = self.check_family_name(self.fields["template"]["family"].get())
        self.app.db_services["template"].create(
            name=template_name,
            family_id=family.id,
            type=template_type,
            role=role,
            text=text,
        )

    def submit_protocol(self):
        protocol_name = self.fields["protocol"]["name"].get().strip()
        if not protocol_name:
            raise ValueError("Protocol name cannot be empty.")

        self.app.db_services["protocol"].create(name=protocol_name)
        self.display_feedback("Successfully added to the protocols table.")

    def submit_family(self):
        family_name = self.fields["family"]["name"].get().strip()
        if not family_name:
            raise ValueError("Family name cannot be empty.")

        self.app.db_services["family"].create(name=family_name)
        self.display_feedback("Successfully added to the families table.")

    def submit_device(self):
        device_name = self.fields["device"]["name"].get().strip()
        dev_type = self.fields["device"]["dev_type"].get().strip()

        if not device_name:
            raise ValueError("Device name cannot be empty.")
        if not dev_type:
            raise ValueError("Select device type")

        company = self.check_company_name(self.fields["device"]["company"].get())
        family = self.check_family_name(self.fields["device"]["family"].get())
        self.app.db_services["device"].create(
            name=device_name,
            company_id=company.id,
            family_id=family.id,
            dev_type=dev_type,
        )

        self.display_feedback("Successfully added to the devices table.")

    def submit_company(self):
        company_name = self.fields["company"]["name"].get().strip()
        if not company_name:
            raise ValueError("Company name cannot be empty.")

        self.app.db_services["company"].create(name=company_name)
        self.display_feedback("Successfully added to the companies table.")
