import logging

from gui import BaseTab, apply_error_handler

logger = logging.getLogger(__name__)


@apply_error_handler
class AddTab(BaseTab):
    """Tab for adding new entities to the database."""

    def _create_widgets(self) -> None:
        """Creates the widgets for the tab."""
        logger.debug("Creating widgets for AddTab")
        self.create_block("company", {"name": None}, ("SUBMIT", self.submit_company))
        self.create_block("family", {"name": None}, ("SUBMIT", self.submit_family))
        self.create_block("protocol", {"name": None}, ("SUBMIT", self.submit_protocol))
        self.create_block(
            "device",
            {
                "name": None,
                "company": tuple(
                    c.name for c in self.app.db_services["company"].get_all()
                ),
                "family": tuple(
                    f.name for f in self.app.db_services["family"].get_all()
                ),
                "dev_type": ("switch", "router"),
            },
            ("SUBMIT", self.submit_device),
        )

    def submit_protocol(self) -> None:
        """Submits a new protocol to the database."""
        logger.info("Submitting new protocol")
        if protocol_name := self.fields["protocol"]["name"].get().strip():
            self.app.db_services["protocol"].create(name=protocol_name)
            logger.debug("Protocol created: %s", protocol_name)
        else:
            logger.error("Protocol name cannot be empty")
            raise ValueError("Protocol name cannot be empty.")

    def submit_family(self) -> None:
        """Submits a new family to the database."""
        logger.info("Submitting new family")
        if family_name := self.fields["family"]["name"].get().strip():
            self.app.db_services["family"].create(name=family_name)
            logger.debug("Family created: %s", family_name)
        else:
            logger.error("Family name cannot be empty")
            raise ValueError("Family name cannot be empty.")

    def submit_device(self) -> None:
        """Submits a new device to the database."""
        logger.info("Submitting new device")
        device_name: str = self.fields["device"]["name"].get().strip()
        dev_type: str = self.fields["device"]["dev_type"].get().strip()

        if not device_name:
            logger.error("Device name cannot be empty")
            raise ValueError("Device name cannot be empty.")
        if not dev_type:
            logger.error("Device type not selected")
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
        logger.debug("Device created: %s", device_name)

    def submit_company(self) -> None:
        """Submits a new company to the database."""
        logger.info("Submitting new company")
        if company_name := self.fields["company"]["name"].get().strip():
            self.app.db_services["company"].create(name=company_name)
            logger.debug("Company created: %s", company_name)
        else:
            logger.error("Company name cannot be empty")
            raise ValueError("Company name cannot be empty.")
