#!/usr/bin/python3

"""
Models for the routes of the amenity_views
"""

import json
from flask import Flask
import unittest
from api.v1.app import app


class Test_AmenityAPI(unittest.TestCase):
    """
    This class contains unit tests for the Amenity
    API endpoints.
    """

    def setUp(self):
        """
        Set up the test environment before each test
        method is run.
        """
        app.config['TESTING'] = True
        self.url = "http://0.0.0.0:5000/api/v1/amenities"
        self.client = app.test_client()

    def tearDown(self):
        """
        Clean up the test environment after each test
        method is run.
        """
        app.teardown_appcontext

    def test_get_all_amenities(self):
        """
        Test the GET /amenities endpoint to retrieve all
        amenities.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_specific_amenity(self):
        """
        Test the GET /amenities/<amenity_id> endpoint to
        retrieve a specific amenity.
        """
        raa = self.client.\
            get(self.url)
        data_all_amenities = raa.get_json()
        if data_all_amenities:
            amenity_id = data_all_amenities[0]['id']
            response_specific_amenity = self.client.\
                get(f"{self.url}/{amenity_id}")
            self.assertEqual(response_specific_amenity.
                             status_code, 200)
            data_specific_amenity = response_specific_amenity.get_json()
            self.assertIsInstance(data_specific_amenity, dict)
            self.assertEqual(data_specific_amenity['id'],
                             amenity_id)

    def test_get_nonexistent_amenity(self):
        """
        Test the GET /amenities/<amenity_id>
        endpoint with a nonexistent amenity ID.
        """
        response = self.client.get(f"{self.url}\
            /nonexistent_amenity_id")
        self.assertEqual(response.status_code, 404)

    def test_delete_amenity(self):
        """
        Test the DELETE /amenities/<amenity_id> endpoint
        to delete an amenity.
        """
        raa = self.client.\
            get(self.url)
        data_all_amenities = raa.get_json()
        if data_all_amenities:
            amenity_id = data_all_amenities[0]['id']
            response_delete = self.client.\
                delete(f"{self.url}/{amenity_id}")
            self.assertEqual(response_delete.
                             status_code, 200)
            data_delete = response_delete.get_json()
            self.assertIsInstance(data_delete, dict)
            self.assertEqual(data_delete, {})

    def test_delete_nonexistent_amenity(self):
        """
        Test the DELETE /amenities/<amenity_id>
        endpoint with a nonexistent amenity ID.
        """
        response = self.client.delete(
            f"{self.url}/nonexistent_amenity_id")
        self.assertEqual(response.status_code, 404)

    def test_create_amenity(self):
        """
        Test the POST /amenities endpoint to create a
        new amenity.
        """
        amenity_data = {"name": "New Amenity"}
        response = self.client.post(self.url,
                                    json=amenity_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['name'], amenity_data['name'])

    def test_create_amenity_invalid_json(self):
        """
        Test the POST /amenities endpoint with invalid
        JSON data.
        """
        k = 'invalid_json'
        c = 'application/json'
        r = self.client.post(self.url, data=k, content_type=c)
        self.assertEqual(r.status_code, 400)

    def test_create_amenity_missing_name(self):
        """
        Test the POST /amenities endpoint with missing
        'name' field in the JSON data.
        """
        amenity_data = {"other_key": "value"}
        response = self.client.post(self.url,
                                    json=amenity_data)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'Missing name')

    def test_update_amenity(self):
        """
        Test the PUT /amenities/<amenity_id> endpoint to
        update an existing amenity.
        """
        raa = self.client.get(self.url)
        data_all_amenities = raa.get_json()
        if data_all_amenities:
            amenity_id = data_all_amenities[0]['id']
            updated_data = {"name": "Updated Amenity"}
            response_update = self.client.put(
                f"{self.url}/{amenity_id}", json=updated_data)
            self.assertEqual(response_update.status_code, 200)
            data_update = response_update.get_json()
            self.assertIsInstance(data_update, dict)
            self.assertEqual(data_update['name'],
                             updated_data['name'])

    def test_update_nonexistent_amenity(self):
        """
        Test the PUT /amenities/<amenity_id> endpoint with
        a nonexistent amenity ID.
        """
        updated_data = {"name": "Updated Amenity"}
        response = self.client.put(f"{self.url}\
            /nonexistent_amenity_id", json=updated_data)
        self.assertEqual(response.status_code, 404)

    def test_update_amenity_invalid_json(self):
        """
        Test the PUT /amenities/<amenity_id> endpoint with
        invalid JSON data.
        """
        raa = self.client.get(self.url)
        data_all_amenities = raa.\
            get_json()
        if data_all_amenities:
            a_id = data_all_amenities[0]['id']
            ct = 'application/json'
            pl = 'invalid_json'
            r = self.client.put(f"{self.url}/{a_id}", data=pl, content_type=ct)
            self.assertEqual(r.status_code, 400)

    def test_update_amenity_ignore_fields(self):
        """
        Test the PUT /amenities/<amenity_id> endpoint to
        update an amenity while ignoring certain fields.
        """
        raa = self.client.get(self.url)
        data_all_amenities = raa.get_json()
        if data_all_amenities:
            amenity_id = data_all_amenities[0]['id']
            updated_data = {"name": "Updated Amenity",
                            "id": "invalid_id",
                            "created_at": "invalid_created_at",
                            "updated_at": "invalid_updated_at"}
            response_update = self.client.put(
                f"{self.url}/{amenity_id}", json=updated_data)
            self.assertEqual(response_update.status_code, 200)
            data_update = response_update.get_json()
            self.assertIsInstance(data_update, dict)
            self.assertEqual(data_update['name'],
                             updated_data['name'])
            self.assertNotEqual(data_update['id'],
                                updated_data['id'])
            self.assertNotEqual(data_update['created_at'],
                                updated_data['created_at'])
            self.assertNotEqual(data_update['updated_at'],
                                updated_data['updated_at'])
