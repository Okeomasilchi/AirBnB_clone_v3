#!/usr/bin/python3

"""
default model for the flask app instance
"""

import unittest
from api.v1.app import app


class Test_Index(unittest.TestCase):
    """
    Test class for the index endpoint
    """
    def setUp(self):
        """
        Set up method that runs before each test case
        """
        app.config['TESTING'] = True
        self.home = "http://0.0.0.0:5000/api/v1"
        self.client = app.test_client()

    def tearDown(self):
        """
        Tear down method that runs after each test case
        """
        app.teardown_appcontext

    def test_status(self):
        """
        Test case for checking the status endpoint
        """
        s1 = self.client.get(self.home + "/status")
        s2 = self.client.get(self.home + "/status")
        self.assertEqual(s1.data, s2.data)

    def test_status_code(self):
        """
        Test case for checking the status code of the status endpoint
        """
        s1 = self.client.get(self.home + "/status")
        s2 = self.client.get(self.home + "/status")
        self.assertEqual(s1.status_code, s2.status_code)
        self.assertEqual(s1.status_code, 200)
        self.assertEqual(s2.status_code, 200)

    def test_status_data(self):
        """
        Test case for checking the data of the status endpoint
        """
        s1 = self.client.get(self.home + "/status")
        s2 = self.client.get(self.home + "/status")
        self.assertIsNotNone(s1.data)
        self.assertIsNotNone(s2.data)

    def test_status_endpoint_exists(self):
        """
        Test case for checking if the status endpoint exists
        """
        response = self.client.get(self.home + "/status")
        self.assertEqual(response.status_code, 200)

    def test_status_content_type(self):
        """
        Test case for checking the content type of the status endpoint
        """
        response = self.client.get(self.home + "/status")
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_status_response_structure(self):
        """
        Test case for checking the structure of the
        response from the status endpoint
        """
        response = self.client.get(self.home + "/status")
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'OK')

    def test_status_response_format(self):
        """
        Test case for checking the format of the
        response from the status endpoint
        """
        response = self.client.get(self.home + "/status")
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn('status', data)
        self.assertIsInstance(data['status'], str)

    def test_status_response_status_code(self):
        """
        Test case for checking the status code of the
        response from the status endpoint
        """
        response = self.client.get(self.home + "/status")
        self.assertEqual(response.status_code, 200)

    def test_status_response_headers(self):
        """
        Test case for checking the headers of the
        response from the status endpoint
        """
        response = self.client.get(self.home + "/status")
        self.assertEqual('application/json', response.headers['Content-Type'])
        self.assertEqual('16',
                         response.headers['Content-Length'])

    def test_status_response_caching(self):
        """
        Test case for checking the caching headers of
        the response from the status endpoint
        """
        response = self.client.get(self.home + "/status")
        self.assertIn('Content-Type', response.headers)
        self.assertIn('Access-Control-Allow-Origin',
                      response.headers)

    def test_status_response_error_handling(self):
        """
        Test case for checking the error handling of
        the response from the status endpoint
        """
        response = self.client.get(self.home +
                                   "/nonexistent_endpoint")
        self.assertEqual(response.status_code, 404)


class Test_404ErrorHandler(unittest.TestCase):
    """
    Test class for the 404 error handler
    """
    def setUp(self):
        """
        Set up method that runs before each test case
        """
        app.config['TESTING'] = True
        self.home = "http://0.0.0.0:5000/api/v1"
        self.invalid_endpoint = self.home + "/nop"
        self.client = app.test_client()

    def tearDown(self):
        """
        Tear down method that runs after each test case
        """
        app.teardown_appcontext

    def test_404_error_handler_content_type(self):
        """
        Test case for checking the content type of the
        404 error handler response
        """
        response = self.client.get(self.invalid_endpoint)
        self.assertEqual(response.headers['Content-Type'],
                         'application/json')

    def test_404_error_handler_response_structure(self):
        """
        Test case for checking the structure of the
        response from the 404 error handler
        """
        response = self.client.get(self.invalid_endpoint)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Not found')

    def test_404_error_handler_response_status_code(self):
        """
        Test case for checking the status code of the
        response from the 404 error handler
        """
        response = self.client.get(self.invalid_endpoint)
        self.assertEqual(response.status_code, 404)

    def test_404_error_handler_response_performance(self):
        """
        Test case for checking the performance of the
        response from the 404 error handler
        """
        import time
        start_time = time.time()
        response = self.client.get(self.invalid_endpoint)
        end_time = time.time()
        response_time = end_time - start_time
        self.assertLess(response_time, 1.0,
                        "Response time exceeds 1 second")

    def test_404_error_handler_response_headers(self):
        """
        Test case for checking the headers of the response
        from the 404 error handler
        """
        response = self.client.get(self.invalid_endpoint)
        self.assertIn('Content-Type', response.headers)
        self.assertIn('Access-Control-Allow-Origin',
                      response.headers)

    def test_404_error_handler_response_error_handling(self):
        """
        Test case for checking the error handling of the
        response from the 404 error handler
        """
        response = self.client.get(self.invalid_endpoint +
                                   "/nonexistent_endpoint")
        self.assertEqual(response.status_code, 404)
