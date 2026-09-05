import getpass
import re

from .connection import investigate_device
from .utils import normalize_mac, validate_ip


BANNER = r"""
███╗   ███╗ █████╗  ██████╗
████╗ ████║██╔══██╗██╔════╝
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║╚██████╗
╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝

        I N V E S T I G A T O R
        Network MAC Discovery Tool
"""


VENDORS = {
    "1": ("Cisco", "cisco_ios"),
    "2": ("Juniper", "juniper"),
    "3": ("Arista", "arista_eos"),
}


def normalize_mac(mac):
    """
    Normalize a MAC address to Cisco-style format:
    0011.2233.4455
    """

    cleaned = re.sub(r"[^0-9a-fA-F]", "", mac)

    if len(cleaned) != 12:
        raise ValueError("Invalid MAC address")

    if not re.fullmatch(r"[0-9a-fA-F]{12}", cleaned):
        raise ValueError("Invalid MAC address")

    return ".".join(
        cleaned[i:i + 4].lower()
        for i in range(0, 12, 4)
    )


def ask_vendor():
    """Ask the user to select the network vendor."""

    while True:
        print("\nSelect network device type:\n")
        print("[1] Cisco")
        print("[2] Juniper")
        print("[3] Arista")

        choice = input("\nChoice: ").strip()

        if choice in VENDORS:
            return VENDORS[choice]

        print("\n[ERROR] Invalid choice.")
        print("Please select 1, 2, or 3.")


def ask_credentials():
    """Ask for SSH credentials."""

    print("\n" + "-" * 60)
    print("                    SSH CREDENTIALS")
    print("-" * 60)

    username = input("\nUsername: ").strip()
    password = getpass.getpass("Password: ")

    return username, password


def ask_mac():
    """Ask for and validate the target MAC address."""

    while True:
        mac = input("\nMAC address to investigate: ").strip()

        try:
            normalized = normalize_mac(mac)

            print(f"[+] Target MAC: {normalized}")

            return normalized

        except ValueError:
            print("\n[ERROR] Invalid MAC address.")
            print("Accepted formats:")
            print("  00:11:22:33:44:55")
            print("  00-11-22-33-44-55")
            print("  0011.2233.4455")
            print("  001122334455")


def validate_ip(ip):
    """Validate an IPv4 or IPv6 address."""

    import ipaddress

    try:
        ipaddress.ip_address(ip)
        return True

    except ValueError:
        return False


def load_csv():
    """Load device IP addresses from a CSV file."""

    import csv
    from pathlib import Path

    while True:

        path = input("\nCSV file path: ").strip()

        file = Path(path)

        if not file.exists():
            print(f"[ERROR] CSV file not found: {path}")
            continue

        try:

            with file.open(
                "r",
                encoding="utf-8-sig",
                newline=""
            ) as csv_file:

                reader = csv.DictReader(csv_file)

                if not reader.fieldnames:
                    print("[ERROR] CSV file is empty.")
                    continue

                # Allow "ip" regardless of capitalization.
                ip_column = None

                for column in reader.fieldnames:

                    if column.strip().lower() == "ip":
                        ip_column = column
                        break

                if ip_column is None:
                    print("[ERROR] CSV must contain an 'ip' column.")
                    continue

                devices = []

                for row in reader:

                    ip = row.get(ip_column, "").strip()

                    if not ip:
                        continue

                    if not validate_ip(ip):

                        print(
                            f"[WARNING] Invalid IP ignored: {ip}"
                        )

                        continue

                    if ip not in devices:
                        devices.append(ip)

                if not devices:

                    print(
                        "[ERROR] No valid IP addresses "
                        "found in CSV."
                    )

                    continue

                print(
                    f"\n[+] Loaded {len(devices)} "
                    "devices from CSV."
                )

                return devices

        except Exception as error:

            print(
                f"[ERROR] Could not read CSV: {error}"
            )


def load_manual_ips():
    """Ask the user to manually enter device IPs."""

    print("\nEnter device IP addresses.")
    print("Press ENTER on an empty line when finished.\n")

    devices = []

    while True:

        ip = input("IP: ").strip()

        # Empty line = finished.
        if not ip:
            break

        if not validate_ip(ip):

            print("[ERROR] Invalid IP address.")
            continue

        if ip not in devices:
            devices.append(ip)

        else:
            print("[WARNING] IP already added.")

    return devices


def ask_devices():
    """Choose CSV or manual IP input."""

    while True:

        print("\n" + "-" * 60)
        print("                  DEVICE INPUT")
        print("-" * 60)

        print("\nHow do you want to provide the network devices?\n")

        print("[1] CSV file")
        print("[2] Enter IP addresses manually")

        choice = input("\nChoice: ").strip()

        if choice == "1":

            return load_csv()

        if choice == "2":

            devices = load_manual_ips()

            if devices:

                print(
                    f"\n[+] Loaded {len(devices)} devices."
                )

                return devices

            print(
                "[ERROR] No IP addresses provided."
            )

            continue

        print(
            "[ERROR] Invalid choice. "
            "Select 1 or 2."
        )


def print_starting_screen(
    vendor,
    mac,
    devices,
):
    """Display investigation information."""

    print("\n" + "=" * 60)
    print("                 STARTING INVESTIGATION")
    print("=" * 60)

    print(f"\nTarget MAC : {mac}")
    print(f"Devices    : {len(devices)}")
    print(f"Platform   : {vendor}")

    print("\n" + "-" * 60)


def print_result(result):
    """Display a successful MAC discovery."""

    print("\n" + "=" * 60)
    print("                    MAC FOUND")
    print("=" * 60)

    print(f"\nMAC Address : {result['mac']}")
    print("Status      : FOUND")

    print("\nDevice")
    print("-" * 60)

    print(f"IP          : {result['device_ip']}")
    print(f"Hostname    : {result['hostname']}")
    print(f"Vendor      : {result['vendor']}")

    print("\nMAC Details")
    print("-" * 60)

    print(f"VLAN        : {result['vlan']}")
    print(f"Interface   : {result['interface']}")
    print(f"Type        : {result['type']}")


def print_not_found(mac, devices_count):
    """Display a MAC-not-found result."""

    print("\n" + "=" * 60)
    print("                  MAC NOT FOUND")
    print("=" * 60)

    print(f"\nMAC Address : {mac}")
    print(f"Devices     : {devices_count}")
    print(
        "Result      : "
        "No matching MAC address was found."
    )


def print_summary(
    mac,
    devices,
    successful_ssh,
    failed_ssh,
    results,
):
    """Display final investigation summary."""

    print("\n" + "=" * 60)
    print("                    INVESTIGATION SUMMARY")
    print("=" * 60)

    print(f"\nTarget MAC       : {mac}")
    print(f"Devices checked  : {len(devices)}")
    print(f"Successful SSH   : {successful_ssh}")
    print(f"Failed SSH       : {failed_ssh}")
    print(
        f"MAC found        : "
        f"{'YES' if results else 'NO'}"
    )
    print(f"Results          : {len(results)}")

    print("\n" + "=" * 60)


def run_investigation(
    vendor,
    username,
    password,
    mac,
    devices,
):
    """Run the MAC investigation against every device."""

    results = []
    failures = []

    for index, ip in enumerate(devices, start=1):

        print(
            f"\n[{index}/{len(devices)}] "
            f"Connecting to {ip} ........"
        )

        result = investigate_device(
            ip=ip,
            vendor=vendor,
            username=username,
            password=password,
            mac=mac,
        )

        if result["status"] == "error":

            print(
                f"[ERROR] {ip} - "
                f"{result['error']}"
            )

            failures.append(
                {
                    "ip": ip,
                    "error": result["error"],
                }
            )

            continue

        if result["results"]:

            print(
                f"[FOUND] MAC found on {ip}"
            )

            for entry in result["results"]:

                results.append(entry)

        else:

            print(
                f"[OK] {ip} - MAC not found"
            )

    return results, failures


def run():
    """Main MAC Investigator application."""

    print(BANNER)

    print("=" * 60)
    print("                 MAC INVESTIGATOR")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Vendor
    # ---------------------------------------------------------

    vendor, device_type = ask_vendor()

    print(f"\n[+] Selected: {vendor}")

    # device_type is already handled by connection.py.
    _ = device_type

    # ---------------------------------------------------------
    # 2. Credentials
    # ---------------------------------------------------------

    username, password = ask_credentials()

    # ---------------------------------------------------------
    # 3. MAC
    # ---------------------------------------------------------

    mac = ask_mac()

    # ---------------------------------------------------------
    # 4. Devices
    # ---------------------------------------------------------

    devices = ask_devices()

    # ---------------------------------------------------------
    # 5. Start investigation
    # ---------------------------------------------------------

    print_starting_screen(
        vendor=vendor,
        mac=mac,
        devices=devices,
    )

    # ---------------------------------------------------------
    # 6. Run investigation
    # ---------------------------------------------------------

    results, failures = run_investigation(
        vendor=vendor,
        username=username,
        password=password,
        mac=mac,
        devices=devices,
    )

    # ---------------------------------------------------------
    # 7. Display results
    # ---------------------------------------------------------

    if results:

        print("\n")

        for result in results:
            print_result(result)

    else:

        print_not_found(
            mac=mac,
            devices_count=len(devices),
        )

    # ---------------------------------------------------------
    # 8. Summary
    # ---------------------------------------------------------

    successful_ssh = len(devices) - len(failures)

    print_summary(
        mac=mac,
        devices=devices,
        successful_ssh=successful_ssh,
        failed_ssh=len(failures),
        results=results,
    )

