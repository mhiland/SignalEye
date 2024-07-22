#!/bin/bash

# Define variables
SERVICE_NAME="wifi_monitor"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="${SCRIPT_DIR}/../backend/wifi_monitor/${SERVICE_NAME}_service.py"
LOG_DIR="/var/log/${SERVICE_NAME}"
LOG_FILE="${LOG_DIR}/${SERVICE_NAME}.log"

# Stop and disable any existing service
echo "Stopping and disabling existing ${SERVICE_NAME} service if it exists."
sudo systemctl stop ${SERVICE_NAME}
sudo systemctl disable ${SERVICE_NAME}

# Remove the old service file
echo "Removing old service file at ${SERVICE_FILE}."
sudo rm -f ${SERVICE_FILE}

# Reload systemd to ensure the old service is removed
echo "Reloading systemd daemon."
sudo systemctl daemon-reload

# Clear the log directory if it exists and create it anew
echo "Clearing and creating log directory at ${LOG_DIR}."
if [ -d "${LOG_DIR}" ]; then
  sudo rm -rf "${LOG_DIR}"
fi
sudo mkdir -p ${LOG_DIR}
sudo chown mhiland:mhiland ${LOG_DIR}

# Create the service file content
SERVICE_CONTENT="[Unit]
Description=WiFi Monitor Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 ${SCRIPT_PATH}
WorkingDirectory=/home/mhiland/Projects/RedCanary/backend/wifi_monitor
Restart=always
User=mhiland
Group=mhiland
StandardOutput=file:${LOG_FILE}
StandardError=file:${LOG_FILE}

[Install]
WantedBy=multi-user.target"

# Write the service content to the service file
echo "Creating service file at ${SERVICE_FILE}."
echo "${SERVICE_CONTENT}" | sudo tee ${SERVICE_FILE} > /dev/null

# Set proper permissions for the script
sudo chown mhiland:mhiland ${SCRIPT_PATH}
sudo chmod 755 ${SCRIPT_PATH}

# Reload systemd to recognize the new service
echo "Reloading systemd daemon."
sudo systemctl daemon-reload

# Enable the service to start on boot
echo "Enabling ${SERVICE_NAME} service to start on boot."
sudo systemctl enable ${SERVICE_NAME}

# Start the service immediately
echo "Starting ${SERVICE_NAME} service."
sudo systemctl start ${SERVICE_NAME}

# Check the status of the service
echo "Checking ${SERVICE_NAME} service status."
sudo systemctl status ${SERVICE_NAME}