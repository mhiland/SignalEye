import os
import logging

APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(APP_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'wifi_monitor.log')
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def print_last_log_lines():
    try:
        print(f"\n{'Logs':<30}")
        print('=' * 100)
        num_lines=5
        with open(LOG_FILE, 'r') as file:
            lines = file.readlines()
            print("".join(lines[-num_lines:]))
    except FileNotFoundError:
        print(f"Log file {LOG_FILE} not found")
    except Exception as e:
        print(f"Error reading log file: {e}")