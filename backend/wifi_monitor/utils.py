import os
from datetime import datetime, timedelta


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_timestamp():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Last updated: {timestamp}")
    print('=' * 150)


def print_networks(networks):
    now = datetime.now()
    time_window = timedelta(days=1)

    recent_networks = []
    remaining_networks = []

    for network in networks:
        last_seen_time = network.get('Last Seen', 'Never')
        if last_seen_time != 'Never':
            try:
                # Convert string to datetime
                last_seen_time = datetime.strptime(
                    last_seen_time, '%Y-%m-%d %H:%M:%S')
                if last_seen_time >= now - time_window:
                    recent_networks.append(network)
                else:
                    remaining_networks.append(network)
            except ValueError:
                # Handle unexpected format of last_seen_time here if needed
                remaining_networks.append(network)
        else:
            remaining_networks.append(network)

    # Print recent networks
    print(f"Networks seen within the last {time_window.days} days:")
    print_networks2(recent_networks)

    # Print remaining networks
    print("\nOlder networks:")
    print_networks2(remaining_networks)


class NetworkAdapter:
    def __init__(self, details):
        self.details = details

    def get_encryption(self):
        encryption_info = self.details.get('Encryption Info', {})
        encryption_status = encryption_info.get('Encryption', 'Unknown')

        if encryption_status == 'Enabled':
            encryption_types = []

            wpa3_info = encryption_info.get('WPA3')
            wpa2_info = encryption_info.get('WPA2')
            wpa_info = encryption_info.get('WPA')
            wep_info = encryption_info.get('WEP')

            if wpa3_info is not None:
                encryption_types.append("WPA3")
            if wpa2_info is not None:
                encryption_types.append("WPA2")
            if wpa_info is not None:
                encryption_types.append("WPA")
            if wep_info is not None and wep_info == "Enabled":
                encryption_types.append("WEP")
            if encryption_types:
                return ",".join(encryption_types)
            return "Unknown"
        return "Open"


def print_networks2(networks):
    max_manufacturer_length = 27
    print(f"{'SSID':<30} {'Address':<20} {'Manufacturer':<30} {'Frequency':<10} {'Channel':<8} {'Quality':<8} {'Signal Level':<12} {'Encryption':<10} {'Mode':<8} {'Active':<8} {'First Seen':<20} {'Last Seen':<20}")
    print('-' * 150)
    seen_addresses = set()
    for net in networks:
        ssid = net.get('ESSID', '')
        address = net.get('Address', 'Unknown')
        manufacturer = net.get('Manufacturer', 'N/A')[:max_manufacturer_length]
        frequency = net.get('Frequency', 'Unknown')
        channel = net.get('Channel', 'Unknown')
        quality = net.get('Quality', 'Unknown')
        signal_level = net.get('Signal Level', 'Unknown')
        network = NetworkAdapter(net)
        encryption = network.get_encryption()
        mode = net.get('Mode', 'Unknown')
        active = net.get('Active', False)
        first_seen = net.get('First Seen', 'Never')
        last_seen = net.get('Last Seen', 'Never')
        if (ssid, address) not in seen_addresses:
            print(f"{ssid:<30} {address:<20} {manufacturer:<30} {frequency:<10} {channel:<8} {quality:<8} {signal_level:<12} {encryption:<10} {mode:<8} {str(active):<8} {first_seen:<20} {last_seen:<20}")
            seen_addresses.add((ssid, address))


def print_suspicious_networks(networks):
    if networks:
        print(f"\n{'Suspicious Networks':<30}")
        print('=' * 100)
        seen_addresses = set()
        for net in networks:
            ssid = net.get('ESSID', '')
            address = net.get('Address', 'Unknown')
            reason = net.get('Reason', 'Unknown')
            if (ssid, address) not in seen_addresses:
                print(f"{ssid:<30} {address:<20} {reason}")
                seen_addresses.add((ssid, address))
