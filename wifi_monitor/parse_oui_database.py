import os

# Global dictionary to store the parsed OUI database
oui_dict = {}

# Parse the OUI database file and store it in the global dictionary
def parse_oui_database(file_path):
    global oui_dict
    with open(file_path, 'r') as file:
        for line in file:
            if '(hex)' in line:
                parts = line.split('(hex)')
                oui = parts[0].strip().replace('-', ':')
                manufacturer = parts[1].strip()
                oui_dict[oui] = manufacturer

# Initialize the OUI dictionary by parsing the file once
current_dir = os.path.dirname(os.path.abspath(__file__))
OUI_FILE = os.path.join(current_dir, 'oui.txt')
parse_oui_database(OUI_FILE)

# Lookup the manufacturer using the parsed OUI database
def lookup_manufacturer(mac_address):
    mac_prefix = mac_address.upper()[:8]
    return oui_dict.get(mac_prefix, 'N/A')
