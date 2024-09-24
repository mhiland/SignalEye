
<p align="center">
  <img src="images/seye-logo.svg" alt="SeyE Logo" width="200"/>
</p>

# About

> Detect malicious actors before they gain access to your network.

Signal Eye (pronounced sigh) is a signals intelligence tool designed to run on a Raspberry Pi, continuously monitoring your local wireless environment. It scans for suspicious activity in real-time, detecting anomalous behavior, rogue access points, and potential security threats, including attacks initiated by Pineapple-like devices. With Signal Eye, you gain a powerful tool to safeguard your wireless network, providing early detection of intrusions and ensuring robust network security.

## Key Features

- **Real-time Monitoring**: Constantly observes the WiFi spectrum for any unusual behavior or unauthorized devices.
- **Device Identification**: Utilizes advanced algorithms to differentiate between legitimate and malicious access points.
- **Data Logging**: Maintains detailed logs of all activities for further analysis.
- **User-friendly Interface**: Provides an intuitive dashboard for easy monitoring and management of network security.

## Use Cases

- **Home Network Security**: Keep your home WiFi safe from unauthorized users and potential cyber threats.
- **Office Environment**: Ensure a secure workplace by preventing access to rogue devices and maintaining the integrity of your corporate network.

## Technical Details

- **Platform**: Raspberry Pi 3B+/5, Firewalla
- **Programming Languages**: Python, Bash
- **Dependencies**: `iwlist`

## Installation and Setup

1. Download the latest Docker image:
    ```
    docker pull ghcr.io/mhiland/signaleye:latest
    ```
2. Initialize the Docker container:
    ```
    docker run --net=host --cap-add=NET_ADMIN --cap-add=NET_RAW -d --name signal_eye_container -v /var/log/wifi_monitor:/app/backend/wifi_monitor/logs ghcr.io/mhiland/signaleye:latest
    ```

## Contribution Guidelines

Follow our [contribution guidelines](CONTRIBUTING.md) to ensure proper code style and testing practices.

## Security Policy

Refer to our [security policy](SECURITY.md) for details on how to report vulnerabilities or security issues.
