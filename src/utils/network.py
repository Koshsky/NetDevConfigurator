from scapy.all import ARP, Ether, srp
import ipaddress


def scan_network(network):
    arp = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=2, verbose=0)[0]

    active_ips = [received.psrc for sent, received in result]
    active_ips.sort(key=lambda x: int(x.split(".")[-1]))
    return active_ips


def find_first_available_ip(
    network, filter=lambda ip: ip.packed[-1] >= 100 and ip.packed[-1] < 201
):
    net = ipaddress.IPv4Network(network, strict=False)
    active_ips = scan_network(network)
    for ip in net.hosts():
        if filter(ip) and str(ip) not in active_ips:
            return ip


if __name__ == "__main__":
    active_ips = scan_network("192.168.3.0/24")
    for ip in active_ips:
        print(ip)
    print(len(active_ips))
