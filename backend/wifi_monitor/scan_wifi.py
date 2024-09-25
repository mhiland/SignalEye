import os
import subprocess
import logging
import logging_config
import time

def scan_wifi():
    attempt = 0
    max_attempts = 3
    sleep_duration_seconds = 5

    wlan_env = os.getenv('WLAN', '0')
    interface = f"wlan{wlan_env}"

    while attempt < max_attempts:
        try:
            result = subprocess.run(
                ['iwlist', interface, 'scan'], capture_output=True, text=True, timeout=30)
            if result.returncode == 255:
                attempt += 1
                if attempt < max_attempts:
                    time.sleep(sleep_duration_seconds)
                    continue
            elif result.returncode != 0:
                logging.warning(f"iwlist scan failed with return code {result.returncode}.")
                return ""

            return result.stdout

        except subprocess.TimeoutExpired:
            logging.warning("iwlist scan timed out.")
            attempt += 1
            if attempt < max_attempts:
                time.sleep(sleep_duration_seconds)
                continue

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            attempt += 1
            if attempt < max_attempts:
                time.sleep(sleep_duration_seconds)
                continue

    return ""



if __name__ == "__main__":
    result = scan_wifi()
    print(result)
    LOG_DIR = os.path.join('/', 'var', 'log', 'wifi_monitor')
    SCAN_FILE = os.path.join(LOG_DIR, 'scan.out')
    with open(SCAN_FILE, 'w', encoding='utf-8') as file:
        file.write(result)
