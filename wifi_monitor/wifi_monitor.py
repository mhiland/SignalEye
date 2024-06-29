import os
import time
import logging
import sys

# Add the directory containing your scripts to the sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from scan_wifi import scan_wifi
from parse_networks import parse_networks
from update_networks_list import update_networks_list
from detect_suspicious_networks import detect_suspicious_networks
from load_persistent_networks import load_persistent_networks, save_persistent_networks
from utils import clear_console, print_timestamp, print_networks, print_suspicious_networks

# Configure logging
LOG_FILE = os.path.join(current_dir, 'wifi_monitor.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def monitor_wifi(interval=60):
    persistent_networks = load_persistent_networks()
    while True:
        logging.info("WiFi monitor is running...")
        scan_output = scan_wifi()
        if scan_output:
            current_networks = parse_networks(scan_output)
            update_networks_list(persistent_networks, current_networks)
            save_persistent_networks(persistent_networks)
            clear_console()
            print_timestamp()
            print_networks(persistent_networks)
            suspicious_networks = detect_suspicious_networks(persistent_networks)
            print_suspicious_networks(suspicious_networks)
        
        time.sleep(interval)

if __name__ == "__main__":
    monitor_wifi()
