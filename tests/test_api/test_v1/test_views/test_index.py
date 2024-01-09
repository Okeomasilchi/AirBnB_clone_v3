#!/usr/bin/python3
"""
Models for the routes of the api's health & stats
"""

import unittest
from api.v1.app import app


class Test_StatsEndpoint(unittest.TestCase):
    """
    A class to test the stats endpoint of the API
    """

    def setUp(self):
        """
        Set up method that runs before each test case
        """
        app.config['TESTING'] = True
        self.stats_url = "http://0.0.0.0:5000/api/v1/stats"
        self.client = app.test_client()

    def tearDown(self):
        """
        Tear down method that runs after each test case
        """
        app.teardown_appcontext

    def test_stats_endpoint_exists(self):
        """
        Test if the stats endpoint exists
        """
        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, 200)

    def test_stats_content_type(self):
        """
        Test if the stats endpoint returns the correct content type
        """
        response = self.client.get(self.stats_url)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_stats_response_structure(self):
        """
        Test if the stats endpoint returns the expected response structure
        """
        response = self.client.get(self.stats_url)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn('amenities', data)
        self.assertIn('cities', data)
        self.assertIn('places', data)
        self.assertIn('reviews', data)
        self.assertIn('states', data)
        self.assertIn('users', data)

    def test_stats_response_format(self):
        """
        Test if the stats endpoint returns the expected response format
        """
        response = self.client.get(self.stats_url)
        data = response.get_json()
        for key, value in data.items():
            self.assertIsInstance(value, int)

    def test_stats_response_status_code(self):
        """
        Test if the stats endpoint returns the expected status code
        """
        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, 200)

    def test_stats_response_unauthorized(self):
        """
        Test if the stats endpoint handles unauthorized access
        """
        response = self.client.get(
            self.stats_url,
            headers={'Authorization': 'Bearer invalid_token'}
            )
        self.assertEqual(response.status_code, 200)

    def test_stats_response_performance(self):
        """
        Test the performance of the stats endpoint
        """
        import time
        start_time = time.time()
        response = self.client.get(self.stats_url)
        end_time = time.time()
        response_time = end_time - start_time
        self.assertLess(response_time, 1.0, "Response time exceeds 1 second")

    def test_stats_response_error_handling(self):
        """
        Test the error handling of the stats endpoint
        """
        response = self.client.get(self.stats_url + "/nonexistent_endpoint")
        self.assertEqual(response.status_code, 404)
