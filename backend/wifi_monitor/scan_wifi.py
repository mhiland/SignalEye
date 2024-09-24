import os
import subprocess
import logging
import logging_config


def scan_wifi():
    try:
        wlan_env = os.getenv('WLAN', '0')
        interface = f"wlan{wlan_env}"
        result = subprocess.run(
            ['iwlist', interface, 'scan'], capture_output=True, text=True, timeout=30)
        return result.stdout
    except subprocess.TimeoutExpired:
        logging.warning("iwlist scan timed out.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    return ""



if __name__ == "__main__":
    result = scan_wifi()
    print(result)
    LOG_DIR = os.path.join('/', 'var', 'log', 'wifi_monitor')
    SCAN_FILE = os.path.join(LOG_DIR, 'scan.out')
    with open(SCAN_FILE, 'w', encoding='utf-8') as file:
        file.write(result)
