import logging
import os

from drivers.core import get_core
from utils.environ import set_env
from utils.filesystem import find_most_recent_file

logger = logging.getLogger("mock")


class MockDriver:
    def __init__(self, device, **driver):
        self.core = get_core(device["family"]["name"])
        self.device = device

    def send_command(self, command):
        logger.info("Send: %s", command)
        return f"<resp>{command}<@resp>\n"

    def _execute(self, commands):
        if isinstance(commands, str):
            return self.send_command(commands)
        elif isinstance(commands, list):
            return "".join(self.send_command(command) for command in commands)
        else:
            raise TypeError(
                f"send_commands: argument must be str or List[str]. Given: {type(commands).__name__}"
            )

    def __enter__(self):
        self._execute(self.core.open_sequence)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def show_run(self):
        self._execute(self.core.show_run)
        return f"""{self.core.comment_symbol}Building configuration...
{self.core.comment_symbol}ISS config ver. 9; SW ver. 10.3.6.6 (728c49ab) for MES2424 rev.B. Do not remove or edit this line
!
hostname "rami-mes2424-tsh2"
debug-logging log-path flash:/mnt/
dump core-file flash:/mnt/
!
no spanning-tree
!
vlan 2-4
  vlan active
!
clock time source ntp
!
switching-mode cut-through
!
username mvsadmin password encrypted zbICg2SPBsvT1IfFwRpH3Q== privilege 15
username admin_rec password encrypted Ts6Wa2/X/ebD/HnwyJC5NQ== privilege 15
!
vlan 2
  name "VIDEO"
!
vlan 3
  name "DATA"
!
vlan 4
  name "MGMT"
!
interface vlan 4
  ip address 10.4.2.11 255.255.0.0
!
interface gigabitethernet 0/1
  switchport general allowed vlan add 2
  switchport general allowed vlan add 3 untagged
  switchport forbidden default-vlan
  switchport general pvid 3
!
interface gigabitethernet 0/2
  switchport general allowed vlan add 2
  switchport general allowed vlan add 3 untagged
  switchport forbidden default-vlan
  switchport general pvid 3
!
interface gigabitethernet 0/3
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/4
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/5
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/6
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/7
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/8
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/9
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/10
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/11
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/12
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/13
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/14
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/15
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/16
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/17
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/18
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/19
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/20
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/21
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/22
  switchport mode access
  switchport access vlan 3
!
interface gigabitethernet 0/23
  switchport mode access
  switchport access vlan 4
!
interface gigabitethernet 0/24
  switchport mode access
  switchport access vlan 4
!
interface tengigabitethernet 0/1
  switchport general allowed vlan add 2
  switchport forbidden default-vlan
!
interface tengigabitethernet 0/2
  switchport general allowed vlan add 2
  switchport forbidden default-vlan
!
interface tengigabitethernet 0/3
  switchport general allowed vlan add 3-4
  switchport forbidden default-vlan
!
interface tengigabitethernet 0/4
  switchport general allowed vlan add 3-4
  switchport forbidden default-vlan
!
ip route 0.0.0.0  0.0.0.0 10.4.0.254
!
no feature telnet
!
ztp disable
end

"""

    def get_header(self):
        config = self.show_run()
        header = "".join(
            line + "\n"
            for line in config.split("\n")
            if line.startswith(self.core.comment_symbol)
        )
        return header + "!\n"

    def update_startup_config(self):
        return self._execute(self.core.update_startup_config)

    def reboot(self):
        return self._execute(self.core.reload)

    def update_boot(self):
        filename = find_most_recent_file(
            f"{os.environ['TFTP_FOLDER']}/firmware", self.device["pattern"]["boot"]
        )
        if filename is None:
            logger.warning(
                "There is no boot file for %s in %s matching %s",
                self.device["name"],
                os.environ["TFTP_FOLDER"],
                self.device["pattern"]["boot"],
            )
            return f"There is no boot file for {self.device['name']}\n"
        else:
            set_env("FILENAME", filename)
            return self._execute(self.core.load_boot)

    def update_uboot(self):
        filename = find_most_recent_file(
            f"{os.environ['TFTP_FOLDER']}/firmware", self.device["pattern"]["uboot"]
        )
        if filename is None:
            logger.warning(
                "There is no uboot file for %s in %s matching %s",
                self.device["name"],
                os.environ["TFTP_FOLDER"],
                self.device["pattern"]["uboot"],
            )
            return f"There is no uboot file for {self.device['name']}\n"
        else:
            set_env("FILENAME", filename)
            return self._execute(self.core.load_uboot)

    def update_firmware(self):
        filename = find_most_recent_file(
            f"{os.environ['TFTP_FOLDER']}/firmware", self.device["pattern"]["firmware"]
        )
        if filename is None:
            logger.warning(
                "There is no firmware file for %s in %s matching %s",
                self.device["name"],
                os.environ["TFTP_FOLDER"],
                self.device["pattern"]["firmware"],
            )
            return f"There is no firmware file for {self.device['name']}\n"
        else:
            set_env("FILENAME", filename)
            return self._execute(self.core.load_firmware)

    def update_firmwares(self):
        res = self.update_boot()
        res += self.update_uboot()
        return res + self.update_firmware()
