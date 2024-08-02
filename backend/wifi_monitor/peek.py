import time
import logging_config
from detect_suspicious_networks import detect_suspicious_networks
from load_persistent_networks import load_persistent_networks
from utils import clear_console, print_timestamp, print_networks, print_suspicious_networks


def monitor_wifi(interval=60):
    persistent_networks = load_persistent_networks()
    try:
        while True:
            persistent_networks = load_persistent_networks()
            clear_console()
            print_timestamp()
            print_networks(persistent_networks)
            suspicious_networks = detect_suspicious_networks(
                persistent_networks)
            print_suspicious_networks(suspicious_networks)
            logging_config.print_last_log_lines()

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nexiting...")


if __name__ == "__main__":
    monitor_wifi()
