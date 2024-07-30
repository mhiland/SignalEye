## Local
> pip install --no-cache-dir -r requirements.txt

> python app.py

## Docker

### Build
> docker build -t flask-network-app .

### Run
> docker run -p 5000:5000 -v /var/log/wifi_monitor:/var/log/wifi_monitor flask-network-app
