# macinvest/utils.py

import ipaddress
import re


def normalize_mac(mac):
    """Normalize a MAC address to Cisco dotted format."""
    cleaned = re.sub(r"[^0-9a-fA-F]", "", mac)

    if len(cleaned) != 12:
        raise ValueError("Invalid MAC address")

    return ".".join(
        cleaned[i:i + 4].lower()
        for i in range(0, 12, 4)
    )


def validate_ip(ip):
    """Return True if the value is a valid IPv4/IPv6 address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def clean_hostname(prompt):
    """Clean a network device CLI prompt."""
    return prompt.strip().rstrip("#>").strip()