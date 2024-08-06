import os
import re
import json
from parse_oui_database import lookup_manufacturer


def extract_encryption_details(section):
    """ Extract GroupCipher, PairwiseCiphers, and AuthenticationSuites from a section """
    group_cipher = re.search(r'Group Cipher : (\w+)', section)
    group_cipher = group_cipher.group(1) if group_cipher else None

    pairwise_ciphers = re.search(r'Pairwise Ciphers \(\d+\) : ([\w\s]+?)(?=Authentication Suites)', section, re.DOTALL)
    pairwise_ciphers = re.sub(r'\s+', ' ', pairwise_ciphers.group(1)).strip() if pairwise_ciphers else None

    auth_suites_match = re.search(r'Authentication Suites \(\d+\) : ([\w\s()]+)', section, re.DOTALL)
    auth_suites = auth_suites_match.group(1).strip() if auth_suites_match else ""

    return {
        "GroupCipher": group_cipher,
        "PairwiseCiphers": pairwise_ciphers,
        "AuthenticationSuites": ", ".join(auth_suites)
    }, auth_suites


def parse_encryption_info(cell_data):
    encryption_info = {
        "Encryption": "Open",
        'RSN': None
    }

    if "Encryption key:on" in cell_data:
        encryption_info["Encryption"] = "Enabled"

        # Extract WPA2/WPA3 information
        wpa2_info = re.search(r'IE: IEEE 802\.11i/WPA2 Version 1.*?(?=(IE|$))', cell_data, re.DOTALL)
        if wpa2_info:
            wpa2_section = wpa2_info.group(0)
            rsn_details, auth_suites = extract_encryption_details(wpa2_section)
            encryption_info["RSN"] = rsn_details

            if "PSK" in auth_suites:
                if "unknown (8)" in auth_suites:
                    encryption_info["Encryption"] = "WPA2/WPA3"
                elif "unknown (4)" in auth_suites:
                    encryption_info["Encryption"] = "WPA2/FT"
                else:
                    encryption_info["Encryption"] = "WPA2"
            elif "unknown (8)" in auth_suites:
                encryption_info["Encryption"] = "WPA3"


        # Extract WPA information
        wpa_info = re.search(r'IE: WPA Version 1.*?(?=(IE|$))', cell_data, re.DOTALL)
        if wpa_info:
            wpa_section = wpa_info.group(0)
            wpa_details, auth_suites = extract_encryption_details(wpa_section)
            encryption_info["RSN"] = wpa_details
            encryption_info["Encryption"] = "WPA"

        # Check for WEP encryption
        if "Encryption key:on" in cell_data and not (wpa2_info or wpa_info):
            encryption_info["Encryption"] = "WEP"

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
        info["SignalLevel"] = re.search(
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
        additional_info["EncryptionInfo"] = parse_encryption_info(cell_data)
        networks.append(additional_info)

    return networks


if __name__ == "__main__":
    LOG_DIR = os.path.join('/', 'var', 'log', 'wifi_monitor')
    SCAN_FILE = os.path.join(LOG_DIR, 'scan.out')
    with open(SCAN_FILE, 'r', encoding='utf-8') as file:
        network_data = file.read()
    parsed_networks = parse_networks(network_data)
    print(json.dumps(parsed_networks, indent=4))
