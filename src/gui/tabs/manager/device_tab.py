from gui import BaseTab, apply_error_handler


@apply_error_handler
class DeviceTab(BaseTab):
    def create_widgets(self):
        self.create_block(
            "device",
            {
                "name": self.app.entity_collections["device"],
                "protocols": list(self.app.entity_collections["protocol"]),
                "ports": {
                    f"{i}": self.app.entity_collections["port"] for i in range(60)
                },
            },
            width=12,
        )
        self.create_button_in_line(("WRITE", self.write_device))
        self.create_feedback_area()

    def write_device(self):
        device = self.check_device_name(self.fields["device"]["name"].get())
        self._validate_port_input(self.fields["device"]["ports"])

        self.write_protocols(device)
        self.write_ports(device)

        self.display_feedback("SUCCESS")

    def write_ports(self, device):
        self.app.db_services["device"].reset_ports(device.id)
        for _, combo in self.fields["device"]["ports"].items():
            if combo.get() == "None":
                break
            port = self.check_port_name(combo.get())
            self.app.db_services["device"].add_port_by_id(device.id, port.id)

    def write_protocols(self, device):
        self.app.db_services["device"].reset_protocols(device.id)
        for protocol_name, checkbox in self.fields["device"]["protocols"].items():
            if checkbox.get() == 1:
                protocol = self.check_protocol_name(protocol_name)
                self.app.db_services["device"].add_protocol_by_id(
                    device.id, protocol.id
                )

    def _validate_port_input(self, ports_input):
        def check_none_in_the_middle(fields):
            res = False
            for _, combo in fields.items():
                if combo.get() == "None":
                    res = True
                elif res:  # res == true if None was previously encountered and not now
                    raise ValueError(
                        "[NONE] encountered in the middle of port enumeration"
                    )

        def check_mixed_speeds(fields):
            is1000mpbs = True
            for _, combo in fields.items():
                if "1000Mbps" not in combo.get():
                    is1000mpbs = False
                elif not is1000mpbs and "1000Mbps" in combo.get():
                    raise ValueError("Mixed speeds in port enumeration")

        check_none_in_the_middle(ports_input)
        check_mixed_speeds(ports_input)
