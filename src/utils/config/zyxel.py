import logging
import re
from typing import Any, Dict, List

from utils.environ import set_env

logger = logging.getLogger(__name__)


def prepare_zyxel_environs(json_config: Dict[str, Any]) -> Dict[str, Any]:
    """Prepares environment variables for Zyxel configuration.

    Processes the JSON configuration to extract port information for VLANs
    and sets environment variables accordingly.

    Args:
        json_config: The JSON configuration dictionary.

    Returns:
        The original JSON configuration dictionary.
    """
    logger.debug("Preparing Zyxel environment variables...")

    allowed_vlans = ["2", "3", "4", "5", "30"]
    fixed_ports = {vlan: [] for vlan in allowed_vlans}
    forbidden_ports = {vlan: [] for vlan in allowed_vlans}
    untagged_ports = {vlan: [] for vlan in allowed_vlans}

    interfaces = filter(
        lambda item: item[1]["type"] == "interface", json_config.items()
    )
    for interface_id, info in interfaces:
        logger.debug("Processing interface: %s", interface_id)
        try:
            n = int(interface_id.split()[-1])
        except (ValueError, IndexError):
            logger.warning("Invalid interface ID format: %s", interface_id)
            continue  # Skip invalid interface IDs

        for ports in forbidden_ports.values():
            ports.append(n)

        for vlan_id in re.findall(r"pvid (\d+)", info["text"]):
            logger.debug("Found PVID %s for interface %s", vlan_id, interface_id)
            if vlan_id in fixed_ports:
                fixed_ports[vlan_id].append(n)
                forbidden_ports[vlan_id].remove(n)
                if "frame-type tagged" not in info["text"]:
                    untagged_ports[vlan_id].append(n)
            else:
                logger.warning("VLAN ID %s not in allowed VLANs.", vlan_id)

    for vlan in allowed_vlans:
        set_env(f"FIXED_PORTS_{vlan}", range_formatter(fixed_ports[vlan]))
        set_env(f"FORBIDDEN_PORTS_{vlan}", range_formatter(forbidden_ports[vlan]))
        set_env(f"UNTAGGED_PORTS_{vlan}", range_formatter(untagged_ports[vlan]))

    logger.debug("Zyxel environment variables prepared.")
    return json_config


def range_formatter(nums: List[int]) -> str:
    """Formats a list of integers into a comma-separated string of ranges.

    Example:
        [1, 2, 3, 5, 7, 8, 9] -> "1-3,5,7-9"

    Args:
        nums: A list of integers.

    Returns:
        A string representing the ranges.
    """
    logger.debug("Formatting ranges: %s", nums)
    if not nums:
        return '""'

    nums.sort()
    res = []
    start = nums[0]
    end = nums[0]

    for num in nums[1:]:
        if num != end + 1:
            res.append(str(start) if start == end else f"{start}-{end}")
            start = num
        end = num
    res.append(str(start) if start == end else f"{start}-{end}")
    formatted_range = ",".join(res)
    logger.debug("Formatted range: %s", formatted_range)
    return formatted_range
