# syntax=docker/dockerfile:1

# Stage 1: Build the backend
FROM python:3.11-slim AS backend_build

WORKDIR /app/backend

COPY backend/wifi_monitor /app/backend/wifi_monitor

RUN pip install --no-cache-dir -r /app/backend/wifi_monitor/requirements.txt

RUN python -m compileall /app/backend/wifi_monitor

# Stage 2: Build the frontend
FROM python:3.11-slim AS frontend_build

WORKDIR /app/frontend

COPY frontend /app/frontend

RUN pip install --no-cache-dir -r /app/frontend/requirements.txt

# Stage 3: Runtime
FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y iw wireless-tools iproute2 net-tools && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/backend/wifi_monitor
RUN mkdir -p /app/frontend
RUN mkdir -p /var/log/wifi_monitor

WORKDIR /app

# Copy dependencies from build stages
COPY --from=backend_build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend_build /app/backend/wifi_monitor /app/backend/wifi_monitor
COPY --from=frontend_build /app/frontend /app/frontend

RUN pip install --no-cache-dir -r /app/frontend/requirements.txt

VOLUME [ "/var/log/wifi_monitor" ]

EXPOSE 5000

CMD ["sh", "-c", "python3 backend/wifi_monitor/wifi_monitor.py & python3 frontend/app.py"]
