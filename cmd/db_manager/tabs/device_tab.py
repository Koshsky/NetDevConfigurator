from internal.db_app import BaseTab, error_handler
import pprint


class DeviceTab(BaseTab):
    def create_widgets(self):
        self.create_block("device", {
                "name":None,
                "protocols": self.app.protocols,
                "ports": self.get_port_list()
        }, width=12)
        self.create_button_in_line(("WRITE", self.write_device))
        self.create_feedback_area()

    @error_handler
    def write_device(self):
        device = self.check_device_name(self.fields["device"]["name"].get())
        self._clear_device(device)
        ports = self._get_port_input(device.company_id)
        self.display_feedback(pprint.pformat(ports))
        self._write_ports(device.id, ports)
        self._write_protocols(device)
            
    def _get_port_input(self, company_id: int):
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
                
        
        check_none_in_the_middle(self.fields['device']['ports'])
        check_mixed_speeds(self.fields['device']['ports'])
        if self.app.entity_services['company'].get_by_id(company_id).name == 'Eltex':  #  TODO: ПОКА ТОЛЬКО ЕЛТЕКС. НАД ЭТИМ НУЖНО ДУМАТЬ
            return self._get_eltex_mes_ports(self.fields['device']['ports'])
        else:
            return {}
    
    def _get_eltex_mes_ports(self, ports_input):
        ports = {}
        cnt = 0
        is1000mpbs = True
        for _, combo in ports_input.items():  # for eltex-mes
            if combo.get() == 'None':
                break
                
            port = self.check_port_name(combo.get())
            if port.speed == 1000:
                ports[f'gigabitethernet 0/{cnt}'] = port.id
            elif is1000mpbs and port.speed == 10000:
                cnt = 0
                is1000mpbs = False
                ports[f'tengigabitethernet 0/{cnt}'] = port.id
            elif port.speed == 10000:
                ports[f'tengigabitethernet 0/{cnt}'] = port.id
            else:
                raise ValueError(f"Unsupported port speed: {port.speed}")
            cnt += 1
            
        return ports
        
    def _write_ports(self, device_id, ports):
        for name, port_id in ports.items():
            self.app.entity_services['device_port'].create({"device_id": device_id, "port_id": port_id, 'name': name})
            
    def _write_protocols(self, device):
        for protocol_name, checkbox in self.fields["device"]["protocols"].items():
            if checkbox.get() == 1:
                protocol = self.check_protocol_name(protocol_name)
                self.app.entity_services['device_protocol'].create({"device_id": device.id, "protocol_id": protocol.id})
            
    def _clear_device(self, device):
        device_protocols = self.app.entity_services['device_protocol'].get_device_protocols(device.id)
        for device_protocol in device_protocols:
            self.app.entity_services['device_protocol'].delete_by_id(device_protocol.id)
            
        device_ports = self.app.entity_services['device_port'].get_device_ports(device.id)  # TODO: подумать о необходимости такого подхода. нужен ли он?
        for device_port in device_ports:
            self.app.entity_services['device_port'].delete_by_id(device_port.DevicePorts.id)

    def get_port_list(self):
        return {        
            f"{i}": self.app.ports
            for i in range(60)
        }
        