import subprocess
import time
import os
from datetime import datetime

def scan_wifi():
    # Using subprocess.run with a timeout to ensure it waits long enough
    try:
        result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], capture_output=True, text=True, timeout=30)
        return result.stdout
    except subprocess.TimeoutExpired:
        print("iwlist scan timed out.")
        return ""

def parse_networks(scan_output):
    networks = []
    lines = scan_output.split('\n')
    current_network = {}
    for line in lines:
        line = line.strip()
        if line.startswith('Cell'):
            if current_network:
                networks.append(current_network)
                current_network = {}
            address = line.split(' ')[4]
            current_network['Address'] = address
        elif 'ESSID' in line:
            essid = line.split(':')[1].strip().strip('"')
            current_network['ESSID'] = essid
        elif 'Frequency' in line:
            frequency = line.split(':')[1].split()[0]
            current_network['Frequency'] = frequency
        elif 'Quality' in line and 'Signal level' in line:
            quality = line.split('=')[1].split('/')[0]
            signal_level = line.split('Signal level=')[1].split(' ')[0]
            current_network['Quality'] = quality
            current_network['Signal level'] = signal_level
        elif 'Channel' in line:
            channel = line.split(':')[1].strip()
            current_network['Channel'] = channel
        elif 'Encryption key' in line:
            encryption = 'WPA/WPA2' if 'on' in line else 'Open'
            current_network['Encryption'] = encryption

    if current_network:
        networks.append(current_network)
    
    return networks

def update_networks_list(persistent_networks, current_networks):
    current_essids = {net['ESSID'] for net in current_networks if 'ESSID' in net}

    for net in persistent_networks:
        net['Active'] = net['ESSID'] in current_essids

    persistent_essids = {net['ESSID'] for net in persistent_networks}
    for current_net in current_networks:
        if 'ESSID' in current_net and current_net['ESSID'] not in persistent_essids:
            current_net['Active'] = True
            persistent_networks.append(current_net)

    persistent_networks.sort(key=lambda x: x['ESSID'].lower())

def monitor_wifi(interval=60):
    persistent_networks = []
    while True:
        scan_output = scan_wifi()
        if scan_output:
            current_networks = parse_networks(scan_output)
            update_networks_list(persistent_networks, current_networks)
            clear_console()
            print_timestamp()
            print_networks(persistent_networks)

        time.sleep(interval)

def print_networks(networks):
    print(f"{'SSID':<30} {'Address':<20} {'Frequency':<10} {'Channel':<8} {'Quality':<8} {'Signal Level':<12} {'Encryption':<10} {'Active'}")
    print('-' * 100)
    for net in networks:
        ssid = net.get('ESSID', 'Unknown')
        address = net.get('Address', 'Unknown')
        frequency = net.get('Frequency', 'Unknown')
        channel = net.get('Channel', 'Unknown')
        quality = net.get('Quality', 'Unknown')
        signal_level = net.get('Signal level', 'Unknown')
        encryption = net.get('Encryption', 'Unknown')
        active = net.get('Active', False)
        print(f"{ssid:<30} {address:<20} {frequency:<10} {channel:<8} {quality:<8} {signal_level:<12} {encryption:<10} {active}")

def print_timestamp():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Last updated: {timestamp}")
    print('=' * 100)

def clear_console():
    # Clear console based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    monitor_wifi()
