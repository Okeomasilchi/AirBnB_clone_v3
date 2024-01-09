#!/usr/bin/python3

"""
Models for the routes of the city_views
"""


import json
from flask import Flask
import unittest
from api.v1.app import app


class Test_CityAPI(unittest.TestCase):
    """
    This class contains unit tests for the City API endpoints.
    """

    def setUp(self):
        """
        Set up the test environment before each test method is run.
        """
        app.config['TESTING'] = True
        self.states_url = "http://0.0.0.0:5000/api/v1/states"
        self.url = "http://0.0.0.0:5000/api/v1/cities"
        self.client = app.test_client()

    def tearDown(self):
        """
        Clean up the test environment after each test method is run.
        """
        app.teardown_appcontext

    def test_get_all_cities_by_state(self):
        """
        Test the GET request to retrieve all cities by state.
        """
        # Assuming there is at least one state in the database
        response_all_states = self.client.get(self.states_url)
        data_all_states = response_all_states.get_json()
        if data_all_states:
            state_id = data_all_states[0]['id']
            response = self.client.get(f"{self.states_url}/{state_id}/cities")
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIsInstance(data, list)

    def test_get_all_cities_by_nonexistent_state(self):
        """
        Test the GET request to retrieve all cities by a nonexistent state.
        """
        response = self.client.get(
            f"{self.states_url}/nonexistent_state_id/cities"
            )
        self.assertEqual(response.status_code, 404)

    def test_get_specific_city(self):
        """
        Test the GET request to retrieve a specific city.
        """
        # Assuming there is at least one city in the database
        r_a_c = self.client.get(self.states_url)
        r_a_c = r_a_c.get_json()[0]["id"]
        r_a_c = self.client.get(self.states_url + "/" + r_a_c + "/cities")
        data_all_cities = r_a_c.get_json()
        if data_all_cities:
            city_id = data_all_cities[0]['id']
            response_specific_city = self.client.get(f"{self.url}/{city_id}")
            self.assertEqual(response_specific_city.status_code, 200)
            data_specific_city = response_specific_city.get_json()
            self.assertIsInstance(data_specific_city, dict)
            self.assertEqual(data_specific_city['id'], city_id)

    def test_get_nonexistent_city(self):
        """
        Test the GET request to retrieve a nonexistent city.
        """
        response = self.client.get(f"{self.url}/nonexistent_city_id")
        self.assertEqual(response.status_code, 404)

    def test_delete_city(self):
        """
        Test the DELETE request to delete a city.
        """
        # Assuming there is at least one city in the database
        r_a_c = self.client.get(self.states_url)
        r_a_c = r_a_c.get_json()[0]["id"]
        r_a_c = self.client.get(self.states_url + "/" + r_a_c + "/cities")
        data_all_cities = r_a_c.get_json()
        if data_all_cities:
            city_id = data_all_cities[0]['id']
            r_delete = self.client.delete(f"{self.url}/{city_id}")
            self.assertEqual(r_delete.status_code, 200)
            data_delete = r_delete.get_json()
            self.assertIsInstance(data_delete, dict)
            self.assertEqual(data_delete, {})

    def test_delete_nonexistent_city(self):
        """
        Test the DELETE request to delete a nonexistent city.
        """
        response = self.client.delete(f"{self.url}/nonexistent_city_id")
        self.assertEqual(response.status_code, 404)

    def test_create_city(self):
        """
        Test the POST request to create a city.
        """
        # Assuming there is at least one state in the database
        response_all_states = self.client.get(self.states_url)
        data_all_states = response_all_states.get_json()
        if data_all_states:
            state_id = data_all_states[0]['id']
            city_data = {"name": "New City"}
            response = self.client.post(
                f"{self.states_url}/{state_id}/cities", json=city_data)
            self.assertEqual(response.status_code, 201)
            data = response.get_json()
            self.assertIsInstance(data, dict)
            self.assertEqual(data['name'], city_data['name'])

    def test_create_city_invalid_json(self):
        """
        Test the POST request to create a city with invalid JSON data.
        """
        # Assuming there is at least one state in the database
        response_all_states = self.client.get(self.states_url)
        data_all_states = response_all_states.get_json()
        if data_all_states:
            state_id = data_all_states[0]['id']
            response = self.client.post(
                f"{self.states_url}/{state_id}/cities",
                data='invalid_json',
                content_type='application/json'
                )
            self.assertEqual(response.status_code, 400)

    def test_create_city_missing_name(self):
        """
        Test the POST request to create a city with missing name field.
        """
        # Assuming there is at least one state in the database
        response_all_states = self.client.get(self.states_url)
        data_all_states = response_all_states.get_json()
        if data_all_states:
            state_id = data_all_states[0]['id']
            city_data = {"other_key": "value"}
            response = self.client.post(
                f"{self.states_url}/{state_id}/cities", json=city_data)
            self.assertEqual(response.status_code, 400)
            data = response.get_json()
            self.assertEqual(data['error'], 'Missing name')

    def test_create_city_nonexistent_state(self):
        """
        Test the POST request to create a city with a nonexistent state.
        """
        response = self.client.post(
            f"{self.states_url}/nonexistent_state_id/cities",
            json={"name": "New City"}
            )
        self.assertEqual(response.status_code, 404)

    def test_update_city(self):
        """
        Test the PUT request to update a city.
        """
        # Assuming there is at least one city in the database
        r_a_c = self.client.get(self.states_url)
        r_a_c = r_a_c.get_json()[0]["id"]
        r_a_c = self.client.get(self.states_url + "/" + r_a_c + "/cities")
        data_all_cities = r_a_c.get_json()
        if data_all_cities:
            city_id = data_all_cities[0]['id']
            updated_data = {"name": "Updated City"}
            response_update = self.client.put(
                f"{self.url}/{city_id}", json=updated_data)
            self.assertEqual(response_update.status_code, 200)
            data_update = response_update.get_json()
            self.assertIsInstance(data_update, dict)
            self.assertEqual(data_update['name'], updated_data['name'])

    def test_update_nonexistent_city(self):
        """
        Test the PUT request to update a nonexistent city.
        """
        updated_data = {"name": "Updated City"}
        response = self.client.put(
            f"{self.url}/nonexistent_city_id", json=updated_data)
        self.assertEqual(response.status_code, 404)

    def test_update_city_invalid_json(self):
        """
        Test the PUT request to update a city with invalid JSON data.
        """
        # Assuming there is at least one city in the database
        r_a_c = self.client.get(self.states_url)
        r_a_c = r_a_c.get_json()[0]["id"]
        r_a_c = self.client.get(self.states_url + "/" + r_a_c + "/cities")
        data_all_cities = r_a_c.get_json()
        if data_all_cities:
            city_id = data_all_cities[0]['id']
            p = 'invalid_json'
            c = 'application/json'
            response = self.client.put(
                f"{self.url}/{city_id}", data=p, content_type=c)
            self.assertEqual(response.status_code, 400)
