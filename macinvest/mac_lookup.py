def get_mac_command(vendor, mac):
    commands = {
        "Cisco": f"show mac address-table address {mac}",
        "Arista": f"show mac address-table address {mac}",
        "Juniper": f"show ethernet-switching table | match {mac}",
    }

    return commands[vendor]