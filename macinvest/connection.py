from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)

from .mac_lookup import get_mac_command
from .parsers import parse_mac_output
from .utils import clean_hostname

def investigate_device(
    ip,
    vendor,
    username,
    password,
    mac,
):
    device_types = {
        "Cisco": "cisco_ios",
        "Juniper": "juniper",
        "Arista": "arista_eos",
    }

    device = {
        "device_type": device_types[vendor],
        "host": ip,
        "username": username,
        "password": password,
        "conn_timeout": 8,
        "auth_timeout": 8,
        "banner_timeout": 8,
    }

    connection = None

    try:
        connection = ConnectHandler(**device)

        hostname = clean_hostname(connection.find_prompt())
        hostname = hostname.rstrip("#>").strip()

        command = get_mac_command(vendor, mac)

        output = connection.send_command(command)

        parsed_results = parse_mac_output(
            vendor,
            output,
            mac,
        )

        results = []

        for result in parsed_results:
            result["device_ip"] = ip
            result["hostname"] = hostname
            result["vendor"] = vendor

            results.append(result)

        return {
            "status": "success",
            "results": results,
            "error": None,
        }

    except NetmikoAuthenticationException:
        return {
            "status": "error",
            "results": [],
            "error": "Authentication failed",
        }

    except NetmikoTimeoutException:
        return {
            "status": "error",
            "results": [],
            "error": "Connection timeout",
        }

    except Exception as e:
        return {
            "status": "error",
            "results": [],
            "error": str(e),
        }

    finally:
        if connection:
            connection.disconnect()