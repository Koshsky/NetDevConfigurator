from internal.db_app.base_tab import BaseTab

class FamilyInfoTab(BaseTab):
    def create_widgets(self):
        self.create_block("family", {"name":None}, ("SHOW", self.show_information))
        self.create_feedback_area()

    def show_information(self):
        try:
            family = self.check_family_name(self.fields["family"]["name"].get())
            associated_devices = self.app.entity_services["device"].get_devices_by_family_id(family.id)

            device_list = "\n\t".join(device.name for device in associated_devices) if associated_devices else "No associated devices."
            
            output_message = (
                f"Family Information:\n"
                f"Name: {family.name}\n"
                f"ID: {family.id}\n"
                f"Associated devices:\n\t{device_list}\n"
            )
            
            self.display_feedback(output_message)
        except Exception as e:
            self.display_feedback(f"Error retrieving family information:\n{e}")
