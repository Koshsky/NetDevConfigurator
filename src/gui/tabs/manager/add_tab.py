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

        company = self.app.db_services["company"].get_one(
            name=self.fields["device"]["company"].get()
        )
        family = self.app.db_services["family"].get_one(
            name=self.fields["device"]["family"].get()
        )
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
