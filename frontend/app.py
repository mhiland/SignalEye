from flask import Flask, render_template, send_file, jsonify
from datetime import datetime, timedelta
import json
import os, sys, pytz
import io
from jsonschema import validate, ValidationError
test_file_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.abspath(os.path.join(
    test_file_dir, '../backend/wifi_monitor'))
sys.path.insert(0, module_path)
from json_schema import schema

app = Flask(__name__)

# Load JSON data
DATA_FILE = '/var/log/wifi_monitor/persistent_networks.json'
LOG_FILE = '/var/log/wifi_monitor/wifi_monitor.log'

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, encoding='utf-8') as f:
        networks_data = json.load(f)
        validate(instance=networks_data, schema=schema)
else:
    networks_data = []


def filter_last_24_hours(data):
    cutoff_time = datetime.now(pytz.UTC) - timedelta(hours=24)
    filtered_data = []

    for network in data:
        last_seen = datetime.strptime(
            network["LastSeen"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)
        if last_seen >= cutoff_time:
            filtered_data.append(network)

    return filtered_data


def process_data(data):
    data = filter_last_24_hours(data)
    spectrum_data = {
        "2.4GHz": [],
        "5GHz": []
    }

    for network in data:
        frequency = float(network["Frequency"])
        channel = int(network["Channel"])
        signal_level = int(network["SignalLevel"])
        essid = network["ESSID"]

        if 2.4 <= frequency < 2.5:
            spectrum_data["2.4GHz"].append(
                {"channel": channel, "signal_level": signal_level, "essid": essid})
        elif 5.0 <= frequency < 6.0:
            spectrum_data["5GHz"].append(
                {"channel": channel, "signal_level": signal_level, "essid": essid})

    spectrum_data["2.4GHz"].sort(key=lambda x: x["channel"])
    spectrum_data["5GHz"].sort(key=lambda x: x["channel"])

    return spectrum_data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def data():
    now = datetime.now(pytz.UTC)
    last_24hrs = now - timedelta(hours=24)

    recent_networks = []
    older_networks = []

    for network in networks_data:
        last_seen_str = network.get("LastSeen")
        last_seen_time = datetime.strptime(last_seen_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)

        if last_seen_time >= last_24hrs:
            recent_networks.append(network)
        else:
            older_networks.append(network)

    return jsonify({
        'recent_networks': recent_networks,
        'older_networks': older_networks
    })


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


@app.route('/spectrum')
def spectrum():
    spectrum_data = process_data(networks_data)
    return render_template('spectrum.html', spectrum_data=json.dumps(spectrum_data))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
