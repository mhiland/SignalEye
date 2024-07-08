

## Install Tools
> sudo apt install python3-daemon

## Setup Service
> sudo chmod +x /home/mhiland/Projects/RedCanary/wifi_monitor/wifi_monitor.py
> chmod +x create_wifi_monitor_service.sh
> ./create_wifi_monitor_service.sh


## Check the status of the service

> sudo systemctl status wifi_monitor.service


## Debugging

To debug, check the log file at /var/log/wifi_monitor/wifi_monitor.log for any errors or messages that can help pinpoint the issue.

> sudo tail -f /var/log/wifi_monitor/wifi_monitor.log
