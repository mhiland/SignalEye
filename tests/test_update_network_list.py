import pytest
from unittest.mock import patch
from datetime import datetime
import sys
import os
os.environ['UNIT_TESTING'] = 'True'
test_file_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.abspath(
    os.path.join(
        test_file_dir,
        '../backend/wifi_monitor'))
sys.path.insert(0, module_path)
from update_networks_list import update_networks_list

@pytest.fixture
def setup_networks():
    persistent_networks = [{'ESSID': 'Network1',
                            'Address': '00:11:22:33:44:55',
                            'info': 'persistent info'},
                           {'ESSID': 'Network2',
                            'Address': 'AA:BB:CC:DD:EE:FF',
                            'info': 'persistent info'}]
    current_networks = [{'ESSID': 'Network1',
                         'Address': '00:11:22:33:44:55',
                         'additional_info': 'current info'},
                        {'ESSID': 'Network3',
                         'Address': '11:22:33:44:55:66',
                         'additional_info': 'current info'}]
    return persistent_networks, current_networks


@patch('update_networks_list.datetime')
def test_update_existing_network(mock_datetime, setup_networks):
    persistent_networks, current_networks = setup_networks
    fake_now = datetime(2023, 10, 5, 12, 0, 0)
    mock_datetime.now.return_value = fake_now
    update_networks_list(persistent_networks, current_networks)

    # Assert that Network1 is updated and marked as Active
    assert persistent_networks[0].get('Active') is True
    assert persistent_networks[0].get(
        'LastSeen') == fake_now.strftime("%Y-%m-%d %H:%M:%S")
    assert persistent_networks[0].get('additional_info') == 'current info'


@patch('update_networks_list.datetime')
def test_add_new_network(mock_datetime, setup_networks):
    persistent_networks, current_networks = setup_networks
    fake_now = datetime(2023, 10, 5, 12, 0, 0)
    mock_datetime.now.return_value = fake_now
    update_networks_list(persistent_networks, current_networks)

    # Construct the expected network dictionary
    expected_new_network = {
        'ESSID': 'Network3',
        'Address': '11:22:33:44:55:66',
        'additional_info': 'current info',
        'Active': True,
        'Uptime': '0.0006944444444444445',
        'FirstSeen': fake_now.strftime("%Y-%m-%d %H:%M:%S"),
        'LastSeen': fake_now.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Assert that Network3 is added to persistent networks list
    assert expected_new_network in persistent_networks


@patch('update_networks_list.datetime')
def test_deactivate_non_matching_network(mock_datetime, setup_networks):
    persistent_networks, current_networks = setup_networks
    fake_now = datetime(2023, 10, 5, 12, 0, 0)
    mock_datetime.now.return_value = fake_now
    update_networks_list(persistent_networks, current_networks)

    # Assert that Network2 is marked as Inactive
    assert persistent_networks[1].get('Active', True) is False


def test_sorting_persistent_networks(setup_networks):
    persistent_networks, current_networks = setup_networks
    persistent_networks.append(
        {'ESSID': 'ANetwork', 'Address': 'FF:EE:DD:CC:BB:AA'})
    update_networks_list(persistent_networks, current_networks)

    # Assert that persistent networks are sorted by ESSID
    sorted_essids = sorted(net['ESSID'] for net in persistent_networks)
    assert [net['ESSID'] for net in persistent_networks] == sorted_essids
