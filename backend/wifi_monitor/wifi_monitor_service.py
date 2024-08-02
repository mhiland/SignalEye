from wifi_monitor import monitor_wifi
import daemon
import os
import sys

# Add the directory containing your scripts to the sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


def run_as_service():
    with daemon.DaemonContext():
        monitor_wifi()


if __name__ == "__main__":
    run_as_service()
