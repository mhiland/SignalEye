
import pytest
from jsonschema import validate, exceptions, ValidationError
import sys, os
import json
os.environ['UNIT_TESTING'] = 'True'
test_file_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.abspath(os.path.join(
    test_file_dir, '../backend/wifi_monitor'))
sys.path.insert(0, module_path)
from json_schema import schema

valid_data = [
    {
        "ESSID": "",
        "Address": "B4:20:46:10:08:47",
        "Manufacturer": "eero inc.",
        "Frequency": "5.5",
        "Channel": "100",
        "Quality": "36",
        "SignalLevel": "-74",
        "Mode": "Master",
        "EncryptionInfo": {
            "Encryption": "Open",
            "RSN": None
        },
        "Active": True,
        "LastSeen": "2024-08-04 06:13:39",
        "FirstSeen": "2024-07-29 05:49:48",
        "Suspicious": True,
        "Reason": "Hidden SSID; Open network; Unusual channel; SSID spoofing detected"
    }
]

invalid_data = [
    {
        "ESSID": "",
        "Address": "B4:20:46:10:08:47",
        "Manufacturer": "eero inc.",
        "Frequency": "5.5",
        "Channel": "100",
        "Quality": "36",
        "SignalLevel": "-74",
        "Mode": "Master",
        "EncryptionInfo": {
            "Encryption": "Open",
            "RSN": None
        },
        "Active": "yes",  # Invalid value (should be a boolean)
        "LastSeen": "2024-08-04 06:13:39",
        "FirstSeen": "2024-07-29 05:49:48",
        "Suspicious": True,
        "Reason": "Hidden SSID; Open network; Unusual channel; SSID spoofing detected"
    }
]


def test_valid_data_no_exception_raised():
    try:
        validate(instance=valid_data, schema=schema)
        assert True
    except ValidationError:
        assert False, "Valid data did not pass validation."


def test_invalid_data_exception_raised():
    with pytest.raises(ValidationError):
        validate(instance=invalid_data, schema=schema)

def test_current_data_if_exists():
    data_file = '/var/log/wifi_monitor/persistent_networks.json'
    if os.path.exists(data_file):
        with open(data_file, encoding='utf-8') as f:
            networks_data = json.load(f)
            try:
                validate(instance=networks_data, schema=schema)
                assert True
            except ValidationError:
                assert False, "Valid data did not pass validation."
    else:
        assert True
