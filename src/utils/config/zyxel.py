import re
from typing import List

from utils.environ import set_env


def prepare_zyxel_environs(json_config):
    allowed_vlan = [
        "2",
        "3",
        "4",
        "5",
        "30",
    ]
    fixed = {vlan: [] for vlan in allowed_vlan}
    forbidden = {vlan: [] for vlan in allowed_vlan}
    untagged = {vlan: [] for vlan in allowed_vlan}

    interfaces = filter(
        lambda item: item[1]["type"] == "interface", json_config.items()
    )
    for interface_id, info in interfaces:  # interface_id - 'port-channel N'
        N = int(interface_id.split()[-1])
        for _, L in forbidden.items():
            L.append(N)
        for vlan_id in re.findall(r"pvid (\d+)", info["text"]):
            fixed[vlan_id].append(N)
            forbidden[vlan_id].remove(N)

            # `frame-type tagged` occurs (optional) only if PVID is single
            if "frame-type tagged" not in info["text"]:
                untagged[vlan_id].append(N)

    for vlan in allowed_vlan:
        set_env(f"FIXED_PORTS_{vlan}", range_formatter(fixed[vlan]))
        set_env(f"FORBIDDEN_PORTS_{vlan}", range_formatter(forbidden[vlan]))
        set_env(f"UNTAGGED_PORTS_{vlan}", range_formatter(untagged[vlan]))
    return json_config


# TODO: стоит переместить эту функцию в другое место
# если необходимо использовать ее где-то еще.
def range_formatter(nums: List[int]) -> str:
    if not nums:
        return '""'
    res = []
    prev = nums[0]
    cur_first = nums[0]
    for num in nums[1:]:
        if num - 1 != prev:
            if cur_first == prev:
                res.append(str(prev))
            else:
                res.append(f"{cur_first}-{prev}")
            cur_first = num
        prev = num

    if cur_first == prev:
        res.append(str(prev))
    else:
        res.append(f"{cur_first}-{prev}")
    return ",".join(res)
