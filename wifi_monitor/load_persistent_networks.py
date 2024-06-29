import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
PERSISTENT_FILE = os.path.join(current_dir, 'persistent_networks.json')

def load_persistent_networks():
    if os.path.exists(PERSISTENT_FILE):
        with open(PERSISTENT_FILE, 'r') as f:
            return json.load(f)
    return []

def save_persistent_networks(persistent_networks):
    with open(PERSISTENT_FILE, 'w') as f:
        json.dump(persistent_networks, f, indent=4)
