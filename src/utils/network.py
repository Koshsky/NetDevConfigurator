import ipaddress

from scapy.all import ARP, Ether, srp


# TODO: set up network interface with given netplan configuration
def set_up_dev(dev: str):
    pass


def scan_network(network):
    arp = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=2, verbose=0)[0]

    active_ips = [received.psrc for sent, received in result]
    active_ips.sort(key=lambda x: int(x.split(".")[-1]))
    return active_ips


def find_available_ip(network, filter=None):
    net = ipaddress.IPv4Network(network, strict=False)
    active_ips = scan_network(network)
    for ip in net.hosts():
        if str(ip) not in active_ips:
            if filter is not None and not filter(ip):
                continue
            return str(ip)


if __name__ == "__main__":
    active_ips = scan_network("192.168.3.0/24")
    for ip in active_ips:
        print(ip)
    print(len(active_ips))
