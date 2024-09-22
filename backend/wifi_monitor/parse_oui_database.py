import os
import re
import json
from difflib import SequenceMatcher
import logging
import logging_config


class OUILookup:
    def __init__(self):
        self.oui_dict = {}
        self.exact_match_dict = {}
        self.log_dir = os.path.join('/', 'var', 'log', 'wifi_monitor')
        self.exact_match_file = os.path.join(self.log_dir, 'oui_known.json')

        try:
            self.current_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            # Fallback if __file__ is not defined
            self.current_dir = os.getcwd()

        self.oui_file = os.path.join(self.current_dir, 'data', 'oui.txt')

        # Initialize the OUI dictionary and exact match dictionary
        self.parse_oui_database(self.oui_file)
        self.parse_exact_matches(self.exact_match_file)

    # Parse the OUI database file and store it in the global dictionary
    def parse_oui_database(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if '(hex)' in line:
                        parts = line.split('(hex)')
                        oui = parts[0].strip().replace('-', ':')
                        manufacturer = parts[1].strip()
                        self.oui_dict[oui] = manufacturer
        except FileNotFoundError:
            logging.debug(f"File not found: {file_path}")
        except Exception as e:
            logging.debug(f"Error reading OUI file: {e}")

    # Parse the exact matches file and store it in a separate dictionary
    def parse_exact_matches(self, file_path):
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        self.exact_match_dict = json.load(file)
                    except json.JSONDecodeError:
                        self.exact_match_dict = {}
            except Exception as e:
                logging.debug(
                    f"Error loading exact matches from {file_path}: {e}")
        else:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    # Create an empty JSON file if it doesn't exist
                    json.dump({}, file)
            except Exception as e:
                logging.debug(f"Error creating exact match file: {e}")

    # Write a new exact match to the file and dictionary
    def write_exact_match(self, mac_address, manufacturer, essid=None):
        mac_address = mac_address.upper()
        if mac_address not in self.exact_match_dict:
            self.exact_match_dict[mac_address] = {
                'manufacturer': manufacturer, 'essid': essid}
            try:
                with open(self.exact_match_file, 'w', encoding='utf-8') as file:
                    json.dump(self.exact_match_dict, file, indent=4)
            except Exception as e:
                logging.debug(f"Error writing to exact match file: {e}")

    def is_mac_address(self, string):
        mac_pattern = re.compile(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$")
        return mac_pattern.match(string) is not None

    def similarity(self, str1, str2):
        if self.is_mac_address(str1) and self.is_mac_address(str2):
            str1 = str1.replace(':', '')
            str2 = str2.replace(':', '')
        return SequenceMatcher(None, str1, str2).ratio()

    # Lookup the manufacturer using the parsed OUI database or exact match
    # variations
    def lookup_manufacturer(self, mac_address, essid=None):
        mac_address = mac_address.upper()
        mac_prefix = mac_address[:8]

        # Step 1: OUI lookup using the prefix
        if mac_prefix in self.oui_dict:
            manufacturer = self.oui_dict[mac_prefix]
            self.write_exact_match(mac_address, manufacturer, essid)
            return manufacturer

        # Step 2: Calculate combined similarity scores based on MAC and ESSID
        best_match = None
        highest_score = 0.0

        for stored_mac, details in self.exact_match_dict.items():
            stored_manufacturer = details['manufacturer']
            stored_essid = details.get('essid', '')
            mac_similarity_score = self.similarity(mac_address, stored_mac)
            essid_similarity_score = self.similarity(
                essid, stored_essid) if essid and stored_essid else 0

            # Combined score, equally weighted
            combined_score = (
                mac_similarity_score + essid_similarity_score) / 2

            if combined_score > highest_score:
                highest_score = combined_score
                best_match = (stored_manufacturer, combined_score)

        # Return the best match with the highest score
        if best_match and highest_score > 0.4:
            return f"{best_match[0]}* (Combined Score: {highest_score:.2f})"

        return 'N/A'
