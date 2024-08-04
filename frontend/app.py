from flask import Flask, render_template, send_file
import json
import os
import io

app = Flask(__name__)

# Load JSON data
DATA_FILE = '/var/log/wifi_monitor/persistent_networks.json'
LOG_FILE = '/var/log/wifi_monitor/wifi_monitor.log'

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, encoding='utf-8') as f:
        networks_data = json.load(f)
else:
    networks_data = []


@app.route('/')
def index():
    return render_template('index.html', networks=networks_data)


@app.route('/download')
def download():
    temp_file = io.BytesIO()
    temp_file.write(json.dumps(networks_data).encode('utf-8'))
    temp_file.seek(0)

    return send_file(
        temp_file,
        as_attachment=True,
        download_name='persistent_networks.json')


@app.route('/logs')
def logs():
    log_content = ''
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            log_content = f.read()
    return render_template('logs.html', log_content=log_content)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
