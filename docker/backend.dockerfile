# Build
FROM python:3.11-slim AS build

WORKDIR /app

COPY backend/wifi_monitor /app/backend/wifi_monitor

RUN pip install --no-cache-dir -r /app/backend/wifi_monitor/requirements.txt

RUN python -m compileall /app/backend/wifi_monitor

# Runtime
FROM python:3.11-slim AS runtime

RUN apt-get update && \
    apt-get install -y iw wireless-tools iproute2 net-tools && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/backend/wifi_monitor
RUN mkdir -p /var/log/wifi_monitor

WORKDIR /app

COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /app/backend/wifi_monitor /app/backend/wifi_monitor

VOLUME [ "/var/log/wifi_monitor" ]

CMD ["python3", "backend/wifi_monitor/wifi_monitor.py"]
