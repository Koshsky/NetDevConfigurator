import ipaddress
import logging
from typing import Callable, Optional

from scapy.all import ARP, Ether, srp

logger = logging.getLogger("utils")


def set_up_dev(dev: str):
    """Sets up the given network interface using Netplan."""
    raise NotImplementedError("Setting up network interface is not yet implemented.")


def scan_network(network):
    """
    Scans the given network for active IP addresses using ARP.

    Args:
        network: The network to scan (e.g., "192.168.1.0/24").

    Returns:
        A sorted list of active IP addresses (strings).
    """
    try:
        arp = ARP(pdst=network)
    except Exception as e:
        logger.error("Error scanning network: %s", e)
        return []
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=2, verbose=0)[0]

    return sorted(
        [received.psrc for sent, received in result],
        key=lambda x: int(x.split(".")[-1]),
    )


def find_available_ip(
    network: str, filter_func: Optional[Callable[[str], bool]] = None
) -> Optional[str]:
    """
    Finds an available IP address in the given network.

    Searches for an available IP address in the specified network, optionally filtering
    the results using a provided function.

    Args:
        network: The network to scan (e.g., "192.168.1.0/24").
        filter_func: An optional function that takes an IP address string as input
            and returns True if the IP should be considered available, False otherwise.

    Returns:
        An available IP address as a string, or None if no available IP is found.
    """
    logger.info("Searching for available IP address in %s...", network)
    net = ipaddress.IPv4Network(network, strict=False)
    active_ips = scan_network(network)
    for ip in net.hosts():
        ip_str = str(ip)
        if ip_str not in active_ips:
            if filter_func is not None and not filter_func(ip_str):
                continue
            logger.info("Found available IP address: %s", ip_str)
            return ip_str
    return None


if __name__ == "__main__":
    active_ips = scan_network("192.168.3.0/24")
    for ip in active_ips:
        print(ip)
    print(len(active_ips))
