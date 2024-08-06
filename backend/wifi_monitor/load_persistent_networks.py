import os
import json
from jsonschema import validate, ValidationError
from json_schema import schema
import logging
import logging_config
import hashlib
import re

LOG_DIR = os.path.join('/', 'var', 'log', 'wifi_monitor')
TRAINING_DIR = os.path.join('/', 'var', 'log', 'wifi_monitor', 'training_data')
PERSISTENT_FILE = os.path.join(LOG_DIR, 'persistent_networks.json')


def load_persistent_networks():
    if os.path.exists(PERSISTENT_FILE):
        with open(PERSISTENT_FILE, 'r', encoding='utf-8') as f:
            persistent_networks = json.load(f)
            try:
                validate(instance=persistent_networks, schema=schema)
                return persistent_networks
            except ValidationError as e:
                logging.error("Validation error loading persistent networks.")
    return []


def save_persistent_networks(persistent_networks):
    try:
        validate(instance=persistent_networks, schema=schema)
        with open(PERSISTENT_FILE, 'w', encoding='utf-8') as f:
            json.dump(persistent_networks, f, indent=4)
    except ValidationError as e:
        logging.error("Validation error saving persistent networks.")


def save_training_data(networks):
    networks = networks.split('Cell ')[1:]

    if not os.path.exists(TRAINING_DIR):
        os.makedirs(TRAINING_DIR)

    for network in networks:
        # Extract ESSID, BSSID (Address), and Frequency
        essid_match = re.search(r'ESSID:"(.*?)"', network)
        bssid_match = re.search(r'Address: (.*?)\n', network)
        freq_match = re.search(r'Frequency:(\d+\.\d+)', network)

        if essid_match and bssid_match and freq_match:
            essid = essid_match.group(1)
            bssid = bssid_match.group(1)
            freq = freq_match.group(1)

            # Create a unique filename based on the hash of ESSID, BSSID, and Frequency
            unique_str = f"{essid}-{bssid}-{freq}"
            unique_filename = hashlib.sha256(unique_str.encode()).hexdigest() + '.nd'
            file_path = os.path.join(TRAINING_DIR, unique_filename)

            # If the file already exists, skip writing
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(network)
