import os
import codecs
import re
import json
from parse_oui_database import OUILookup
import logging
import logging_config


def parse_encryption_info(cell_data):
    encryption_info = {
        "Encryption": "Open",
        "RSN": None
    }

    if "Encryption key:on" in cell_data:
        # Default to Enabled if encryption key is on
        encryption_info["Encryption"] = "Enabled"

        # Extract WPA2/WPA3 information
        wpa2_info = re.search(r'IE: IEEE 802\.11i/WPA2 Version 1.*?(?=(IE|$))', cell_data, re.DOTALL)
        if wpa2_info:
            wpa2_section = wpa2_info.group(0)
            rsn_details, auth_suites = extract_encryption_details(wpa2_section)
            encryption_info["RSN"] = rsn_details

            # Determine WPA2, WPA3, or FT based on Authentication Suites
            if auth_suites:
                if "PSK" in auth_suites:
                    if "unknown (8)" in auth_suites:
                        encryption_info["Encryption"] = "WPA2/WPA3"
                    elif "unknown (4)" in auth_suites:
                        encryption_info["Encryption"] = "WPA2/FT"
                    else:
                        encryption_info["Encryption"] = "WPA2"
                elif "unknown (8)" in auth_suites:
                    encryption_info["Encryption"] = "WPA3"
                elif "802.1x" in auth_suites:
                    encryption_info["Encryption"] = "WPA2"

        # Extract WPA information
        wpa_info = re.search(r'IE: WPA Version 1.*?(?=(IE|$))', cell_data, re.DOTALL)
        if wpa_info:
            wpa_section = wpa_info.group(0)
            wpa_details, auth_suites = extract_encryption_details(wpa_section)
            encryption_info["RSN"] = wpa_details
            encryption_info["Encryption"] = "WPA"

        # Check for WEP encryption (fall-back if no WPA/WPA2/WPA3 found)
        if not wpa2_info and not wpa_info:
            encryption_info["Encryption"] = "WEP"

    return encryption_info


def extract_encryption_details(section):
    """ Extract GroupCipher, PairwiseCiphers, and AuthenticationSuites from a section """
    group_cipher = re.search(r'Group Cipher : (\w+)', section)
    group_cipher = group_cipher.group(1) if group_cipher else None

    pairwise_ciphers = re.search(r'Pairwise Ciphers \(\d+\) : ([\w\s]+?)(?=\n|Authentication Suites)', section, re.DOTALL)
    pairwise_ciphers = re.sub(r'\s+', ' ', pairwise_ciphers.group(1)).strip() if pairwise_ciphers else None

    auth_suites_match = re.search(r'Authentication Suites \(\d+\) : ([\w\s/.(),]+)', section, re.DOTALL)
    if auth_suites_match:
        auth_suites = auth_suites_match.group(1).strip()
    else:
        auth_suites = None

    return {
        "GroupCipher": group_cipher,
        "PairwiseCiphers": pairwise_ciphers,
        "AuthenticationSuites": auth_suites
    }, auth_suites


def clean_ssid_string(ssid: str) -> str:
    try:
        hex_pattern = re.compile(r'\\x[0-9A-Fa-f]{2}')
        if hex_pattern.search(ssid):
            decoded_ssid = codecs.decode(ssid.encode(), 'unicode_escape').decode('utf-8')
            return decoded_ssid
        return ssid
    except Exception as e:
        logging.error(f"Error decoding SSID ({ssid}): {e}")
        return ssid


def parse_cell_information(cell_data):
    info = {}
    try:
        # Extract ESSID
        essid_match = re.search(r'ESSID:"([^"]*)"', cell_data)
        raw_essid = essid_match.group(1) if essid_match else ""
        info["ESSID"] = clean_ssid_string(raw_essid)

        # Extract MAC Address (BSSID)
        address_match = re.search(r'Address: ([\w:]+)', cell_data)
        info["Address"] = address_match.group(1) if address_match else ""

        # Lookup Manufacturer based on MAC Address
        _ouilookup_instance = OUILookup()
        info["Manufacturer"] = _ouilookup_instance.lookup_manufacturer(info["Address"], info["ESSID"] )

        # Extract Frequency
        frequency_match = re.search(r'Frequency:([\d\.]+ GHz)', cell_data)
        info["Frequency"] = frequency_match.group(1).split(' ')[0] if frequency_match else ""

        # Extract Channel
        channel_match = re.search(r'Channel:(\d+)', cell_data)
        info["Channel"] = channel_match.group(1) if channel_match else ""

        # Extract Quality
        quality_match = re.search(r'Quality=([\d/]+)', cell_data)
        info["Quality"] = quality_match.group(1).split('/')[0] if quality_match else ""

        # Extract Signal Level
        signal_level_match = re.search(r'Signal level=([\-\d]+ dBm)', cell_data)
        info["SignalLevel"] = signal_level_match.group(1).split(' ')[0] if signal_level_match else ""

        # Extract Mode
        mode_match = re.search(r'Mode:(\w+)', cell_data)
        mode = mode_match.group(1) if mode_match else "Unknown"
        if mode == 'Unknown/bug':
            mode = 'Unknown'
        info["Mode"] = mode
    except AttributeError as e:
        logging.error(f"An error occurred while parsing cell information. {e}")
        logging.debug(f"Cell data causing error: {cell_data}")

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
