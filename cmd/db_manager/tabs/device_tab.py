from internal.db_app import BaseTab, error_handler
import pprint


class DeviceTab(BaseTab):
    def create_widgets(self):
        self.create_block("device", {
                "name":None,
                "protocols": self.app.entity_collections['protocol'],
                "ports": {f"{i}": self.app.entity_collections['port'] for i in range(60)}
        }, width=12)
        self.create_button_in_line(("WRITE", self.write_device))
        self.create_feedback_area()

    @error_handler
    def write_device(self):
        device = self.check_device_name(self.fields["device"]["name"].get())
        ports = self._get_port_input(device.company_id)
        self._clear_protocols(device)
        self._write_protocols(device)

        if ports:
            self._clear_ports(device)
            self._write_ports(device.id, ports)

        self.display_feedback("SUCCESS")

    def _get_port_input(self, company_id):
        company_name = self.app.entity_services['company'].get_by_id(company_id).name
        self._validate_port_input(self.fields['device']['ports'])
        strategy_method = getattr(self, f'_get_{company_name}_ports', None)
        if strategy_method is None:
            raise ValueError(f"There is not strategy_method for {company_name}")
        return strategy_method(self.fields['device']['ports'])

    def _write_ports(self, device_id, ports):
        for interface, port_id in ports.items():
            self.app.entity_services['device_port'].create({"device_id": device_id, "port_id": port_id, 'interface': interface})

    def _write_protocols(self, device):
        for protocol_name, checkbox in self.fields["device"]["protocols"].items():
            if checkbox.get() == 1:
                protocol = self.check_protocol_name(protocol_name)
                self.app.entity_services['device_protocol'].create({"device_id": device.id, "protocol_id": protocol.id})

    def _clear_ports(self, device):
        device_ports = self.app.entity_services['device_port'].get_device_ports(device.id)  # TODO: подумать о необходимости такого подхода. нужен ли он?
        for device_port in device_ports:
            self.app.entity_services['device_port'].delete_by_id(device_port.DevicePorts.id)

    def _clear_protocols(self, device):
        device_protocols = self.app.entity_services['device_protocol'].get_protocols_by_device_id(device.id)
        for device_protocol, _ in device_protocols:
            self.app.entity_services['device_protocol'].delete_by_id(device_protocol.id)

    def _validate_port_input(self, ports_input):
        def check_none_in_the_middle(fields):
            res = False
            for _, combo in fields.items():
                if combo.get() == 'None':
                    res = True
                elif res:  # res == true if None was previously encountered and not now
                    raise ValueError('[NONE] encountered in the middle of port enumeration')
        def check_mixed_speeds(fields):
            is1000mpbs = True
            for _, combo in fields.items():
                if '1000Mbps' not in combo.get():
                    is1000mpbs = False
                elif not is1000mpbs and '1000Mbps' in combo.get():
                    raise ValueError('Mixed speeds in port enumeration')

        check_none_in_the_middle(ports_input)
        check_mixed_speeds(ports_input)

    def _get_Eltex_ports(self, ports_input):
        ports = {}
        cnt = {'1000Mbps': 0, '10000Mbps': 0}
        current_speed = '1000Mbps'

        for _, combo in ports_input.items():
            if combo.get() == 'None':
                break

            port = self.check_port_name(combo.get())
            port_speed = '1000Mbps' if port.speed == 1000 else '10000Mbps'

            if port_speed != current_speed:
                current_speed = port_speed
                cnt[current_speed] = 0

            ports_map = {
                '1000Mbps': f'gigabitethernet 0/{cnt["1000Mbps"]}',
                '10000Mbps': f'tengigabitethernet 0/{cnt["10000Mbps"]}'
            }

            ports[ports_map[current_speed]] = port.id
            cnt[current_speed] += 1

        return ports

    def _default_port_strategy(self, ports_input):
        # Default strategy if no company-specific strategy exists
        return {}
