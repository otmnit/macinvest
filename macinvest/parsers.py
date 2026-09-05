import re


def parse_mac_output(vendor, output, mac):
    results = []

    if vendor in ("Cisco", "Arista"):
        for line in output.splitlines():

            if mac.lower() not in line.lower():
                continue

            parts = line.split()

            if len(parts) < 4:
                continue

            results.append({
                "mac": mac,
                "vlan": parts[0],
                "type": parts[-2],
                "interface": parts[-1],
            })

    elif vendor == "Juniper":
        for line in output.splitlines():

            if mac.lower() not in line.lower():
                continue

            parts = line.split()

            if len(parts) < 2:
                continue

            results.append({
                "mac": mac,
                "vlan": parts[0],
                "type": "UNKNOWN",
                "interface": parts[-1],
            })

    return results