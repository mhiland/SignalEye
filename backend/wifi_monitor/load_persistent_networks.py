import os
import json
from jsonschema import validate, ValidationError
from json_schema import schema
import logging
import logging_config

LOG_DIR = os.path.join('/', 'var', 'log', 'wifi_monitor')
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
