
## Background Service

### Install Tools
> sudo apt install python3-daemon

### Setup Service
> sudo chmod +x /backend/wifi_monitor/wifi_monitor.py
> chmod +x create_wifi_monitor_service.sh
> ./create_wifi_monitor_service.sh

### Check the status of the service

> sudo systemctl status wifi_monitor.service

### Debugging

To debug, check the log file at /var/log/wifi_monitor/wifi_monitor.log for any errors or messages that can help pinpoint the issue.

> sudo tail -f /var/log/wifi_monitor/wifi_monitor.log


## Docker

### Backend

#### Build

> docker build -f docker/backend.dockerfile -t wifi_monitor_image .

#### Run
> docker run --net=host --cap-add=NET_ADMIN --cap-add=NET_RAW -d --name wifi_monitor_container -v /var/log/wifi_monitor:/app/backend/wifi_monitor/logs wifi_monitor_image


#### Debug

> docker exec -it wifi_monitor_container /bin/bash