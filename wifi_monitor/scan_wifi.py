import subprocess

def scan_wifi():
    try:
        result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], capture_output=True, text=True, timeout=30)
        return result.stdout
    except subprocess.TimeoutExpired:
        print("iwlist scan timed out.")
        return ""

if __name__ == "__main__":
    result = scan_wifi()
    print(result)
    with open('scan.out', 'w') as file:
        file.write(result)