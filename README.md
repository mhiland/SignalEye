
# Developing Code

## Setup
Install runtime requirements
> sudo apt-get update

> sudo apt-get install docker-compose

> sudo pip install -r requirements.txt

> pre-commit install

## Docker

### Docker Compose
> docker-compose up -d

If wanting to change the wireless interface use environment variable, wlan=1 == wlan1. default: 0
> wlan=1 docker-compose up -d --build

### Debug
> docker exec -it wifi_monitor_container /bin/bash

## Committing Code

### Test
> pytest

### Pylint
Run pylint manually
> pylint $(git ls-files '*.py')

### autopep8
autopep8 can automatically fix trailing whitespace issues along with other PEP 8 formatting issues.
> autopep8 --in-place --aggressive --aggressive --recursive .

### Pre-Commit Validation
> pre-commit run --all-files
