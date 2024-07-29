import os
import time
import signal
import sys

# Add the directory containing your scripts to the sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import logging 
import logging_config
from scan_wifi import scan_wifi
from parse_networks import parse_networks
from update_networks_list import update_networks_list
from detect_suspicious_networks import detect_suspicious_networks
from load_persistent_networks import load_persistent_networks, save_persistent_networks

def signal_handler(sig, frame):
    print('Graceful shutdown...')
    logging.info("WiFi monitor is stopping...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def monitor_wifi(interval=60):
    persistent_networks = load_persistent_networks()
    logging.info("WiFi monitor is starting...")
    try:
        while True:
            scan_output = scan_wifi()
            if scan_output:
                try:
                    current_networks = parse_networks(scan_output)
                    update_networks_list(persistent_networks, current_networks)
                    save_persistent_networks(persistent_networks)
                    detect_suspicious_networks(persistent_networks)
                except Exception as e:
                    logging.error(f"Error processing networks: {e}")
            else:
                logging.warning("No scan output received")

            time.sleep(interval)
    except KeyboardInterrupt:
        logging.info("WiFi monitor is stopping...")

if __name__ == "__main__":
    monitor_wifi()
