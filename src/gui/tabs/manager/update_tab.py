from gui import BaseTab, apply_error_handler


@apply_error_handler
class UpdateTab(BaseTab):
    def render_widgets(self):
        self.create_block(
            "",
            {
                "device": self.app.entity_collections["device"],
                "mask": {"boot": ("",), "uboot": ("",), "firmware": ("",)},
                "protocols": list(self.app.entity_collections["protocol"]),
                "ports": {
                    f"{i}": (None,) + self.app.entity_collections["port"]
                    for i in range(1, 61)
                },
            },
            width=12,
        )
        self.create_button_in_line(("UPDATE MASKS", self.write_mask))
        self.create_button_in_line(("UPDATE PROTOCOLS", self.update_protocols))
        self.create_button_in_line(("UPDATE PORTS", self.update_ports))
        self.create_feedback_area()

    def write_mask(self):
        device = self.check_device_name(self.fields[""]["device"].get().strip())
        self.app.db_services["device"].update_files(
            device,
            boot=self.fields[""]["mask"]["boot"].get().strip(),
            uboot=self.fields[""]["mask"]["uboot"].get().strip(),
            firmware=self.fields[""]["mask"]["firmware"].get().strip(),
        )
        self.display_feedback("Linked device with MASKS successfully.")

    def update_ports(self):
        device = self.check_device_name(self.fields[""]["device"].get().strip())
        port_input = list(map(lambda x: x[1].get(), self.fields[""]["ports"].items()))
        ports = self.prepare_port_input(port_input)
        self.app.db_services["device"].reset_ports(device.id)
        for port in ports:
            self.app.db_services["device"].add_port_by_id(device.id, port.id)
        self.display_feedback("Linked device with PORTS successfully.")

    def update_protocols(self):
        device = self.check_device_name(self.fields[""]["device"].get().strip())
        self.app.db_services["device"].reset_protocols(device)
        for protocol_name, checkbox in self.fields[""]["protocols"].items():
            if checkbox.get() == 1:
                protocol = self.check_protocol_name(protocol_name)
                self.app.db_services["device"].add_protocol_by_id(
                    device.id, protocol.id
                )
        self.display_feedback("Linked device with PROTOCOLS successfully.")

    def prepare_port_input(self, port_input):
        def strip_none(ports):
            while ports[-1] == "None":
                ports.pop()
            return ports

        def check_mixed_speeds(fields):
            is1000mbps = False
            res = []
            for port_name in fields[::-1]:
                if port_name == "None":
                    res.append(res[-1])
                    continue
                # may raise exception (invalid name)
                port = self.app.db_services["port"].get_by_name(port_name)
                if port.speed != 10000:
                    is1000mbps = True
                elif is1000mbps and port.speed == 10000:
                    raise ValueError("Mixed speeds in port enumeration")
                res.append(port)
            return res[::-1]

        return check_mixed_speeds(strip_none(port_input))
