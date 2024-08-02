import os
import re
import json
from parse_oui_database import lookup_manufacturer


def parse_encryption_info(cell_data):
    encryption_info = {
        "Encryption": "Open",
        'WPA3': None,
        "WPA2": None,
        "WPA": None,
        "WEP": None
    }

    if "Encryption key:on" in cell_data:
        encryption_info["Encryption"] = "Enabled"

        # Extract WPA3 information
        wpa3_info = re.search(r'IE:.*?WPA3.*?(?=IE|$)', cell_data, re.DOTALL)
        if wpa3_info:
            wpa3_section = wpa3_info.group(0)
            group_cipher = re.search(
                r'Group Cipher : (\w+)',
                wpa3_section).group(1)
            pairwise_ciphers_match = re.search(
                r'Pairwise Ciphers \(\d+\) : ([\w\s]+?)(?=Authentication Suites)',
                wpa3_section,
                re.DOTALL)
            pairwise_ciphers = re.sub(
                r'\s+',
                ' ',
                pairwise_ciphers_match.group(1)).strip() if pairwise_ciphers_match else None
            auth_suites = re.search(
                r'Authentication Suites \(\d+\) : (\w+)',
                wpa3_section).group(1)
            encryption_info['WPA3'] = {
                'Group Cipher': group_cipher,
                'Pairwise Ciphers': pairwise_ciphers,
                'Authentication Suites': auth_suites
            }

        # Extract WPA2 information
        wpa2_info = re.search(
            r'IE: IEEE 802\.11i/WPA2 Version 1.*?(?=(IE|$))',
            cell_data,
            re.DOTALL)
        if wpa2_info:
            wpa2_section = wpa2_info.group(0)
            pairwise_ciphers_match = re.search(
                r'Pairwise Ciphers \(\d+\) : ([\w\s]+?)(?=Authentication Suites)',
                wpa2_section,
                re.DOTALL)
            pairwise_ciphers = re.sub(
                r'\s+',
                ' ',
                pairwise_ciphers_match.group(1)).strip() if pairwise_ciphers_match else None
            encryption_info["WPA2"] = {
                "Group Cipher": re.search(
                    r'Group Cipher : (\w+)',
                    wpa2_section).group(1),
                "Pairwise Ciphers": pairwise_ciphers,
                "Authentication Suites": re.search(
                    r'Authentication Suites \(\d+\) : (\w+)',
                    wpa2_section).group(1)}

        # Extract WPA information
        wpa_info = re.search(
            r'IE: WPA Version 1.*?(?=(IE|$))',
            cell_data,
            re.DOTALL)
        if wpa_info:
            wpa_section = wpa_info.group(0)
            pairwise_ciphers_match = re.search(
                r'Pairwise Ciphers \(\d+\) : ([\w\s]+?)(?=Authentication Suites)',
                wpa_section,
                re.DOTALL)
            pairwise_ciphers = re.sub(
                r'\s+',
                ' ',
                pairwise_ciphers_match.group(1)).strip() if pairwise_ciphers_match else None
            encryption_info["WPA"] = {
                "Group Cipher": re.search(
                    r'Group Cipher : (\w+)',
                    wpa_section).group(1),
                "Pairwise Ciphers": pairwise_ciphers,
                "Authentication Suites": re.search(
                    r'Authentication Suites \(\d+\) : (\w+)',
                    wpa_section).group(1)}

        # Check for WEP encryption
        if "Encryption key:on" in cell_data and not (
                wpa3_info or wpa2_info or wpa_info):
            encryption_info["WEP"] = "Enabled"

    return encryption_info


def parse_cell_information(cell_data):
    info = {}
    try:
        essid_match = re.search(r'ESSID:"([^"]*)"', cell_data)
        info["ESSID"] = essid_match.group(1) if essid_match else ""
        address = re.search(r'Address: ([\w:]+)', cell_data).group(1)
        info["Address"] = address
        info["Manufacturer"] = lookup_manufacturer(address)
        info["Frequency"] = re.search(
            r'Frequency:([\d\.]+ GHz)',
            cell_data).group(1).split(' ')[0]
        info["Channel"] = re.search(r'Channel:(\d+)', cell_data).group(1)
        info["Quality"] = re.search(
            r'Quality=([\d/]+)',
            cell_data).group(1).split('/')[0]
        info["Signal Level"] = re.search(
            r'Signal level=([\-\d]+ dBm)',
            cell_data).group(1).split(' ')[0]
        mode = re.search(r'Mode:(\w+)', cell_data).group(1)
        if mode == 'Unknown/bug':
            mode = 'Unknown'
        info["Mode"] = mode
    except AttributeError:
        pass  # Handle cases where one of the regex does not match

    return info


def parse_networks(data):
    networks = []
    cells = data.split('Cell ')[1:]  # Split the data into individual cells

    for cell in cells:
        cell_data = 'Cell ' + cell
        additional_info = parse_cell_information(cell_data)
        additional_info["Encryption Info"] = parse_encryption_info(cell_data)
        networks.append(additional_info)

    return networks


if __name__ == "__main__":
    LOG_DIR = os.path.join('/', 'var', 'log', 'wifi_monitor')
    SCAN_FILE = os.path.join(LOG_DIR, 'scan.out')
    with open(SCAN_FILE, 'r', encoding='utf-8') as file:
        network_data = file.read()
    parsed_networks = parse_networks(network_data)
    print(json.dumps(parsed_networks, indent=4))
