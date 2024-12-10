from internal.db_app.base_tab import BaseTab

class CompanyInfoTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)

    def create_widgets(self):
        self.create_block("company", {"name":None}, ("SHOW", self.show_information))  # TODO: тут должен быть нормальный список компаний...
        self.create_feedback_area()

    def show_information(self):
        try:
            company = self.check_company_name(self.fields["company"]["name"].get())
            associated_devices = self.app.device_service.get_devices_by_company_id(company.id)

            device_list = "\n\t".join(device.name for device in associated_devices) if associated_devices else "No associated devices."
            
            output_message = (
                f"Company Information:\n"
                f"Name: {company.name}\n"
                f"ID: {company.id}\n"
                f"Associated devices:\n\t{device_list}\n"
            )
            
            self.display_feedback(output_message)
        except Exception as e:
            self.display_feedback(f"Error retrieving company information:\n{e}")
