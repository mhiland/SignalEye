FROM python:3.11-slim

WORKDIR /app

COPY frontend /app

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5000

VOLUME ["/var/log/wifi_monitor"]

CMD ["python3", "app.py"]
