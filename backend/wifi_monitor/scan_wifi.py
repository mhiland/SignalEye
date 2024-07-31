import os
import subprocess

def scan_wifi():
    try:
        result = subprocess.run(['iwlist', 'wlan0', 'scan'], capture_output=True, text=True, timeout=30)
        return result.stdout
    except subprocess.TimeoutExpired:
        print("iwlist scan timed out.")
        return ""

if __name__ == "__main__":
    result = scan_wifi()
    print(result)
    LOG_DIR = os.path.join('/', 'var', 'log', 'wifi_monitor')
    SCAN_FILE = os.path.join(LOG_DIR, 'scan.out')
    with open(SCAN_FILE, 'w') as file:
        file.write(result)