"""
This module contains tests for the frontend application.
"""

import unittest
import sys
import os
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../frontend')))
from app import app, networks_data, DATA_FILE


class FlaskAppTestCase(unittest.TestCase):
    """
    Test cases for the frontend application.
    """
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

    def test_index_route(self):
        response = self.app.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_download_route(self):
        response = self.app.get('/download')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(
            response.headers['Content-Disposition'],
            'attachment; filename=persistent_networks.json')


if __name__ == '__main__':
    unittest.main()
