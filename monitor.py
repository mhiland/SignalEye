import subprocess
import time
import os
from datetime import datetime
import json

PERSISTENT_FILE = 'persistent_networks.json'

def scan_wifi():
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
        if net['ESSID'] in current_essids:
            net['Active'] = True
            net['Last Seen'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            net['Active'] = False

    persistent_essids = {net['ESSID'] for net in persistent_networks}
    for current_net in current_networks:
        if 'ESSID' in current_net and current_net['ESSID'] not in persistent_essids:
            current_net['Active'] = True
            current_net['Last Seen'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            persistent_networks.append(current_net)

    persistent_networks.sort(key=lambda x: x['ESSID'].lower() if x['ESSID'] else "")

def detect_suspicious_networks(networks):
    ssid_counts = {}
    suspicious_networks = []
    seen_addresses = set()

    for net in networks:
        ssid = net.get('ESSID', '')
        encryption = net.get('Encryption', 'Unknown')
        address = net.get('Address', 'Unknown')
        
        # Check for multiple networks with the same SSID
        if ssid not in ssid_counts:
            ssid_counts[ssid] = []
        ssid_counts[ssid].append(address)

        # Check for open networks
        if encryption == 'Open' and address not in seen_addresses:
            net['Suspicious'] = True
            net['Reason'] = 'Open network'
            suspicious_networks.append(net)
            seen_addresses.add(address)

        # Check for very short or unusual SSID names
        if len(ssid) < 3 and ssid and address not in seen_addresses:
            net['Suspicious'] = True
            net['Reason'] = 'Short or unusual SSID name'
            suspicious_networks.append(net)
            seen_addresses.add(address)

    # Add networks with duplicate SSIDs to suspicious list
    for ssid, addresses in ssid_counts.items():
        if len(addresses) > 1:
            for net in networks:
                if net['ESSID'] == ssid and net['Address'] not in seen_addresses:
                    net['Suspicious'] = True
                    net['Reason'] = 'SSID spoofing'
                    suspicious_networks.append(net)
                    seen_addresses.add(net['Address'])

    return suspicious_networks

def load_persistent_networks():
    if os.path.exists(PERSISTENT_FILE):
        with open(PERSISTENT_FILE, 'r') as f:
            return json.load(f)
    return []

def save_persistent_networks(persistent_networks):
    with open(PERSISTENT_FILE, 'w') as f:
        json.dump(persistent_networks, f, indent=4)

def monitor_wifi(interval=60):
    persistent_networks = load_persistent_networks()
    while True:
        scan_output = scan_wifi()
        if scan_output:
            current_networks = parse_networks(scan_output)
            update_networks_list(persistent_networks, current_networks)
            save_persistent_networks(persistent_networks)
            clear_console()
            print_timestamp()
            print_networks(persistent_networks)
            suspicious_networks = detect_suspicious_networks(persistent_networks)
            print_suspicious_networks(suspicious_networks)

        time.sleep(interval)

def print_networks(networks):
    print(f"{'SSID':<30} {'Address':<20} {'Frequency':<10} {'Channel':<8} {'Quality':<8} {'Signal Level':<12} {'Encryption':<10} {'Active':<8} {'Last Seen'}")
    print('-' * 120)
    for net in networks:
        ssid = net.get('ESSID', '')
        address = net.get('Address', 'Unknown')
        frequency = net.get('Frequency', 'Unknown')
        channel = net.get('Channel', 'Unknown')
        quality = net.get('Quality', 'Unknown')
        signal_level = net.get('Signal level', 'Unknown')
        encryption = net.get('Encryption', 'Unknown')
        active = net.get('Active', False)
        last_seen = net.get('Last Seen', 'Never')
        print(f"{ssid:<30} {address:<20} {frequency:<10} {channel:<8} {quality:<8} {signal_level:<12} {encryption:<10} {str(active):<8} {last_seen}")

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

def print_timestamp():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Last updated: {timestamp}")
    print('=' * 120)

def clear_console():
    # Clear console based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    monitor_wifi()
