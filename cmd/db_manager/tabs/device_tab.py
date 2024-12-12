from internal.db_app.base_tab import BaseTab
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
        
    def write_device(self):
        try:
            device = self.check_device_name(self.fields["device"]["name"].get())
            self._clear_device(device)
            ports = self._check_port_input()
            self.display_feedback(pprint.pformat(ports))
            # self._write_ports(device)
            self._write_protocols(device)

        except Exception as e:
            self.display_feedback(str(e))
            print(f"Error writing device configuration to db:\n{e}")
            
    def _check_port_input(self):
        def none_in_the_middle(fields):
            res = False
            for _, combo in fields.items():
                if combo.get() == 'None':
                    res = True
                elif res:  # res == true if None was previously encountered and not now
                    return True
            return False
        
        def mixed_speeds(fields):
            is1000mpbs = True
            for _, combo in fields.items():
                if '1000Mbps' not in combo.get():
                    is1000mpbs = False
                elif not is1000mpbs and '1000Mbps' in combo.get():
                    return True
            return False
                
        
        if none_in_the_middle(self.fields['device']['ports']):
            raise ValueError('[NONE] encountered in the middle of port enumeration')
        elif mixed_speeds(self.fields['device']['ports']):
            raise ValueError('Mixed speeds in port enumeration')
        
        ports = {}
        cnt = 0
        is1000mpbs = True
        for _, combo in self.fields["device"]["ports"].items():  # for eltex-mes
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

            
    def _write_ports(self, device):
        for port_num, combo in self.fields["device"]["ports"].items():
            if combo.get() == 'None':
                break
            port = self.check_port_name(combo.get())
            self.app.entity_services['device_port'].create({"device_id": device.id, "port_id": port.id})
            
    def _write_protocols(self, device):
        for protocol_name, checkbox in self.fields["device"]["protocols"].items():
            if checkbox.get() == 1:
                protocol = self.check_protocol_name(protocol_name)
                self.app.entity_services['device_protocol'].create({"device_id": device.id, "protocol_id": protocol.id})
            
    def _clear_device(self, device):
        device_protocols = self.app.entity_services['device_protocol'].get_device_protocols(device.id)
        for device_protocol in device_protocols:
            self.app.entity_services['device_protocol'].delete_by_id(device_protocol.id)
            
        device_ports = self.app.entity_services['device_port'].get_device_ports(device.id)
        for device_port in device_ports:
            self.app.entity_services['device_port'].delete_by_id(device_port.id)

    def get_port_list(self):
        return {        
            f"{i}": self.app.ports
            for i in range(60)
        }
        