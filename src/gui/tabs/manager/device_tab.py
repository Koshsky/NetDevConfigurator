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

        self.write_protocols(device)
        self.write_ports(device)

        self.display_feedback("SUCCESS")

    def write_ports(self, device):
        port_input = list(
            map(lambda x: x[1].get(), self.fields["device"]["ports"].items())
        )
        ports = self.prepare_port_input(port_input)
        self.app.db_services["device"].reset_ports(device.id)
        for port in ports:
            self.app.db_services["device"].add_port_by_id(device.id, port.id)

    def write_protocols(self, device):
        self.app.db_services["device"].reset_protocols(device.id)
        for protocol_name, checkbox in self.fields["device"]["protocols"].items():
            if checkbox.get() == 1:
                protocol = self.check_protocol_name(protocol_name)
                self.app.db_services["device"].add_protocol_by_id(
                    device.id, protocol.id
                )

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

        port_input = strip_none(port_input)

        return check_mixed_speeds(port_input)
