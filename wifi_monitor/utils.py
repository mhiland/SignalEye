import os
from datetime import datetime

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_timestamp():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Last updated: {timestamp}")
    print('=' * 150)

def print_networks(networks):
    print(f"{'SSID':<30} {'Address':<20} {'Manufacturer':<30} {'Frequency':<10} {'Channel':<8} {'Quality':<8} {'Signal Level':<12} {'Encryption':<10} {'Mode':<8} {'Active':<8} {'Last Seen'}")
    print('-' * 150)
    for net in networks:
        ssid = net.get('ESSID', '')
        address = net.get('Address', 'Unknown')
        manufacturer = net.get('Manufacturer', 'N/A')
        frequency = net.get('Frequency', 'Unknown')
        channel = net.get('Channel', 'Unknown')
        quality = net.get('Quality', 'Unknown')
        signal_level = net.get('Signal level', 'Unknown')
        encryption = net.get('Encryption', 'Unknown')
        mode = net.get('Mode', 'Unknown')
        active = net.get('Active', False)
        last_seen = net.get('Last Seen', 'Never')
        print(f"{ssid:<30} {address:<20} {manufacturer:<30} {frequency:<10} {channel:<8} {quality:<8} {signal_level:<12} {encryption:<10} {mode:<8} {str(active):<8} {last_seen}")

def print_suspicious_networks(networks):
    if networks:
        print(f"\n{'Suspicious Networks':<30}")
        print('=' * 100)
        seen_addresses = set()
        for net in networks:
            ssid = net.get('ESSID', '')
            address = net.get('Address', 'Unknown')
            reason = net.get('Reason', 'Unknown')
            if address not in seen_addresses:
                print(f"{ssid:<30} {address:<20} {reason}")
                seen_addresses.add(address)
