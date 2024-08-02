

## Docker

### Backend

#### Build

> docker build -f docker/backend.dockerfile -t wifi_monitor_backend .

#### Run
> docker run --net=host --cap-add=NET_ADMIN --cap-add=NET_RAW -d --name wifi_monitor_backend -v /var/log/wifi_monitor:/var/log/wifi_monitor wifi_monitor_backend


#### Debug

> docker exec -it wifi_monitor_container /bin/bash

### Frontend

#### Build
> docker build -f docker/frontend.dockerfile -t wifi_monitor_frontend .

#### Run
> docker run -p 5000:5000 -d --name wifi_monitor_frontend -v /var/log/wifi_monitor:/var/log/wifi_monitor wifi_monitor_frontend


### Bundled

#### Build
> docker build -f docker/bundled.dockerfile -t wifi_monitor_bundled .

#### Run
> docker run --net=host --cap-add=NET_ADMIN --cap-add=NET_RAW -p 5000:5000 -d --name wifi_monitor_bundled -v /var/log/wifi_monitor:/var/log/wifi_monitor wifi_monitor_bundled


## Docker Compose
> docker-compose up -d



## Test
> python -m unittest discover tests


## Pylint
Run pylint manually
> pip install pre-commit
pylint $(git ls-files '*.py')
