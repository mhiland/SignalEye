import subprocess
import time
import os
from datetime import datetime


def run_bluetoothctl_command(command, timeout=10):
    try:
        result = subprocess.run(
            ['bluetoothctl'] +
            command.split(),
            capture_output=True,
            text=True,
            timeout=timeout)
        return result.stdout
    except subprocess.TimeoutExpired:
        print(f"Command '{command}' timed out.")
        return ""


def scan_bluetooth():
    # Ensure the Bluetooth device is powered on
    run_bluetoothctl_command('power on')
    # Make sure the agent is active
    run_bluetoothctl_command('agent on')
    # Start a Bluetooth scan
    run_bluetoothctl_command('scan on')
    # Give it some time to discover devices
    time.sleep(10)
    # Stop the scan
    run_bluetoothctl_command('scan off')
    # Get the list of devices
    result = run_bluetoothctl_command('devices', timeout=30)
    return result


def get_device_info(address):
    result = run_bluetoothctl_command(f'info {address}', timeout=10)
    return result


def parse_devices(scan_output):
    devices = []
    lines = scan_output.split('\n')
    for line in lines:
        if line.startswith('Device'):
            parts = line.split(' ')
            address = parts[1]
            name = ' '.join(parts[2:]).strip()
            device_info = get_device_info(address)
            rssi = 'Unknown'
            alias = 'Unknown'
            for info_line in device_info.split('\n'):
                if 'RSSI' in info_line:
                    rssi = info_line.split(':')[1].strip()
                if 'Alias' in info_line:
                    alias = info_line.split(':')[1].strip()
            devices.append({'Name': name, 'Alias': alias,
                           'Address': address, 'RSSI': rssi})
    return devices


def update_devices_list(persistent_devices, current_devices):
    current_addresses = {device['Address'] for device in current_devices}

    for device in persistent_devices:
        device['Active'] = device['Address'] in current_addresses

    persistent_addresses = {device['Address'] for device in persistent_devices}
    for current_device in current_devices:
        if current_device['Address'] not in persistent_addresses:
            current_device['Active'] = True
            persistent_devices.append(current_device)

    persistent_devices.sort(key=lambda x: x['Name'].lower())


def monitor_bluetooth(interval=60):
    persistent_devices = []
    while True:
        scan_output = scan_bluetooth()
        if scan_output:
            current_devices = parse_devices(scan_output)
            update_devices_list(persistent_devices, current_devices)
            clear_console()
            print_timestamp()
            print_devices(persistent_devices)

        time.sleep(interval)


def print_devices(devices):
    print(f"{'Name':<30} {'Alias':<30} {'Address':<20} {'RSSI':<10} {'Active'}")
    print('-' * 120)
    for device in devices:
        name = device.get('Name', 'Unknown')
        alias = device.get('Alias', 'Unknown')
        address = device.get('Address', 'Unknown')
        rssi = device.get('RSSI', 'Unknown')
        active = device.get('Active', False)
        print(f"{name:<30} {alias:<30} {address:<20} {rssi:<10} {active}")


def print_timestamp():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Last updated: {timestamp}")
    print('=' * 120)


def clear_console():
    # Clear console based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    monitor_bluetooth()
