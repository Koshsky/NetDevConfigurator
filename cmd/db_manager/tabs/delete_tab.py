from internal.db_app import BaseTab, error_handler


class DeleteTab(BaseTab):
    def create_widgets(self):
        self.create_block("company", {"name":None}, ("delete", self.delete_company))
        self.create_block("family", {"name":None}, ("delete", self.delete_family))
        self.create_block("device", {"name":None}, ("delete", self.delete_device))
        self.create_block("firmware", {"name":None}, ("delete", self.delete_firmware))
        self.create_block("protocol", {"name":None}, ("delete", self.delete_protocol))
        self.create_feedback_area()

    @error_handler
    def delete_protocol(self):
        protocol = self.check_protocol_name(self.fields["protocol"]["name"].get())
        self.app.entity_services['protocol'].delete(protocol)
        self.display_feedback("Successfully deleted from the protocols table.")

    @error_handler
    def delete_family(self):
        family = self.check_family_name(self.fields["family"]["name"].get())
        self.app.entity_services['family'].delete(family)
        self.display_feedback("Successfully deleted from the families table.")

    @error_handler
    def delete_company(self):
        company = self.check_company_name(self.fields["company"]["name"].get())
        self.app.entity_services["company"].delete(company)
        self.display_feedback("Successfully deleted from the companies table.")
        
    @error_handler
    def delete_firmware(self):
        firmware = self.check_firmware_name(self.fields["firmware"]["name"].get())
        self.app.entity_services["firmware"].delete(firmware)
        self.display_feedback("Successfully deleted from the firmwares table.")

    @error_handler
    def delete_device(self):
        device = self.check_device_name(self.fields["device"]["name"].get())
        self.app.entity_services["device"].delete(device)
        self.display_feedback("Successfully deleted from the devices table.")
