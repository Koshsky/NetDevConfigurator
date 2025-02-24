from gui import BaseTab, apply_error_handler


@apply_error_handler
class UpdateTab(BaseTab):
    def _create_widgets(self):
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
        self.create_button_in_line(("UPDATE MASKS", self.update_masks))
        self.create_button_in_line(("UPDATE PROTOCOLS", self.update_protocols))
        self.create_button_in_line(("UPDATE PORTS", self.update_ports))

    def update_masks(self):
        self.app.db_services["device"].update_masks(
            self.selected_device,
            boot=self.fields[""]["mask"]["boot"].get().strip(),
            uboot=self.fields[""]["mask"]["uboot"].get().strip(),
            firmware=self.fields[""]["mask"]["firmware"].get().strip(),
        )

    def update_ports(self):
        self.app.db_services["device"].update_ports(
            self.selected_device, self.port_input
        )

    def update_protocols(self):
        self.app.db_services["device"].update_protocols(
            self.selected_device, self.protocol_input
        )

    @property
    def selected_device(self):
        return self.app.db_services["device"].get_one(
            name=self.fields[""]["device"].get().strip()
        )

    @property
    def protocol_input(self):
        res = []
        for protocol_name, checkbox in self.fields[""]["protocols"].items():
            if checkbox.get() == 1:
                protocol = self.app.db_services["protocol"].get_one(name=protocol_name)
                res.append(protocol)
        return res

    @property
    def port_input(self):
        raw_input = list(map(lambda x: x[1].get(), self.fields[""]["ports"].items()))

        def strip_none(ports):
            while ports and ports[-1] == "None":
                ports.pop()
            return ports

        def check_mixed_speeds(fields):
            is1000mbps = False
            res = []
            for port_name in fields[::-1]:
                if port_name == "None":
                    res.append(res[-1])
                    continue
                port = self.app.db_services["port"].get_one(name=port_name)
                if port.speed != 10000:
                    is1000mbps = True
                elif is1000mbps and port.speed == 10000:
                    raise ValueError("Mixed speeds in port enumeration")
                res.append(port)
            return res[::-1]

        return check_mixed_speeds(strip_none(raw_input))
