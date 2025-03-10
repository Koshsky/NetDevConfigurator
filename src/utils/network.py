import ipaddress
import logging
from typing import Callable, Optional

from scapy.all import ARP, Ether, srp

logger = logging.getLogger(__name__)


def set_up_dev(dev: str):
    """Sets up the given network interface using Netplan."""
    logger.debug("Setting up network interface: %s", dev)
    raise NotImplementedError("Setting up network interface is not yet implemented.")


def scan_network(network):
    """
    Scans the given network for active IP addresses using ARP.

    Args:
        network: The network to scan (e.g., "192.168.1.0/24").

    Returns:
        A sorted list of active IP addresses (strings).
    """
    logger.debug("Scanning network: %s", network)
    try:
        arp = ARP(pdst=network)
    except Exception as e:
        logger.exception("Error creating ARP packet: %s", e)
        return []
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    logger.debug("Sending ARP request...")
    result = srp(packet, timeout=2, verbose=0)[0]
    logger.debug("Received ARP responses: %s", result)

    active_ips = sorted(
        [received.psrc for sent, received in result],
        key=lambda x: int(x.split(".")[-1]),
    )
    logger.debug("Active IPs found: %s", active_ips)
    return active_ips


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
    logger.debug("Searching for available IP address in %s...", network)
    net = ipaddress.IPv4Network(network, strict=False)
    active_ips = scan_network(network)
    logger.debug("Active IPs: %s", active_ips)

    for ip in net.hosts():
        ip_str = str(ip)
        logger.debug("Checking IP: %s", ip_str)
        if ip_str not in active_ips:
            if filter_func is not None and not filter_func(ip):
                logger.debug("IP %s filtered out by filter function.", ip_str)
                continue
            logger.info("Found available IP address: %s", ip_str)
            return ip_str
    logger.warning("No available IP address found in %s", network)
    return None


if __name__ == "__main__":
    active_ips = scan_network("192.168.3.0/24")
    for ip in active_ips:
        print(ip)
    print(len(active_ips))
