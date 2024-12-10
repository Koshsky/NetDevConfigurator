from .base_tab import BaseTab


class DeleteTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app, "DELETE")

    def create_widgets(self):
        self.create_block("company", {"name":None}, self.delete_company)
        self.create_block("firmware", {"name":None}, self.delete_firmware)
        self.create_block("device", {"name":None}, self.delete_device)
        self.create_block("protocol", {"name":None}, self.delete_protocol)
        self.create_feedback_area()

    def delete_protocol(self):
        try:
            protocol = self.check_protocol_name(self.fields["protocol"]["name"].get())
            self.app.protocol_service.delete(protocol)
            self.display_feedback(f"Successfully deleted from the protocols table.")
        except Exception as e:
            self.display_feedback(f"Error deleting protocol: {e}")
            self.app.session.rollback()
            
    def delete_company(self):
        try:
            company = self.check_company_name(self.fields["company"]["name"].get())
            self.app.company_service.delete(company)
            self.display_feedback(f"Successfully deleted from the companies table.")
        except Exception as e:
            self.display_feedback(f"Error deleting company: {e}")
            self.app.session.rollback()

    def delete_firmware(self):
        try:
            firmware = self.check_firmware_name(self.fields["firmware"]["name"].get())
            self.app.firmware_service.delete(firmware)
            self.display_feedback(f"Successfully deleted from the firmwares table.")
        except Exception as e:
            self.display_feedback(f"Error deleting firmware: {e}")
            self.app.session.rollback()

    def delete_device(self):
        try:
            device = self.check_device_name(self.fields["device"]["name"].get())
            self.app.device_service.delete(device)
            self.display_feedback(f"Successfully deleted from the devices table.")
        except Exception as e:
            self.display_feedback(f"Error deleting device: {e}")
            self.app.session.rollback()
