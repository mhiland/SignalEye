import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
import os
os.environ['UNIT_TESTING'] = 'True'
import logging
# Ensure correct path insertion for importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/wifi_monitor/')))
from update_networks_list import update_networks_list

class TestUpdateNetworksList(unittest.TestCase):

    def setUp(self):
        self.persistent_networks = [
            {'ESSID': 'Network1', 'Address': '00:11:22:33:44:55', 'info': 'persistent info'},
            {'ESSID': 'Network2', 'Address': 'AA:BB:CC:DD:EE:FF', 'info': 'persistent info'}
        ]
        self.current_networks = [
            {'ESSID': 'Network1', 'Address': '00:11:22:33:44:55', 'additional_info': 'current info'},
            {'ESSID': 'Network3', 'Address': '11:22:33:44:55:66', 'additional_info': 'current info'}
        ]

    @patch('update_networks_list.datetime')
    def test_update_existing_network(self, mock_datetime):
        fake_now = datetime(2023, 10, 5, 12, 0, 0)
        mock_datetime.now.return_value = fake_now
        update_networks_list(self.persistent_networks, self.current_networks)

        # Assert that Network1 is updated and marked as Active
        self.assertTrue(self.persistent_networks[0].get('Active'))
        self.assertEqual(self.persistent_networks[0].get('Last Seen'), fake_now.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(self.persistent_networks[0].get('additional_info'), 'current info')

    @patch('update_networks_list.datetime')
    def test_add_new_network(self, mock_datetime):
        fake_now = datetime(2023, 10, 5, 12, 0, 0)
        mock_datetime.now.return_value = fake_now
        update_networks_list(self.persistent_networks, self.current_networks)

        # Construct the expected network dictionary
        expected_new_network = {
            'ESSID': 'Network3',
            'Address': '11:22:33:44:55:66',
            'additional_info': 'current info',
            'Active': True,
            'First Seen': fake_now.strftime("%Y-%m-%d %H:%M:%S"),
            'Last Seen': fake_now.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Assert that Network3 is added to persistent networks list
        self.assertIn(expected_new_network, self.persistent_networks)

    @patch('update_networks_list.datetime')
    def test_deactivate_non_matching_network(self, mock_datetime):
        fake_now = datetime(2023, 10, 5, 12, 0, 0)
        mock_datetime.now.return_value = fake_now
        update_networks_list(self.persistent_networks, self.current_networks)

        # Assert that Network2 is marked as Inactive
        self.assertFalse(self.persistent_networks[1].get('Active', True))

    def test_sorting_persistent_networks(self):
        self.persistent_networks.append({'ESSID': 'ANetwork', 'Address': 'FF:EE:DD:CC:BB:AA'})
        update_networks_list(self.persistent_networks, self.current_networks)

        # Assert that persistent networks are sorted by ESSID
        sorted_essids = sorted(net['ESSID'] for net in self.persistent_networks)
        self.assertEqual([net['ESSID'] for net in self.persistent_networks], sorted_essids)

if __name__ == '__main__':
    unittest.main()
