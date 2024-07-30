from flask import Flask, render_template, send_file
import json
import os

app = Flask(__name__)

# Load JSON data
DATA_FILE = '/var/log/wifi_monitor/persistent_networks.json'
if os.path.exists(DATA_FILE):
    with open(DATA_FILE) as f:
        networks_data = json.load(f)
else:
    networks_data = []

@app.route('/')
def index():
    return render_template('index.html', networks=networks_data)

@app.route('/download')
def download():
    return send_file(DATA_FILE, as_attachment=True, download_name='persistent_networks.json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
